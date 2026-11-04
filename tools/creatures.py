"""Summons (called by Summoners and bosses) and the newer bosses. All original, facing down-left."""
from monsters import blob_eyes
from pixel import Spr, ramp


def wisp():
    s = Spr()
    flame, core = ramp('#4fe0c0', 1.1, 1.1), ramp('#e8fff8', .7)
    s.piv['head'] = (28, 46)
    with s.grp('head'):
        s.part(flame, [('ell', 28, 40, 9, 8.5), ('poly', [(19.5, 38), (22, 30), (25, 34), (28, 24), (31, 33), (34, 29), (36.5, 38)])], soft=2.5)
        s.part(core, [('ell', 28, 41.5, 5, 4.5)], soft=1.5, gloss=1, line=False)
        blob_eyes(s, (25, 30), 40, h=2)
    for x, y, a in ((22, 49, 200), (28, 51, 150), (33, 48, 180), (18, 34, 140), (38, 26, 160)):
        s.glow(x, y, (150, 255, 225), a)
    return s


def wolf():
    s = Spr()
    fur, belly, dark = ramp('#8a92a0', 1.2), ramp('#d8dce4', .8), ramp('#4a505c', 1.2)
    s.piv.update(legL=(18, 41), legR=(38, 41), cape=(44, 38), head=(16, 34))
    with s.grp('cape'):   # tail
        s.part(fur, [('poly', [(42, 36), (50, 28), (54, 30), (49, 38), (44, 41)])], soft=1.2)
    with s.grp('legR'):
        s.part(dark, [('cap', 37, 42, 38, 51, 2), ('cap', 41, 42, 42.5, 50.5, 2)], soft=.8)
    with s.grp('legL'):
        s.part(dark, [('cap', 17, 42, 16, 51, 2), ('cap', 21, 42, 21.5, 51, 2)], soft=.8)
    with s.grp('body'):
        s.part(fur, [('ell', 30, 38, 15, 7.5)], soft=2.5, cast=1)
        s.part(belly, [('ell', 29, 42, 10, 3)], soft=1, line=False)
    with s.grp('head'):
        s.part(fur, [('ell', 15, 31, 7.5, 6.5), ('poly', [(9, 31), (2.5, 34), (4, 37), (10, 36)])], soft=2, cast=1)
        s.part(dark, [('poly', [(10, 26), (11.5, 18), (15, 25)]), ('poly', [(16, 25), (19, 18), (20.5, 26)])], soft=.6)
        s.part(dark, [('ell', 3.2, 34.5, 1.5, 1.2)], soft=.4, line=False)
        for x in (11, 12, 16):
            s.mark(x, 30, (255, 220, 80))
    return s


def guardian():
    s = Spr()
    rock, moss, rune = ramp('#a09a8c', 1.25), ramp('#6aa84a'), ramp('#6ad8ff', 1.2, 1.2)
    s.piv.update(armL=(14, 29), armR=(42, 29), head=(28, 26))
    s.group = 'body'
    s.part(rock, [('poly', [(19, 42), (26, 42), (26, 53), (18, 53)]), ('poly', [(30, 42), (37, 42), (38, 53), (30, 53)])], soft=1.5)
    with s.grp('armL'):
        s.part(rock, [('cap', 13, 30, 10, 44, 3.6), ('ell', 10, 46, 4, 3.6)], soft=1.6, gloss=.3)
    with s.grp('armR'):
        s.part(rock, [('cap', 43, 30, 46, 44, 3.6), ('ell', 46, 46, 4, 3.6)], soft=1.6, gloss=.3)
    s.part(rock, [('poly', [(17, 27), (39, 27), (37, 43), (19, 43)])], soft=2.5, cast=1)
    s.part(moss, [('chord', 28, 28, 11, 3, 180, 360)], soft=1)
    s.part(rune, [('poly', [(26, 32), (30, 32), (28, 38)]), ('line', [(20, 30), (23, 34), (21, 39)], .45), ('line', [(36, 30), (33, 34), (35, 39)], .45)], soft=.4, flat=True, bias=.25, line=False)
    with s.grp('head'):
        s.part(rock, [('poly', [(21, 16), (35, 16), (36, 27), (20, 27)])], soft=2, cast=1)
        s.part(moss, [('rect', 21, 15, 35, 17.5)], soft=.6)
        for x in (24, 25, 31, 32):
            s.mark(x, 21, (120, 230, 255))
    return s


