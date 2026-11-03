"""Tiny pixel-art engine: draw smooth shapes at high resolution, then
downsample to crisp pixels with 3D-ish shading, cast shadows and outlines."""
import colorsys
import numpy as np
from PIL import Image, ImageDraw

K = 6            # supersampling factor
W, H = 56, 54    # sprite size in pixels (game draws 54px tall at scale 1)
LIGHT = np.array([-0.62, -0.78])  # light comes from the upper left


def hx(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _toward(h, target, amt):
    d = (target - h + 0.5) % 1 - 0.5
    return (h + d * amt) % 1


def ramp(base, contrast=1.0, sat=1.0):
    """6 colours: [line, shade3, shade2, base, light1, light2], hue-shifted."""
    h, l, s = colorsys.rgb_to_hls(*hx(base))
    s = min(1, s * sat)
    out = []
    for t in (-2.6, -1.6, -0.8, 0, 0.85, 1.6):
        dl = t * 0.1 * contrast
        nl = min(0.96, max(0.04, l + dl))
        if t < 0:
            nh = _toward(h, 0.70, min(0.5, -t * 0.06))
            ns = min(1, s * (1 + -t * 0.08))
        else:
            nh = _toward(h, 0.15, t * 0.05)
            ns = s * (1 - t * 0.12)
        if t <= -2.5:
            nl = min(nl, 0.16)
        out.append(tuple(int(round(v * 255)) for v in colorsys.hls_to_rgb(nh, nl, ns)))
    return out


def _blur1(a, r, axis):
    if r < 1:
        return a
    c = np.cumsum(np.pad(a, [(r + 1, r) if i == axis else (0, 0) for i in range(2)], mode='edge'), axis=axis)
    n = a.shape[axis]
    hi = np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=axis)
    lo = np.take(c, np.arange(0, n), axis=axis)
    return (hi - lo) / (2 * r + 1)


def blur(a, r):
    for _ in range(2):
        a = _blur1(_blur1(a, r, 0), r, 1)
    return a


