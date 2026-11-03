"""Original chibi pixel-art sprites for the auto battler.

Each character is built from layered vector parts drawn at 8x, reduced to 1x masks,
then shaded (light from top-left), hue-shifted and outlined like hand-made pixel art.
Run:  python tools/make_sprites.py   -> assets/units/<id>.png + assets/preview.png
"""
import colorsys, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

S = 8            # supersampling
W, H = 52, 54    # canvas (H = in-game draw height, so sprites render at exactly 1x)
LIGHT = np.array([-0.55, -0.75, 0.62]); LIGHT /= np.linalg.norm(LIGHT)
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')


def hx(c):
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))


def shift_hue(h, target, amt):
    d = ((target - h + 0.5) % 1) - 0.5
    return (h + d * amt) % 1


def ramp(base, shiny=False):
    """5 tones: outline, dark, mid, light, highlight (hue-shifted)."""
    h, s, v = colorsys.rgb_to_hsv(*hx(base))
    spec = [(-0.16, 1.25, 0.30), (-0.08, 1.12, 0.66), (0, 1, 1), (0.06, 0.82, 1.2), (0.1, 0.5, 1.42)]
    if shiny:
        spec = [(-0.16, 1.2, 0.28), (-0.08, 1.1, 0.6), (0, 1, 1), (0.06, 0.6, 1.3), (0.1, 0.12, 1.7)]
    out = []
    for dh, ms, mv in spec:
        hh = shift_hue(h, 0.68, -dh * 1.0) if dh < 0 else shift_hue(h, 0.13, dh)
        ss = min(1, s * ms) if s > 0.04 else s
        vv = min(1, v * mv)
        out.append(tuple(round(x * 255) for x in colorsys.hsv_to_rgb(hh, ss, vv)))
    return out


class D:
    def __init__(s, d): s.d = d

    def e(s, cx, cy, rx, ry=None, f=255):
        ry = rx if ry is None else ry
        s.d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], fill=f)

    def r(s, x0, y0, x1, y1, rad=0, f=255):
        s.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=rad * S, fill=f)

    def p(s, pts, f=255):
        s.d.polygon([(x * S, y * S) for x, y in pts], fill=f)

    def l(s, pts, w, f=255):
        s.d.line([(x * S, y * S) for x, y in pts], fill=f, width=max(1, int(w * S)), joint='curve')
        for x, y in (pts[0], pts[-1]): s.e(x, y, w / 2, f=f)


class Fig:
    def __init__(s):
        s.parts = []; s.stamps = []

    def add(s, color, fn, rim=3, shiny=False, outline=True, flat=False):
        im = Image.new('L', (W * S, H * S), 0)
        fn(D(ImageDraw.Draw(im)))
        s.parts.append(dict(mask=np.array(im) > 127, ramp=ramp(color, shiny), rim=rim, outline=outline, flat=flat))

    def px(s, x, y, rgb): s.stamps.append((x, y, rgb))

    def render(s):
        img = np.zeros((H, W, 4), np.uint8)
        pid = np.full((H, W), -1)
        tone = np.zeros((H, W), int)
        for i, pt in enumerate(s.parts):
            m = pt['mask']
            lo = m.reshape(H, S, W, S).mean((1, 3)) > 0.5
            if not lo.any(): continue
            R = pt['rim'] * S
            dist = ndimage.distance_transform_edt(m)
            dn = np.clip(dist / R, 0, 1)
            hgt = R * np.sqrt(1 - (1 - dn) ** 2)
            gy, gx = np.gradient(hgt)
            n = np.stack([-gx, -gy, np.ones_like(gx)], -1)
            n /= np.linalg.norm(n, axis=-1, keepdims=True)
            lam = (n @ LIGHT) * m
            cnt = m.reshape(H, S, W, S).sum((1, 3))
            lam_lo = lam.reshape(H, S, W, S).sum((1, 3)) / np.maximum(cnt, 1)
            lam_lo -= 0.10 * (np.arange(H)[:, None] / H)
            t = np.where(lam_lo > 0.86, 4, np.where(lam_lo > 0.66, 3, np.where(lam_lo > 0.34, 2, 1)))
            if pt['flat']: t = np.full_like(t, 2)
            pid[lo] = i; tone[lo] = t[lo]
        # cast-shadow seams where a lower part touches a higher one
        out = tone.copy()
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1)):
            nb = np.roll(np.roll(pid, dy, 0), dx, 1)
            seam = (pid >= 0) & (nb > pid) & (dy <= 0)
            out[seam] = np.maximum(1, np.minimum(out[seam], tone[seam] - 1))
        tone = out
        # outer outline (selective: darkest tone of own material)
        opaque = pid >= 0
        edge = opaque & ~ndimage.binary_erosion(opaque, border_value=0)
        for y, x in zip(*np.nonzero(opaque)):
            pt = s.parts[pid[y, x]]
            k = 0 if (edge[y, x] and pt['outline']) else tone[y, x]
            if not pt['outline'] and edge[y, x]: k = max(2, k)
            img[y, x] = (*pt['ramp'][k], 255)
        for x, y, rgb in s.stamps:
            img[y, x] = (*rgb, 255)
        return Image.fromarray(img, 'RGBA')


# ---------------------------------------------------------------- body kit
SKIN = '#f5c9a0'
HAIR_SHAPES = {}


def hair(name):
    def reg(f): HAIR_SHAPES[name] = f; return f
    return reg


