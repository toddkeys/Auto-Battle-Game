"""Builds all 15 anime-style unit sprites -> assets/units/<id>.png + assets/preview.png
Run:  python tools/build_sprites.py   then   python tools/build_game.py"""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import kit  # noqa: E402
import classes  # noqa: E402
import monsters  # noqa: E402
from pixel import W, H  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
CHARS = dict(swordsman=kit.swordsman, **classes.CLASSES, **monsters.MONSTERS)


def preview(sprites, scale=4, cols=5):
    cw, ch = W * scale + 16, H * scale + 30
    rows = (len(sprites) + cols - 1) // cols
    sheet = Image.new('RGBA', (cw * cols, ch * rows), (52, 68, 44, 255))
    d = ImageDraw.Draw(sheet)
    for i, (cid, im) in enumerate(sprites.items()):
        x, y = (i % cols) * cw, (i // cols) * ch
        d.rectangle([x + 2, y + 2, x + cw - 3, y + ch - 3], fill=(70, 120, 60, 255) if i % 2 else (84, 136, 70, 255))
        sheet.alpha_composite(im.resize((W * scale, H * scale), Image.NEAREST), (x + 8, y + 4))
        d.text((x + 10, y + ch - 22), cid, fill=(255, 255, 255, 255))
    sheet.save(os.path.join(OUT, 'preview.png'))


if __name__ == '__main__':
    os.makedirs(os.path.join(OUT, 'units'), exist_ok=True)
    ims = {}
    for cid, fn in CHARS.items():
        ims[cid] = fn().render()
        ims[cid].save(os.path.join(OUT, 'units', cid + '.png'))
    preview(ims)
    print('built', len(ims))
