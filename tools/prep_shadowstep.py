"""One-off prep for the Shadowstep art (assets/art/src/shadowstep_sheet.png, drawn on a black background).
Cuts the standing pose and the back view off the dark background, puts the sheet's separate glowing katana in his
front hand (blade up and forward, like the other sword heroes), and saves assets/art/shadowstep(_back).png."""
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.dirname(__file__))
import prep_art  # noqa: E402

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, '..', 'assets', 'art', 'src', 'shadowstep_sheet.png')
OUT = os.path.join(HERE, '..', 'assets', 'art')


def cut_dark(sheet, box, dark=16):
    """near-black pixels connected to the box edge are background; keep the biggest shape (drops sparkles)"""
    a = np.asarray(sheet.crop(box).convert('RGBA')).copy()
    near = a[..., :3].max(axis=2) <= dark
    lab, _ = ndimage.label(near)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    shadow = (a[..., 2] > a[..., 1] + 8) & (a[..., :3].max(axis=2) < 150) & (a[..., 0] > 25)   # the purple ground glow under the feet
    rows = np.arange(a.shape[0])[:, None] > a.shape[0] - 20
    bg |= shadow & rows
    body, n = ndimage.label(~bg, structure=np.ones((3, 3)))
    if n > 1:
        sizes = ndimage.sum(np.ones_like(body), body, range(1, n + 1))
        bg |= body != (1 + int(np.argmax(sizes)))
    a[bg, 3] = 0
    pic = Image.fromarray(a)
    return pic.crop(pic.getbbox())


def finish(pic, cid):
    w, h = pic.size
    pic = pic.resize((round(w * prep_art.HEIGHT / h), prep_art.HEIGHT), Image.LANCZOS)
    pic = prep_art.polish(pic)
    pic.save(os.path.join(OUT, cid + '.png'), optimize=True)
    print('saved', cid, pic.size)


def main():
    sheet = Image.open(SRC).convert('RGB')
    sheet.paste((5, 4, 7), (868, 1000, 915, 1220))   # the scarf drawn beside the katana's lower blade
    hero = cut_dark(sheet, (8, 884, 152, 1232))          # standing pose, facing us
    back = cut_dark(sheet, (412, 884, 542, 1232))        # back view
    sword = cut_dark(sheet, (812, 888, 912, 1218), dark=20)   # the separate glowing katana: hilt at the top, tip at the bottom
    sa = np.asarray(sword)
    ys, xs = np.nonzero(sa[..., 3] > 0)
    top = ys.min()
    hx = xs[ys < top + 6].mean()                        # the hilt end
    sw = sword.resize((round(sword.width * .74), round(sword.height * .74)), Image.LANCZOS)
    hx, hy = hx * .74, (top + 4) * .74
    ang = 220   # hilt at the bottom, blade up and forward (to the left)
    cx, cy = sw.width / 2, sw.height / 2
    rot = sw.rotate(ang, expand=True, resample=Image.BICUBIC)
    t = np.radians(ang)
    dx, dy = hx - cx, hy - cy
    rx, ry = dx * np.cos(t) + dy * np.sin(t), -dx * np.sin(t) + dy * np.cos(t)
    hx2, hy2 = rot.width / 2 + rx, rot.height / 2 + ry   # where the hilt end landed
    # the front fist (on the left of the picture): the hilt end goes a little below it so the grip sits in the hand
    fist = (29, 205)
    pad = 160
    canvas = Image.new('RGBA', (hero.width + pad * 2, hero.height + pad * 2), (0, 0, 0, 0))
    canvas.alpha_composite(hero, (pad, pad))
    canvas.alpha_composite(rot, (round(pad + fist[0] - hx2), round(pad + fist[1] + 10 - hy2)))
    fz = hero.crop((fist[0] - 14, fist[1] - 13, fist[0] + 14, fist[1] + 13))   # the fist back over the grip
    canvas.alpha_composite(fz, (pad + fist[0] - 14, pad + fist[1] - 13))
    canvas = canvas.crop(canvas.getbbox())
    finish(canvas, 'shadowstep')
    finish(back, 'shadowstep_back')


if __name__ == '__main__':
    main()