@hair('spiky')
def _(f, c, back):
    if back: return
    def fn(d):
        d.e(25, 13, 10, 9.2)
        for x, y in ((17, 2.5), (23, 1), (29, 2.2), (34, 6.5)): d.p([(x - 4, 9), (x, y), (x + 3.5, 9)])
        d.r(15, 13, 30, 30, f=0)
        d.p([(15, 12), (31, 12), (30, 16), (27.5, 13.5), (25, 16.5), (22.5, 13.5), (20, 16), (18, 13.5), (15.5, 16.8)])
        d.p([(31, 11), (34.5, 12), (34, 22), (31, 19.5)])
    f.add(c, fn, rim=3)


@hair('pony')
def _(f, c, back):
    if back:
        f.add(c, lambda d: (d.e(35, 16, 3.6, 4), d.l([(36, 17), (38, 24), (36.5, 31)], 3.4)), rim=2); return
    def fn(d):
        d.e(25, 13, 9.8, 9)
        d.r(15, 13.5, 30.5, 30, f=0)
        d.p([(15, 12), (31, 12), (29.5, 15), (26, 13), (23, 16), (20, 13.2), (16, 17), (15.2, 14)])
        d.p([(31, 11), (34.2, 12), (33.6, 21), (31, 18)])
        d.p([(14.6, 13), (17.5, 13), (16.5, 21), (14.8, 19)])
    f.add(c, fn, rim=3)


@hair('bob')
def _(f, c, back):
    if back:
        f.add(c, lambda d: d.r(15, 12, 35, 24, 5), rim=2); return
    def fn(d):
        d.e(25, 13, 10, 9.3)
        d.r(16.5, 14, 30.5, 30, f=0)
        d.p([(15, 12), (32, 12), (30, 15), (26, 14), (21, 15.5), (16.5, 15)])
        d.p([(14.3, 12), (17.5, 13), (17.3, 23), (14.6, 22.5)])
        d.p([(31, 11), (35, 12), (35.2, 23.5), (31, 22)])
    f.add(c, fn, rim=3)


@hair('long')
def _(f, c, back):
    if back:
        f.add(c, lambda d: d.p([(16, 12), (35, 12), (38, 36), (32, 38), (24, 33)]), rim=3); return
    HAIR_SHAPES['bob'](f, c, False)


@hair('none')
def _(f, c, back): pass


def eyes(f, iris, x0=18, y0=16, gap=6):
    r = ramp(iris)
    for k, x in enumerate((x0, x0 + gap)):
        w = 2 if k == 0 else 3 - 1
        f.px(x, y0, r[0]); f.px(x + 1, y0, r[0])
        f.px(x, y0 + 1, r[1]); f.px(x + 1, y0 + 1, (255, 255, 255))
        f.px(x, y0 + 2, r[3]); f.px(x + 1, y0 + 2, r[2])
    f.px(x0 - 1, y0, r[0])  # lash
    f.px(x0 + gap + 2, y0, r[0])
    sk = ramp(SKIN)
    f.px(x0 + 3, y0 + 5, sk[1])  # mouth
    f.px(x0 - 1, y0 + 3, (240, 150, 140)); f.px(x0 + gap + 2, y0 + 3, (240, 150, 140))  # blush


def body(f, c, behind=None, before_torso=None, over_torso=None, head_extra=None, front=None,
         robe=False, legs=True):
    """Standard 3/4 chibi pose facing left. Callbacks add layers at the right depth."""
    if behind: behind(f)
    HAIR_SHAPES[c['hair']](f, c['hair_c'], True)
    # back arm (viewer right)
    f.add(c['sleeve'], lambda d: d.l([(31.5, 25.5), (34, 30.5), (34, 34.5)], 3.8), rim=2)
    f.add(SKIN, lambda d: d.e(34, 35.8, 2.2), rim=2)
    if legs:
        f.add(c['pants'], lambda d: d.r(25, 36, 30, 48, 2), rim=2)
        f.add(c['pants'], lambda d: d.r(19.5, 36, 24.5, 48, 2), rim=2)
        f.add(c['boots'], lambda d: (d.r(24.5, 45, 31, 52.6, 2), d.r(25, 50, 32, 53, 1)), rim=2)
        f.add(c['boots'], lambda d: (d.r(18.5, 45, 25, 52.6, 2), d.r(16, 49.5, 24.5, 53.4, 1.6)), rim=2)
    if before_torso: before_torso(f)
    f.add(c['body'], lambda d: d.p([(18.5, 24), (31.5, 24), (33, 29), (31.5, 38.5), (18.5, 38.5), (17, 29)]), rim=3)
    if robe:
        f.add(robe, lambda d: d.p([(18, 31), (32, 31), (35.5, 52.5), (15, 52.5)]), rim=3)
    if over_torso: over_torso(f)
    f.add(SKIN, lambda d: d.r(22.5, 21, 27.5, 26, 1), rim=1)
    f.add(SKIN, lambda d: (d.e(24, 15.5, 8.5, 8.2), d.e(32.2, 17, 1.6, 2.4)), rim=5)
    HAIR_SHAPES[c['hair']](f, c['hair_c'], False)
    eyes(f, c.get('eye', '#4a6fd0'))
    if head_extra: head_extra(f)
    if front: front(f)


def front_arm(f, sleeve, pose='down'):
    if pose == 'down':
        f.add(sleeve, lambda d: d.l([(19, 25.5), (16.5, 30.5), (17, 34.5)], 4), rim=2)
        f.add(SKIN, lambda d: d.e(17, 36, 2.3), rim=2)
    else:  # raised forward
        f.add(sleeve, lambda d: d.l([(19, 25.5), (15.5, 29), (12.5, 31)], 4), rim=2)
        f.add(SKIN, lambda d: d.e(11.6, 31.2, 2.3), rim=2)


