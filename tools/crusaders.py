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
    # the Aegis Paladin: radiant white-and-gold plate, a winged helm, a glowing holy warhammer,
    # a great sun shield, a deep blue cape, a halo of light behind
    s = Spr()
    plate, gold, sky, light = ramp('#f2ecdc', 1.25), P['gold'], ramp('#3a6ab8', 1.2), ramp('#fff4c8', 1.0)
    cape(s, ramp('#1e3a7a', 1.25), 1.5, 53)
    with s.grp('cape'):   # halo of light behind the head
        s.part(light, [('ell', 28, 15, 15, 13)], sub=[('ell', 28, 15, 12.5, 10.8)], soft=.6, gloss=1, line=False)
    legs(s, plate, ramp('#c8b080', 1.3))
    torso(s, plate, hem=46)
    with s.grp('body'):
        s.part(sky, [('poly', [(24, 32), (32, 32), (32.5, 47), (28, 49), (23.5, 47)])], soft=1)
        s.part(gold, [('poly', [(20.5, 28.5), (35.5, 28.5), (34.5, 33), (28, 35.5), (21.5, 33)])], soft=1, gloss=1.3)
        _sun(s, ramp('#fff3a0', 1.2), 28, 40, 3.2)
    belt(s, gold, 40, sky)
    with s.grp('weapon'):   # holy warhammer
        s.part(P['wood'], [('cap', 41, 46, 46, 17, 1.1)], soft=.5)
        s.part(gold, [('rect', 41, 10, 52, 17)], soft=.8, gloss=1.4)
        s.part(light, [('rect', 42.5, 11.5, 50.5, 15.5)], soft=.4, gloss=1.6, line=False)
        _sun(s, ramp('#fff8d8', 1.2), 46.5, 13.5, 2.2)
    arm(s, plate, plate, (35, 30), (39, 36), (42, 41), r=3.1)
    s.part(gold, [('chord', 36, 31, 6, 5.2, 180, 360)], soft=1.2, gloss=1.3, cast=1)
    arm(s, plate, plate, (21, 30), (18.5, 35), (17, 39), r=3.1)
    s.part(gold, [('ell', 13, 37, 9, 9.5)], soft=2, gloss=1.3)   # great sun shield
    s.part(plate, [('ell', 13, 37, 6.2, 6.6)], soft=1.5, gloss=1.2)
    _sun(s, gold, 13, 37, 5.2, 12)
    s.part(sky, [('ell', 13, 37, 2, 2.2)], soft=.6, gloss=1.4, line=False)
    head(s)
    bangs(s, ramp('#f4e0a0', 1.1), 'swept', shine=10)
    s.part(plate, [('chord', 28, 16.5, 12, 10.5, 180, 360), ('rect', 16, 14, 19, 24), ('rect', 37, 14, 40, 24)], soft=2, gloss=1.3, cast=2)
    s.part(gold, [('rect', 16, 14, 40, 15.6), ('poly', [(26.5, 3), (29.5, 3), (28, 14)])], soft=.5, gloss=1.2, cast=1)
    wing = ramp('#fafaff', .9)
    s.part(wing, [('poly', [(15.5, 14), (6, 3), (8, 10), (2, 8), (7, 14), (3, 16), (16, 18)])], soft=1)
    s.part(wing, [('poly', [(40.5, 14), (50, 3), (48, 10), (54, 8), (49, 14), (53, 16), (40, 18)])], soft=1)
    face(s, '#3a7ad0')
    for x, y in ((3, 30), (24, 46), (53, 24), (52, 4)):
        sparkle(s, x, y, (255, 240, 190))
    return s


CRUSADERS = dict(bulwark=bulwark, templar=templar, aegispaladin=aegispaladin)
