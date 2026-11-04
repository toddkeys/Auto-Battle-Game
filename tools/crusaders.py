"""Designs for the Crusader class (original characters): shield-bearers who guard the back line."""
import math

from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import sparkle
from pixel import Spr, ramp


def _sun(s, rp, cx, cy, r, rays=8, line=False):
    """a sun emblem: a disc with pointed rays"""
    pts = []
    for i in range(rays * 2):
        a = math.pi * i / rays - math.pi / 2
        rr = r if i % 2 == 0 else r * .58
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    s.part(rp, [('poly', pts)], soft=.4, gloss=1.2, line=line)


def _plume(s, rp, x, y, d=1):
    s.part(rp, [('poly', [(x, y), (x + 4 * d, y - 6), (x + 11 * d, y - 7), (x + 7 * d, y - 3), (x + 13 * d, y - 1), (x + 4 * d, y + 1)])], soft=.8)


def bulwark():
    # the Guardian: ivory-and-steel heavy plate, a full great helm with a glowing visor slit, a towering
    # shield with a golden sun, a flanged mace, a deep blue cape
    s = Spr()
    steel, ivory, gold, blue, dark = ramp('#a8b4c8', 1.35), ramp('#efe8d8', .85), P['gold'], ramp('#2a4a8a', 1.2), ramp('#1e2230', 1.2)
    cape(s, blue, 1.2, 52)
    legs(s, steel, ramp('#5a6478', 1.3))
    torso(s, steel, hem=45)
    with s.grp('body'):
        s.part(ivory, [('poly', [(24, 30), (32, 30), (32.5, 47), (28, 49), (23.5, 47)])], soft=1)   # ivory tabard
        _sun(s, gold, 28, 37, 3.6)
        s.part(gold, [('poly', [(21, 28.5), (35, 28.5), (34, 32), (28, 33.5), (22, 32)])], soft=.8, gloss=1.2)   # gorget
    belt(s, dark, 40, gold)
    with s.grp('weapon'):   # flanged mace
        s.part(P['wood'], [('cap', 41, 46, 45, 26, 1)], soft=.5)
        s.part(steel, [('ell', 45.5, 23.5, 3.4, 3.8)], soft=.8, gloss=1.4)
        for dx, dy in ((-3.6, 0), (3.6, 0), (0, -4), (-2.6, -2.8), (2.6, -2.8)):
            s.part(steel, [('poly', [(45.5 + dx * .6, 23.5 + dy * .6), (45.5 + dx * 1.3, 23.5 + dy * 1.3), (45.5 + dx * .9 + .8, 23.5 + dy * .9)])], soft=.3, gloss=1.3)
    arm(s, steel, steel, (35, 30), (38.5, 36), (41, 40), r=3)
    s.part(steel, [('chord', 36, 31, 5.8, 5, 180, 360)], soft=1.2, gloss=1.2, cast=1)
    s.part(gold, [('chord', 36, 31, 5.8, 5, 200, 340)], soft=.4, gloss=1.2, line=False)
    arm(s, steel, steel, (21, 30), (18.5, 35), (17, 39), r=3)
    # towering shield in front: ivory face, steel rim, golden sun
    s.part(steel, [('poly', [(4.5, 25), (22.5, 25), (22.5, 46), (13.5, 54), (4.5, 46)])], soft=1.4, gloss=1)
    s.part(ivory, [('poly', [(6.5, 27), (20.5, 27), (20.5, 45.5), (13.5, 52), (6.5, 45.5)])], soft=1.4, gloss=.6)
    _sun(s, gold, 13.5, 38, 6.5, 10)
    s.part(ramp('#ffe9a0', 1.2), [('ell', 13.5, 38, 2.4, 2.4)], soft=.5, gloss=1.5, line=False)
    head(s)
    s.part(steel, [('ell', 28, 18, 11, 10.5), ('rect', 17, 17, 39, 28)], soft=2, gloss=1.3, cast=2)   # great helm
    s.part(gold, [('rect', 27, 8, 29, 28)], soft=.4, gloss=1.2)   # centre ridge
    s.part(dark, [('rect', 18.5, 18.5, 37.5, 21.5), ('rect', 26.8, 21.5, 29.2, 26)], soft=.3)   # T-visor
    s.part(ramp('#9fdcff', 1.3), [('rect', 19.5, 19.3, 36.5, 20.6)], soft=.2, line=False, flat=True, bias=.35)   # glowing slit
    _plume(s, blue, 28, 8, 1)
    face(s, '#4a7ad0', mouth=None, blush=False)
    return s


