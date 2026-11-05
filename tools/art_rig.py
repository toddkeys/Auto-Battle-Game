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
    # Wukong (2g): staff held upright in the front fist; it lifts and chops like the Paladin's sword
    'stonemonkey': {
        'fill': 9, 'fillTop': 80,   # the staff crosses his body and tail below the shoulders
        'order': ['body', 'head', 'armL', 'weapon', 'armR'],
        'parts': {
            'armR': {'poly': [(28, 84), (50, 80), (54, 96), (46, 108), (28, 108)], 'piv': (48, 84)},
            'weapon': {'poly': [(8, 0), (30, 0), (42, 90), (42, 162), (25, 162), (17, 90)], 'piv': (36, 98)},
            'head': {'poly': [(10, 20), (30, 0), (95, 5), (102, 40), (96, 70), (80, 82), (60, 85), (45, 78), (38, 60), (15, 40)], 'piv': (62, 82)},
            'armL': {'poly': [(76, 82), (106, 84), (106, 112), (84, 115), (76, 98)], 'piv': (78, 86)},
        },
    },
    # Mythic Wukong (4g): staff held level in both hands, front end forward; it sweeps like the Valkyrie's halberd
    'wukong': {
        'order': ['body', 'head', 'weapon', 'armL', 'armR'],
        'parts': {
            'head': {'poly': [(10, 40), (20, 5), (60, 0), (110, 20), (112, 60), (104, 80), (70, 92), (45, 90), (30, 82), (5, 70)], 'piv': (68, 92)},
            'armR': {'poly': [(12, 90), (50, 86), (58, 100), (48, 116), (10, 116)], 'piv': (52, 98)},
            'armL': {'poly': [(100, 78), (126, 78), (128, 100), (112, 104), (100, 96)], 'piv': (98, 86)},
            'weapon': {'polys': [[(-1, 86), (13, 86), (13, 114), (-1, 114)], [(126, 84), (171, 84), (171, 110), (126, 110)]], 'piv': (25, 103)},
        },
    },
    # Worldbreaker: bare-fisted guard stance; the front fist jabs, the back fist guards
    'grandmaster': {
        'order': ['body', 'head', 'armL', 'armR'],
        'parts': {
            'armR': {'poly': [(4, 56), (34, 54), (42, 66), (42, 92), (20, 95), (4, 88)], 'piv': (36, 60)},
            'armL': {'poly': [(64, 56), (92, 56), (98, 70), (98, 95), (78, 95), (66, 80)], 'piv': (66, 60)},
            'head': {'poly': [(20, 10), (40, 0), (75, 2), (82, 30), (80, 48), (65, 56), (40, 56), (25, 48), (18, 30)], 'piv': (50, 55)},
        },
    },
    # Stormweaver: a short storm staff raised in the front hand; it lifts and swings forward to cast
    'voidsage': {
        'order': ['body', 'head', 'armL', 'armR', 'weapon'],
        'parts': {
            'weapon': {'poly': [(0, 18), (34, 18), (36, 50), (30, 58), (22, 62), (0, 62)], 'piv': (32, 63)},
            'armR': {'poly': [(22, 56), (42, 55), (62, 57), (64, 78), (44, 84), (30, 74), (22, 66)], 'piv': (60, 62)},
            'armL': {'poly': [(78, 60), (96, 60), (108, 80), (106, 96), (88, 96), (78, 80)], 'piv': (82, 62)},
            'head': {'poly': [(45, 0), (100, 0), (108, 30), (100, 55), (80, 60), (55, 60), (46, 45), (44, 20)], 'piv': (70, 58)},
        },
    },
    # Eclipse Witch: a long eclipse staff held two-handed across the body, orb forward and up; it sweeps like the halberd
    'eclipsewitch': {
        'fill': 7, 'fillTop': 58,   # the staff crosses her robe below the shoulders
        'order': ['body', 'head', 'weapon', 'armL', 'armR'],
        'parts': {
            'armR': {'poly': [(60, 50), (78, 50), (90, 58), (90, 74), (72, 74), (60, 64)], 'piv': (86, 62)},
            'armL': {'poly': [(98, 78), (122, 80), (124, 98), (104, 100), (96, 90)], 'piv': (108, 70)},
            'head': {'poly': [(80, 5), (120, 0), (140, 10), (142, 40), (132, 55), (106, 60), (86, 56), (78, 35)], 'piv': (108, 58)},
            'weapon': {'polys': [[(0, 0), (58, 0), (62, 46), (70, 54), (64, 62), (52, 58), (0, 58)],
                                 [(70, 64.5), (74, 59.5), (184, 142), (192, 152), (184, 160), (176, 152)]], 'piv': (68, 60)},   # just the shaft, ~6px wide
        },
    },
    # Shadowstep: three-quarter stance, the glowing katana held low in the front hand, blade down and forward;
    # it lifts and chops like the Paladin's sword
    'shadowstep': {
        'order': ['body', 'head', 'armL', 'weapon', 'armR'],
        'parts': {
            'armR': {'poly': [(50, 60), (62, 60), (60, 80), (56, 105), (44, 105), (48, 80)], 'piv': (57, 62)},
            'weapon': {'poly': [(48, 87), (58, 92), (52, 107), (50, 116), (14, 167), (-8, 167), (-8, 149), (22, 106), (32, 96)], 'piv': (49, 101)},
            'armL': {'poly': [(78, 64), (94, 64), (96, 96), (84, 98), (78, 84)], 'piv': (82, 66)},
            'head': {'poly': [(48, 0), (88, 0), (92, 20), (90, 46), (80, 56), (56, 56), (50, 46), (48, 20)], 'piv': (68, 54)},
        },
    },
    # Crimson Ravager: an axe hanging in each hand; the front axe lifts and chops like the Paladin's sword, the other swings with its arm
    'chieftain': {
        'nofill': ['weapon'],   # the front axe hangs beside his leg: no body behind it
        'order': ['body', 'head', 'armL', 'weapon', 'armR'],
        'parts': {
            'armR': {'poly': [(28, 66), (46, 66), (44, 90), (40, 112), (26, 112), (26, 90)], 'piv': (38, 68)},
            'weapon': {'poly': [(-2, 94), (30, 94), (36, 108), (30, 146), (-2, 146)], 'piv': (32, 104)},
            'armL': {'poly': [(72, 64), (90, 64), (98, 84), (119, 82), (119, 136), (96, 140), (84, 118), (76, 100)], 'piv': (80, 68)},
            'head': {'poly': [(28, 0), (80, 0), (90, 20), (88, 45), (75, 55), (45, 55), (35, 45), (28, 25)], 'piv': (58, 52)},
        },
    },
}


