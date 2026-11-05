"""One-off prep for the Stormweaver art (assets/art/src/voidsage_sheet.png): every purple shade (hair, eyes, coat,
crystals, lightning) becomes the matching electric blue, then prep_art cuts the stance and the back view."""
import colorsys
import os
import sys

import numpy as np
from PIL import Image, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
import prep_art  # noqa: E402

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, '..', 'assets', 'art', 'src', 'voidsage_sheet.png')
TMP = os.path.join(HERE, '..', 'assets', 'art', 'src', 'stormweaver_work.png')


def main():
    a = np.asarray(Image.open(SRC).convert('RGB')).astype(int)
    for y0, y1, x0, x1 in ((870, 892, 0, 160), (1220, 1240, 530, 670)):   # ground shadows (lavender)
        reg = a[y0:y1, x0:x1]
        r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
        reg[(b > g + 6) & (r > 100) & (b > 140) & (abs(r - g) < 40)] = 255
    f = a.astype(float) / 255
    h, s, v = np.vectorize(colorsys.rgb_to_hsv)(f[..., 0], f[..., 1], f[..., 2])
    purple = (h > 245 / 360) & (h < 345 / 360) & (s > .14)   # violet through magenta highlights
    nh = np.where(purple, 205 / 360 + (h - 275 / 360) * .3, h)   # keep a little of the original hue spread
    ns = np.where(purple, np.minimum(1, s * 1.05), s)
    nv = np.where(purple, np.minimum(1, v * 1.12), v)
    r, g, b = np.vectorize(colorsys.hsv_to_rgb)(nh, ns, nv)
    out = (np.stack([r, g, b], -1) * 255).round().astype(np.uint8)
    Image.fromarray(out).save(TMP)
    prep_art.prep(TMP, 'voidsage', (12, 712, 151, 888))
    prep_art.prep(TMP, 'voidsage_back', (536, 915, 664, 1232))
    p = os.path.join(HERE, '..', 'assets', 'art', 'voidsage.png')
    ImageOps.mirror(Image.open(p)).save(p)   # like every hero, she faces left
    os.remove(TMP)


if __name__ == '__main__':
    main()