def templar():
    # the Templar: a knight in white and crimson with a sun emblem, an open helm with a crimson plume,
    # a war-spear with a long banner, a round shield
    s = Spr()
    plate, robe, red, gold = ramp('#c8ccd8', 1.35), ramp('#f6f0e2', .8), ramp('#b8202a', 1.2, 1.1), P['gold']
    cape(s, red, 1.3, 52)
    legs(s, plate, ramp('#7a8090', 1.3))
    torso(s, robe, hem=46)
    with s.grp('body'):
        s.part(red, [('poly', [(25, 29), (31, 29), (31.5, 46), (24.5, 46)])], soft=.8)   # crimson band
        _sun(s, gold, 28, 36, 4)
        s.part(plate, [('poly', [(21, 28.5), (35, 28.5), (34, 31.5), (22, 31.5)])], soft=.8, gloss=1.2)
    belt(s, P['darkleather'], 40, gold)
    with s.grp('weapon'):   # war-spear with a long crimson banner
        s.part(P['wood'], [('cap', 43, 52, 45, 5, .95)], soft=.5)
        s.part(P['steel'], [('poly', [(45, -1), (48, 5), (45, 9.5), (42, 5)])], soft=.6, gloss=1.4)
        s.part(gold, [('rect', 43, 9, 47, 10.5)], soft=.3, gloss=1.2)
        s.part(red, [('poly', [(45.5, 10.5), (55, 12), (52, 15), (55, 19), (45.5, 18)])], soft=.6)
        _sun(s, gold, 49.5, 14.5, 2)
    arm(s, plate, plate, (35, 30), (39, 36), (43.5, 40), r=2.9)
    s.part(gold, [('chord', 36, 31, 5.4, 4.6, 180, 360)], soft=1.2, gloss=1.2, cast=1)
    arm(s, plate, plate, (21, 30), (18.5, 35), (18, 39), r=2.9)
    s.part(plate, [('ell', 14.5, 38, 6.4, 7.2)], soft=1.5, gloss=1)   # round shield
    s.part(red, [('ell', 14.5, 38, 4.6, 5.4)], soft=1.2)
    _sun(s, gold, 14.5, 38, 3.4)
    head(s)
    bangs(s, ramp('#e8c870', 1.1), 'swept', shine=10)
    s.part(plate, [('chord', 28, 16, 12, 10, 180, 360), ('rect', 16, 13, 19.5, 25), ('rect', 36.5, 13, 40, 25)], soft=2, gloss=1.3, cast=2)   # open helm
    s.part(gold, [('rect', 16, 13.5, 40, 15)], soft=.4, gloss=1.2, cast=1)
    _plume(s, red, 29, 7, 1)
    face(s, '#3a8a50')
    return s


