"""One-off prep for the 2g Wukong art (assets/art/src/monkeys_sheet_clean.png): recolours the outfit (orange cloth ->
jade, blue sash/undershirt -> gold), puts the sheet's separate staff in his front fist, then hands off to prep_art."""
import colorsys
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.dirname(__file__))
import prep_art  # noqa: E402

SRC = os.path.join(os.path.dirname(__file__), '..', 'assets', 'art', 'src', 'monkeys_sheet_clean.png')
TMP = os.path.join(os.path.dirname(__file__), '..', 'assets', 'art', 'src', 'monkey2g_work.png')


def recolour(a, box, below):
    x0, y0, x1, y1 = box
    reg = a[y0:y1, x0:x1, :3].astype(float) / 255
    h, s, v = np.vectorize(colorsys.rgb_to_hsv)(reg[..., 0], reg[..., 1], reg[..., 2])
    rows = (np.arange(y0, y1) >= below)[:, None]   # cloth only: below the neck, so hair and skin keep their colours
    orange = rows & (h > 4 / 360) & (h < 46 / 360) & (s > .72)   # dyed cloth is far more saturated than the brown tail or skin
    blue = (h > 195 / 360) & (h < 250 / 360) & (s > .3) & (v > .18)
    blue &= rows
    nh = np.where(orange, 158 / 360, np.where(blue, 44 / 360, h))
    ns = np.where(orange, np.minimum(1, s * .8), np.where(blue, np.minimum(1, s * 1.1 + .25), s))
    nv = np.where(orange, v * .66, np.where(blue, np.minimum(1, v * 1.25 + .15), v))
    r, g, b = np.vectorize(colorsys.hsv_to_rgb)(nh, ns, nv)
    out = np.stack([r, g, b], -1) * 255
    m = orange | blue
    reg2 = a[y0:y1, x0:x1]
    reg2[m, :3] = out[m].astype(np.uint8)


def main():
    im = Image.open(SRC).convert('RGBA')
    a = np.asarray(im).copy()
    # sparkles touching his hair on the left, and the red sheet's fire effect next door
    for x0, y0, x1, y1 in ((636, 830, 696, 902), (766, 890, 782, 918)):   # sparkles and a speed dash
        reg = a[y0:y1, x0:x1]
        spark = (reg[..., 0] > 195) & (reg[..., 1] > 140)
        reg[spark] = (255, 255, 255, 255)
    a[780:985, 590:650] = (255, 255, 255, 255)
    recolour(a, (655, 800, 780, 980), 880)      # front pose
    recolour(a, (975, 975, 1085, 1180), 1068)    # back view
    sheet = Image.fromarray(a)
    # the staff drawn on its own on the sheet: cut it out, shorten it, tilt it forward, put it in the front fist
    st = sheet.crop((1076, 976, 1130, 1182))
    sa = np.asarray(st).copy()
    bg = (sa[..., :3].min(axis=2) > 222)
    sa[bg, 3] = 0
    lab, n = ndimage.label(sa[..., 3] > 0, structure=np.ones((3, 3)))   # just the staff: drop the sparkle drawn beside it
    if n > 1:
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        sa[lab != 1 + int(np.argmax(sizes)), 3] = 0
    st = Image.fromarray(sa)
    st = st.crop(st.getbbox())
    st = st.resize((round(st.width * .74), round(st.height * .74)), Image.LANCZOS)
    st = st.rotate(22, expand=True, resample=Image.BICUBIC)   # top leans forward (left)
    fist = (672, 914)
    grip = .64   # how far down the staff the fist is (0 = top)
    ox, oy = round(fist[0] - st.width * (1 - grip)), round(fist[1] - st.height * grip)
    keep = sheet.crop((659, 902, 686, 927))   # the fist goes back over the shaft
    ka = np.asarray(keep).copy()
    ka[ka[..., :3].min(axis=2) > 222, 3] = 0
    sheet.alpha_composite(st, (ox, oy))
    sheet.alpha_composite(Image.fromarray(ka), (659, 902))
    sheet.convert('RGB').save(TMP)
    print('staff at', ox, oy, st.size)
    prep_art.prep(TMP, 'stonemonkey', (min(640, ox - 2), min(796, oy - 2), 776, 976))
    prep_art.prep(TMP, 'stonemonkey_back', (972, 975, 1082, 1180))


if __name__ == '__main__':
    main()