class Spr:
    def __init__(self):
        self.parts = []
        self.fx = []      # (x, y, rgba) drawn last, no outline
        self.marks = []   # (x, y, rgb) drawn after shading, before outline
        # rig: every part belongs to a group (body, head, armL, armR, legL, legR, cape, fx, ...)
        # that the game moves around its pivot. None = decided at layer time from position.
        self.group = None
        self.piv = {}     # group -> (x, y) joint
        self.hands = {}   # arm group -> hand position (weapons held there follow the arm)

    def grp(self, g):
        """with s.grp('head'): ... tags every part drawn inside with that group"""
        spr = self

        class _G:
            def __enter__(self):
                self.prev, spr.group = spr.group, g

            def __exit__(self, *a):
                spr.group = self.prev
        return _G()

    # -- shapes in pixel coordinates --------------------------------------
    @staticmethod
    def _draw(d, sh, val):
        kind, *a = sh
        S = lambda v: v * K
        if kind == 'ell':
            cx, cy, rx, ry = a
            d.ellipse([S(cx - rx), S(cy - ry), S(cx + rx), S(cy + ry)], fill=val)
        elif kind == 'poly':
            d.polygon([(S(x), S(y)) for x, y in a[0]], fill=val)
        elif kind == 'rect':
            x0, y0, x1, y1 = a
            d.rectangle([S(x0), S(y0), S(x1) - 1, S(y1) - 1], fill=val)
        elif kind == 'cap':
            x0, y0, x1, y1, r = a
            d.line([S(x0), S(y0), S(x1), S(y1)], fill=val, width=max(1, int(S(2 * r))))
            for x, y in ((x0, y0), (x1, y1)):
                d.ellipse([S(x - r), S(y - r), S(x + r), S(y + r)], fill=val)
        elif kind == 'line':  # polyline of capsules
            pts, r = a
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                Spr._draw(d, ('cap', x0, y0, x1, y1, r), val)
        elif kind == 'chord':
            cx, cy, rx, ry, a0, a1 = a
            d.chord([S(cx - rx), S(cy - ry), S(cx + rx), S(cy + ry)], a0, a1, fill=val)
        elif kind == 'pie':
            cx, cy, rx, ry, a0, a1 = a
            d.pieslice([S(cx - rx), S(cy - ry), S(cx + rx), S(cy + ry)], a0, a1, fill=val)
        else:
            raise ValueError(kind)

    def part(self, rp, shapes, sub=(), soft=1.6, cast=0, line=True, flat=False,
             thr=0.5, bias=0.0, gloss=0.0, clip=None, shine=None):
        im = Image.new('L', (W * K, H * K), 0)
        d = ImageDraw.Draw(im)
        for sh in shapes:
            self._draw(d, sh, 255)
        for sh in sub:
            self._draw(d, sh, 0)
        m = np.asarray(im, dtype=np.float32) / 255
        if clip is not None:
            m = m * clip.hi
        self.parts.append(dict(m=m, rp=rp, soft=soft, cast=cast, line=line, g=self.group,
                               flat=flat, thr=thr, bias=bias, gloss=gloss, shine=shine))
        return self.parts[-1]

    def mark(self, x, y, rgb):
        self.marks.append((x, y, rgb, len(self.parts) - 1))

    def glow(self, x, y, rgb, a=255):
        self.fx.append((x, y, (*rgb, a), len(self.parts) - 1, self.group))

    # -- render ------------------------------------------------------------
    def render(self):
        return self._render(self.parts, [m[:3] for m in self.marks], [f[:3] for f in self.fx])

    def _resolve(self):
        """Give untagged parts (weapons, shields, emblems...) a group from where they sit."""
        for p in self.parts:
            if p['g']:
                continue
            m = p['m'].reshape(H, K, W, K).mean(axis=(1, 3)) >= p['thr']
            ys, xs = np.nonzero(m)
            if not len(xs):
                p['g'] = 'body'
                continue
            near = lambda pt, r=1: m[max(0, int(pt[1]) - r):int(pt[1]) + r + 1, max(0, int(pt[0]) - r):int(pt[0]) + r + 1].any()
            g = next((a for a, hd in self.hands.items() if near(hd)), None)
            if g is None and xs.max() - xs.min() < 10:
                g = next((a for a in self.hands if near(self.piv[a], 0)), None)
            p['g'] = g or ('head' if ys.mean() < 26 else 'body')

    def layers(self):
        """Render each run of same-group parts as its own full layer (nothing hidden behind
        other groups, so limbs can move without leaving holes). Returns [(group, Image)]."""
        self._resolve()
        runs = []
        for i, p in enumerate(self.parts):
            if runs and runs[-1][0] == p['g']:
                runs[-1][1].append(i)
            else:
                runs.append((p['g'], [i]))
        out = []
        fp = getattr(self, 'face_part', None)
        self.face_layer = next((i for i, (_, idx) in enumerate(runs) if fp is not None and idx[0] <= fp <= idx[-1]), None)
        for g, idx in runs:
            lo, hi = idx[0], idx[-1]
            marks = [m[:3] for m in self.marks if lo <= m[3] <= hi]
            fx = [f[:3] for f in self.fx if (f[4] or g) == g and lo <= max(f[3], 0) <= hi and f[4] != 'fx']
            out.append((g, self._render([self.parts[i] for i in idx], marks, fx)))
        fx = [f[:3] for f in self.fx if f[4] == 'fx']
        if fx:
            out.append(('fx', self._render([], [], fx)))
        return out

    def _render(self, parts, marks, fxs):
        n = len(parts)
        owner = -np.ones((H, W), int)
        level = np.zeros((H, W), int)
        cov_all = []
        for i, p in enumerate(parts):
            m = p['m']
            cov = m.reshape(H, K, W, K).mean(axis=(1, 3))
            inside = cov >= p['thr']
            cov_all.append(inside)
            if p['flat']:
                v = np.full((H, W), 0.6 + p['bias'])
            else:
                r = max(1, int(p['soft'] * K))
                b = blur(m, r)
                gy, gx = np.gradient(b)
                g = (-gx * LIGHT[0] - gy * LIGHT[1]) * r * 2.2
                ys = np.arange(H * K)[:, None] / (H * K)
                v = 0.56 + g * 0.55 - (ys - 0.5) * 0.12 + p['bias']
                if p['gloss']:
                    v = v + p['gloss'] * np.clip(g, 0, None) ** 2 * 2
                w = m.reshape(H, K, W, K).sum(axis=(1, 3)) + 1e-6
                v = (v * m).reshape(H, K, W, K).sum(axis=(1, 3)) / w
            lv = np.digitize(v, [0.46, 0.80]) + 2  # anime cel: shadow / base / highlight
            if p['shine'] is not None:  # glossy streak across hair
                sy = p['shine']
                for x in range(W):
                    yy = int(round(sy + abs(x - 27) * 0.12))
                    if (x + 1) % 5 and 0 <= yy < H and inside[yy, x]:
                        lv[yy, x] = 5
            owner[inside] = i
            level[inside] = lv[inside]
        # cast shadows from parts in front onto parts behind
        for y in range(H):
            for x in range(W):
                o = owner[y, x]
                if o < 0:
                    continue
                for dy in (1, 2):
                    if y - dy < 0:
                        break
                    up = owner[y - dy, x]
                    if up > o and parts[up]['cast'] >= dy:
                        level[y, x] = max(1, level[y, x] - 1)
                        break
        img = np.zeros((H, W, 4), np.uint8)
        for y in range(H):
            for x in range(W):
                o = owner[y, x]
                if o >= 0:
                    img[y, x, :3] = parts[o]['rp'][level[y, x]]
                    img[y, x, 3] = 255
        # internal lines: back part pixels touching a front part
        for y in range(H):
            for x in range(W):
                o = owner[y, x]
                if o < 0 or not parts[o]['line']:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < W and 0 <= yy < H:
                        q = owner[yy, xx]
                        if q > o and parts[q]['rp'] is not parts[o]['rp'] and parts[q]['line']:
                            img[y, x, :3] = parts[o]['rp'][1] if dy == 1 else parts[o]['rp'][0]
                            break
        for x, y, rgb in marks:
            img[y, x, :3] = rgb
            img[y, x, 3] = 255
        # outer outline (selective: darker on bottom/right)
        out = img.copy()
        for y in range(H):
            for x in range(W):
                if img[y, x, 3]:
                    continue
                best = None
                for dx, dy in ((0, 1), (1, 0), (-1, 0), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < W and 0 <= yy < H and owner[yy, xx] >= 0:
                        best = owner[yy, xx]
                        break
                if best is not None:
                    out[y, x, :3] = parts[best]['rp'][0]
                    out[y, x, 3] = 255
        for x, y, rgba in fxs:
            if 0 <= x < W and 0 <= y < H:
                if out[y, x, 3] == 0 or rgba[3] == 255:
                    out[y, x] = rgba
        return Image.fromarray(out, 'RGBA')
