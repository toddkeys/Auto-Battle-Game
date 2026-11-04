"""Designs for the newer bosses (original characters). Drawn on the usual 56x54 canvas; the game scales bosses up."""
import math

from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from pixel import Spr, ramp


def thornmother():
    # thorn witch: a pale wooden mask with glowing green eye slits, an antler crown of thorns,
    # a dark bramble cloak, moss tendrils, and a staff topped with a glowing seed pod
    s = Spr()
    bark, dark, thorn, moss, mask = ramp('#4a3424', 1.3), ramp('#2a1e1a', 1.2), ramp('#6a3a4a', 1.2), ramp('#3f7a34', 1.2), ramp('#d8cdb0', .8)
    seed, glow = ramp('#9aff5a', 1.3, 1.3), (190, 255, 120)
    s.piv.update(armL=(18, 28), armR=(38, 28), head=(28, 24), cape=(28, 26))
    with s.grp('cape'):   # tattered bramble cloak
        s.part(dark, [('poly', [(13, 24), (43, 24), (53, 49), (47, 46), (44, 53), (38, 47), (33, 53), (28, 48), (23, 53), (18, 47), (12, 53), (9, 46), (3, 49)])], soft=2.5)
        for x, y in ((8, 44), (48, 44), (16, 50), (40, 50)):
            s.part(thorn, [('poly', [(x, y), (x + 1.2, y - 4), (x + 2.2, y)])], soft=.3, line=False)
    with s.grp('armR'):   # crooked staff with a glowing seed pod caged in thorns
        s.part(bark, [('line', [(45, 53), (44, 40), (46, 28), (44, 16), (46, 9)], 1.1)], soft=.6)
        s.part(thorn, [('poly', [(42, 4), (46, 1), (50, 4), (48, 12), (44, 12)])], sub=[('ell', 46, 7, 2.6, 3)], soft=.5, line=False)
        s.part(seed, [('ell', 46, 7, 2.3, 2.8)], soft=.8, gloss=1.5, line=False)
        s.part(bark, [('cap', 38, 28, 44, 33, 2.8)], soft=1.1)
    with s.grp('body'):   # hunched bark gown with thorns growing out of it
        s.part(bark, [('poly', [(20, 25), (36, 25), (41, 51), (34, 50), (28, 52), (22, 50), (15, 51)])], soft=2.5, cast=1)
        s.part(moss, [('poly', [(21, 26), (35, 26), (32, 33), (28, 35), (24, 33)])], soft=1)
        for x, y, d in ((19, 38, -1), (37, 36, 1), (21, 46, -1), (35, 45, 1)):
            s.part(thorn, [('poly', [(x, y), (x + 3.5 * d, y - 2), (x, y + 1.5)])], soft=.3)
        for x, y in ((25, 40), (31, 43), (28, 48)):
            s.part(seed, [('ell', x, y, .9, .9)], soft=.3, line=False, flat=True, bias=.3)
    with s.grp('armL'):   # gnarled branch arm, a spore cloud in the claw
        s.part(bark, [('line', [(18, 28), (13, 31), (10, 29)], 2.6)], soft=1.1)
        s.part(bark, [('poly', [(9, 27), (6, 24), (9, 26), (8, 22), (11, 26)])], soft=.4)
        s.part(seed, [('ell', 8, 31, 3, 3)], soft=1.2, gloss=1.4, line=False)
    with s.grp('head'):
        s.part(dark, [('ell', 28, 19, 8.5, 9)], soft=2)   # hood of shadow behind the mask
        s.part(mask, [('poly', [(21.5, 14), (34.5, 14), (34, 22), (30, 27), (26, 27), (22, 22)])], soft=1.5, gloss=.5)   # wooden mask
        s.part(ramp('#8a7a5a'), [('cap', 28, 15, 28, 25, .35)], soft=.2, line=False)   # crack down the mask
        for x0 in (23.5, 30):   # glowing eye slits
            s.part(ramp('#3a5a1a'), [('poly', [(x0, 18.5), (x0 + 3, 17.5), (x0 + 3, 19.5), (x0, 20)])], soft=.2, line=False)
        for x in (24, 25, 31, 32):
            s.mark(x, 18 if x in (25, 32) else 19, glow)
        for sx in (-1, 1):   # antler crown of thorny branches
            pts = [(28 + sx * 6, 14), (28 + sx * 9, 6), (28 + sx * 12, 2), (28 + sx * 10.5, 8), (28 + sx * 14, 7), (28 + sx * 10, 11), (28 + sx * 8, 14)]
            s.part(bark, [('poly', pts)], soft=.5, cast=2)
        s.part(moss, [('poly', [(20, 21), (17, 34), (21, 30)]), ('poly', [(36, 21), (39, 34), (35, 30)])], soft=.8)   # hanging moss
    for x, y, a in ((6, 18, 200), (50, 30, 180), (8, 42, 160), (46, 2, 220)):
        s.glow(x, y, glow, a)
    return s


