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
    # the Aegis Paladin as a holy-war maiden: long violet hair streaming in the wind, great layered gold pauldrons
    # over a blue tunic, a long split overcoat with cross bands, a pale lavender cape, silver gauntlets and greaves,
    # a long sword held forward and a tall gold-trimmed kite shield
    s = Spr()
    hair, blue, coat, inner = ramp('#5a4aa8', 1.25), ramp('#3a5ab8', 1.2), ramp('#6a4a2e', 1.2), ramp('#d8b878', 1.05)
    gold, steel, lav, dark = ramp('#e8b840', 1.25, 1.15), ramp('#d0d8e6', 1.35), ramp('#cfc2ea', .85), ramp('#2a2030', 1.2)
    back_hair(s, hair, 47, 12.5)   # long hair down the back
    with s.grp('cape'):   # pale cape, and hair streaming out to the side in the wind
        s.part(lav, [('poly', [(18, 27), (38, 27), (49, 51), (44, 48), (40, 53), (16, 53), (11, 49), (7, 51)])], soft=2.4)
        s.part(ramp('#c8b8e8', .9), [('poly', [(38, 30), (47, 49), (43, 47)])], soft=.8, line=False)
        s.part(hair, [('poly', [(37, 15), (46, 20), (53, 30), (49, 29), (52, 37), (45, 30), (40, 26)])], soft=1.4)
    legs(s, steel, steel)   # silver greaves
    with s.grp('legL'):
        s.part(steel, [('poly', [(19, 50), (15.5, 53.5), (21, 53)])], soft=.4, gloss=1)   # pointed sabatons
    with s.grp('legR'):
        s.part(steel, [('poly', [(35, 50), (39.5, 53.5), (34, 53)])], soft=.4, gloss=1)
    torso(s, blue, hem=40)
    with s.grp('body'):
        s.part(inner, [('poly', [(21, 38), (35, 38), (37.5, 52), (18.5, 52)])], soft=1.2)   # tan under-skirt
        for side in (-1, 1):   # long split overcoat panels with cross bands and a lavender saw-tooth hem
            x0 = 28 + side * 1.6
            pts = [(x0, 38), (28 + side * 9.5, 38), (28 + side * 13, 53), (x0 + side * 1.5, 53)]
            s.part(coat, [('poly', pts)], soft=1.2, gloss=.4)
            s.part(ramp('#4a3220', 1.2), [('cap', x0 + side * 3, 39, x0 + side * 4.5, 52, .5), ('cap', x0 + side * 6.5, 39, x0 + side * 8.8, 52, .5)], soft=.2, line=False)
            for k in range(4):
                xx = x0 + side * (1.5 + k * 3)
                s.part(lav, [('poly', [(xx, 51.6), (xx + side * 3, 51.6), (xx + side * 1.5, 53.6)])], soft=.2, line=False)
        s.part(gold, [('poly', [(22, 28), (34, 28), (33, 31.5), (28, 33), (23, 31.5)])], soft=.8, gloss=1.2)   # gold gorget
        s.part(gold, [('rect', 27.3, 32.5, 28.7, 37.5), ('rect', 25.8, 34, 30.2, 35.3)], soft=.2, gloss=1, line=False)   # cross on the chest
    belt(s, ramp('#2a3a7a', 1.2), 38.5, gold)
    with s.grp('body'):
        s.part(ramp('#c03030'), [('rect', 30, 38.3, 33.5, 40.5)], soft=.2, line=False)   # small red-and-white sash
        s.part(ramp('#f4f0e8', .7), [('rect', 31, 38.3, 32.2, 40.5)], soft=.1, line=False)
    sword(s, steel, gold, x0=42, y0=43, x1=48, y1=6, w=1.5, guard=4.8)   # long, slender blade, held forward
    arm(s, blue, SKIN, (35, 30), (38.5, 36), (42, 41), r=2.7, glove=steel)
    arm(s, blue, SKIN, (21, 30), (18, 35), (17, 39.5), r=2.7, glove=steel)
    # tall kite shield: gold rim, dark bronze face, a gold winged cross
    s.part(gold, [('poly', [(3, 25), (21, 25), (22, 40), (12.5, 54), (3, 40)])], soft=1.5, gloss=1.4)
    s.part(ramp('#5a3e22', 1.2), [('poly', [(5, 27), (19.5, 27), (20, 39.5), (12.5, 51.5), (5, 39.5)])], soft=1.4, gloss=.8)
    s.part(gold, [('rect', 11.6, 29, 13.4, 47), ('rect', 7, 33.5, 18, 35.3)], soft=.3, gloss=1.2)   # gold cross
    s.part(ramp('#4a8aff', 1.2, 1.2), [('ell', 12.5, 34.4, 1.7, 1.7)], soft=.3, gloss=1.6)   # blue gem at its heart
    for side in (-1, 1):   # great layered gold pauldrons
        x = 28 + side * 8.5
        s.part(gold, [('chord', x + side * .5, 30.5, 7.6, 6.4, 180, 360)], soft=1.2, gloss=1.5, cast=1)
        s.part(gold, [('chord', x + side * 1.4, 33.4, 6.2, 4, 180, 360)], soft=1, gloss=1.2, cast=1)
        s.part(ramp('#a07020', 1.1), [('cap', x - 4.5, 30.6, x + 4.5, 30.6, .35)], soft=.1, line=False)
    head(s)
    bangs(s, hair, 'long', shine=10)
    with s.grp('head'):   # side locks framing the face
        s.part(hair, [('poly', [(16.5, 17), (14.5, 33), (18.5, 29), (19.5, 20)]), ('poly', [(39.5, 17), (41.5, 33), (37.5, 29), (36.5, 20)])], soft=1)
        s.part(gold, [('rect', 18, 11.6, 23, 13), ('ell', 20.5, 12.3, 1.2, 1.2)], soft=.3, gloss=1.2)   # small gold hair clasp
    face(s, '#8a6ad8', mouth=None, blush=False)
    if not kit_expr():
        s.mark(24, 25, (180, 110, 110)); s.mark(25, 25, (180, 110, 110))   # calm, serious mouth
    sparkle(s, 2, 20, (255, 236, 160)); sparkle(s, 53, 10, (230, 220, 255))
    return s


def kit_expr():
    import kit
    return kit.EXPR


CRUSADERS = dict(bulwark=bulwark, templar=templar, aegispaladin=aegispaladin)