def aegispaladin():
    # the Aegis Paladin, powered up: tall flame-like golden hair standing on end, fierce teal eyes,
    # gold battle armour with broad shoulder flaps over a dark blue bodysuit, a crackling golden aura,
    # a raised gauntlet charging a ball of holy light, a gold-rimmed round shield
    s = Spr()
    gold, deep, suit, aura, light = ramp('#f0b830', 1.35, 1.1), ramp('#b87a18', 1.3), ramp('#1e2a6a', 1.25), ramp('#fff4b0', .5), ramp('#fff6c0', .8)
    hair = ramp('#ffc820', 1.45, 1.25)
    with s.grp('cape'):   # golden power aura, flame-shaped
        s.part(aura, [('poly', [(28, -2), (34, 6), (41, 2), (42, 12), (50, 12), (46, 24), (52, 32), (45, 38), (48, 50), (38, 46), (28, 54),
                                (18, 46), (8, 50), (11, 38), (4, 32), (10, 24), (6, 12), (14, 12), (15, 2), (22, 6)])],
               sub=[('ell', 28, 28, 17.5, 25)], soft=.6, gloss=.4, line=False)
    legs(s, suit, ramp('#f2f2f2', .8))
    with s.grp('legL'):
        s.part(gold, [('rect', 21.5, 46, 27.5, 48)], soft=.3, gloss=1.2, line=False)
    with s.grp('legR'):
        s.part(gold, [('rect', 29.5, 46, 35, 48)], soft=.3, gloss=1.2, line=False)
    torso(s, suit, hem=44)
    with s.grp('body'):   # gold battle armour
        s.part(gold, [('poly', [(21, 29), (35, 29), (35, 40), (28, 41.5), (21, 40)])], soft=1.4, gloss=1.6)
        s.part(deep, [('cap', 23, 33.5, 33, 33.5, .4), ('cap', 28, 30, 28, 40.5, .35)], soft=.2, line=False)   # chest plate lines
        s.part(gold, [('poly', [(21, 40), (35, 40), (36.5, 46), (31, 45), (28, 47), (25, 45), (19.5, 46)])], soft=1, gloss=1.3)   # hip flaps
        s.part(light, [('ell', 28, 34, 1.6, 1.6)], soft=.2, gloss=1.6, line=False)
    belt(s, suit, 39.5, gold)
    with s.grp('weapon'):   # holy light charging in the raised fist
        s.part(aura, [('ell', 45, 22, 4.4, 4.4)], soft=.6, gloss=1.2, line=False)
        s.part(light, [('ell', 45, 22, 2.6, 2.6)], soft=.3, gloss=1.8, line=False)
    arm(s, suit, suit, (35, 30), (40, 29), (44, 25.5), r=2.9, glove=gold)   # fist raised
    arm(s, suit, suit, (21, 30), (18.5, 35), (17.5, 39.5), r=2.9, glove=gold)
    for cx in (36.5, 19.5):   # broad shoulder flaps
        s.part(gold, [('poly', [(cx - 6.5, 29.5), (cx - 4, 26), (cx + 4, 26), (cx + 6.5, 29.5), (cx + 5, 33), (cx - 5, 33)])], soft=1, gloss=1.5, cast=1)
    s.part(gold, [('ell', 12.5, 38, 6.5, 6.8)], soft=1.5, gloss=1.5)   # round shield
    s.part(suit, [('ell', 12.5, 38, 4.6, 4.8)], soft=1, gloss=1)
    s.part(light, [('poly', [(12.5, 34), (14, 38), (12.5, 42), (11, 38)])], soft=.3, gloss=1.6, line=False)
    head(s)
    with s.grp('head'):   # golden hair standing on end
        s.part(hair, [('chord', 28, 16.5, 12, 11.5, 175, 365),
                      ('poly', [(16, 15), (9, 7), (17, 9), (15, 0), (22, 6), (23, -4), (28, 3), (33, -4), (34, 6), (41, 0), (39, 9), (47, 7), (40, 15)]),
                      ('poly', [(16.5, 16), (18, 22), (20, 17.5), (23, 20), (25, 16.5), (27, 21), (29, 16.5), (31, 19), (33, 16.5), (36, 20.5), (39.5, 16)])],
               soft=1.6, cast=2, shine=6)
    face(s, '#18c0b0', mouth=None, blush=False)
    if not kit_expr():
        for x0, x1 in ((20, 23), (27, 30)):   # fierce brows
            for x in range(x0, x1):
                s.mark(x, 18, (150, 100, 20))
        s.mark(19, 17, (150, 100, 20)); s.mark(30, 17, (150, 100, 20))
        for x in (24, 25, 26):
            s.mark(x, 25, (150, 70, 70))
    for x, y in ((3, 18), (53, 40), (50, 4), (6, 48)):
        sparkle(s, x, y, (255, 240, 150))
    return s


def kit_expr():
    import kit
    return kit.EXPR


CRUSADERS = dict(bulwark=bulwark, templar=templar, aegispaladin=aegispaladin)