def stormdjinn():
    # storm wraith: a hood of thunderhead with two white eyes and no face, a body of storm cloud
    # split by lightning veins, crackling hands, a crown of floating lightning shards, a funnel-cloud tail
    s = Spr()
    cloud, dark, light, bolt = ramp('#5a6a8a', 1.2), ramp('#2a3048', 1.2), ramp('#c8d8f0', .8), ramp('#ffe45a', 1.2, 1.3)
    s.piv.update(armL=(18, 27), armR=(38, 27), head=(28, 22), cape=(28, 40))
    with s.grp('cape'):   # twisting funnel-cloud tail
        s.part(cloud, [('poly', [(19, 37), (37, 37), (38, 43), (33, 47), (36, 51), (29, 54), (30, 49), (24, 46), (19, 42)])], soft=2.5, gloss=.3)
        s.part(light, [('cap', 23, 42, 34, 44, 1), ('cap', 26, 48, 33, 50, .8)], soft=.5, line=False)
    with s.grp('body'):   # storm-cloud torso split by lightning veins
        s.part(cloud, [('poly', [(17, 25), (39, 25), (37, 39), (19, 39)])], soft=2.5, cast=1)
        s.part(dark, [('ell', 28, 31, 6.5, 5)], soft=1.5)
        s.part(bolt, [('line', [(22, 27), (25, 31), (23, 34), (27, 38)], .45), ('line', [(34, 27), (31, 30), (33, 34), (30, 38)], .45)], soft=.2, line=False, flat=True, bias=.3)
        s.part(ramp('#bfe8ff', 1.2), [('ell', 28, 31, 2.3, 2.3)], soft=1, gloss=1.6, line=False)   # glowing heart of the storm
    for g, sh, hd in (('armL', (18, 27), (10, 22)), ('armR', (38, 27), (46, 22))):   # cloud arms, lightning in the claws
        with s.grp(g):
            s.part(cloud, [('cap', *sh, *hd, 3.3)], soft=1.2)
            s.part(light, [('ell', hd[0], hd[1], 3, 2.6)], soft=1, gloss=.5)
            s.part(bolt, [('poly', [(hd[0] - 1, hd[1] - 2), (hd[0] + 2, hd[1] - 8), (hd[0] + .5, hd[1] - 4.5), (hd[0] + 3.5, hd[1] - 4.5), (hd[0] - 1.5, hd[1] + 1)])], soft=.3, gloss=1.4, line=False)
    with s.grp('head'):
        s.part(cloud, [('ell', 28, 18, 8.5, 8.5), ('poly', [(20, 18), (36, 18), (34, 26), (22, 26)])], soft=2, cast=1)   # thunderhead hood
        s.part(ramp('#10121c'), [('ell', 28, 20, 5.5, 5.2)], soft=1.2)   # empty dark face
        for x in (25, 26, 30, 31):
            s.mark(x, 19, (255, 255, 255))
        for x in (25, 30):
            s.mark(x + 1, 20, (190, 220, 255))
        for i, x in enumerate((19, 23.5, 28, 32.5, 37)):   # crown of floating lightning shards
            y = 7 - (2 if i == 2 else 1 if i in (1, 3) else 0)
            s.part(bolt, [('poly', [(x - 1, y + 3), (x, y - 2), (x + 1, y + 3)])], soft=.3, gloss=1.2, line=False)
    for x, y, a in ((6, 30, 200), (50, 34, 200), (12, 8, 180), (46, 8, 180), (28, 1, 220)):
        s.glow(x, y, (255, 240, 140), a)
    return s


