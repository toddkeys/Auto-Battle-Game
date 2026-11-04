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
    # the Aegis Paladin, from the user's character sheet: long wavy purple hair fading to pink, amber eyes and a soft
    # smile, riveted gold pauldrons and a round gold breastplate with a cross over a blue bodice, a golden skirt panel
    # inside brown coat panels with white lace, a dark indigo cape with ragged pink ends, silver plate over blue
    # leggings, a long sword with a red-gem guard and a dark steel kite shield with gold swirls and a red gem
    s = Spr()
    hair, tips = ramp('#6a4ab8', 1.25), ramp('#c868b8', 1.1)
    blue, coat, skirt, lace = ramp('#4a6ac8', 1.15), ramp('#7a5a34', 1.2), ramp('#e8c060', 1.15, 1.1), ramp('#f6f2ea', .6)
    gold, steel, ruby = ramp('#e8b840', 1.3, 1.15), ramp('#d4dae6', 1.35), ramp('#e8303a', 1.2, 1.2)
    back_hair(s, hair, 48, 15.5)   # long, full hair
    with s.grp('cape'):   # dark indigo cape fading to ragged pink ends
        s.part(ramp('#3a2a6a', 1.2), [('poly', [(17, 27), (39, 27), (50, 47), (45, 45), (47, 52), (40, 49), (16, 49), (9, 52), (11, 45), (6, 47)])], soft=2.4)
        s.part(ramp('#c060a8', 1.1), [('poly', [(8, 44), (13, 45), (11, 51), (6, 47)]), ('poly', [(48, 44), (43, 45), (47, 52), (50, 47)])], soft=1, line=False)
    with s.grp('head'):   # wavy hair spilling over both shoulders, pink at the ends
        for side in (-1, 1):
            x = 28 + side * 13
            s.part(hair, [('poly', [(x - side * 3, 14), (x + side * 5, 22), (x + side * 3, 30), (x + side * 8, 38), (x + side * 4, 47), (x - side * 2, 42), (x, 33), (x - side * 3, 25)])], soft=1.6)
            s.part(tips, [('poly', [(x + side * 4, 35), (x + side * 8, 38), (x + side * 4, 47), (x - side * 2, 42), (x - side * .5, 37)])], soft=1.2, line=False)
    legs(s, ramp('#3a4a9a', 1.15), steel)   # blue leggings, silver boots
    for g, x in (('legL', 24.7), ('legR', 31.7)):
        with s.grp(g):
            s.part(steel, [('ell', x, 44.5, 2.6, 2)], soft=.6, gloss=1.4)   # knee plates
    torso(s, blue, hem=40)
    with s.grp('body'):
        s.part(coat, [('poly', [(20, 38), (36, 38), (40.5, 51), (15.5, 51)])], soft=1.2, gloss=.3)   # brown coat panels
        for side in (-1, 1):   # cross bands on the coat
            x = 28 + side * 8
            s.part(ramp('#c8a870', 1), [('cap', x, 40, x + side * 1.6, 50, .45), ('cap', x - 2, 44, x + 2.6 * side + 2 * (side < 0), 44, .45)], soft=.2, line=False)
        s.part(skirt, [('poly', [(24, 38), (32, 38), (34, 51), (31, 52.5), (28, 51), (25, 52.5), (22, 51)])], soft=1, gloss=.8)   # golden centre panel
        for k in range(9):   # white lace hem
            xx = 16 + k * 2.8
            s.part(lace, [('poly', [(xx, 50.6), (xx + 2.8, 50.6), (xx + 1.4, 53)])], soft=.2, line=False)
        s.part(gold, [('ell', 28, 33, 5.8, 5)], soft=1, gloss=1.5, cast=1)   # round gold breastplate
        s.part(ramp('#c88a20', 1.1), [('rect', 27.4, 29.5, 28.6, 36.5), ('rect', 25.5, 31.8, 30.5, 33)], soft=.2, gloss=1, line=False)   # cross
    belt(s, ramp('#8a5a2a', 1.15), 38.5, ruby)
    sword(s, steel, gold, x0=42, y0=43, x1=48, y1=6, w=1.6, guard=4.8)   # long sword
    with s.grp('weapon'):
        s.part(ruby, [('ell', 42, 40.2, 1.1, 1.1)], soft=.2, gloss=1.6, line=False)   # red gem in the guard
    plate = ramp('#aeb6c8', 1.3)
    arm(s, plate, SKIN, (35, 30), (38.5, 36), (42, 41), r=2.6, glove=steel)   # silver plate arms
    arm(s, plate, SKIN, (21, 30), (18, 35), (17, 39.5), r=2.6, glove=steel)
    # tall kite shield: gold rim, dark steel face, gold swirls and a red gem
    s.part(gold, [('poly', [(3, 25), (21, 25), (22, 40), (12.5, 54), (3, 40)])], soft=1.5, gloss=1.4)
    s.part(ramp('#4a4e5a', 1.25), [('poly', [(5, 27), (19.5, 27), (20, 39.5), (12.5, 51.5), (5, 39.5)])], soft=1.4, gloss=1.1)
    s.part(gold, [('line', [(8, 30), (11, 33), (9, 37), (12.5, 40), (16, 37), (14, 33), (17, 30)], .7),
                  ('line', [(12.5, 40), (12.5, 48)], .7)], soft=.3, gloss=1.2, thr=.3)   # gold swirls
    s.part(ruby, [('ell', 12.5, 40, 1.6, 1.6)], soft=.3, gloss=1.6)
    for side in (-1, 1):   # riveted gold pauldrons
        x = 28 + side * 9
        s.part(gold, [('chord', x + side * .5, 30.5, 7.2, 6.2, 180, 360)], soft=1.2, gloss=1.5, cast=1)
        s.part(gold, [('chord', x + side * 1.2, 33.2, 5.8, 3.8, 180, 360)], soft=1, gloss=1.2, cast=1)
        for dx in (-3.5, 0, 3.5):
            s.mark(int(x + dx), 27, (150, 90, 20))
    head(s)
    bangs(s, hair, 'long', shine=10)
    with s.grp('head'):   # soft side locks framing the face
        s.part(hair, [('poly', [(16.5, 16), (14.5, 31), (18.5, 27), (19.5, 19)]), ('poly', [(39.5, 16), (41.5, 31), (37.5, 27), (36.5, 19)])], soft=1)
    face(s, '#d89030', 'smile')   # amber eyes, a soft smile
    sparkle(s, 2, 14, (255, 220, 120)); sparkle(s, 52, 8, (255, 220, 120)); sparkle(s, 6, 6, (255, 200, 140))
    return s


def kit_expr():
    import kit
    return kit.EXPR


CRUSADERS = dict(bulwark=bulwark, templar=templar, aegispaladin=aegispaladin)
