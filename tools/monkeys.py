"""Monkey class (original characters inspired by the old Journey to the West legend): agile staff fighters."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import sparkle
from pixel import Spr, ramp


def monkey_head(s, fur, muzzle, band=None, band_gem=None):
    """furry round head, a pale heart-shaped face, round ears, eyes via kit.face()"""
    s.part(fur, [('ell', 28, 17.5, 10.5, 10), ('ell', 16.5, 19, 3.2, 3.6), ('ell', 39.5, 19, 3.2, 3.6),
                 ('poly', [(19, 11), (21, 6), (24, 9), (27, 4.5), (30, 8.5), (34, 5.5), (36, 11)])], soft=2.4)   # fur tufts on top
    s.part(muzzle, [('ell', 16.5, 19, 1.6, 2), ('ell', 39.5, 19, 1.6, 2)], soft=.5, line=False)   # inner ears
    s.part(muzzle, [('poly', [(19.5, 16.5), (24, 15), (28, 18), (32, 15), (36.5, 16.5), (36, 23), (31.5, 28), (24.5, 28), (20, 23)])], soft=1.6)   # heart-shaped face
    if band:
        s.part(band, [('rect', 17.5, 12, 38.5, 14.2)], soft=.4, gloss=1.2, cast=1)   # circlet
        if band_gem:
            s.part(band_gem, [('ell', 28, 13, 1.4, 1.4)], soft=.3, gloss=1.4, line=False)


def wukong():
    # monkey sage, fierce: wild golden mane, narrow glowing eyes and fangs, a gold circlet,
    # dark crimson lamellar armour with bronze plates and gold trim, a red sash streaming behind,
    # an iron staff raised overhead, standing on a small golden cloud
    s = Spr()
    fur, mane, muzzle = ramp('#c8742a', 1.25, 1.1), ramp('#8a3a1a', 1.2), ramp('#ecc8a0', .8)
    armor, bronze, gold, sash, iron = ramp('#6a1418', 1.3), ramp('#b87a3a', 1.25), P['gold'], ramp('#d83a2a', 1.2, 1.1), ramp('#2a2a32', 1.3)
    cloud = ramp('#ffe8a0', .8)
    with s.grp('cape'):
        s.part(cloud, [('ell', 20, 51, 9, 3), ('ell', 30, 50.5, 11, 3.5), ('ell', 40, 51.5, 7, 2.6)], soft=1.6, gloss=.6)   # golden cloud
        s.part(sash, [('poly', [(32, 37), (36, 36), (47, 40), (52, 36), (50, 43), (44, 44), (37, 41)])], soft=1)   # sash streaming behind
        s.part(fur, [('line', [(35, 42), (44, 47), (50, 42), (47, 37)], 1.3)], soft=.8)   # curling tail
    legs(s, ramp('#3a1a1a', 1.2), ramp('#1e1214', 1.2))
    torso(s, armor, hem=44)
    with s.grp('body'):
        for y in (31, 34, 37, 40):   # lamellar rows
            for x in (22.5, 26.5, 30.5, 34.5):
                s.part(bronze, [('rect', x - 1.6, y, x + 1.6, y + 2.2)], soft=.3, gloss=.8, line=False)
        s.part(gold, [('poly', [(21, 28), (35, 28), (33.5, 31), (28, 33), (22.5, 31)])], soft=.8, gloss=1.3)   # gold collar
        s.part(gold, [('cap', 20, 43.5, 36, 43.5, .7)], soft=.3, gloss=1.2)
    belt(s, sash, 41, gold)
    with s.grp('weapon'):   # iron staff raised overhead, golden caps
        s.part(iron, [('cap', 30, 46, 52, 3, 1.25)], soft=.5, gloss=1.3)
        s.part(gold, [('cap', 29.5, 47, 31.3, 43.5, 1.6), ('cap', 50.8, 5.5, 52.5, 2, 1.6)], soft=.4, gloss=1.5)
        s.part(ramp('#ffd060', 1.3), [('cap', 33, 40, 49, 9, .35)], soft=.2, line=False, flat=True, bias=.3)   # glint along the staff
    arm(s, fur, fur, (35, 30), (40, 26), (43, 22), r=2.8, glove=ramp('#4a2a18'))   # raised arm
    arm(s, fur, fur, (21, 30), (17.5, 35), (17, 40), r=2.8, glove=ramp('#4a2a18'))
    s.part(bronze, [('chord', 36, 30.5, 5.5, 4.4, 180, 360), ('chord', 20, 30.5, 5.5, 4.4, 180, 360)], soft=1, gloss=1.2, cast=1)   # pauldrons
    s.part(gold, [('poly', [(31.5, 27.5), (36, 24), (40.5, 27.5)]), ('poly', [(15.5, 27.5), (20, 24), (24.5, 27.5)])], soft=.4, gloss=1.2)   # pauldron spikes
    with s.grp('head'):
        s.part(mane, [('ell', 28, 18, 13, 11.5), ('poly', [(15, 20), (10, 26), (16, 25)]), ('poly', [(41, 20), (46, 26), (40, 25)]),
                      ('poly', [(17, 11), (15, 3), (21, 8), (24, 1), (28, 6), (32, 1), (35, 8), (41, 3), (39, 11)])], soft=2.2)   # wild mane
        monkey_head(s, fur, muzzle, gold, ramp('#ff3a3a', 1.2))
    face(s, '#ffb020', mouth=None, blush=False)
    for x0, x1 in ((20, 23), (27, 30)):   # fierce: brows slanting down to the nose, narrow glowing eyes
        for x in range(x0, x1):
            s.mark(x, 19, (40, 16, 10))
    s.mark(19, 18, (40, 16, 10)); s.mark(30, 18, (40, 16, 10))
    for x in (20, 21, 22, 27, 28, 29):
        s.mark(x, 22, (236, 200, 160))   # narrow the eyes from below
    for x in (23, 24, 25, 26):
        s.mark(x, 25, (60, 20, 20))   # snarl
    s.mark(23, 26, (255, 255, 240)); s.mark(26, 26, (255, 255, 240))   # fangs
    for x, y in ((52, 12), (8, 30), (10, 46), (54, 28)):
        sparkle(s, x, y, (255, 220, 140))
    return s

def stonemonkey():
    # a young stone-grey monkey: leaf-green vest, rope belt, a red headband with flying tails, a plain wooden staff
    s = Spr()
    fur, muzzle = ramp('#8a8a92', 1.2), ramp('#e8dcc8', .8)
    vest, band = ramp('#4a8a3a', 1.1), ramp('#d83a2a', 1.1)
    with s.grp('cape'):
        s.part(fur, [('line', [(35, 41), (42, 46), (46, 42)], 1.2)], soft=.8)   # tail
    legs(s, ramp('#5a4a3a'), ramp('#3a2a20'))
    torso(s, fur, hem=43)
    with s.grp('body'):
        s.part(vest, [('poly', [(20.5, 28), (26, 28), (24.5, 41), (20, 41)]), ('poly', [(30, 28), (35.5, 28), (36, 41), (31.5, 41)])], soft=1.2)   # leaf vest
        s.part(muzzle, [('ell', 28, 35, 3.6, 4.5)], soft=1, line=False)   # pale belly
    belt(s, ramp('#b89a5a'), 40)
    with s.grp('weapon'):   # wooden staff
        s.part(P['wood'], [('cap', 36, 49, 48, 14, .9)], soft=.5, gloss=.6)
    arm(s, fur, fur, (35, 30), (38.5, 35.5), (41.5, 32), r=2.5)
    arm(s, fur, fur, (21, 30), (18.5, 35), (18, 39), r=2.5)
    with s.grp('head'):
        monkey_head(s, fur, muzzle)
        s.part(band, [('rect', 17.5, 12.5, 38.5, 14.5)], soft=.4, cast=1)
        s.part(band, [('poly', [(38, 13), (46, 10), (44, 14), (47, 17), (38, 15)])], soft=.4)   # flying headband tails
    face(s, '#6a4a2a', blush=False)
    return s


MONKEYS = dict(wukong=wukong, stonemonkey=stonemonkey)
