"""Turns a hand-made character picture into a hero sprite: assets/art/<id>.png.
A hero with a picture in assets/art uses it instead of its code-drawn pixel sprite (build_sprites.py copies it to
assets/units and skips the limb rig, so it animates as one piece).
Run:  python tools/prep_art.py <picture> <id> <left> <top> <right> <bottom> [erase boxes x0,y0,x1,y1 ...]
      (the box crops the pose out of a sheet; the white background is removed; erase boxes, in sheet
      coordinates, clear scenery that touches the character)"""
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'art')
HEIGHT = 162   # 3x the 54px sprite height: drawn about 1:1 on most screens


def polish(pic):
    """Bake in what the game would otherwise do every frame: a little more colour and contrast (painted art reads
    paler than the pixel heroes) and a thin dark outline so the hero stands out on the grass."""
    from PIL import ImageEnhance
    rgb = ImageEnhance.Contrast(ImageEnhance.Color(pic.convert('RGB')).enhance(1.2)).enhance(1.06)
    out = np.asarray(rgb.convert('RGBA')).copy()
    alpha = np.asarray(pic)[..., 3]
    out[..., 3] = alpha
    solid = alpha > 40
    ring = ndimage.binary_dilation(solid, iterations=2) & ~solid
    out[ring] = (28, 16, 10, 230)
    return Image.fromarray(out)


def prep(src, cid, box, erase=()):
    im = Image.open(src).convert('RGBA')
    for x0, y0, x1, y1 in erase:
        im.paste((255, 255, 255, 255), (x0, y0, x1, y1))
    im = im.crop(box)
    a = np.asarray(im).astype(np.int16)
    rgb = a[..., :3]
    # background: near-white, low-saturation pixels connected to the border
    light = (rgb.min(axis=2) > 226) & (rgb.max(axis=2) - rgb.min(axis=2) < 26)
    lab, _ = ndimage.label(light)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, lab.max() + 1))
    pure = (rgb.min(axis=2) > 240)
    gap = 600 * ((box[3] - box[1]) / 800) ** 2   # smaller figures on the sheet have smaller gaps
    big = [i + 1 for i, n in enumerate(sizes) if n > gap and pure[lab == i + 1].mean() > .8]
    bg |= np.isin(lab, big)   # large pure-white gaps enclosed by hair (armour and eye highlights are smaller)
    # keep only the biggest shape (drops sparkles, scenery and stray specks)
    body, n = ndimage.label(~bg, structure=np.ones((3, 3)))
    if n > 1:
        sizes = ndimage.sum(np.ones_like(body), body, range(1, n + 1))
        bg |= body != (1 + int(np.argmax(sizes)))
    out = np.asarray(im).copy()
    out[bg, 3] = 0
    pic = Image.fromarray(out)
    pic = pic.crop(pic.getbbox())
    w, h = pic.size
    pic = pic.resize((round(w * HEIGHT / h), HEIGHT), Image.LANCZOS)
    pic = polish(pic)
    os.makedirs(OUT, exist_ok=True)
    pic.save(os.path.join(OUT, cid + '.png'), optimize=True)
    print('saved', cid, pic.size)


if __name__ == '__main__':
    prep(sys.argv[1], sys.argv[2], tuple(int(v) for v in sys.argv[3:7]), [tuple(int(v) for v in b.split(',')) for b in sys.argv[7:]])
