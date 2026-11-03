"""Builds assets/vfx/<name>.png (frames side by side) + <name>.json from the downloaded effect packs.
Credits / licenses: assets/vfx/CREDITS.txt (all CC0).
Run:  python tools/build_vfx.py <folder with the extracted packs>   then   python tools/build_game.py"""
import glob
import json
import os
import re
import sys
from PIL import Image

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'vfx')


def numbered(pattern):
    return [Image.open(f).convert('RGBA') for f in sorted(glob.glob(os.path.join(SRC, pattern)), key=lambda f: int(re.findall(r'(\d+)\.png$', f)[0]))]


def sheet(path, fw, fh, n):
    im = Image.open(os.path.join(SRC, path)).convert('RGBA')
    cols = im.width // fw
    return [im.crop(((i % cols) * fw, (i // cols) * fh, (i % cols) * fw + fw, (i // cols) * fh + fh)) for i in range(n)]


# name -> (frames, max frames kept, max height in px)
EFFECTS = {
    'strike': (numbered('fx/fx1_blue_topEffect/*.png'), 14, 150),     # lightning strike from the sky (Mikodrak)
    'slash': (numbered('fx/fx2_swordFire/*.png'), 16, 70),           # burning sword arc
    'blaze': (numbered('fx/fx3_fireBall/*.png'), 14, 80),            # fire swirl explosion
    'sigil': (numbered('fx/fx4_sign_of_fire/*.png'), 12, 110),       # glowing sigil
    'scissor': (numbered('fx/fx5_fire_scissors/*.png'), 10, 110),    # two blades of flame snapping together
    'geyser': (numbered('fx/fx6_eaterFire/*.png'), 14, 110),         # fountain burst
    'nova': (numbered('fx/fx7_energyBall/*.png'), 16, 70),           # white energy burst (tinted per skill)
    'spark': (numbered('fx/fx8_lighteningBall/*.png'), 12, 60),      # electric ball
    'smoke': (numbered('fx/fx10_blackExplosion/*.png'), 12, 60),     # black smoke puff
    'boom': (sheet('explosion2_4.png', 100, 100, 56), 20, 100),      # ring explosion (BenHickling)
    # projectiles (16px, 6 frames) - DevWizard / StarsteelGaming
    'p_fire': (sheet('dw/Pixelart Spells/PNG Files/Fireball.png', 16, 16, 6), 6, 16),
    'p_ice': (sheet('dw/Pixelart Spells/PNG Files/Ice Lance.png', 16, 16, 4), 4, 16),
    'p_light': (sheet('dw/Pixelart Spells/PNG Files/Light Bolt.png', 16, 16, 6), 6, 16),
    'p_dark': (sheet('dw/Pixelart Spells/PNG Files/Darkness Orb.png', 16, 16, 6), 6, 16),
    'p_arcane': (sheet('dw/Pixelart Spells/PNG Files/Magic Orb.png', 16, 16, 6), 6, 16),
    'p_plant': (sheet('dw/Pixelart Spells/PNG Files/Plant Missle.png', 16, 16, 6), 6, 16),
}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for name, (frames, keep, maxh) in EFFECTS.items():
        if len(frames) > keep:   # evenly drop frames
            frames = [frames[round(i * (len(frames) - 1) / (keep - 1))] for i in range(keep)]
        box = None
        for f in frames:   # union of the visible area over all frames
            b = f.getbbox()
            if b:
                box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
        full = frames[0].size
        frames = [f.crop(box) for f in frames]
        k = min(1, maxh / frames[0].height)
        if k < 1:
            frames = [f.resize((max(1, round(f.width * k)), max(1, round(f.height * k))), Image.LANCZOS) for f in frames]
        fw, fh = frames[0].size
        strip = Image.new('RGBA', (fw * len(frames), fh))
        for i, f in enumerate(frames):
            strip.paste(f, (i * fw, 0))
        p = os.path.join(OUT, name + '.png')
        strip.save(p, optimize=True)
        # anchor: where the original frame's centre lands inside the cropped frame (0..1)
        ax = (full[0] / 2 - box[0]) / (box[2] - box[0])
        ay = (full[1] / 2 - box[1]) / (box[3] - box[1])
        with open(os.path.join(OUT, name + '.json'), 'w') as fjs:
            json.dump({'fw': fw, 'fh': fh, 'n': len(frames), 'ax': round(ax, 3), 'ay': round(ay, 3)}, fjs)
        total += os.path.getsize(p)
    print(f'built {len(EFFECTS)} effects, {total // 1024} KB')