# ---------------------------------------------------------------- props
METAL = '#aab4c8'; GOLD = '#e8b440'; WOOD = '#9a6236'; LEATHER = '#8a5a3a'


def sword(f, x=17, y=36, tip=(7, 17), w=2.4, blade=METAL, guard=GOLD, hilt=LEATHER):
    dx, dy = tip[0] - x, tip[1] - y; n = (dx * dx + dy * dy) ** .5; ux, uy = dx / n, dy / n
    f.add(blade, lambda d: (d.l([(x + ux * 2, y + uy * 2), (tip[0] - ux * 1.5, tip[1] - uy * 1.5)], w),
                            d.p([(tip[0] - ux * 2 - uy * w / 2, tip[1] - uy * 2 + ux * w / 2), tip,
                                 (tip[0] - ux * 2 + uy * w / 2, tip[1] - uy * 2 - ux * w / 2)])), rim=1, shiny=True)
    f.add(hilt, lambda d: d.l([(x - ux * 2.2, y - uy * 2.2), (x + ux * 1.5, y + uy * 1.5)], 1.6), rim=1)
    gx, gy = x + ux * 2.2, y + uy * 2.2
    f.add(guard, lambda d: d.l([(gx - uy * 3.2, gy + ux * 3.2), (gx + uy * 3.2, gy - ux * 3.2)], 1.8), rim=1, shiny=True)


def staff(f, x=17, top=(13, 11), bottom=(19, 50), shaft=WOOD):
    f.add(shaft, lambda d: d.l([bottom, top], 1.8), rim=1)


def orb(f, cx, cy, r, color, glow=True):
    if glow:
        f.add(color, lambda d: d.e(cx, cy, r + 1.6), rim=2, outline=False, flat=True)
        f.parts[-1]['ramp'] = [tuple(min(255, int(v * 0.6 + 255 * 0.4)) for v in ramp(color)[3])] * 5
    f.add(color, lambda d: d.e(cx, cy, r), rim=r, shiny=True)


def shield_round(f, cx=35, cy=33, rx=5.6, ry=6.2, face=WOOD, rim_c=METAL, boss=METAL):
    f.add(rim_c, lambda d: d.e(cx, cy, rx, ry), rim=2, shiny=True)
    f.add(face, lambda d: d.e(cx, cy, rx - 1.3, ry - 1.3), rim=3)
    f.add(boss, lambda d: d.e(cx - .4, cy - .4, 1.7), rim=2, shiny=True)


def kite_shield(f, cx=35.5, top=26.5, face='#3b62b8', trim=METAL, emblem=GOLD):
    pts = [(cx - 5.5, top), (cx + 5.5, top), (cx + 5.2, top + 7), (cx, top + 15), (cx - 5.2, top + 7)]
    f.add(trim, lambda d: d.p(pts), rim=2, shiny=True)
    inner = [(cx - 4.2, top + 1.2), (cx + 4.2, top + 1.2), (cx + 4, top + 6.8), (cx, top + 13), (cx - 4, top + 6.8)]
    f.add(face, lambda d: d.p(inner), rim=3)
    f.add(emblem, lambda d: (d.r(cx - .8, top + 2.8, cx + .8, top + 10), d.r(cx - 3, top + 4.6, cx + 3, top + 6.2)), rim=1, shiny=True)


def cape(f, color, x0=17.5, x1=32.5, y=24, bottom=50, spread=4.5, tatter=False):
    def fn(d):
        d.p([(x0, y), (x1, y), (x1 + spread, bottom), (x0 - spread, bottom)])
        if tatter:
            for k in range(5):
                bx = x0 - spread + 2 + k * (x1 - x0 + 2 * spread - 4) / 4
                d.p([(bx - 1.6, bottom + .2), (bx, bottom - 3), (bx + 1.6, bottom + .2)], f=0)
    f.add(color, fn, rim=3)


def pauldron(f, cx, cy, color, rx=4.2, ry=3.2, shiny=True):
    f.add(color, lambda d: d.e(cx, cy, rx, ry), rim=2, shiny=shiny)


def belt(f, color=LEATHER, buckle=GOLD, y=33.5):
    f.add(color, lambda d: d.p([(17.6, y), (32.4, y), (32.2, y + 2), (17.8, y + 2)]), rim=1)
    f.add(buckle, lambda d: d.r(22.5, y - .3, 25.5, y + 2.3, .5), rim=1, shiny=True)


def bow(f, color=WOOD, string='#e8e4d8', x=12, y0=20, y1=50, bend=4.5):
    mid = (y0 + y1) / 2
    f.add(string, lambda d: d.l([(x + 1.2, y0 + 1), (x + 1.2, y1 - 1)], 0.9), rim=1, outline=False, flat=True)
    pts = [(x + 1, y0), (x - bend * .7, y0 + 5), (x - bend, mid), (x - bend * .7, y1 - 5), (x + 1, y1)]
    f.add(color, lambda d: d.l(pts, 2), rim=1)


# ---------------------------------------------------------------- characters
def mk(fn):
    f = Fig(); fn(f); return f.render()


def swordsman(f):
    c = dict(hair='spiky', hair_c='#7a4a2a', sleeve='#3d6fb0', body='#3d6fb0', pants='#5a4636', boots=LEATHER, eye='#3b6fd4')
    def over(f):
        belt(f)
        f.add('#c8402e', lambda d: (d.r(19, 22.5, 31, 26, 1.6), d.p([(29, 24), (33.5, 25), (34.5, 32), (31, 29)])), rim=2)
        pauldron(f, 31.5, 26, METAL)
    def front(f):
        sword(f, 17, 36, (8, 15), 3.4)
        front_arm(f, c['sleeve'])
    body(f, c, before_torso=lambda f: shield_round(f, 36, 33), over_torso=over, front=front)