def colossus():
    # clockwork titan: dark iron armour plates over brass, a spinning gear core, a glowing visor slit,
    # smokestacks venting light on the shoulders, piston arms with heavy riveted fists
    s = Spr()
    iron, brass, dark, steel = ramp('#4a5262', 1.3), ramp('#c89a3a', 1.2, 1.1), ramp('#2a2a32', 1.2), P['steel']
    core, eye = ramp('#7ff0ff', 1.3, 1.3), ramp('#7ff0ff', 1.2, 1.3)
    s.part(iron, [('poly', [(16, 42), (25, 42), (25.5, 53), (15, 53)]), ('poly', [(31, 42), (40, 42), (41, 53), (30.5, 53)])], soft=1.2)   # legs
    s.part(brass, [('rect', 14.5, 49.5, 26, 53), ('rect', 30, 49.5, 41.5, 53)], soft=.8, gloss=.8)
    s.piv.update(armL=(13, 27), armR=(43, 27), head=(28, 22))
    s.group = 'body'
    for x in (16, 40):   # shoulder smokestacks
        s.part(dark, [('rect', x - 2, 13, x + 2, 24)], soft=.6)
        s.part(brass, [('rect', x - 2.6, 12, x + 2.6, 14)], soft=.4, gloss=1)
    for g, x0, x1 in (('armL', 13, 8), ('armR', 43, 48)):   # piston arms with heavy fists
        with s.grp(g):
            s.part(dark, [('cap', x0, 30, x1, 42, 3.4)], soft=1)
            s.part(steel, [('cap', x0, 31, x1 + (x0 - x1) * .3, 36, 1.4)], soft=.4, gloss=1.2, line=False)
            s.part(iron, [('ell', x1, 45, 5.4, 4.8)], soft=1.4, gloss=1)
            for dx in (-2.5, 0, 2.5):
                s.mark(int(x1 + dx), 44, (200, 160, 90))
            s.part(iron, [('ell', x0, 27, 7, 6)], soft=1.5, gloss=1, cast=1)
            s.part(brass, [('chord', x0, 27, 7, 6, 200, 340)], soft=.5, gloss=1, line=False)
    s.part(iron, [('poly', [(15, 25), (41, 25), (39, 43), (17, 43)])], soft=2.5, gloss=.8, cast=1)   # armoured hull
    s.part(brass, [('rect', 17, 39, 39, 41)], soft=.4, gloss=1)
    for x, y in ((17, 27), (39, 27), (19, 37), (37, 37)):
        s.mark(x, y, (220, 180, 100))
    s.part(dark, [('ell', 28, 32.5, 6.4, 6.4)], soft=.8)
    for i in range(8):   # gear teeth
        a = i * math.pi / 4
        s.part(brass, [('ell', 28 + math.cos(a) * 6.4, 32.5 + math.sin(a) * 6.4, 1.3, 1.3)], soft=.3, gloss=1, line=False)
    s.part(core, [('ell', 28, 32.5, 3.6, 3.6)], soft=1.2, gloss=1.6, line=False)
    with s.grp('head'):
        s.part(iron, [('chord', 28, 22, 8, 8, 180, 360), ('rect', 20, 21.5, 36, 25.5)], soft=1.5, gloss=1, cast=1)
        s.part(brass, [('poly', [(26.5, 14), (29.5, 14), (28, 9)])], soft=.4, gloss=1)   # crest fin
        s.part(dark, [('rect', 20.5, 18, 35.5, 21.5)], soft=.4)
        s.part(eye, [('rect', 22, 19, 34, 20.5)], soft=.3, gloss=1.4, line=False)   # glowing visor slit
    for x, y, a in ((28, 32, 180), (28, 19, 220), (16, 10, 200), (40, 10, 200), (15, 7, 120), (41, 7, 120)):
        s.glow(x, y, (140, 240, 255), a)
    return s


BOSSES = dict(thornmother=thornmother, stormdjinn=stormdjinn, colossus=colossus)
