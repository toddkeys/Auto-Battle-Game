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
    # the monkey sage: golden fur, a gold circlet, red-and-gold scale armour with cloud trim,
    # a short red cape, a long iron staff with golden caps, a curling tail
    s = Spr()
    fur, muzzle = ramp('#c8862e', 1.2, 1.1), ramp('#f2d8b0', .8)
    armor, gold, red, iron = ramp('#b82a2a', 1.2, 1.1), P['gold'], ramp('#8a1a1a', 1.2), ramp('#3a3a44', 1.3)
    with s.grp('cape'):
        s.part(fur, [('line', [(36, 40), (44, 44), (48, 38), (45, 33)], 1.4)], soft=.8)   # curling tail
        s.part(red, [('poly', [(20, 28), (36, 28), (41, 46), (35, 44), (28, 47), (21, 44), (15, 46)])], soft=1.8)   # short cape
    legs(s, ramp('#3a2a2a'), ramp('#2a1a1a'))
    torso(s, armor, hem=44)
    with s.grp('body'):
        for y in (31, 34, 37):   # scale rows
            s.part(ramp('#d84a3a', 1.1), [('chord', 24, y, 3, 2, 0, 180), ('chord', 32, y, 3, 2, 0, 180)], soft=.3, line=False)
        s.part(gold, [('poly', [(21, 28), (35, 28), (33.5, 31), (28, 32.5), (22.5, 31)])], soft=.8, gloss=1.2)   # gold collar
        s.part(gold, [('poly', [(20, 41), (36, 41), (37, 45), (33, 43.5), (28, 45.5), (23, 43.5), (19, 45)])], soft=.5, gloss=1)   # cloud-trimmed skirt
    belt(s, gold, 39, ramp('#ff5a4a', 1.2))
    with s.grp('weapon'):   # long iron staff with golden caps, held diagonally across
        s.part(iron, [('cap', 34, 50, 50, 8, 1.1)], soft=.5, gloss=1.2)
        s.part(gold, [('cap', 33.5, 51, 35, 47, 1.4), ('cap', 49, 11, 50.5, 7, 1.4)], soft=.4, gloss=1.4)
    arm(s, fur, fur, (35, 30), (38.5, 36), (41.5, 31), r=2.7, glove=ramp('#5a3a22'))
    arm(s, fur, fur, (21, 30), (18.5, 35), (18, 39.5), r=2.7, glove=ramp('#5a3a22'))
    s.part(gold, [('chord', 36, 30.5, 5, 4, 180, 360), ('chord', 20, 30.5, 5, 4, 180, 360)], soft=1, gloss=1.2, cast=1)   # shoulder guards
    with s.grp('head'):
        monkey_head(s, fur, muzzle, gold, ramp('#ff3a3a', 1.2))
    face(s, '#d8a020', blush=False)
    for x, y in ((52, 6), (8, 30), (52, 40)):
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