def drake():
    s = Spr()
    scale, belly, wing = ramp('#4a6ad8', 1.2, 1.1), ramp('#bfe0ff', .8), ramp('#7a5ad0', 1.1)
    s.piv.update(wingL=(24, 30), wingR=(33, 30), head=(18, 30), cape=(38, 42))
    with s.grp('wingR'):
        s.part(wing, [('poly', [(32, 31), (44, 14), (46, 22), (52, 20), (47, 30), (38, 36)])], soft=1.2)
    with s.grp('cape'):   # tail
        s.part(scale, [('poly', [(36, 40), (48, 44), (54, 40), (52, 47), (40, 47)])], soft=1)
    with s.grp('body'):
        s.part(scale, [('ell', 30, 40, 10, 8)], soft=2.5, cast=1)
        s.part(belly, [('ell', 28, 43, 6, 4)], soft=1, line=False)
        s.part(scale, [('cap', 25, 47, 24, 52, 1.8), ('cap', 34, 47, 35, 52, 1.8)], soft=.8)
    with s.grp('wingL'):
        s.part(wing, [('poly', [(25, 31), (12, 13), (11, 21), (5, 20), (10, 30), (20, 36)])], soft=1.2)
    with s.grp('head'):
        s.part(scale, [('ell', 18, 30, 7, 6), ('poly', [(12, 30), (6, 33), (7, 36), (13, 35)])], soft=2, cast=1)
        s.part(ramp('#fff3a0', 1.1), [('poly', [(16, 25), (14, 18), (19, 24)]), ('poly', [(21, 25), (22, 18), (24, 25)])], soft=.5, gloss=1)
        s.mark(14, 29, (255, 240, 120)); s.mark(15, 29, (255, 240, 120))
    for x, y in ((8, 10), (48, 12), (30, 22)):
        s.glow(x, y, (255, 245, 180), 200)
    return s


def skeleton():
    s = Spr()
    bone, dark, rust = ramp('#ece4d0', .9), ramp('#3a3440', 1.2), ramp('#9a8a70', 1.2)
    s.piv.update(legL=(25, 40), legR=(31, 40), armL=(21, 30), armR=(35, 30), head=(28, 27))
    with s.grp('legL'):
        s.part(bone, [('cap', 25, 40, 24, 51, 1.3), ('ell', 23, 52, 2.6, 1.3)], soft=.6)
    with s.grp('legR'):
        s.part(bone, [('cap', 31, 40, 32, 51, 1.3), ('ell', 33, 52, 2.6, 1.3)], soft=.6)
    with s.grp('body'):
        s.part(bone, [('cap', 28, 28, 28, 40, 1.2)], soft=.6)
        s.part(bone, [('ell', 28, 33, 6, 4.8)], sub=[('rect', 23, 32, 33, 33), ('rect', 23, 35, 33, 36)], soft=1, cast=1)
        s.part(rust, [('ell', 28, 40, 5, 2)], soft=.6)
    with s.grp('armR'):
        s.part(rust, [('poly', [(40, 41), (42, 41), (46, 20), (44.5, 19)])], soft=.5, gloss=.8)
        s.part(bone, [('line', [(35, 30), (38, 36), (41, 40)], 1.1)], soft=.5)
    with s.grp('armL'):
        s.part(bone, [('line', [(21, 30), (18.5, 35.5), (18, 39)], 1.1)], soft=.5)
        s.part(rust, [('ell', 15.5, 38, 5, 5.5)], soft=1.3, gloss=.6)   # battered round shield
        s.part(dark, [('ell', 15.5, 38, 1.4, 1.4)], soft=.4, gloss=1)
    with s.grp('head'):
        s.part(bone, [('ell', 28, 19, 8.5, 8), ('rect', 23, 23, 33, 28)], soft=2, cast=1)
        s.part(rust, [('chord', 28, 17, 9.2, 7.5, 180, 360), ('rect', 18.8, 15.5, 37.2, 17.5)], soft=1, gloss=.6, cast=1)   # dented helmet
        s.part(dark, [('poly', [(27, 9.5), (29, 9.5), (28, 4)])], soft=.3)
        s.part(dark, [('ell', 24.5, 20, 2.4, 2.4), ('ell', 31.5, 20, 2.4, 2.4), ('poly', [(27, 24), (29, 24), (28, 22)])], soft=.4, line=False)
        s.mark(24, 20, (255, 80, 80)); s.mark(31, 20, (255, 80, 80))
    return s