def archer(f):
    c = dict(hair='pony', hair_c='#e8c060', sleeve='#4f9a52', body='#4f9a52', pants='#7a6a4a', boots='#6a4a2e', eye='#3a9a4a')
    def behind(f):
        f.add(LEATHER, lambda d: d.l([(31, 22), (36, 38)], 4.4), rim=2)
        for k, col in enumerate(('#e8e4d8', '#d84a3a', '#e8e4d8')):
            f.add(col, lambda d, k=k: d.p([(29.5 + k * 1.6, 15.5 + k * .4), (31.3 + k * 1.6, 15 + k * .4), (32 + k * 1.6, 21), (30.4 + k * 1.6, 21.5)]), rim=1)
    def over(f):
        f.add('#2f6f3a', lambda d: d.p([(17.4, 30), (32.6, 30), (34, 40), (16, 40)]), rim=2)
        belt(f, y=31)
        f.add(LEATHER, lambda d: d.l([(19.5, 24.5), (31, 35)], 1.6), rim=1)
    def front(f):
        bow(f, x=12.5, y0=21, y1=49)
        front_arm(f, c['sleeve'])
    body(f, c, behind=behind, over_torso=over, front=front)


def acolyte(f):
    c = dict(hair='bob', hair_c='#3a3048', sleeve='#e8e2d4', body='#e8e2d4', pants='#e8e2d4', boots='#7a6a5a', eye='#7a5ad0')
    def over(f):
        f.add('#4a78c8', lambda d: (d.p([(23, 24), (27, 24), (26.5, 52.5), (23.5, 52.5)])), rim=1)
        f.add('#4a78c8', lambda d: d.r(18.6, 23, 31.4, 26.5, 1.6), rim=1)
        f.add(GOLD, lambda d: (d.r(24.3, 27, 25.7, 32), d.r(22.8, 28.2, 27.2, 29.6)), rim=1, shiny=True)
    def front(f):
        f.add('#8a3a3a', lambda d: d.r(12.5, 32.5, 19.5, 40, 1), rim=2)
        f.add('#f0e8d0', lambda d: d.r(13.5, 33.5, 19.5, 39, .5), rim=1, flat=True)
        f.add(GOLD, lambda d: d.r(15.3, 34.4, 16.7, 37.6), rim=1, shiny=True)
        front_arm(f, c['sleeve'])
    body(f, c, over_torso=over, front=front, robe='#e8e2d4')


def thief(f):
    c = dict(hair='spiky', hair_c='#2e2a3a', sleeve='#2f5f66', body='#2f5f66', pants='#3a3a4a', boots='#2a2a32', eye='#c0a030')
    def over(f):
        belt(f, '#5a3a2a', METAL)
        f.add('#7a4ab0', lambda d: d.l([(19.5, 25), (31, 25)], 3.4), rim=2)
        f.add(LEATHER, lambda d: d.r(28.5, 33.5, 32.5, 38, 1), rim=1)
    def head(f):
        f.add('#7a4ab0', lambda d: (d.r(15.2, 9.8, 33.5, 13.2, 1.5), d.p([(32, 11), (39, 9.5), (37, 14.5)]), d.p([(32, 12), (38, 16), (34.5, 18)])), rim=2)
    def front(f):
        f.add(METAL, lambda d: (d.l([(16.8, 38.5), (12, 46.5)], 1.9), d.p([(11.2, 45.8), (10.3, 48.7), (12.9, 47)])), rim=1, shiny=True)
        f.add('#3a2a20', lambda d: d.l([(18.2, 36), (16.6, 38.8)], 1.6), rim=1)
        f.add(METAL, lambda d: d.l([(15.4, 37.6), (19.4, 39.4)], 1.3), rim=1, shiny=True)
        front_arm(f, c['sleeve'])
    body(f, c, over_torso=over, head_extra=head, front=front)


def mage(f):
    c = dict(hair='bob', hair_c='#b05a3a', sleeve='#36408a', body='#36408a', pants='#36408a', boots='#3a2a40', eye='#d07a30')
    def over(f):
        f.add('#e8c050', lambda d: (d.p([(18, 50.5), (35.2, 50.5), (35.5, 52.5), (15, 52.5)])), rim=1)
        belt(f, '#e8c050', '#d04060', y=31.5)
        f.add('#e8e2d4', lambda d: d.p([(21, 23.5), (29, 23.5), (25, 28)]), rim=1)
    def head(f):
        def hat(d):
            d.e(24.5, 9.6, 13.5, 3.2)
            d.p([(17, 9.5), (31.5, 9.5), (30, 4), (35, 0.6), (26, 2.2), (21.5, 4.5)])
        f.add('#36408a', hat, rim=2)
        f.add('#e8c050', lambda d: d.p([(17.6, 8), (31, 8), (31.2, 9.8), (17.4, 9.8)]), rim=1)
    def front(f):
        staff(f, top=(12.5, 15), bottom=(19, 50))
        orb(f, 12, 13, 2.6, '#5ad0ff')
        front_arm(f, c['sleeve'])
    body(f, c, over_torso=over, head_extra=head, front=front, robe='#36408a')


