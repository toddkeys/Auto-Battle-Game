"""Designs for the Crusader class (original characters): shield-bearers who guard the back line."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import sparkle
from pixel import Spr, ramp


def _cross(s, rp, cx, cy, h=6, w=4.4, t=1.4):
    s.part(rp, [('rect', cx - t / 2, cy - h / 2, cx + t / 2, cy + h / 2), ('rect', cx - w / 2, cy - h / 2 + 1.4, cx + w / 2, cy - h / 2 + 1.4 + t)],
           soft=.4, gloss=.8, line=False)


def bulwark():
    s = Spr()
    steel, tabard, gold = ramp('#a8b4c8', 1.3), ramp('#e8e2d0', .8), P['gold']
    legs(s, ramp('#6a7488', 1.2), ramp('#4a5468', 1.2))
    torso(s, steel, hem=44)
    s.part(tabard, [('poly', [(24, 29), (32, 29), (32.5, 46), (28, 48), (23.5, 46)])], soft=1)
    _cross(s, ramp('#c03a3a'), 28, 37, 8, 6)
    belt(s, P['darkleather'], 39, gold)
    sword(s, P['steel'], P['leather'], x0=41, y0=42, x1=46, y1=24)
    arm(s, steel, steel, (35, 30), (38.5, 36), (41, 40), r=2.8)
    s.part(steel, [('chord', 36, 31, 5, 4.4, 180, 360)], soft=1.2, gloss=1, cast=1)
    arm(s, steel, steel, (21, 30), (18.5, 35), (17, 39), r=2.8)
    # tower shield, white and gold
    s.part(ramp('#f2eee2', .8), [('poly', [(6, 27), (21, 27), (21, 46), (13.5, 53), (6, 46)])], soft=1.5, gloss=.6)
    s.part(gold, [('poly', [(6, 27), (21, 27), (21, 29), (6, 29)]), ('poly', [(13, 29), (14, 29), (14, 50), (13, 50)])], soft=.4, flat=True)
    _cross(s, ramp('#c03a3a'), 13.5, 38, 12, 9, 2.2)
    head(s)
    bangs(s, ramp('#6a4a30'), 'neat', shine=10)
    s.part(steel, [('chord', 28, 16.5, 12, 10.5, 180, 360), ('rect', 16, 14, 19, 24), ('rect', 37, 14, 40, 24)], soft=2, gloss=1, cast=2)
    s.part(gold, [('rect', 16, 14, 40, 15.6)], soft=.5, gloss=.8, cast=1)
    face(s, '#4a7ad0')
    return s


def templar():
    s = Spr()
    plate, robe, red, gold = ramp('#c8ccd8', 1.3), ramp('#f4efe2', .8), ramp('#b82a30'), P['gold']
    cape(s, red, 1.1, 52)
    legs(s, plate, ramp('#8a90a0', 1.3))
    torso(s, robe, hem=46)
    _cross(s, red, 28, 36, 12, 8, 2.2)
    belt(s, P['darkleather'], 40, gold)
    # spear with a pennant
    with s.grp('weapon'):
        s.part(P['wood'], [('cap', 43, 52, 45, 6, .9)], soft=.5)
        s.part(P['steel'], [('poly', [(45, 0), (47.5, 6), (45, 9), (42.5, 6)])], soft=.6, gloss=1.2)
        s.part(red, [('poly', [(45.5, 10), (53, 12), (45.5, 15)])], soft=.6)
    arm(s, plate, plate, (35, 30), (39, 36), (43.5, 40), r=2.8)
    s.part(gold, [('chord', 36, 31, 5.2, 4.5, 180, 360)], soft=1.2, gloss=1, cast=1)
    arm(s, plate, plate, (21, 30), (18.5, 35), (18, 39), r=2.8)
    s.part(ramp('#d8dce8', 1.2), [('ell', 15, 38, 5.5, 6.5)], soft=1.5, gloss=.8)   # round shield
    _cross(s, gold, 15, 38, 8, 6, 1.8)
    head(s)
    bangs(s, ramp('#e8d8a0', 1.1), 'swept', shine=10)
    s.part(gold, [('rect', 18, 11.5, 38, 13)], soft=.5, gloss=1)
    face(s, '#3a8a50')
    return s


def aegispaladin():
    s = Spr()
    plate, gold, sky = ramp('#e8d8a8', 1.2, 1.1), P['gold'], ramp('#6ab0f0', 1.1)
    cape(s, ramp('#2a4a8a', 1.2), 1.3, 52)
    legs(s, plate, ramp('#b09060', 1.3))
    torso(s, plate, hem=45)
    s.part(sky, [('poly', [(24, 32), (32, 32), (32.5, 46), (28, 48), (23.5, 46)])], soft=1)
    s.part(gold, [('poly', [(21, 29), (35, 29), (34, 33), (28, 35), (22, 33)])], soft=1, gloss=.9)
    belt(s, gold, 40, sky)
    with s.grp('weapon'):   # radiant blade
        s.part(ramp('#fff4d0', 1.1), [('poly', [(40, 39), (44, 39), (49, 10), (47.5, 6), (46, 10)])], soft=.7, gloss=1.3)
        s.part(gold, [('poly', [(37, 39), (47, 39.6), (47, 41.6), (37, 41)]), ('cap', 42, 41, 41.6, 47, 1)], soft=.6, gloss=.8)
    arm(s, plate, plate, (35, 30), (39, 36), (42, 41), r=3)
    s.part(gold, [('chord', 36, 31, 5.6, 4.8, 180, 360)], soft=1.2, gloss=1, cast=1)
    arm(s, plate, plate, (21, 30), (18.5, 35), (17, 39), r=3)
    # great round sun-shield
    s.part(gold, [('ell', 13.5, 37, 8.5, 9)], soft=2, gloss=1)
    s.part(ramp('#fff4d0', 1.0), [('ell', 13.5, 37, 5.6, 6)], soft=1.5, gloss=1.2)
    s.part(sky, [('ell', 13.5, 37, 2.6, 2.8)], soft=.8, gloss=1.2, line=False)
    head(s)
    bangs(s, ramp('#f4e0a0', 1.1), 'swept', shine=10)
    s.part(plate, [('chord', 28, 16.5, 12, 10.5, 180, 360), ('rect', 16, 14, 19, 24), ('rect', 37, 14, 40, 24)], soft=2, gloss=1, cast=2)
    s.part(gold, [('rect', 16, 14, 40, 15.6), ('poly', [(26.5, 4), (29.5, 4), (28, 14)])], soft=.5, gloss=.9, cast=1)
    wing = ramp('#fafaff', .9)
    s.part(wing, [('poly', [(15.5, 14), (7, 5), (9, 11), (4, 10), (9, 16), (16, 18)])], soft=1)
    s.part(wing, [('poly', [(40.5, 14), (49, 5), (47, 11), (52, 10), (47, 16), (40, 18)])], soft=1)
    face(s, '#3a7ad0')
    for x, y in ((4, 30), (24, 44), (51, 22)):
        sparkle(s, x, y, (255, 240, 190))
    return s


CRUSADERS = dict(bulwark=bulwark, templar=templar, aegispaladin=aegispaladin)