def lich():
    s = Spr()
    robe, ice, bone, trim = ramp('#2a1f4a', 1.3, 1.1), ramp('#9ae8ff', 1.3, 1.2), ramp('#e8e4d8', .9), ramp('#9ab8ff', 1.2)
    s.piv.update(armL=(18, 28), armR=(38, 28), head=(28, 25), cape=(28, 26))
    with s.grp('cape'):
        s.part(ramp('#141c3a', 1.3), [('poly', [(16, 24), (40, 24), (50, 52), (42, 50), (36, 53), (28, 50), (20, 53), (14, 50), (6, 52)])], soft=2.5)
    with s.grp('armR'):   # ice staff
        s.part(ramp('#3a3050', 1.2), [('cap', 44, 53, 45, 10, 1)], soft=.6)
        s.part(ice, [('poly', [(45, 1), (49, 8), (45, 14), (41, 8)])], soft=1, gloss=1.4)
        s.part(robe, [('cap', 38, 28, 42, 34, 3.4)], soft=1.1)
        s.part(bone, [('ell', 44, 35.5, 2, 2)], soft=.6)
    with s.grp('body'):
        s.part(robe, [('poly', [(19, 25), (37, 25), (42, 50), (35, 51), (28, 50), (21, 51), (14, 50)])], soft=2.5, cast=1)
        s.part(ramp('#1a2448', 1.2), [('poly', [(25, 27), (31, 27), (32, 50), (24, 50)])], soft=.8)
        s.part(trim, [('poly', [(19.5, 25), (36.5, 25), (34, 29), (28, 31), (22, 29)])], soft=1, gloss=.8)
        s.part(bone, [('rect', 25, 32, 31, 33.2), ('rect', 25, 35, 31, 36.2), ('rect', 25, 38, 31, 39.2)], soft=.3, line=False)
        s.part(ice, [('poly', [(28, 41), (31, 44.5), (28, 48), (25, 44.5)])], sub=[('poly', [(28, 42.6), (29.6, 44.5), (28, 46.4), (26.4, 44.5)])], soft=.3, gloss=1.2, line=False)   # frost rune
        for sx in (-1, 1):   # ice spikes on the shoulders
            s.part(ice, [('poly', [(28 + sx * 7, 26), (28 + sx * 11, 18), (28 + sx * 10, 27)]), ('poly', [(28 + sx * 4, 25.5), (28 + sx * 6.5, 20), (28 + sx * 7, 26)])], soft=.4, gloss=1.2)
    with s.grp('armL'):
        s.part(robe, [('cap', 18, 28, 13, 34, 3.4)], soft=1.1)
        s.part(bone, [('ell', 12, 35.5, 2, 2)], soft=.6)
        s.part(ice, [('ell', 11, 31, 3.2, 3.2)], soft=1.2, gloss=1.2, line=False)
    with s.grp('head'):
        s.part(robe, [('chord', 28, 17, 11, 11, 180, 360), ('poly', [(17, 17), (21, 17), (21, 27), (16, 27)]), ('poly', [(35, 17), (39, 17), (40, 27), (35, 27)])],
               sub=[('ell', 28, 19.5, 7.5, 7)], soft=2, cast=2)
        s.part(bone, [('ell', 28, 20, 6.8, 6.4), ('rect', 24, 23, 32, 27)], soft=1.8)
        s.part(ramp('#1a1a2a', 1.2), [('ell', 25.3, 20, 1.9, 1.9), ('ell', 30.7, 20, 1.9, 1.9)], soft=.4, line=False)
        s.part(ice, [('poly', [(19, 9), (15, 0), (22, 7)]), ('poly', [(25.5, 7), (28, -1), (30.5, 7)]), ('poly', [(34, 7), (41, 0), (37, 9)]),
                     ('rect', 19, 8, 37, 10.5)], soft=.6, gloss=1.3)   # horned ice crown
        s.mark(25, 20, (120, 230, 255)); s.mark(30, 20, (120, 230, 255))
    for x, y, a in ((6, 20, 200), (50, 28, 180), (10, 44, 160), (48, 8, 220)):
        s.glow(x, y, (200, 245, 255), a)
    return s


