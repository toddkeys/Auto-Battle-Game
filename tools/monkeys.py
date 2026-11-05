"""Monkey class (original characters inspired by the old Journey to the West legend): half-human, half-monkey
staff fighters — anime faces and hair with furry monkey ears and long curling tails."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import sparkle
from pixel import Spr, ramp


def monkey_ears(s, fur, inner):
    """round furry monkey ears on the sides of the head (instead of human ears)"""
    with s.grp('head'):
        s.part(fur, [('ell', 15.5, 18.5, 3.6, 4), ('ell', 40.5, 18.5, 3.6, 4)], soft=1.2)
        s.part(inner, [('ell', 15.8, 18.8, 1.8, 2.3), ('ell', 40.2, 18.8, 1.8, 2.3)], soft=.4, line=False)


def tail(s, fur, tip, pts, w=1.5):
    """a long curling monkey tail behind the body, with a fluffy tip"""
    with s.grp('cape'):
        s.part(fur, [('line', pts, w)], soft=.8, gloss=.5)
        x, y = pts[-1]
        s.part(tip, [('ell', x, y, w * 1.5, w * 1.5)], soft=.6)


def wukong():
    # the monkey sage as a young half-monkey warrior: wild golden-orange hair, golden-furred monkey ears,
    # a gold circlet, fierce amber eyes and a confident grin, fur-trimmed crimson-and-gold armour,
    # a red sash, a long golden tail, an iron staff with golden caps held forward like a blade
    s = Spr()
    hair, fur, inner = ramp('#f0902a', 1.3, 1.15), ramp('#e0a040', 1.2), ramp('#f6d6b0', .8)
    armor, gold, sash, iron = ramp('#a8202a', 1.25, 1.1), P['gold'], ramp('#e04a2a', 1.2, 1.1), ramp('#2c2c36', 1.3)
    cream = ramp('#f4e2c0', .8)
    tail(s, fur, cream, [(34, 42), (43, 46), (49, 41), (47, 35), (51, 31)], 1.5)
    back_hair(s, hair, 31, 12)   # wild mane falling down the back
    with s.grp('cape'):
        s.part(hair, [('poly', [(17, 22), (12, 32), (19, 29)]), ('poly', [(39, 22), (44, 32), (37, 29)])], soft=.8)
    with s.grp('cape'):   # sash ends streaming behind
        s.part(sash, [('poly', [(31, 39), (35, 39), (43, 47), (40, 49), (34, 44)])], soft=.8)
    legs(s, ramp('#3a2a2a', 1.2), ramp('#2a1e1a', 1.2))
    with s.grp('legL'):
        s.part(cream, [('rect', 21.5, 45, 27.5, 46.6)], soft=.5, line=False)   # fur leg wraps
    with s.grp('legR'):
        s.part(cream, [('rect', 29.5, 45, 35, 46.6)], soft=.5, line=False)
    torso(s, armor, hem=44)
    with s.grp('body'):
        s.part(gold, [('poly', [(22.5, 30.5), (33.5, 30.5), (33, 38), (28, 40), (23, 38)])], soft=1, gloss=1.5)   # gold chest plate
        s.part(armor, [('cap', 28, 31, 28, 39, .4)], soft=.2, line=False)
        s.part(cream, [('poly', [(20, 27.5), (36, 27.5), (34.5, 31), (28, 32.5), (21.5, 31)])], soft=1.4)   # fur collar
        s.part(gold, [('poly', [(21, 41), (35, 41), (36, 45.5), (28, 46.5), (20, 45.5)])], soft=.8, gloss=1.2)   # tassets
    belt(s, sash, 39.5, gold)
    with s.grp('weapon'):   # iron staff held forward like the swordsmen's blades
        s.part(iron, [('cap', 40, 50, 50, 8, 1.15)], soft=.5, gloss=1.4)
        s.part(gold, [('cap', 39.6, 51.5, 40.7, 47.5, 1.5), ('cap', 49.4, 10.5, 50.4, 6.5, 1.5)], soft=.4, gloss=1.6)
        s.part(ramp('#ffd060', 1.3), [('cap', 42, 41, 48.5, 13, .3)], soft=.2, line=False, flat=True, bias=.3)   # glint
    arm(s, armor, SKIN, (35, 30), (38.5, 36), (42, 41), r=2.8, glove=ramp('#4a2a18'))
    arm(s, armor, SKIN, (21, 30), (18.5, 35), (18, 39.5), r=2.8, glove=ramp('#4a2a18'))
    for cx in (36, 20):   # gold pauldrons with fur edges
        s.part(gold, [('chord', cx, 30.5, 5.4, 4.6, 180, 360)], soft=1, gloss=1.5, cast=1)
        s.part(cream, [('cap', cx - 5, 30.6, cx + 5, 30.6, .8)], soft=.6, line=False)
    head(s)
    monkey_ears(s, fur, inner)
    with s.grp('head'):   # wild spikes growing out of the crown of the head
        s.part(hair, [('poly', [(18.5, 13), (14, 7), (21.5, 8.5), (22, 2.5), (27, 6.5), (31, -1), (32.5, 6), (38, 2.5), (36.5, 9), (42, 9.5), (38, 13)])], soft=1.4, cast=2, shine=7)
    bangs(s, hair, 'swept', shine=9)
    with s.grp('head'):   # the circlet
        s.part(gold, [('cap', 17.5, 14.6, 38.5, 14.6, .7)], soft=.3, gloss=1.5, cast=1)
        s.part(ramp('#ff3a3a', 1.2), [('ell', 28, 14.6, 1.2, 1.2)], soft=.2, gloss=1.5, line=False)
    face(s, '#f0a020', mouth=None, blush=False)
    if not kit_expr():
        for x0, x1 in ((20, 23), (27, 30)):   # fierce brows
            for x in range(x0, x1):
                s.mark(x, 18, (120, 60, 20))
        for x in (24, 25, 26):   # confident grin with a fang
            s.mark(x, 25, (150, 60, 60))
        s.mark(23, 24, (150, 60, 60)); s.mark(25, 26, (255, 255, 240))
    for x, y in ((52, 6), (8, 30), (54, 26)):
        sparkle(s, x, y, (255, 220, 140))
    return s


def stonemonkey():
    # a young half-monkey kid: messy grey-brown hair, round grey monkey ears, a cheeky grin,
    # a leaf-green vest over a tan shirt, a red headband with flying tails, a long tail, a plain wooden staff
    s = Spr()
    hair, fur, inner = ramp('#7a6a62', 1.2), ramp('#8a8a92', 1.15), ramp('#ecd8c8', .8)
    vest, shirt, band = ramp('#4a9a3a', 1.15), ramp('#d8b888', .9), ramp('#d83a2a', 1.15)
    tail(s, fur, inner, [(34, 42), (42, 46), (47, 42), (45, 37)], 1.3)
    back_hair(s, hair, 25, 11)
    legs(s, ramp('#6a5440'), ramp('#3a2a20'))
    torso(s, shirt, hem=43)
    with s.grp('body'):
        s.part(vest, [('poly', [(20.5, 28), (26, 28), (24.5, 41), (20, 41)]), ('poly', [(30, 28), (35.5, 28), (36, 41), (31.5, 41)])], soft=1.2)   # leaf vest
        for x, y in ((22, 33), (34, 36)):
            s.part(ramp('#6ac04a'), [('ell', x, y, 1, 1.6)], soft=.3, line=False)   # leaf pattern
    belt(s, ramp('#b89a5a'), 40)
    with s.grp('weapon'):   # wooden staff held forward
        s.part(P['wood'], [('cap', 40, 49, 48, 12, .95)], soft=.5, gloss=.7)
        s.part(ramp('#c8a060'), [('cap', 47.4, 15, 48.2, 11.5, 1.2)], soft=.3, gloss=1)
    arm(s, shirt, SKIN, (35, 30), (38.5, 36), (42, 41), r=2.5)
    arm(s, shirt, SKIN, (21, 30), (18.5, 35), (18, 39.5), r=2.5)
    head(s)
    monkey_ears(s, fur, inner)
    with s.grp('head'):   # messy tufts on top
        s.part(hair, [('poly', [(20, 12), (20, 6), (24, 9), (27, 4), (30, 8.5), (34, 5.5), (36, 12)])], soft=1.4, cast=2, shine=7)
    bangs(s, hair, 'swept', shine=8)
    with s.grp('head'):
        s.part(band, [('rect', 17.5, 12.6, 38.5, 14.4)], soft=.4, cast=1)
        s.part(band, [('poly', [(38, 13), (46, 10), (44, 14), (47, 17), (38, 15)])], soft=.4)   # flying headband tails
    face(s, '#8a5a2a', 'open', blush=True)
    return s


def kit_expr():
    import kit
    return kit.EXPR


MONKEYS = dict(wukong=wukong, stonemonkey=stonemonkey)