def knight(f):
    c = dict(hair='spiky', hair_c='#c08a3a', sleeve=METAL, body=METAL, pants='#4a4a5a', boots='#6a7080', eye='#3a6ad0')
    def over(f):
        f.add('#3a5ab0', lambda d: d.p([(21, 27), (29, 27), (29.5, 44), (25, 46), (20.5, 44)]), rim=2)
        f.add(GOLD, lambda d: (d.r(24.2, 30, 25.8, 39), d.r(21.8, 32.4, 28.2, 34)), rim=1, shiny=True)
        belt(f, '#3a3a48', GOLD, y=35.6)
        pauldron(f, 31.8, 25.6, METAL, 4.8, 3.6)
        f.add(METAL, lambda d: d.r(20, 21, 30, 25.4, 2), rim=2, shiny=True)
    def front(f):
        sword(f, 17, 36, (5, 7), 3.8)
        front_arm(f, METAL)
        pauldron(f, 18.4, 25.4, METAL, 4.8, 3.6)
    body(f, c, before_torso=lambda f: kite_shield(f), over_torso=over, front=front)
    for p in f.parts[-3:]: pass


def hunter(f):
    c = dict(hair='long', hair_c='#5a3a28', sleeve='#7a5a3a', body='#6a7a3a', pants='#5a4a34', boots='#4a3424', eye='#3a8a5a')
    def behind(f):
        cape(f, '#4a5a2e', spread=4)
        f.add(LEATHER, lambda d: d.l([(32, 22), (37, 37)], 4.4), rim=2)
        for k in range(3):
            f.add('#f0f0f0', lambda d, k=k: d.p([(30.3 + k * 1.7, 15.5), (32.2 + k * 1.7, 15.2), (32.8 + k * 1.7, 21), (31 + k * 1.7, 21.5)]), rim=1)
    def over(f):
        f.add(LEATHER, lambda d: d.p([(17.4, 24), (32.6, 24), (33.6, 29), (16.4, 29)]), rim=2)
        belt(f, '#4a3020', GOLD, y=33)
        f.add('#4a3020', lambda d: d.l([(19.5, 26), (31, 36)], 1.6), rim=1)
    def head(f):
        def hat(d):
            d.e(24.5, 9.5, 11.5, 3)
            d.p([(16, 9.8), (32.5, 9.8), (31, 4.5), (24, 3), (18, 5.5)])
        f.add('#4a5a2e', hat, rim=2)
        f.add('#d84a3a', lambda d: d.p([(29, 6), (39, 0.6), (37, 3), (31, 8)]), rim=1)
        f.add('#f0f0e8', lambda d: d.p([(30, 7), (40, 3.4), (38, 5.8), (31.5, 8.6)]), rim=1)
    def front(f):
        bow(f, '#5a3a20', x=11.5, y0=16, y1=52, bend=5.5)
        f.add(GOLD, lambda d: d.r(5.3, 32.5, 8, 35.5, .6), rim=1, shiny=True)
        front_arm(f, c['sleeve'])
    body(f, c, behind=behind, over_torso=over, head_extra=head, front=front)


def priest(f):
    c = dict(hair='long', hair_c='#e8d8a8', sleeve='#f2f0ea', body='#f2f0ea', pants='#f2f0ea', boots='#8a7a6a', eye='#4a8ad0')
    def over(f):
        f.add('#2f9a8a', lambda d: (d.p([(22.6, 24), (27.4, 24), (28, 52.5), (22, 52.5)])), rim=1)
        f.add(GOLD, lambda d: (d.r(24.2, 28, 25.8, 36), d.r(21.4, 30, 28.6, 31.6)), rim=1, shiny=True)
        f.add(GOLD, lambda d: d.p([(16.2, 50.4), (34.6, 50.4), (35.5, 52.5), (15, 52.5)]), rim=1, shiny=True)
        f.add('#2f9a8a', lambda d: d.r(18, 22.5, 32, 26.5, 2), rim=2)
        belt(f, GOLD, '#2f9a8a', y=33)
    def front(f):
        staff(f, top=(13, 9), bottom=(19, 50), shaft=GOLD)
        f.parts[-1]['shiny'] = True
        f.add(GOLD, lambda d: (d.e(12.6, 6.6, 3.6), d.e(12.6, 6.6, 2.2, f=0)), rim=1, shiny=True)
        orb(f, 12.6, 6.6, 1.3, '#9af0e0')
        front_arm(f, c['sleeve'])
    body(f, c, over_torso=over, front=front, robe='#f2f0ea')


def assassin(f):
    c = dict(hair='none', hair_c='#1a1a22', sleeve='#2a2830', body='#2a2830', pants='#2a2830', boots='#1e1c22', eye='#e04040')
    def behind(f):
        f.add('#b02a3a', lambda d: d.p([(30, 22), (35, 23), (44, 33), (41, 35.5), (38, 31), (36, 36), (32, 27)]), rim=2)
        cape(f, '#3a3440', x0=19, x1=31, y=27, bottom=46, spread=3, tatter=True)
    def over(f):
        f.add('#b02a3a', lambda d: d.r(18, 21.8, 31.5, 26.4, 2), rim=2)
        belt(f, '#b02a3a', METAL)
        for k in range(3): f.add('#4a4652', lambda d, k=k: d.r(18.5, 28 + k * 1.8, 31.5, 28.9 + k * 1.8), rim=1)
        f.add('#d8dce8', lambda d: (d.p([(35, 36.5), (37.5, 36), (42, 47), (40.6, 49)])), rim=1, shiny=True)
    def head(f):
        def hood(d):
            d.e(24.5, 14, 10.6, 10.6)
            d.p([(30, 6), (38, 13), (34.5, 20)])
            d.e(22.8, 17.2, 7.6, 6.6, f=0)
        f.add('#2a2830', hood, rim=3)
        f.add('#b02a3a', lambda d: d.p([(16, 20), (31.5, 20), (30, 24.6), (17.4, 24.6)]), rim=1)
    def front(f):
        f.add('#d8dce8', lambda d: d.p([(15.2, 34), (17.6, 33.6), (13, 22), (10.6, 18.8), (12.4, 23.6)]), rim=1, shiny=True)
        f.add(METAL, lambda d: d.r(14, 34, 20, 38, 1), rim=1, shiny=True)
        front_arm(f, c['sleeve'])
    body(f, c, behind=behind, over_torso=over, head_extra=head, front=front)
    f.stamps = [s for s in f.stamps if s[1] < 20]  # mask covers mouth/blush