def wyrm():
    s = Spr()
    scale, belly, wing, horn = ramp('#3a2a34', 1.3), ramp('#ff8a2a', 1.3, 1.2), ramp('#6a1a1a', 1.3), ramp('#e8dcc0', .9)
    s.piv.update(wingL=(24, 26), wingR=(34, 26), head=(16, 26), cape=(40, 42), legL=(24, 44), legR=(36, 44))
    with s.grp('wingR'):
        s.part(wing, [('poly', [(33, 27), (46, 4), (49, 13), (55, 12), (50, 24), (54, 27), (42, 34)])], soft=1.3)
    with s.grp('cape'):   # tail
        s.part(scale, [('poly', [(38, 40), (50, 46), (55, 40), (54, 50), (40, 50)])], soft=1.2)
    with s.grp('legR'):
        s.part(scale, [('cap', 36, 44, 37, 52, 2.4)], soft=.9)
    with s.grp('body'):
        s.part(scale, [('ell', 30, 38, 13, 10)], soft=3, cast=1)
        s.part(belly, [('ell', 26, 42, 8, 6)], soft=1.2, line=False)
        for y in (38, 41, 44):
            s.part(ramp('#ffd060', 1.2), [('rect', 20, y, 32, y + .8)], soft=.3, line=False)
        for i, x in enumerate((24, 29, 34, 39)):   # spines along the back
            s.part(horn, [('poly', [(x - 1.6, 29.5 + i * .6), (x + .8, 24 + i * .8), (x + 1.6, 30 + i * .6)])], soft=.3, gloss=.8)
    with s.grp('legL'):
        s.part(scale, [('cap', 23, 44, 21, 52, 2.4)], soft=.9)
    with s.grp('head'):
        s.part(scale, [('cap', 22, 32, 16, 26, 4)], soft=1.5)   # neck
        s.part(scale, [('ell', 14, 22, 7.5, 6.5), ('poly', [(8, 21), (1, 25), (3, 29), (10, 27)])], soft=2, cast=1)
        s.part(horn, [('poly', [(14, 17), (19, 8), (18, 17)]), ('poly', [(10, 17), (11, 10), (13, 17)])], soft=.5, gloss=1)
        s.part(ramp('#ff8a20', 1.2, 1.2), [('poly', [(2, 27), (0, 29), (3, 30)])], soft=.3, line=False, flat=True, bias=.2)
        s.mark(10, 21, (255, 230, 60)); s.mark(11, 21, (255, 230, 60))
    with s.grp('wingL'):
        s.part(wing, [('poly', [(25, 27), (16, 3), (13, 12), (7, 10), (11, 22), (5, 26), (19, 33)])], soft=1.3)
    for x, y, a in ((30, 12, 160), (42, 20, 140), (20, 50, 120)):
        s.glow(x, y, (255, 150, 60), a)
    return s


CREATURES = dict(wisp=wisp, wolf=wolf, guardian=guardian, drake=drake, skeleton=skeleton, lich=lich, wyrm=wyrm)