# Coordinated 2026 skins: polygons measured on the trimmed 162px-high artwork.
# Keep weapon and gripping hand together so they cannot slide apart during attacks.
_SKIN_PARTS = {
 'stonemonkey': {'head': ([(18,0),(102,0),(94,48),(70,60),(39,57),(22,35)],(63,57)),
                 'armR': ([(0,107),(36,83),(39,65),(56,66),(51,87),(112,46),(113,57),(43,100),(0,117)],(49,69)),
                 'armL': ([(77,55),(88,62),(84,82),(65,90),(61,81),(74,71)],(76,60))},
 'wukong': {'head': ([(10,0),(101,0),(108,42),(83,61),(48,61),(20,43)],(65,60)),
            'armR': ([(0,100),(24,88),(33,64),(48,65),(45,88),(113,45),(115,55),(39,101),(0,111)],(43,68)),
            'armL': ([(80,60),(94,67),(90,86),(70,93),(65,83),(79,77)],(82,66))},
 'eclipsewitch': {'head': ([(37,0),(85,0),(99,30),(85,51),(60,51),(44,37)],(70,49)),
                  'armR': ([(0,0),(35,0),(42,27),(24,43),(39,97),(33,105),(16,46),(0,34)],(42,62)),
                  'armL': ([(82,62),(100,74),(102,93),(91,99),(83,82)],(84,65))},
 'voidsage': {'head': ([(36,13),(79,13),(91,34),(79,56),(56,55),(42,42)],(66,54)),
              'armR': ([(0,0),(38,0),(41,38),(27,47),(39,108),(31,115),(18,46),(0,34)],(42,63)),
              'armL': ([(79,63),(96,75),(103,92),(94,97),(81,85)],(79,67))},
 'chieftain': {'head': ([(43,0),(98,0),(103,30),(88,47),(64,48),(49,32)],(75,46)),
               'armR': ([(0,31),(32,33),(47,71),(61,66),(63,79),(37,93),(24,81),(13,69),(0,65)],(55,56)),
               'armL': ([(106,31),(149,32),(150,66),(134,80),(120,92),(104,80),(98,61),(112,67),(120,72)],(100,54))},
 'grandmaster': {'head': ([(38,0),(83,0),(87,31),(75,46),(54,46),(40,31)],(65,44)),
                 'armR': ([(22,41),(38,35),(52,49),(47,68),(33,75),(20,64)],(47,50)),
                 'armL': ([(79,44),(93,41),(104,55),(101,71),(86,69),(79,57)],(80,49))},
 'shadowstep': {'head': ([(5,0),(66,0),(75,27),(57,48),(29,49),(10,34)],(42,47)),
                'armR': ([(12,61),(32,61),(37,88),(19,102),(103,149),(97,153),(7,106),(5,92)],(27,64)),
                'armL': ([(66,54),(80,60),(90,81),(81,88),(67,74)],(67,57))},
}
for _cid, _parts in _SKIN_PARTS.items():
    ART_RIGS[_cid] = {'order':['body','head','armL','armR'], 'nofill':['armR','armL'],
                     'parts':{name:{'poly':poly,'piv':piv} for name,(poly,piv) in _parts.items()}}


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
        for poly in part.get('polys', [part.get('poly')]):   # a piece can be several shapes (a staff that passes behind the body)
            ImageDraw.Draw(m).polygon([(x + ox, y + oy) for x, y in poly], fill=255)
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
    wide = dist <= spec.get('fill', 3)   # 'fill': how wide a weapon lying over the body can be
    if 'fillTop' in spec:   # ...but only from this picture row down (above it the weapon is out in the open)
        rows = np.arange(H)[:, None] >= spec['fillTop'] + oy
        wide = (dist <= 3) | (wide & rows)
    fill = taken & (wide | ~(blade if blade is not None else taken))
    if 'nofill' in spec:   # pieces that hang beside the body (a weapon out to the side) leave nothing behind
        for name in spec['nofill']:
            m = Image.new('L', (cw, H), 0)
            for poly in spec['parts'][name].get('polys', [spec['parts'][name].get('poly')]):
                ImageDraw.Draw(m).polygon([(x + ox, y + oy) for x, y in poly], fill=255)
            fill &= ~(np.asarray(m) > 0) | (dist <= 1)
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
