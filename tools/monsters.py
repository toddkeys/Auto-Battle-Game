"""Original monster sprites for monster/boss rounds (all face down-left)."""
from pixel import Spr, ramp

WHITE = (255, 255, 255)
INK = (34, 24, 30)
BLUSH = (255, 140, 150)


def blob_eyes(s, xs, y, iris=INK, h=3):
    for x in xs:
        for dy in range(h):
            s.mark(x, y + dy, iris); s.mark(x + 1, y + dy, iris)
        s.mark(x, y, WHITE)


def mossling():
    s = Spr()
    moss, leaf, thorn = ramp('#3f7a34', 1.2, 1.1), ramp('#2f6a2a', 1.2), ramp('#6a3a4a', 1.2)
    s.piv['head'] = (28, 37)
    with s.grp('head'):
        s.part(leaf, [('cap', 28, 37, 28.5, 30, .8)], soft=.5)
        s.part(leaf, [('poly', [(28.5, 31), (34, 26.5), (38, 28), (33, 32.5)]),
                      ('poly', [(28, 31.5), (22, 27.5), (19, 29.5), (24.5, 33)])], soft=.8)
    s.group = 'body'
    s.part(moss, [('ell', 28, 45, 13.5, 9.5), ('rect', 14.5, 45, 41.5, 53.5)],
           sub=[('ell', 18, 54, 2.5, 1.2), ('ell', 28, 54.2, 2.5, 1.2), ('ell', 38, 54, 2.5, 1.2)], soft=2.5)
    s.part(ramp('#2a5a24'), [('ell', 35, 40, 2, 1.4), ('ell', 19, 47, 1.6, 1.2), ('ell', 37, 49, 1.4, 1)], soft=.5, line=False)
    for x, y, d in ((15, 42, -1), (41, 42, 1), (20, 37, -1), (36, 37, 1), (28, 35.5, 0)):   # thorns
        s.part(thorn, [('poly', [(x - 1.2, y + 1), (x + d * 2.2, y - 3), (x + 1.2, y + 1)])], soft=.3)
    blob_eyes(s, (22, 30), 43)
    for x in (19, 20, 33, 34):
        s.mark(x, 47, BLUSH)
    s.mark(26, 48, INK); s.mark(27, 49, INK); s.mark(28, 48, INK)
    return s


def shroomkin():
    s = Spr()
    stem, cap, spot = ramp('#d8ccb0', .9), ramp('#6a2a8a', 1.2, 1.1), ramp('#a8ff6a', 1.2, 1.2)
    s.piv.update(legL=(24, 47), legR=(32, 47), head=(28, 40))
    with s.grp('legL'):
        s.part(stem, [('ell', 24, 51.5, 3.2, 2)], soft=.8)
    with s.grp('legR'):
        s.part(stem, [('ell', 32, 51.5, 3.2, 2)], soft=.8)
    s.group = 'body'
    s.part(stem, [('cap', 21, 43, 18, 46, 1.3), ('cap', 35, 43, 38, 46, 1.3)], soft=.6)
    s.part(stem, [('ell', 28, 44, 8, 8)], soft=2)
    s.group = 'head'
    s.part(cap, [('chord', 28, 34, 15.5, 12, 180, 360), ('ell', 28, 34, 15.5, 3.2)], soft=2.5, cast=2)
    s.part(spot, [('ell', 21, 28, 2.4, 1.7), ('ell', 30, 25.5, 2.8, 2), ('ell', 37, 31, 1.8, 1.3), ('ell', 16.5, 33, 1.4, 1)],
           soft=.6, line=False, gloss=1)
    s.group = 'body'
    blob_eyes(s, (24, 30), 41, iris=(60, 20, 80))
    for x, y, a in ((14, 26, 170), (42, 24, 150), (22, 20, 130)):
        s.glow(x, y, (170, 255, 120), a)
    s.mark(27, 46, INK); s.mark(28, 46, INK)
    for x in (22, 33):
        s.mark(x, 44, BLUSH)
    return s


