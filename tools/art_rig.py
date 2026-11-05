"""Cuts a hand-made hero picture (assets/art/<id>.png, 3x sprite size) into animation-rig pieces, so it moves like
the drawn heroes: the sword arm swings, the shield and head turn. Writes assets/rig/<id>.png + .json with k=3
(each layer is 168x162 = 3x the 56x54 sprite; pivots are in sprite pixels).
Pieces are polygons in picture pixels. Whatever a moving piece covered on the body is filled with the nearest
body colours, so no holes show when it moves."""
import json
import os

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

K = 3
W, H = 56 * K, 54 * K

# per hero: pieces in draw order (back to front) with polygon + pivot (picture pixels); 'body' takes the rest
ART_RIGS = {
    'aegispaladin': {
        'order': ['body', 'head', 'weapon', 'armR', 'armL'],
        'parts': {
            'head': {'poly': [(42, 6), (112, 6), (118, 28), (108, 50), (92, 54), (66, 54), (50, 44), (44, 24)], 'piv': (80, 52)},
            'weapon': {'poly': [(42, 96), (62, 96), (63, 103), (54.2, 106), (4.2, 162), (-.2, 158), (49.8, 102), (42, 103)], 'piv': (55, 94)},
            'armR': {'poly': [(52, 64), (70, 64), (70, 82), (64, 98), (50, 98), (48, 86)], 'piv': (63, 64)},
            'armL': {'poly': [(96, 40), (118, 36), (160, 58), (158, 142), (140, 156), (112, 136), (100, 104), (96, 70)], 'piv': (100, 62)},
        },
    },
    # the Crimson Valkyrie: both hands on a halberd held across the body; the arms are cut first so the hands
    # stay on top of the shaft, the halberd turns at her front hand
    'starwarden': {
        'order': ['body', 'head', 'weapon', 'armL', 'armR'],   # mirrored: like every hero she faces left, halberd forward
        'parts': {
            'head': {'poly': [(129, 22), (105, 8), (77, 12), (59, 48), (63, 74), (77, 82), (111, 82), (127, 66)], 'piv': (95, 80)},
            'armR': {'poly': [(85, 84), (73, 84), (62, 91), (62, 106), (77, 106), (78.5, 96)], 'piv': (81, 86)},
            'armL': {'poly': [(111, 84), (101, 86), (103, 94), (109, 106), (123, 106), (123, 92)], 'piv': (105, 86)},
            'weapon': {'poly': [(135, 97.5), (55, 96.5), (55, 72), (-1, 70), (-1, 130), (55, 130), (55, 104.5), (135, 104.5)], 'piv': (69, 100)},
        },
    },
}


def build(cid, art_dir, rig_dir):
    spec = ART_RIGS[cid]
    pic = Image.open(os.path.join(art_dir, cid + '.png')).convert('RGBA')
    cw = max(W, -(-pic.width // K) * K)   # a picture wider than the frame gets a wider frame (fw), so nothing is clipped
    fw = cw // K
    canvas = Image.new('RGBA', (cw, H), (0, 0, 0, 0))
    ox, oy = (cw - pic.width) // 2, H - pic.height   # centred, feet on the bottom edge
    canvas.paste(pic, (ox, oy))
    src = np.asarray(canvas).copy()
    opaque = src[..., 3] > 0
    layers, taken, blade = {}, np.zeros(opaque.shape, bool), None
    for name, part in spec['parts'].items():
        m = Image.new('L', (cw, H), 0)
        ImageDraw.Draw(m).polygon([(x + ox, y + oy) for x, y in part['poly']], fill=255)
        mask = (np.asarray(m) > 0) & opaque & ~taken
        taken |= mask
        if name == 'weapon':
            blade = mask
        lay = np.zeros_like(src)
        lay[mask] = src[mask]
        layers[name] = lay
    body = src.copy()
    body[taken] = 0
    # fill what the moving pieces covered with the nearest body colour; a bare blade out over the background stays empty
    has = body[..., 3] > 0
    dist, (iy, ix) = ndimage.distance_transform_edt(~has, return_indices=True)
    fill = taken & ((dist <= 3) | ~(blade if blade is not None else taken))
    body[fill] = body[iy[fill], ix[fill]]
    layers['body'] = body
    strip = Image.new('RGBA', (cw * len(spec['order']), H), (0, 0, 0, 0))
    for i, name in enumerate(spec['order']):
        strip.paste(Image.fromarray(layers[name]), (i * cw, 0))
    strip.save(os.path.join(rig_dir, cid + '.png'), optimize=True)
    piv = {'body': (28, 44), 'cape': (28, 28)}
    for name, part in spec['parts'].items():
        piv[name] = ((part['piv'][0] + ox) / K - (fw - 56) / 2, (part['piv'][1] + oy) / K)   # pivots are on the 56-wide design grid
    with open(os.path.join(rig_dir, cid + '.json'), 'w') as f:
        json.dump({'layers': spec['order'], 'piv': piv, 'k': K, **({'fw': fw} if fw != 56 else {})}, f)
