"""Gunslinger class and the 4-gold Gearmaster (original characters)."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import sparkle
from pixel import Spr, ramp


def revolver(s, x, y, flip=1):
    """a small six-shooter held at (x, y), barrel pointing forward-left (flip=-1 points right)"""
    gun, grip = ramp('#5a6070', 1.3), ramp('#8a5a32')
    s.part(gun, [('rect', x - 5.5 * (flip > 0) + .5 * (flip < 0), y - 1.6, x + .5 * (flip > 0) + 5.5 * (flip < 0), y + .2), ('ell', x, y - .8, 1.6, 1.4)], soft=.4, gloss=1.2)
    s.part(grip, [('poly', [(x - .5, y), (x + 1.5, y), (x + 2.2 * flip, y + 3), (x + .4 * flip, y + 3.2)])], soft=.3)


def gunslinger():
    # drifter: long dust-brown duster, wide-brim hat, red scarf, a revolver in each hand
    s = Spr()
    coat, hat, scarf, shirt = ramp('#8a6a44', 1.1), ramp('#5a3e2a', 1.2), ramp('#c83a2a', 1.1), ramp('#d8c8a8', .8)
    with s.grp('cape'):   # duster tails
        s.part(coat, [('poly', [(20, 36), (36, 36), (40, 51), (34, 49), (28, 51), (22, 49), (16, 51)])], soft=1.8)
    legs(s, ramp('#3a3a48'), ramp('#5a3a24'))
    torso(s, shirt, hem=44)
    with s.grp('body'):
        s.part(coat, [('poly', [(19.5, 28), (25, 28), (24, 44), (18.5, 44)]), ('poly', [(31, 28), (36.5, 28), (37.5, 44), (32, 44)])], soft=1.4)   # open duster
    belt(s, ramp('#3a2a1a'), 39, P['steel'])
    with s.grp('weapon'):
        revolver(s, 42, 39, 1)
    arm(s, coat, SKIN, (35, 30), (38.5, 35.5), (41.5, 38.5), glove=ramp('#4a3424'))
    arm(s, coat, SKIN, (21, 30), (17.5, 34.5), (14, 36), glove=ramp('#4a3424'))
    revolver(s, 13.5, 35, 1)
    s.part(scarf, [('ell', 28, 28.5, 8, 2.8)], soft=1, cast=1)
    s.part(scarf, [('poly', [(31, 28), (34, 28.5), (38, 33), (35, 33)])], soft=.8)
    head(s)
    bangs(s, ramp('#3a2a20'), 'swept', shine=10)
    s.part(hat, [('ell', 28, 12.5, 16, 3.4)], soft=1.2, cast=2)   # wide brim
    s.part(hat, [('chord', 28, 12.5, 9.5, 8, 180, 360)], soft=1.6, cast=2)
    s.part(ramp('#c8a060'), [('rect', 18.6, 10.5, 37.4, 12.5)], soft=.4)   # hat band
    face(s, '#6a8aa0')
    return s


def deadshot():
    # marksman: a long dark greatcoat, a wide feathered hat, a brass scope over one eye, a long rifle
    s = Spr()
    coat, dark, brass, feather = ramp('#2a3a4a', 1.2), ramp('#1a1e28', 1.2), ramp('#d8a040', 1.2, 1.1), ramp('#e8e0d0', .8)
    with s.grp('cape'):   # long greatcoat
        s.part(coat, [('poly', [(19, 30), (37, 30), (43, 52), (36, 50), (28, 52), (20, 50), (13, 52)])], soft=2)
    legs(s, dark, ramp('#3a2a20'))
    torso(s, coat, hem=45)
    with s.grp('body'):
        s.part(ramp('#8a2a2a', 1.1), [('poly', [(25.5, 29), (30.5, 29), (30, 44), (26, 44)])], soft=.8)   # waistcoat
        for y in (32, 35, 39):
            s.mark(28, y, (230, 190, 90))
    belt(s, ramp('#3a2a1a'), 40, brass)
    with s.grp('weapon'):   # long rifle held diagonally
        s.part(P['wood'], [('line', [(38, 46), (42, 38)], 1.3)], soft=.5)
        s.part(ramp('#4a5060', 1.3), [('cap', 41.5, 39, 50, 18, .8)], soft=.4, gloss=1.2)
        s.part(brass, [('cap', 43.5, 33, 46, 27, .9)], soft=.3, gloss=1.2)   # rifle scope
    arm(s, coat, SKIN, (35, 30), (38.5, 35.5), (41, 39), glove=dark)
    arm(s, coat, SKIN, (21, 30), (24, 35), (30, 37), glove=dark)
    head(s)
    bangs(s, ramp('#c8c8d0', 1.1), 'neat', shine=10)
    s.part(dark, [('ell', 28, 12.5, 15, 3.2)], soft=1.2, cast=2)
    s.part(dark, [('chord', 28, 12.5, 9, 8, 180, 360)], soft=1.6, cast=2)
    s.part(feather, [('poly', [(35, 9), (46, 1), (44, 6), (38, 11)])], soft=.5)
    s.part(ramp('#c83a3a'), [('rect', 19, 10.5, 37, 12.5)], soft=.4)
    face(s, '#4a6a8a')
    s.part(brass, [('ell', 29, 21, 2.6, 2.6)], sub=[('ell', 29, 21, 1.5, 1.5)], soft=.3, gloss=1.2, line=False)   # brass eye-scope
    s.part(ramp('#ff5a4a', 1.2), [('ell', 29, 21, 1.3, 1.3)], soft=.3, gloss=1.4, line=False)
    sparkle(s, 51, 16, (255, 200, 160))
    return s


def gearmaster():
    # veteran inventor: leather apron over a brass harness with a mechanical claw arm over the shoulder,
    # big goggles, a glowing power wrench
    s = Spr()
    apron, shirt, brass, steel, glowc = ramp('#6a4a30', 1.1), ramp('#3a5a8a', 1.1), ramp('#d8a040', 1.2, 1.1), P['steel'], ramp('#7ff0ff', 1.3, 1.2)
    with s.grp('cape'):   # backpack engine with a mechanical claw arm reaching over the shoulder
        s.part(ramp('#4a4a52', 1.2), [('rect', 16, 22, 40, 36)], soft=1.5)
        s.part(brass, [('ell', 22, 23, 3, 3), ('ell', 34, 23, 3, 3)], soft=.6, gloss=1)
        s.part(steel, [('line', [(36, 24), (44, 16), (50, 18)], 1.2)], soft=.5, gloss=1.2)
        s.part(steel, [('poly', [(49, 15), (54, 14), (53, 16.5), (51, 17)]), ('poly', [(49, 19), (54, 21), (52, 22.5), (50.5, 20.5)])], soft=.3, gloss=1.2)
    legs(s, ramp('#3a3a48'), P['darkleather'])
    torso(s, shirt, hem=44)
    with s.grp('body'):
        s.part(apron, [('poly', [(22, 31), (34, 31), (35.5, 46), (20.5, 46)])], soft=1.2)
        s.part(brass, [('cap', 21, 29, 35, 29, .8)], soft=.3, gloss=1)
        s.part(glowc, [('ell', 28, 36, 2.2, 2.2)], soft=.8, gloss=1.5, line=False)   # power cell
    belt(s, P['leather'], 41, brass)
    with s.grp('weapon'):   # glowing power wrench
        s.part(steel, [('cap', 42, 43, 46, 26, 1.3), ('poly', [(42.5, 26), (49.5, 23.5), (49.5, 20), (46.5, 22), (45, 19), (42.5, 22.5)])], soft=.6, gloss=1)
        s.part(glowc, [('cap', 43, 38, 45.5, 29, .4)], soft=.2, line=False, flat=True, bias=.3)
    arm(s, shirt, SKIN, (35, 30), (38.5, 36), (42, 40), glove=P['leather'])
    arm(s, shirt, SKIN, (21, 30), (18.5, 35), (18, 39), glove=P['leather'])
    head(s)
    bangs(s, ramp('#a8a8b0', 1.0), 'spiky', shine=9)
    s.part(ramp('#3a2a20'), [('rect', 17, 12, 39, 14.5)], soft=.4, cast=1)
    s.part(brass, [('ell', 23, 12.5, 3.4, 3.2), ('ell', 33, 12.5, 3.4, 3.2)], soft=.5, gloss=1.2)   # big goggles
    s.part(glowc, [('ell', 23, 12.5, 2, 1.9), ('ell', 33, 12.5, 2, 1.9)], soft=.5, gloss=1.4, line=False)
    face(s, '#3a7ad0')
    sparkle(s, 50, 26, (180, 240, 255))
    return s


GUNSLINGERS = dict(gunslinger=gunslinger, deadshot=deadshot, gearmaster=gearmaster)