def emberbat():
    s = Spr()
    body, wing, ember = ramp('#2a1a22', 1.2), ramp('#c84a1a', 1.2, 1.1), ramp('#ffb03a', 1.3, 1.3)
    left = [(22, 28), (8, 19), (10, 25), (5, 29), (12, 30), (9, 36), (21, 34)]
    s.piv.update(wingL=(22, 29), wingR=(34, 29))
    inner = [(22, 29), (11, 22), (12, 26), (9, 29), (14, 30), (12, 34), (21, 32.5)]
    with s.grp('wingL'):
        s.part(wing, [('poly', left)], soft=1.2)
        s.part(ember, [('poly', inner)], soft=.8, line=False)   # fire inside the wing
    with s.grp('wingR'):
        s.part(wing, [('poly', [(56 - x, y) for x, y in left])], soft=1.2)
        s.part(ember, [('poly', [(56 - x, y) for x, y in inner])], soft=.8, line=False)
    s.group = 'body'
    s.part(body, [('poly', [(23, 26), (21.5, 17.5), (26.5, 23)]), ('poly', [(33, 26), (34.5, 17.5), (29.5, 23)])], soft=.8)
    s.part(body, [('ell', 28, 30, 7.5, 8)], soft=2)
    s.part(ember, [('ell', 28, 35.5, 3.5, 3)], soft=1.2, gloss=1, line=False)
    for x in (24, 30):
        s.mark(x, 27, (255, 230, 90)); s.mark(x + 1, 27, (255, 230, 90)); s.mark(x, 28, (255, 160, 40)); s.mark(x + 1, 28, (255, 160, 40))
    s.mark(26, 30, WHITE); s.mark(29, 30, WHITE)
    for x, y, a in ((24, 41, 220), (31, 44, 160), (27, 47, 110), (34, 39, 200)):
        s.glow(x, y, (255, 150, 60), a)
    return s


def golem():
    s = Spr()
    rock, moss, core = ramp('#3e3a40', 1.3), ramp('#ff6a2a', 1.3, 1.2), ramp('#ff8a2a', 1.3, 1.2)
    crystal = ramp('#ff9a4a', 1.3, 1.2)
    s.part(rock, [('poly', [(17, 42), (25, 42), (25.5, 53), (16, 53)]), ('poly', [(31, 42), (39, 42), (40, 53), (30.5, 53)])], soft=1.5)
    s.piv.update(armL=(13, 27), armR=(43, 27), head=(28, 25))
    s.group = 'body'
    with s.grp('armL'):
        s.part(rock, [('cap', 12, 30, 9, 43, 4.5)], soft=2)
    with s.grp('armR'):
        s.part(rock, [('cap', 44, 30, 47, 43, 4.5)], soft=2)
    s.part(rock, [('ell', 28, 34, 15, 11.5)], soft=3, cast=1)
    for g, x in (('armL', 9), ('armR', 47)):
        with s.grp(g):
            s.part(rock, [('ell', x, 46, 4.8, 4.2)], soft=1.5, gloss=.3)
    for g, x in (('armL', 13), ('armR', 43)):
        with s.grp(g):
            s.part(rock, [('ell', x, 27, 7.5, 6)], soft=2, cast=1)
            for dx, h in ((-4, 7), (0, 10), (4, 6)):   # glowing crystal shards
                s.part(crystal, [('poly', [(x + dx - 1.6, 24), (x + dx, 24 - h), (x + dx + 1.6, 24)])], soft=.4, gloss=1.3)
    s.part(moss, [('line', [(18, 30), (21, 34), (19, 39)], .45), ('line', [(39, 31), (36, 36), (38, 40)], .45)], soft=.2, line=False, flat=True, bias=.3)   # magma veins
    with s.grp('head'):
        s.part(rock, [('ell', 28, 19, 8.5, 7)], soft=2.5, cast=1)
    for x in (24, 25, 30, 31):  # eyes: marks attach to the head part just drawn
        s.mark(x, 19, (255, 200, 80))
    for x in (24, 31):
        s.mark(x, 20, (255, 120, 40))
    s.part(core, [('ell', 28, 34, 4, 4)], soft=1.5, gloss=1.5, line=False)
    s.part(core, [('line', [(24, 34), (20, 31), (18, 33)], .5), ('line', [(32, 35), (36, 38), (37, 36)], .5)],
           soft=.3, line=False, flat=True, bias=.25, thr=.3)
    for x, y in ((28, 28), (22, 37), (34, 31)):
        s.glow(x, y, (255, 170, 80), 140)
    return s


MONSTERS = dict(mossling=mossling, shroomkin=shroomkin, emberbat=emberbat, golem=golem)
