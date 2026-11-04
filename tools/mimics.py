"""Mimic and Mesmer classes (original characters): spell thieves and mind-benders."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import sparkle, hem_trim
from pixel import Spr, ramp


def mirrormage():
    # a young mage girl in mint-and-silver robes, silver bob hair, holding up a round hand mirror that glints
    s = Spr()
    robe, trim, hair = ramp('#3aa888', 1.1), ramp('#dfe6ee', 1.1), ramp('#c8d0e0', 1.15)
    cape(s, ramp('#1e6a5a', 1.2), .8, 50)
    back_hair(s, hair, 27, 11)
    legs(s, robe, ramp('#2a3a40'), robe=True)
    torso(s, robe, 'robe', hem=49)
    hem_trim(s, trim)
    with s.grp('body'):
        s.part(trim, [('poly', [(24.5, 28.5), (31.5, 28.5), (28, 34)])], soft=.6)   # collar
        s.part(ramp('#7fffd0', 1.2), [('ell', 28, 31.5, 1.2, 1.2)], soft=.2, gloss=1.5, line=False)
    belt(s, ramp('#1e4a44'), 38, trim)
    with s.grp('weapon'):   # hand mirror
        s.part(P['gold'], [('cap', 42, 41, 44, 34, .8)], soft=.4, gloss=1.2)
        s.part(P['gold'], [('ell', 45, 29.5, 4.4, 5)], soft=.8, gloss=1.4)
        s.part(ramp('#bff8ff', .9), [('ell', 45, 29.5, 3.2, 3.8)], soft=.5, gloss=1.8, line=False)
        s.part(ramp('#ffffff', .4), [('cap', 43.6, 27.8, 45, 26.8, .45)], soft=.1, line=False, flat=True, bias=.5)
    arm(s, robe, SKIN, (35, 30), (38.5, 35.5), (42.5, 39), r=2.7)
    arm(s, robe, SKIN, (21, 30), (18.5, 35), (18.5, 40), r=2.7)
    head(s)
    bangs(s, hair, 'neat', shine=10)
    s.part(ramp('#3aa888', 1.1), [('poly', [(36, 12), (40, 9), (39, 14)])], soft=.4)   # hair ribbon
    face(s, '#2ab89a')
    for x, y in ((50, 24), (49, 35)):
        sparkle(s, x, y, (190, 255, 240))
    return s


def maskedmagus():
    # a tall spell-thief: deep teal hooded cloak with gold trim, a golden mask with two great sweeping horns
    # and glowing eyes, a staff crowned with a crescent mirror, stolen magic swirling at the off hand
    s = Spr()
    cloak, inner, gold, glow = ramp('#1e5a52', 1.3), ramp('#123832', 1.3), P['gold'], ramp('#7fffd0', 1.3)
    cape(s, cloak, 1.6, 54)
    with s.grp('cape'):
        s.part(gold, [('cap', 12, 52.5, 44, 52.5, .7)], soft=.3, gloss=1.2)
    legs(s, inner, ramp('#1a2422'), robe=True)
    torso(s, cloak, 'robe', hem=50)
    hem_trim(s, gold, 48.5)
    with s.grp('body'):
        s.part(inner, [('poly', [(25, 29), (31, 29), (32, 49), (24, 49)])], soft=1)
        for y in (32, 37, 42):
            s.part(gold, [('poly', [(26.5, y), (29.5, y), (28, y + 2.5)])], soft=.3, gloss=1.2)
        s.part(gold, [('poly', [(20.5, 28), (35.5, 28), (34, 31.5), (28, 33), (22, 31.5)])], soft=.8, gloss=1.3)   # mantle clasp
    belt(s, ramp('#2a1a10'), 39, gold)
    with s.grp('weapon'):   # staff with a crescent mirror
        s.part(ramp('#3a2a20', 1.2), [('cap', 41, 50, 44, 11, .9)], soft=.5, gloss=.8)
        s.part(gold, [('ell', 44.3, 7.5, 5, 5)], sub=[('ell', 46, 6.5, 4, 4.4)], soft=.5, gloss=1.4)
        s.part(glow, [('ell', 43.2, 8.3, 1.6, 1.6)], soft=.2, gloss=1.6, line=False)
    arm(s, cloak, cloak, (35, 30), (39, 36), (42.5, 39), r=3, glove=ramp('#2a1a10'))
    arm(s, cloak, cloak, (21, 30), (17, 33), (13, 31), r=3, glove=ramp('#2a1a10'))   # off hand raised
    with s.grp('fx'):   # stolen magic swirling in the off hand
        s.part(glow, [('ell', 11, 28, 3.2, 3.2)], sub=[('ell', 11, 28, 1.8, 1.8)], soft=.3, gloss=1.4, line=False)
    head(s, ramp('#1a1a22'))
    with s.grp('head'):
        s.part(cloak, [('ell', 28, 16, 12.5, 12), ('rect', 15.5, 16, 40.5, 27)], sub=[('ell', 28, 20, 9, 8.5)], soft=2, cast=2)   # hood
        s.part(gold, [('poly', [(19, 14), (37, 14), (36, 24), (31, 27.5), (25, 27.5), (20, 24)])], soft=1.2, gloss=1.5)   # mask
        s.part(gold, [('poly', [(20, 15), (13, 8), (8, -1), (14, 3), (17, 9), (23, 13)]),
                      ('poly', [(36, 15), (43, 8), (48, -1), (42, 3), (39, 9), (33, 13)])], soft=.8, gloss=1.3)   # sweeping horns
        s.part(inner, [('poly', [(21.5, 18.5), (26, 18.5), (25.5, 21), (22, 21)]), ('poly', [(30, 18.5), (34.5, 18.5), (34, 21), (30.5, 21)])], soft=.2)
    for x0 in (22, 31):   # glowing eyes
        for x in range(x0, x0 + 3):
            s.mark(x, 19, (140, 255, 220))
    for x, y in ((6, 22), (16, 25), (52, 14)):
        sparkle(s, x, y, (150, 255, 220))
    return s


def puppeteer():
    # a jester-like puppet master: violet-and-black diamond coat, a two-point cap with bells, a crossbar
    # in one hand with strings down to a little wooden puppet
    s = Spr()
    vio, blk, gold, wood = ramp('#7a3aaa', 1.2), ramp('#24182e', 1.2), P['gold'], P['wood']
    cape(s, blk, 1.0, 50)
    legs(s, vio, blk)
    torso(s, blk, hem=45)
    with s.grp('body'):
        for x, y in ((23.5, 31), (31.5, 31), (27.5, 36), (23.5, 41), (31.5, 41)):   # diamond pattern
            s.part(vio, [('poly', [(x, y - 3), (x + 3, y), (x, y + 3), (x - 3, y)])], soft=.4, line=False)
        s.part(ramp('#f0e6f8', .8), [('poly', [(20, 28), (36, 28), (33, 32), (28, 30.5), (23, 32)])], soft=.6)   # ruff collar
    belt(s, gold, 40)
    with s.grp('weapon'):   # crossbar, strings and a dangling puppet
        s.part(wood, [('cap', 38, 27, 48, 27, .8)], soft=.4)
        for x in (39, 47):
            s.part(ramp('#f0e0ff', .4), [('cap', x, 27.5, 43 + (x - 43) * .3, 40, .25)], soft=0, line=False, flat=True, bias=.4)
        s.part(wood, [('ell', 43, 40, 2, 2), ('rect', 41.5, 42, 44.5, 47), ('cap', 41.8, 47, 41, 51, .6), ('cap', 44.2, 47, 45, 51, .6)], soft=.6, gloss=.6)
        s.part(ramp('#c03a5a'), [('rect', 41.5, 43, 44.5, 45)], soft=.3, line=False)
    arm(s, blk, SKIN, (35, 30), (39, 28), (42.5, 26.5), r=2.6, glove=ramp('#f0e6f8', .8))
    arm(s, blk, SKIN, (21, 30), (18.5, 35), (18.5, 40), r=2.6, glove=ramp('#f0e6f8', .8))
    head(s)
    bangs(s, ramp('#3a2a4a', 1.2), 'swept', shine=9)
    with s.grp('head'):   # two-point jester cap with bells
        s.part(vio, [('chord', 28, 15, 12, 7, 180, 360), ('poly', [(17, 13), (8, 6), (6, 14), (14, 15)]), ('poly', [(39, 13), (47, 4), (50, 12), (42, 15)])], soft=1.2, cast=2)
        s.part(blk, [('poly', [(28, 8.5), (39, 13), (47, 4), (38, 9)])], soft=.6, line=False)
        s.part(gold, [('ell', 6, 14.5, 1.6, 1.6), ('ell', 50, 12.5, 1.6, 1.6)], soft=.3, gloss=1.5)
    face(s, '#b05ae0', 'smile')
    s.mark(20, 23, (190, 60, 120)); s.mark(31, 23, (190, 60, 120))   # painted cheek diamonds
    return s


def rimedragoness():
    # an ice dragon maiden: pale-blue hair, curved crystal horns, frost-white dress with icy scale armour,
    # translucent dragon wings and a scaly tail, a swirling frost orb in her hand
    s = Spr()
    ice, scale, hair, dress, wing = ramp('#9fe4ff', 1.15), ramp('#4a8ac8', 1.25), ramp('#4aa0e8', 1.25), ramp('#eef6ff', .8), ramp('#7fc8f0', 1.0)
    with s.grp('cape'):   # dragon wings and tail
        for d in (1, -1):
            pts = [(28 + 6 * d, 30), (28 + 18 * d, 14), (28 + 26 * d, 16), (28 + 22 * d, 24), (28 + 25 * d, 30), (28 + 18 * d, 33), (28 + 17 * d, 39)]
            s.part(wing, [('poly', pts)], soft=1.2, gloss=.6)
            s.part(scale, [('cap', 28 + 6 * d, 30, 28 + 18 * d, 14, .8), ('cap', 28 + 18 * d, 14, 28 + 26 * d, 16, .6)], soft=.4, gloss=1)
        s.part(scale, [('line', [(33, 46), (42, 50), (48, 47), (51, 42)], 1.6)], soft=.8, gloss=.8)
        s.part(ice, [('poly', [(50, 42), (54, 38), (52.5, 44)])], soft=.3, gloss=1.4)
    back_hair(s, hair, 33, 11.5)
    legs(s, dress, scale, robe=True)
    torso(s, dress, 'robe', hem=49)
    hem_trim(s, ice)
    with s.grp('body'):
        s.part(scale, [('poly', [(22, 29), (34, 29), (33.5, 38), (28, 40), (22.5, 38)])], soft=1, gloss=1.2)   # scale bodice
        for y in (31.5, 34.5):
            for x in (25, 28, 31):
                s.part(ice, [('chord', x, y, 1.5, 1.4, 0, 180)], soft=.2, gloss=1.2, line=False)
    belt(s, ice, 39)
    with s.grp('weapon'):   # frost orb
        s.part(ice, [('ell', 44.5, 33.5, 3.4, 3.4)], soft=.6, gloss=1.6)
        s.part(ramp('#ffffff', .4), [('ell', 43.5, 32.5, 1.2, 1.2)], soft=.2, line=False, flat=True, bias=.5)
    arm(s, dress, SKIN, (35, 30), (39, 35), (43, 37.5), r=2.6, glove=ramp('#bfe8ff'))
    arm(s, dress, SKIN, (21, 30), (18.5, 35), (18.5, 40), r=2.6, glove=ramp('#bfe8ff'))
    head(s)
    bangs(s, hair, 'swept', shine=11)
    with s.grp('head'):   # curved crystal horns
        s.part(ice, [('poly', [(19, 12), (14, 5), (11, -1), (16, 3), (21, 9)]), ('poly', [(37, 12), (42, 5), (45, -1), (40, 3), (35, 9)])], soft=.6, gloss=1.5)
        s.part(scale, [('poly', [(26.5, 11), (28, 8), (29.5, 11), (28, 13)])], soft=.3, gloss=1.4)   # brow gem
    face(s, '#3ab0f0')
    for x, y in ((6, 10), (50, 28), (8, 40)):
        sparkle(s, x, y, (210, 245, 255))
    return s


MIMICS = dict(mirrormage=mirrormage, maskedmagus=maskedmagus, puppeteer=puppeteer, rimedragoness=rimedragoness)
