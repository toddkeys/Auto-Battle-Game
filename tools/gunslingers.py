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
    # master engineer in a power rig: a steam backpack with two glowing exhaust stacks, a huge mechanical
    # right arm ending in a three-finger claw with a coil, a visor of glowing lenses, a heavy leather coat
    s = Spr()
    coat, plate, brass, dark, glowc = ramp('#5a3a24', 1.2), ramp('#5a6474', 1.3), ramp('#d8a040', 1.25, 1.1), ramp('#22242c', 1.2), ramp('#7ff0ff', 1.3, 1.3)
    s.piv.update(armR=(37, 31))   # the mechanical arm swings from the shoulder
    s.hands['armR'] = (45, 37)    # its wrist, where the weapon pivots
    with s.grp('cape'):   # steam backpack with glowing exhaust stacks
        s.part(dark, [('rect', 16, 20, 40, 37)], soft=1.5)
        for x in (19, 37):
            s.part(plate, [('rect', x - 2, 8, x + 2, 22)], soft=.6, gloss=1)
            s.part(brass, [('rect', x - 2.6, 7, x + 2.6, 9)], soft=.4, gloss=1.2)
        s.part(glowc, [('ell', 28, 28, 3, 3)], soft=1, gloss=1.5, line=False)
    legs(s, plate, ramp('#2a2a32', 1.2))
    torso(s, coat, hem=45)
    with s.grp('body'):
        s.part(plate, [('poly', [(21.5, 29), (34.5, 29), (34, 38), (22, 38)])], soft=1.4, gloss=1)   # chest plate
        s.part(glowc, [('ell', 28, 33.5, 2.4, 2.4)], soft=.8, gloss=1.6, line=False)   # power core
        for x, y in ((23.5, 30.5), (32.5, 30.5), (23.5, 36.5), (32.5, 36.5)):
            s.mark(int(x), int(y), (230, 190, 100))
    belt(s, P['leather'], 40, brass)
    with s.grp('weapon'):   # huge mechanical arm with a three-finger claw and a crackling coil
        s.part(plate, [('cap', 37, 31, 45, 37, 3.2), ('cap', 45, 37, 47, 43, 2.8)], soft=1.2, gloss=1.1)
        s.part(brass, [('ell', 37, 31, 3.6, 3.6), ('ell', 45, 37, 2.4, 2.4)], soft=.6, gloss=1.3)
        s.part(dark, [('poly', [(44, 43), (42, 49), (44, 48)]), ('poly', [(47, 44), (47.5, 50.5), (49, 48)]), ('poly', [(49, 42.5), (53, 46), (51, 47)])], soft=.3)
        s.part(glowc, [('cap', 43, 39.5, 48, 41.5, .5)], soft=.2, line=False, flat=True, bias=.35)
    arm(s, coat, SKIN, (21, 30), (18.5, 35), (18, 39.5), glove=P['leather'])
    head(s)
    bangs(s, ramp('#c8c8d0', 1.0), 'spiky', shine=9)
    s.part(dark, [('rect', 17.5, 17.5, 38.5, 21.5)], soft=.4, cast=1)   # visor band over the eyes
    for x in (22, 27.5, 33):
        s.part(glowc, [('ell', x, 19.5, 2, 1.6)], soft=.4, gloss=1.5, line=False)   # three glowing lenses
    s.part(ramp('#3a2a20'), [('rect', 17, 11.5, 39, 13.5)], soft=.4, cast=1)
    face(s, '#3a7ad0', mouth='smile', blush=False)
    for x, y in ((19, 4), (37, 4), (52, 41), (8, 22)):
        sparkle(s, x, y, (180, 240, 255))
    return s


def arctower():
    # the Gearmaster's lightning tower: a riveted base, a tall coil wound in copper, a crackling orb on top
    s = Spr()
    plate, copper, dark, glowc = ramp('#5a6474', 1.3), ramp('#c8742a', 1.25, 1.1), ramp('#22242c', 1.2), ramp('#9ff6ff', 1.3, 1.3)
    s.piv.update(head=(28, 24))
    with s.grp('body'):
        s.part(dark, [('poly', [(17, 53), (39, 53), (36, 45), (20, 45)])], soft=1)   # base
        s.part(plate, [('rect', 21, 41, 35, 46)], soft=.8, gloss=1)
        for x in (22, 28, 34):
            s.mark(x, 43, (230, 190, 100))
        s.part(dark, [('rect', 25.5, 24, 30.5, 41)], soft=.6)   # coil post
        for y in range(26, 41, 3):
            s.part(copper, [('ell', 28, y, 5.2, 1.3)], soft=.3, gloss=1.2)   # copper windings
    with s.grp('head'):
        s.part(plate, [('ell', 28, 22, 6, 2.2)], soft=.6, gloss=1)
        s.part(glowc, [('ell', 28, 16, 5.5, 5.5)], soft=1.5, gloss=1.8, line=False)   # crackling orb
        s.part(ramp('#ffffff', .5), [('ell', 26.5, 14.5, 1.6, 1.6)], soft=.4, line=False, flat=True, bias=.4)
    for x, y, a in ((20, 10, 220), (36, 9, 220), (17, 18, 160), (39, 19, 160), (28, 7, 200)):
        s.glow(x, y, (170, 250, 255), a)
    return s

GUNSLINGERS = dict(gunslinger=gunslinger, deadshot=deadshot, gearmaster=gearmaster, arctower=arctower)