def wizard(f):
    c = dict(hair='long', hair_c='#c8c8d8', sleeve='#5a2e8a', body='#5a2e8a', pants='#5a2e8a', boots='#2e2040', eye='#a05ae0')
    def over(f):
        f.add('#e8c050', lambda d: d.p([(22.4, 24), (27.6, 24), (28.6, 52.5), (21.4, 52.5)]), rim=1, shiny=True)
        f.add('#3a1e5a', lambda d: d.p([(23.3, 25), (26.7, 25), (27.4, 52.5), (22.6, 52.5)]), rim=1)
        for x, y in ((17.5, 44), (31.5, 41), (19.5, 37.5), (33, 48.5)):
            f.add('#f0e070', lambda d, x=x, y=y: d.p([(x, y - 1.4), (x + .5, y), (x, y + 1.4), (x - .5, y)]), rim=1, outline=False, flat=True)
        f.add('#5a2e8a', lambda d: d.e(25, 24, 7.5, 3), rim=2)
    def head(f):
        def hood(d):
            d.e(24.5, 12.5, 10.4, 9.8)
            d.p([(18, 6), (30, 5), (37, 0.6), (31.5, 9)])
            d.e(23.2, 17, 7.6, 6.5, f=0)
            d.r(13.8, 16, 17.5, 22, f=0)
        f.add('#5a2e8a', hood, rim=3)
        f.add('#e8c050', lambda d: d.l([(15.8, 12.5), (21, 8.4), (28.5, 8.8), (32.5, 12.5)], 1.2), rim=1, shiny=True)
    def front(f):
        staff(f, top=(12, 10), bottom=(19, 50), shaft='#4a3048')
        f.add('#4a3048', lambda d: (d.l([(12, 11), (9.5, 7), (10.5, 3.5)], 1.4), d.l([(12, 11), (14.6, 7), (13.5, 3.5)], 1.4)), rim=1)
        f.add('#b070ff', lambda d: d.p([(12, 2.2), (14, 6.8), (12, 9.6), (10, 6.8)]), rim=1, shiny=True)
        front_arm(f, c['sleeve'])
    body(f, c, over_torso=over, head_extra=head, front=front, robe='#5a2e8a')


def lordknight(f):
    c = dict(hair='spiky', hair_c='#d8d0c0', sleeve='#c8ccd8', body='#c8ccd8', pants='#3a3a4a', boots='#9098a8', eye='#d04040')
    ARM = '#c8ccd8'
    def behind(f):
        cape(f, '#b82a34', x0=17, x1=33, y=23, bottom=51, spread=6)
        f.add(METAL, lambda d: d.l([(34, 41), (43, 5)], 4.6), rim=1, shiny=True)
        f.add(METAL, lambda d: d.p([(41, 6), (43.8, 0.4), (45, 7)]), rim=1, shiny=True)
        f.add('#e04050', lambda d: d.l([(38.4, 22), (40.6, 13)], 1), rim=1, outline=False, flat=True)
        f.add(GOLD, lambda d: d.l([(31.5, 40), (39.5, 42.4)], 2.2), rim=1, shiny=True)
        f.add(LEATHER, lambda d: d.l([(33, 41.2), (31.5, 47)], 1.8), rim=1)
    def over(f):
        f.add(GOLD, lambda d: d.p([(18.5, 24), (31.5, 24), (30, 26.5), (20, 26.5)]), rim=1, shiny=True)
        f.add('#b82a34', lambda d: d.p([(19, 34), (31, 34), (33.5, 45), (26, 43), (24, 46), (16.5, 45)]), rim=2)
        f.add(GOLD, lambda d: d.p([(22.5, 28.5), (27.5, 28.5), (25, 32.5)]), rim=1, shiny=True)
        belt(f, '#2e2a38', GOLD, y=33.2)
        pauldron(f, 32.2, 25.4, ARM, 5.4, 4)
        f.add(GOLD, lambda d: d.l([(28, 23.6), (37, 25.4)], 1.1), rim=1, shiny=True)
    def head(f):
        def helm(d):
            d.e(24.5, 12.5, 10.2, 9.4)
            d.r(15.6, 13, 29.6, 30, f=0)
            d.r(31, 12, 34.6, 23, 1.5)
        f.add(ARM, helm, rim=3, shiny=True)
        f.add(GOLD, lambda d: d.l([(14.6, 13), (34.6, 13)], 1.6), rim=1, shiny=True)
        f.add('#e04050', lambda d: d.p([(26, 4.4), (31, 0.4), (40, 1.4), (37, 6), (31, 6.4)]), rim=2)
    def front(f):
        front_arm(f, ARM)
        pauldron(f, 18, 25, ARM, 5.4, 4)
        f.add(GOLD, lambda d: d.l([(13, 25.4), (22, 23.6)], 1.1), rim=1, shiny=True)
    body(f, c, behind=behind, over_torso=over, head_extra=head, front=front)


