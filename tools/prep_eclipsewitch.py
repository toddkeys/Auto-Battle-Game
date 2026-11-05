"""One-off prep for the Eclipse Witch art (assets/art/src/eclipsewitch_sheet.png): prep_art cuts the stance and the back
view, then her white robe becomes a deep eclipse black-violet (her white hair stays)."""
import colorsys
import os
import sys

import numpy as np
from PIL import Image, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
import prep_art  # noqa: E402

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, '..', 'assets', 'art', 'src', 'eclipsewitch_sheet.png')
TMP = os.path.join(HERE, '..', 'assets', 'art', 'src', 'eclipsewitch_work.png')


def hair_to_midnight(a, area):
    f = a.astype(float) / 255
    h, s, v = np.vectorize(colorsys.rgb_to_hsv)(f[..., 0], f[..., 1], f[..., 2])
    hair = area & (((h > 225 / 360) & (h < 310 / 360) & (s > .05) & (s < .42) & (v > .55)) | ((s <= .06) & (v > .72)))   # lavender, and the near-white highlights
    nv = .07 + .42 * v   # keep the light-to-shadow shading, much darker
    r, g, b = np.vectorize(colorsys.hsv_to_rgb)(np.full_like(h, 268 / 360), np.full_like(s, .52), nv)
    out = (np.stack([r, g, b], -1) * 255).round()
    a[hair] = out[hair]
    return hair.sum()


def grid(cid):
    from PIL import ImageDraw
    a = Image.open(os.path.join(HERE, '..', 'assets', 'art', cid + '.png')).convert('RGBA'); S = 4
    bg = Image.new('RGBA', a.size, (52, 68, 44, 255)); bg.alpha_composite(a); im = bg.resize((a.width * S, a.height * S), Image.NEAREST); d = ImageDraw.Draw(im)
    for x in range(0, a.width, 10): d.line([(x * S, 0), (x * S, im.height)], fill=(255, 255, 255, 90) if x % 50 else (255, 255, 0, 200)); d.text((x * S + 2, 2), str(x), fill=(255, 255, 255, 255))
    for y in range(0, a.height, 10): d.line([(0, y * S), (im.width, y * S)], fill=(255, 255, 255, 90) if y % 50 else (255, 255, 0, 200)); d.text((2, y * S + 2), str(y), fill=(255, 255, 255, 255))
    return im


def cut_only():
    a = np.asarray(Image.open(SRC).convert('RGB')).astype(int)
    for y0, y1, x0, x1 in ((838, 860, 0, 200), (1192, 1218, 585, 720)):
        reg = a[y0:y1, x0:x1]
        r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
        reg[(b > g + 6) & (r > 100) & (b > 140)] = 255
    a[795:862, 152:200] = 255
    Image.fromarray(a.astype(np.uint8)).save(TMP)
    prep_art.prep(TMP, 'eclipsewitch', (8, 715, 178, 856))
    prep_art.prep(TMP, 'eclipsewitch_back', (590, 895, 718, 1215))
    os.remove(TMP)


def recolour_art(cid, area, keep):
    """area/keep: functions of (xx, yy) in picture pixels -> where the hair is / what must stay (face)"""
    p = os.path.join(HERE, '..', 'assets', 'art', cid + '.png')
    a = np.asarray(Image.open(p).convert('RGBA')).astype(float)
    f = a[..., :3] / 255
    h, s, v = np.vectorize(colorsys.rgb_to_hsv)(f[..., 0], f[..., 1], f[..., 2])
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    zone, face = area(xx, yy) & (a[..., 3] > 0), keep(xx, yy)
    hair = zone & (((h > 225 / 360) & (h < 310 / 360) & (s > .04) & (s < .42) & (v > .5)) | ((s <= .07) & (v > .7) & ~face))
    nv = .07 + .42 * v   # keep the light-to-shadow shading, much darker
    r, g, b = np.vectorize(colorsys.hsv_to_rgb)(np.full_like(h, 268 / 360), np.full_like(s, .52), nv)
    out = np.stack([r, g, b], -1) * 255
    a[..., :3][hair] = out[hair]
    Image.fromarray(a.round().astype(np.uint8)).save(p)
    print(cid, 'hair pixels', int(hair.sum()))


def robe_to_eclipse(cid, area):
    """the white robe (and its lavender shading) becomes a deep eclipse black-violet; gold trim, skin and hair stay"""
    p = os.path.join(HERE, '..', 'assets', 'art', cid + '.png')
    a = np.asarray(Image.open(p).convert('RGBA')).astype(float)
    f = a[..., :3] / 255
    h, s, v = np.vectorize(colorsys.rgb_to_hsv)(f[..., 0], f[..., 1], f[..., 2])
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    zone = area(xx, yy) & (a[..., 3] > 0)
    robe = zone & (v > .45) & ((s < .08) | ((h > 220 / 360) & (h < 320 / 360) & (s < .4)))   # whites and lavender shading
    nv = .09 + .3 * v
    r, g, b = np.vectorize(colorsys.hsv_to_rgb)(np.full_like(h, 268 / 360), np.full_like(s, .45), nv)
    out = np.stack([r, g, b], -1) * 255
    a[..., :3][robe] = out[robe]
    Image.fromarray(a.round().astype(np.uint8)).save(p)
    print(cid, 'robe pixels', int(robe.sum()))


def main():
    cut_only()
    # the stance (before mirroring): everything below the neck except the long white tail flowing left
    robe_to_eclipse('eclipsewitch', lambda x, y: (y >= 57) & (x > 40) & ~((x < 80) & (y < 100)))
    # the back view: the collar and robe between the twintails, and everything below them
    robe_to_eclipse('eclipsewitch_back', lambda x, y: ((y >= 38) & (x > 20) & (x < 48)) | (y >= 78))
    p = os.path.join(HERE, '..', 'assets', 'art', 'eclipsewitch.png')
    ImageOps.mirror(Image.open(p)).save(p)   # like every hero, she faces left


if __name__ == '__main__':
    main()
