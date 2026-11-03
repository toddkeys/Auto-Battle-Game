"""Designs for the newer bosses (original characters). Drawn on the usual 56x54 canvas; the game scales bosses up."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from pixel import Spr, ramp


def thornmother():
    # ancient dryad: bark gown, a crown of leaves and flowers, a thorned staff, a glowing spore in the other hand
    s = Spr()
    bark, leaf, moss, petal, spore = ramp('#6a4a2e', 1.2), ramp('#4f9a3a', 1.2), ramp('#3a6a2a', 1.1), ramp('#ff8ab8', 1.1), ramp('#bff27a', 1.2, 1.3)
    s.piv.update(armL=(18, 28), armR=(38, 28), head=(28, 24), cape=(28, 26))
    with s.grp('cape'):   # leafy mantle
        s.part(leaf, [('poly', [(14, 24), (42, 24), (52, 50), (46, 47), (42, 53), (36, 48), (28, 53), (20, 48), (14, 53), (10, 47), (4, 50)])], soft=2.5)
    with s.grp('armR'):   # thorned staff crowned with a flower
        s.part(bark, [('cap', 44, 53, 45, 9, 1.1)], soft=.6)
        for y in (18, 26, 34, 42):
            s.part(bark, [('poly', [(45, y), (48, y - 2), (46, y + 1.5)])], soft=.3)
        s.part(petal, [('ell', 45, 6, 4.5, 3.5)], soft=1, gloss=.8)
        s.part(ramp('#ffe27a', 1.1), [('ell', 45, 6, 1.6, 1.4)], soft=.4, gloss=1)
        s.part(bark, [('cap', 38, 28, 43, 34, 3)], soft=1.1)
        s.part(moss, [('ell', 44, 35, 2, 2)], soft=.6)
    with s.grp('body'):   # bark gown
        s.part(bark, [('poly', [(20, 25), (36, 25), (42, 51), (34, 50), (28, 52), (22, 50), (14, 51)])], soft=2.5, cast=1)
        s.part(moss, [('poly', [(22, 26), (34, 26), (31, 34), (28, 36), (25, 34)])], soft=1)
        for x, y in ((22, 42), (33, 38), (27, 47)):
            s.part(petal, [('ell', x, y, 1.6, 1.4)], soft=.4, gloss=.8)
    with s.grp('armL'):   # vine arm holding a glowing spore
        s.part(bark, [('cap', 18, 28, 12, 33, 3)], soft=1.1)
        s.part(spore, [('ell', 10, 31, 3.4, 3.4)], soft=1.2, gloss=1.4, line=False)
    with s.grp('head'):
        s.part(ramp('#c8e0a8', .9), [('ell', 28, 19.5, 7, 7.5)], soft=2)   # pale green face
        s.part(leaf, [('poly', [(16, 16), (19, 6), (23, 13), (26, 3), (29, 12), (33, 4), (35, 13), (39, 6), (40, 17), (36, 13), (28, 11), (20, 13)])], soft=1.2, cast=2)
        for x, y in ((20, 10), (28, 7), (36, 10)):
            s.part(petal, [('ell', x, y, 2, 1.8)], soft=.5, gloss=1)
        s.part(moss, [('poly', [(20, 18), (17, 30), (21, 26)]), ('poly', [(36, 18), (39, 30), (35, 26)])], soft=.8)   # hanging vines
        for x in (25, 26, 30, 31):
            s.mark(x, 20, (230, 255, 120))
    for x, y, a in ((6, 18, 200), (50, 30, 180), (8, 44, 160)):
        s.glow(x, y, (200, 255, 140), a)
    return s


def stormdjinn():
    # a storm spirit: no legs, a swirling cloud tail, lightning hair, golden bands
    s = Spr()
    skin, cloud, gold, bolt = ramp('#4a7ad8', 1.2, 1.1), ramp('#dfefff', .8), P['gold'], ramp('#ffe45a', 1.2, 1.3)
    s.piv.update(armL=(18, 27), armR=(38, 27), head=(28, 22), cape=(28, 40))
    with s.grp('cape'):   # cloud tail
        s.part(cloud, [('poly', [(20, 38), (36, 38), (38, 44), (32, 48), (36, 52), (26, 53), (30, 49), (22, 46)])], soft=2.5, gloss=.4)
        s.part(ramp('#a8c8f0', 1), [('cap', 23, 44, 33, 47, 1.2)], soft=.6, line=False)
    with s.grp('body'):
        s.part(skin, [('poly', [(18, 25), (38, 25), (36, 39), (20, 39)])], soft=2.5, cast=1)   # broad chest
        s.part(ramp('#3a62b8', 1.2), [('cap', 24, 30, 32, 30, .6), ('cap', 28, 30, 28, 37, .6)], soft=.3, line=False)
        s.part(gold, [('rect', 20, 37, 36, 39.5)], soft=.4, gloss=1)
    for g, sh, hd in (('armL', (18, 27), (11, 21)), ('armR', (38, 27), (45, 21))):   # arms raised, lightning in the hands
        with s.grp(g):
            s.part(skin, [('cap', *sh, *hd, 3.4)], soft=1.2)
            s.part(gold, [('ell', (sh[0] + hd[0]) / 2, (sh[1] + hd[1]) / 2, 2.6, 1.6)], soft=.4, gloss=1)
            s.part(bolt, [('poly', [(hd[0] - 1, hd[1] - 2), (hd[0] + 2, hd[1] - 7), (hd[0] + .5, hd[1] - 4), (hd[0] + 3, hd[1] - 4), (hd[0] - 1, hd[1] + 1)])], soft=.3, gloss=1.4, line=False)
    with s.grp('head'):
        s.part(skin, [('ell', 28, 18, 7, 7)], soft=2, cast=1)
        s.part(bolt, [('poly', [(22, 13), (24, 3), (26, 10), (28, 1), (30, 10), (32, 3), (34, 13), (28, 11)])], soft=.6, gloss=1.2)   # lightning hair
        s.part(ramp('#f0f4ff', .7), [('poly', [(24, 22), (32, 22), (30, 29), (28, 31), (26, 29)])], soft=1)   # beard of mist
        s.part(gold, [('ell', 21, 19, 1.2, 1.6), ('ell', 35, 19, 1.2, 1.6)], soft=.3, gloss=1)
        for x in (25, 26, 30, 31):
            s.mark(x, 17, (255, 255, 255))
    for x, y, a in ((6, 30, 200), (50, 34, 200), (12, 8, 180), (46, 8, 180)):
        s.glow(x, y, (255, 240, 140), a)
    return s


def colossus():
    # clockwork colossus: brass hull, a turning gear in the chest, piston arms, one glowing eye
    s = Spr()
    brass, dark, steel, core, eye = ramp('#c89a3a', 1.2, 1.1), ramp('#4a3a2a', 1.2), P['steel'], ramp('#ff8a2a', 1.3, 1.2), ramp('#7ff0ff', 1.2, 1.3)
    s.part(dark, [('poly', [(17, 42), (25, 42), (25.5, 53), (16, 53)]), ('poly', [(31, 42), (39, 42), (40, 53), (30.5, 53)])], soft=1.2)   # legs
    s.part(brass, [('rect', 15.5, 49, 26, 53), ('rect', 30, 49, 40.5, 53)], soft=.8, gloss=.8)
    s.piv.update(armL=(13, 27), armR=(43, 27), head=(28, 22))
    s.group = 'body'
    for g, x0, x1 in (('armL', 13, 9), ('armR', 43, 47)):   # piston arms with big fists
        with s.grp(g):
            s.part(dark, [('cap', x0, 30, x1, 42, 3.2)], soft=1)
            s.part(steel, [('cap', x0, 31, x1 + (x0 - x1) * .3, 36, 1.4)], soft=.4, gloss=1.2, line=False)
            s.part(brass, [('ell', x1, 45, 5, 4.4)], soft=1.4, gloss=1)
            s.part(brass, [('ell', x0, 27, 6.5, 5.5)], soft=1.5, gloss=1, cast=1)
    s.part(brass, [('rect', 16, 25, 40, 43)], soft=2.5, gloss=.8, cast=1)   # hull
    for x, y in ((18, 27), (38, 27), (18, 41), (38, 41)):
        s.mark(x, y, (90, 60, 30))
    s.part(dark, [('ell', 28, 34, 6.2, 6.2)], soft=.8)
    for i in range(8):   # gear teeth
        import math
        a = i * math.pi / 4
        s.part(steel, [('ell', 28 + math.cos(a) * 6.2, 34 + math.sin(a) * 6.2, 1.3, 1.3)], soft=.3, gloss=1, line=False)
    s.part(core, [('ell', 28, 34, 3.5, 3.5)], soft=1.2, gloss=1.5, line=False)
    with s.grp('head'):
        s.part(brass, [('chord', 28, 22, 8, 7, 180, 360), ('rect', 20, 21.5, 36, 25)], soft=1.5, gloss=1, cast=1)
        s.part(dark, [('rect', 21, 17.5, 35, 21)], soft=.4)
        s.part(eye, [('ell', 28, 19.2, 3, 1.5)], soft=.4, gloss=1.4, line=False)
    for x, y, a in ((28, 34, 160), (28, 19, 200)):
        s.glow(x, y, (255, 190, 100) if y > 30 else (140, 240, 255), a)
    return s


BOSSES = dict(thornmother=thornmother, stormdjinn=stormdjinn, colossus=colossus)