def sniper(f):
    c = dict(hair='spiky', hair_c='#4a5a7a', sleeve='#e2e4ea', body='#e2e4ea', pants='#4a4a58', boots='#3a3a44', eye='#40b0d0')
    def behind(f):
        cape(f, '#2e6a8a', x0=18, x1=32, y=26, bottom=50, spread=5)
    def over(f):
        f.add('#2e6a8a', lambda d: (d.p([(17.6, 31), (32.4, 31), (35, 46), (27, 46), (25, 39), (23, 46), (15, 46)])), rim=2)
        belt(f, '#2e2e3a', METAL, y=31)
        f.add('#2e2e3a', lambda d: d.l([(19.5, 24.5), (31, 34)], 1.6), rim=1)
        f.add(METAL, lambda d: d.r(18.5, 22, 31.5, 25.6, 1.6), rim=1, shiny=True)
    def head(f):
        f.add('#3a3a44', lambda d: d.l([(15, 11.5), (34, 11.5)], 1.6), rim=1)
        f.add('#e8a030', lambda d: (d.e(19, 11.4, 2.6, 2.2), d.e(25, 11.4, 2.6, 2.2)), rim=2, shiny=True)
        f.add('#70e0ff', lambda d: (d.e(18.8, 11.2, 1.4, 1.2), d.e(24.8, 11.2, 1.4, 1.2)), rim=1, shiny=True)
    def front(f):
        bow(f, '#3a3a50', x=11, y0=13, y1=53, bend=6)
        f.add(METAL, lambda d: (d.p([(9.6, 15), (5, 12.5), (8, 18)]), d.p([(9.6, 51), (5, 53.6), (8, 48)])), rim=1, shiny=True)
        f.add(GOLD, lambda d: d.r(3.4, 31.5, 6.6, 34.5, .6), rim=1, shiny=True)
        front_arm(f, c['sleeve'])
    body(f, c, behind=behind, over_torso=over, head_extra=head, front=front)


def highpriest(f):
    c = dict(hair='long', hair_c='#f0e6c8', sleeve='#fbfaf6', body='#fbfaf6', pants='#fbfaf6', boots='#b0a080', eye='#d0a030')
    def behind(f):
        f.add('#fbfaf6', lambda d: (d.p([(30, 25), (44, 15), (45.5, 22), (42, 27), (44, 31), (38, 34), (32, 33)])), rim=3)
        f.add('#f0e070', lambda d: (d.e(24.5, 5.5, 8, 2.2), d.e(24.5, 5.5, 6.2, 1, f=0)), rim=1, outline=False, flat=True)
        f.parts[-1]['ramp'] = [(255, 236, 140)] * 5
        cape(f, '#e8d8a8', x0=18, x1=32, y=24, bottom=52, spread=5)
    def over(f):
        f.add(GOLD, lambda d: (d.p([(22, 24), (28, 24), (29, 52.5), (21, 52.5)])), rim=1, shiny=True)
        f.add('#c83a4a', lambda d: (d.p([(23.4, 25), (26.6, 25), (27.2, 52.5), (22.8, 52.5)])), rim=1)
        f.add(GOLD, lambda d: (d.r(24.2, 29, 25.8, 40), d.r(21.8, 32, 28.2, 33.6)), rim=1, shiny=True)
        f.add(GOLD, lambda d: d.e(25, 24, 8.2, 3.2), rim=2, shiny=True)
        f.add('#fbfaf6', lambda d: d.e(25, 23.6, 6.8, 2.2), rim=1)
    def head(f):
        f.add('#fbfaf6', lambda d: (d.p([(17.5, 9), (31.5, 9), (30, 2.5), (24.5, 0.4), (19, 2.5)])), rim=2)
        f.add(GOLD, lambda d: (d.l([(17.4, 8.6), (31.6, 8.6)], 1.6), d.r(23.8, 1.8, 25.2, 7.2), d.r(22, 3.6, 27, 5)), rim=1, shiny=True)
    def front(f):
        staff(f, top=(13, 9), bottom=(19, 51), shaft=GOLD)
        f.add(GOLD, lambda d: (d.p([(13, 0.6), (17.4, 5), (13, 11), (8.6, 5)]), d.p([(13, 2.6), (15.4, 5), (13, 8.8), (10.6, 5)], f=0)), rim=1, shiny=True)
        orb(f, 13, 5.2, 1.4, '#ff8aa0')
        front_arm(f, c['sleeve'])
    body(f, c, behind=behind, over_torso=over, head_extra=head, front=front, robe='#fbfaf6')


