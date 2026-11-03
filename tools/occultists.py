"""Designs for the Occultist class (original characters): curse-casters who weaken the enemy."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import hem_trim, sparkle, wizard_hat
from pixel import Spr, ramp


def hexer():
    s = Spr()
    robe, sick, bone = ramp('#4a5a2a', 1.2), ramp('#9ac040', 1.1), ramp('#ece4d0', .9)
    cape(s, ramp('#2a3418', 1.2), 1.0, 51)
    legs(s, ramp('#3a3a2a'), P['darkleather'], robe=True)
    staff(s, ramp('#5a4030', 1.2), 41, 52, 43, 16, .9)
    s.part(bone, [('ell', 43, 13.5, 3.2, 3), ('rect', 41.5, 15, 44.5, 17.5)], soft=1, gloss=.4)   # skull on the staff
    torso(s, robe, 'robe', hem=49)
    hem_trim(s, sick, 47)
    s.part(sick, [('poly', [(26.5, 29), (29.5, 29), (29.5, 46), (26.5, 46)])], soft=.6, flat=True, bias=.1)
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40), r=3.2)
    arm(s, robe, SKIN, (21, 30), (17.5, 35), (15, 38), r=3.2)
    orb(s, sick, 13.5, 34, 2.2)
    head(s)
    bangs(s, ramp('#3a2a3a', 1.2), 'neat', shine=10)
    s.part(robe, [('chord', 28, 17, 13, 12.5, 180, 360), ('poly', [(15, 17), (19, 17), (19.5, 29), (14, 30)]),
                  ('poly', [(37, 17), (41, 17), (42, 30), (36.5, 29)]), ('poly', [(24, 6), (32, 6), (36, 0.5), (31, 5)])],
           sub=[('ell', 28, 19.5, 9.5, 8.5)], soft=2, cast=2)   # pointed hood
    face(s, '#9ac040', 'smile')
    for x, y in ((9, 28), (8, 40), (49, 24)):
        sparkle(s, x, y, (180, 255, 120))
    return s


def bogwitch():
    s = Spr()
    robe, moss, bog = ramp('#3a5a4a', 1.2), ramp('#6a9a30', 1.1), ramp('#8ac040', 1.2, 1.1)
    back_hair(s, ramp('#2a6a5a', 1.1), 38, 12)
    legs(s, robe, ramp('#2a3a30'), robe=True)
    staff(s, ramp('#4a3a28', 1.3), 42, 52, 44, 12, 1.1)
    s.part(moss, [('ell', 44, 10.5, 3.5, 2.5), ('poly', [(42, 11), (40, 15), (43, 13)])], soft=1)   # mossy staff head
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, moss, 47.8)
    s.part(ramp('#2a3a30', 1.2), [('poly', [(25, 30), (31, 30), (31.5, 48), (24.5, 48)])], soft=.8)
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40), r=3.4)
    arm(s, robe, SKIN, (21, 30), (17.5, 35), (15, 38), r=3.4)
    with s.grp('armL'):   # a bubbling flask
        s.part(ramp('#c8e8d8', .9), [('ell', 13, 34, 3, 3.2), ('rect', 12, 29.5, 14, 31.5)], soft=1, gloss=1)
        s.part(bog, [('ell', 13, 35, 2.2, 1.8)], soft=.6, flat=True, bias=.15, line=False)
    head(s)
    bangs(s, ramp('#2a6a5a', 1.1), 'long', shine=10)
    wizard_hat(s, ramp('#2a3a2a', 1.3), band=moss, tip=(42, 0), brim=15)
    face(s, '#b8d040', 'smile')
    for x, y, a in ((12, 25, 220), (15, 21, 160), (10, 18, 120)):   # bubbles rising from the flask
        s.glow(x, y, (180, 240, 120), a)
    return s


def doomherald():
    s = Spr()
    plate, red, gold = ramp('#3a3440', 1.3), ramp('#9a1a2a'), P['gold']
    cape(s, red, 1.3, 52)
    legs(s, plate, ramp('#22202a', 1.2))
    torso(s, plate, hem=45)
    s.part(red, [('poly', [(24, 32), (32, 32), (32.5, 47), (28, 49), (23.5, 47)])], soft=1)
    s.part(gold, [('poly', [(21, 29), (35, 29), (34, 33), (28, 35), (22, 33)])], soft=1, gloss=.8)
    belt(s, P['darkleather'], 40, gold)
    # bell-headed scepter
    with s.grp('armR'):
        s.part(gold, [('cap', 43, 50, 44.5, 14, .9)], soft=.6, gloss=.8)
        s.part(ramp('#5a4a6a', 1.2), [('poly', [(40, 14), (48, 14), (47, 6), (44, 3.5), (41, 6)])], soft=1, gloss=.8)
        s.part(gold, [('ell', 44, 15.5, 1.5, 1.5)], soft=.5, gloss=1)
    arm(s, plate, plate, (35, 30), (39, 36), (43, 40), r=3)
    s.part(gold, [('chord', 36, 31, 5.4, 4.6, 180, 360)], soft=1.2, gloss=1, cast=1)
    arm(s, plate, plate, (21, 30), (17.5, 34), (14.5, 36.5), r=3)
    with s.grp('armL'):   # a dark tome
        s.part(ramp('#2a1a30', 1.3), [('rect', 9, 33, 17, 40)], soft=.8, gloss=.4)
        s.part(ramp('#c040ff', 1.2), [('rect', 12, 35, 14, 38)], soft=.3, flat=True, bias=.2, line=False)
    head(s)
    bangs(s, ramp('#e8e8f0', 1.0), 'swept', shine=10)
    s.part(plate, [('chord', 28, 16.5, 12, 10.5, 180, 360), ('rect', 16, 14, 19, 24), ('rect', 37, 14, 40, 24)], soft=2, gloss=1, cast=2)
    horn = ramp('#e8dcc0', .9)
    s.part(horn, [('poly', [(17, 12), (11, 4), (12, 11), (16, 15)]), ('poly', [(39, 12), (45, 4), (44, 11), (40, 15)])], soft=.8, gloss=.6)
    s.part(red, [('rect', 16, 14, 40, 15.6)], soft=.5, cast=1)
    face(s, '#c03050', mouth='smile')
    for x, y in ((6, 28), (51, 30), (20, 45)):
        sparkle(s, x, y, (210, 120, 255))
    return s


OCCULTISTS = dict(hexer=hexer, bogwitch=bogwitch, doomherald=doomherald)
