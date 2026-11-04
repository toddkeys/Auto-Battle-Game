"""Builds every unit and monster sprite -> assets/units/<id>.png + assets/preview.png,
plus the animation rig: assets/rig/<id>.png (one 56x54 layer per piece, left to right)
and assets/rig/<id>.json (which group each layer belongs to + joint pivots).
Run:  python tools/build_sprites.py   then   python tools/build_game.py"""
import json
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import kit  # noqa: E402
import classes  # noqa: E402
import monsters  # noqa: E402
import tier4  # noqa: E402
import summoners  # noqa: E402
import creatures  # noqa: E402
import crusaders  # noqa: E402
import occultists  # noqa: E402
import samurai  # noqa: E402
import frostkin  # noqa: E402
import gamblers  # noqa: E402
import newclasses  # noqa: E402
import newclasses2  # noqa: E402
import bosses  # noqa: E402
import hookers  # noqa: E402
import gunslingers  # noqa: E402
import monkeys  # noqa: E402
import mimics  # noqa: E402
from pixel import W, H  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
CHARS = dict(swordsman=kit.swordsman, **classes.CLASSES, **tier4.TIER4, **crusaders.CRUSADERS, **occultists.OCCULTISTS, **samurai.SAMURAI, **frostkin.FROSTKIN, **gamblers.GAMBLERS, **newclasses.NEWCLASSES, **newclasses2.NEWCLASSES2, **hookers.HOOKERS, **gunslingers.GUNSLINGERS, **monkeys.MONKEYS, **mimics.MIMICS, **summoners.SUMMONERS,
             **monsters.MONSTERS, **creatures.CREATURES, **bosses.BOSSES)


def preview(sprites, scale=4, cols=6):
    cw, ch = W * scale + 16, H * scale + 30
    rows = (len(sprites) + cols - 1) // cols
    sheet = Image.new('RGBA', (cw * cols, ch * rows), (52, 68, 44, 255))
    d = ImageDraw.Draw(sheet)
    for i, (cid, im) in enumerate(sprites.items()):
        x, y = (i % cols) * cw, (i // cols) * ch
        d.rectangle([x + 2, y + 2, x + cw - 3, y + ch - 3], fill=(70, 120, 60, 255) if i % 2 else (84, 136, 70, 255))
        sheet.alpha_composite(im.resize((W * scale, H * scale), Image.NEAREST if im.size == (W, H) else Image.LANCZOS), (x + 8, y + 4))
        d.text((x + 10, y + ch - 22), cid, fill=(255, 255, 255, 255))
    sheet.save(os.path.join(OUT, 'preview.png'))


if __name__ == '__main__':
    os.makedirs(os.path.join(OUT, 'units'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'rig'), exist_ok=True)
    ims = {}
    for cid, fn in CHARS.items():
        art = os.path.join(OUT, 'art', cid + '.png')
        if os.path.exists(art):   # a hand-made picture replaces the drawn sprite (no limb rig: it moves as one piece)
            ims[cid] = Image.open(art).convert('RGBA')
            ims[cid].save(os.path.join(OUT, 'units', cid + '.png'))
            for ext in ('.png', '.json'):
                if os.path.exists(os.path.join(OUT, 'rig', cid + ext)):
                    os.remove(os.path.join(OUT, 'rig', cid + ext))
            continue
        ims[cid] = fn().render()
        ims[cid].save(os.path.join(OUT, 'units', cid + '.png'))
        s = fn()
        layers = s.layers()
        frames = [im for _, im in layers]
        meta = {'layers': [g for g, _ in layers], 'piv': {'head': (28, 27), 'body': (28, 44), 'cape': (28, 28), **s.piv}}
        if 'weapon' in meta['layers']:
            meta['piv']['weapon'] = s.hands['armR']   # the wrist
        if s.face_layer is not None:   # heroes: one extra copy of the face layer per expression, appended after the pieces
            meta['faceLayer'], meta['expr'] = s.face_layer, {}
            for e in kit.EXPRESSIONS:
                kit.EXPR = e
                meta['expr'][e] = len(frames)
                frames.append(fn().layers()[s.face_layer][1])
            kit.EXPR = None
        strip = Image.new('RGBA', (W * len(frames), H), (0, 0, 0, 0))
        for i, im in enumerate(frames):
            strip.paste(im, (i * W, 0))
        strip.save(os.path.join(OUT, 'rig', cid + '.png'), optimize=True)
        with open(os.path.join(OUT, 'rig', cid + '.json'), 'w') as f:
            json.dump(meta, f)
    preview(ims)
    print('built', len(ims))