def assassincross(f):
    c = dict(hair='none', hair_c='#1a1a22', sleeve='#24202c', body='#24202c', pants='#24202c', boots='#18161e', eye='#c060ff')
    GLOW = '#c060ff'
    def behind(f):
        cape(f, '#3a1e4e', x0=17, x1=33, y=23, bottom=52, spread=6, tatter=True)
        f.add('#d8dce8', lambda d: d.p([(35, 35.5), (37.6, 35), (45, 45), (43, 49)]), rim=1, shiny=True)
        f.add(GLOW, lambda d: d.l([(37.4, 37.4), (43.6, 46.4)], .9), rim=1, outline=False, flat=True)
    def over(f):
        f.add('#6a2a9a', lambda d: d.r(18, 21.6, 31.8, 26.4, 2), rim=2)
        for k in range(4): f.add('#3e3848', lambda d, k=k: d.r(18.5, 27.4 + k * 1.7, 31.5, 28.2 + k * 1.7), rim=1)
        belt(f, '#6a2a9a', GLOW, y=34.2)
        pauldron(f, 32, 25.6, '#3e3848', 4.4, 3.2, shiny=False)
        f.add(METAL, lambda d: d.p([(33, 23), (36.6, 21.4), (35.4, 25)]), rim=1, shiny=True)
    def head(f):
        def hood(d):
            d.e(24.5, 14, 10.8, 10.8)
            d.p([(17, 8), (14, 0.6), (21, 5)])
            d.p([(29, 5), (35, 0.4), (33.4, 9)])
            d.e(22.8, 17.4, 7.6, 6.4, f=0)
        f.add('#24202c', hood, rim=3)
        f.add('#6a2a9a', lambda d: d.p([(16, 20), (31.5, 20), (30, 24.6), (17.4, 24.6)]), rim=1)
    def front(f):
        f.add('#d8dce8', lambda d: d.p([(15.4, 34), (18, 33.4), (11.4, 18), (8, 13.4), (11, 21)]), rim=1, shiny=True)
        f.add(GLOW, lambda d: d.l([(15.4, 32), (10.6, 19.4)], .9), rim=1, outline=False, flat=True)
        f.add('#3e3848', lambda d: d.r(14, 34, 20, 38, 1), rim=1)
        front_arm(f, c['sleeve'])
        pauldron(f, 18.2, 25.4, '#3e3848', 4.4, 3.2, shiny=False)
        f.add(METAL, lambda d: d.p([(16, 23), (12.6, 21.4), (14, 25)]), rim=1, shiny=True)
    body(f, c, behind=behind, over_torso=over, head_extra=head, front=front)
    f.stamps = [s for s in f.stamps if s[1] < 20]


def highwizard(f):
    c = dict(hair='long', hair_c='#2a2030', sleeve='#9a1e2e', body='#9a1e2e', pants='#9a1e2e', boots='#2a1a20', eye='#ff6a3a')
    def behind(f):
        cape(f, '#1e1a24', x0=17, x1=33, y=23, bottom=52, spread=6)
        f.add('#2a1a2e', lambda d: d.p([(15, 23), (35, 23), (36, 28), (14, 28)]), rim=2)
    def over(f):
        f.add('#e8b440', lambda d: d.p([(22.4, 24), (27.6, 24), (28.6, 52.5), (21.4, 52.5)]), rim=1, shiny=True)
        f.add('#1e1a24', lambda d: d.p([(23.3, 25), (26.7, 25), (27.4, 52.5), (22.6, 52.5)]), rim=1)
        f.add('#e8b440', lambda d: d.p([(15.6, 50.2), (34.8, 50.2), (35.5, 52.5), (15, 52.5)]), rim=1, shiny=True)
        belt(f, '#e8b440', '#ff6a3a', y=31.5)
        f.add('#1e1a24', lambda d: (d.p([(16, 21.5), (34, 21.5), (33, 27), (25, 25), (17, 27)])), rim=2)
    def head(f):
        def hat(d):
            d.e(24.5, 9.6, 14, 3.4)
            d.p([(16.5, 9.5), (32, 9.5), (31, 3.5), (37, 0.4), (25, 1.6), (20, 4)])
        f.add('#1e1a24', hat, rim=2)
        f.add('#9a1e2e', lambda d: d.p([(17.4, 7.8), (31.6, 7.8), (31.8, 9.6), (17.2, 9.6)]), rim=1)
        f.add('#ff6a3a', lambda d: d.e(24, 8.4, 1.6), rim=1, shiny=True)
    def front(f):
        staff(f, top=(12, 11), bottom=(19, 51), shaft='#2a1a20')
        f.add(GOLD, lambda d: (d.p([(12, 13), (8.4, 7), (10, 9.6), (12, 4), (14, 9.6), (15.6, 7)])), rim=1, shiny=True)
        orb(f, 12, 6.4, 2.6, '#ff6a3a')
        front_arm(f, c['sleeve'])
    body(f, c, behind=behind, over_torso=over, head_extra=head, front=front, robe='#9a1e2e')


CHARS = dict(swordsman=swordsman, archer=archer, acolyte=acolyte, thief=thief, mage=mage,
             knight=knight, hunter=hunter, priest=priest, assassin=assassin, wizard=wizard,
             lordknight=lordknight, sniper=sniper, highpriest=highpriest, assassincross=assassincross,
             highwizard=highwizard)


def trim_x(im):
    a = np.array(im)[:, :, 3]; xs = np.nonzero(a.any(0))[0]
    return im.crop((xs[0], 0, xs[-1] + 1, H))


if __name__ == '__main__':
    only = sys.argv[1:] or list(CHARS)
    os.makedirs(os.path.join(OUT, 'units'), exist_ok=True)
    ims = {}
    for k in only:
        ims[k] = trim_x(mk(CHARS[k]))
        ims[k].save(os.path.join(OUT, 'units', k + '.png'))
    # preview: each sprite at 1x and 4x on a checker
    cw, ch, z = 64, 70, 4
    cols = 5; rows = (len(ims) + cols - 1) // cols
    pv = Image.new('RGBA', (cols * cw * z, rows * ch * z), (40, 46, 64, 255))
    for i, (k, im) in enumerate(ims.items()):
        x, y = (i % cols) * cw * z, (i // cols) * ch * z
        tile = Image.new('RGBA', (cw, ch), (52, 68, 44, 255) if i % 2 else (46, 59, 39, 255))
        tile.alpha_composite(im, ((cw - im.width) // 2, ch - H - 4))
        pv.paste(tile.resize((cw * z, ch * z), Image.NEAREST), (x, y))
    pv.save(os.path.join(OUT, 'preview.png'))
    print('ok', list(ims))
