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
    # the Aegis Paladin, an anime-hero heavy knight: messy jet-black hair with a single cowlick, sharp
    # sapphire eyes, gunmetal heavy plate edged in silver with glowing azure seams, layered round pauldrons,
    # a long white-and-azure cape, a huge kite tower shield with a glowing crest, a broad runed longsword
    s = Spr()
    plate, silver, glow, cloth = ramp('#4a5468', 1.35), ramp('#d8e0ec', 1.25), ramp('#6ad8ff', 1.3), ramp('#f2f4fa', .8)
    azure, dark, hair = ramp('#2a64c8', 1.2), ramp('#1a1e2a', 1.2), ramp('#2c3a5c', 1.4, 1.15)
    cape(s, cloth, 1.55, 54)
    with s.grp('cape'):   # azure lining and silver trim along the cape hem
        s.part(azure, [('poly', [(36.5, 34), (45, 51), (40, 53), (36, 44)]), ('poly', [(19.5, 34), (11, 51), (16, 53), (20, 44)])], soft=1)
    legs(s, plate, ramp('#2e3444', 1.3))
    with s.grp('body'):   # knee guards
        s.part(silver, [('ell', 24.5, 47.5, 2.2, 1.6), ('ell', 31.5, 47.5, 2.2, 1.6)], soft=.6, gloss=1.4)
    torso(s, plate, hem=45)
    with s.grp('body'):
        s.part(silver, [('poly', [(22, 29.5), (34, 29.5), (33, 37), (28, 39.5), (23, 37)])], soft=1.2, gloss=1.5)   # breastplate
        s.part(plate, [('poly', [(24.5, 31), (31.5, 31), (31, 36), (28, 37.6), (25, 36)])], soft=1, gloss=1.2)
        s.part(glow, [('poly', [(27.2, 31.5), (28.8, 31.5), (28.8, 36.5), (28, 37.2), (27.2, 36.5)]),
                      ('rect', 25.5, 33.2, 30.5, 34.4)], soft=.2, line=False, flat=True, bias=.4)   # glowing crest-cross
        s.part(azure, [('poly', [(22, 41), (34, 41), (35.5, 47.5), (28, 48.5), (20.5, 47.5)])], soft=1)   # tasset cloth
        s.part(silver, [('cap', 21.5, 41.2, 34.5, 41.2, .6)], soft=.3, gloss=1.3)
    belt(s, dark, 39, silver)
    with s.grp('weapon'):   # broad runed longsword, point up
        s.part(silver, [('poly', [(40.2, 39), (44.2, 39), (46.6, 9), (44.6, 4.5), (42.6, 8.5)])], soft=.7, gloss=1.6)
        s.part(glow, [('cap', 42.7, 37, 44.6, 10, .45)], soft=.2, line=False, flat=True, bias=.45)   # glowing fuller
        s.part(dark, [('cap', 36.5, 39.2, 48, 39.8, 1.1)], soft=.5, gloss=1)   # crossguard
        s.part(azure, [('ell', 42.3, 39.5, 1.3, 1.3)], soft=.3, gloss=1.5, line=False)
        s.part(dark, [('cap', 42.2, 40.5, 41.9, 45, .9), ('ell', 41.8, 46, 1.3, 1.3)], soft=.5, gloss=.8)
    arm(s, plate, plate, (35, 30), (39, 36), (42, 42), r=3.1, glove=dark)
    s.part(plate, [('chord', 36.5, 31, 6.6, 6, 180, 360)], soft=1.4, gloss=1.4, cast=1)   # layered pauldrons
    s.part(silver, [('chord', 36.5, 31.6, 6.6, 3, 180, 360)], soft=.6, gloss=1.5, line=False)
    s.part(glow, [('cap', 31, 31.2, 42.8, 31.2, .35)], soft=.2, line=False, flat=True, bias=.4)
    arm(s, plate, plate, (21, 30), (18.5, 35), (17, 39), r=3.1, glove=dark)
    s.part(plate, [('chord', 19.5, 31, 6.6, 6, 180, 360)], soft=1.4, gloss=1.4, cast=1)
    s.part(silver, [('chord', 19.5, 31.6, 6.6, 3, 180, 360)], soft=.6, gloss=1.5, line=False)
    # huge kite tower shield: dark steel, silver rim, azure field, glowing crest
    s.part(silver, [('poly', [(3, 26), (24, 26), (24, 41), (13.5, 55), (3, 41)])], soft=1.6, gloss=1.4)
    s.part(plate, [('poly', [(5, 28), (22, 28), (22, 40.5), (13.5, 52.5), (5, 40.5)])], soft=1.6, gloss=1.1)
    s.part(azure, [('poly', [(7.5, 30), (19.5, 30), (19.5, 39.5), (13.5, 48.5), (7.5, 39.5)])], soft=1.2, gloss=.8)
    s.part(silver, [('rect', 12.6, 30, 14.4, 48), ('rect', 7.5, 35, 19.5, 36.8)], soft=.4, gloss=1.5)
    s.part(glow, [('poly', [(13.5, 31), (16.5, 35.9), (13.5, 41), (10.5, 35.9)])], soft=.3, gloss=1.6, line=False)   # glowing crest gem
    head(s)
    with s.grp('head'):   # back hair, messy and spiky
        s.part(hair, [('poly', [(17, 20), (13.5, 26), (18.5, 24)]), ('poly', [(39, 20), (42.5, 26), (37.5, 24)])], soft=1)
    bangs(s, hair, 'spiky', shine=8)
    with s.grp('head'):
        s.part(hair, [('poly', [(26, 6), (25, -1), (30.5, 3), (28.5, 6.5)])], soft=.6)   # the cowlick
    face(s, '#2a7ae8', mouth=None, blush=False)
    if not kit_expr():
        for x in (20, 21, 22, 27, 28, 29):   # sharper eyes: heavier upper lash line
            s.mark(x, 18, (34, 24, 30))
        s.mark(24, 25, (150, 80, 80)); s.mark(25, 25, (170, 90, 90)); s.mark(26, 24, (150, 80, 80))   # confident smirk
    for x, y in ((3, 22), (50, 6), (54, 30)):
        sparkle(s, x, y, (160, 230, 255))
    return s


def kit_expr():
    import kit
    return kit.EXPR


CRUSADERS = dict(bulwark=bulwark, templar=templar, aegispaladin=aegispaladin)
