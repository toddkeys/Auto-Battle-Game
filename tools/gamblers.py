"""Designs for the Gambler class (original characters) and the Glacier Warden (Frost Healer)."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import hem_trim, sparkle
from pixel import Spr, ramp

WHITE_DIE = ramp('#f6f2ea', .7)


def die(s, x, y, r, pips):
    s.part(WHITE_DIE, [('rect', x - r, y - r, x + r, y + r)], soft=.6, gloss=.8)
    for dx, dy in pips:
        s.mark(int(x + dx), int(y + dy), (40, 30, 40))


def cardshark():
    s = Spr()
    vest, shirt, red = ramp('#3a2a4a', 1.2), ramp('#f2eee6', .8), ramp('#c0283a')
    legs(s, ramp('#2a2430'), ramp('#3a2a2a'))
    torso(s, shirt, hem=44)
    s.part(vest, [('poly', [(21, 29), (25, 29), (28, 38), (31, 29), (35, 29), (35.5, 44), (20.5, 44)])], soft=1.2)
    s.part(red, [('poly', [(25.5, 28.5), (28, 30), (30.5, 28.5), (30.5, 31), (28, 30), (25.5, 31)])], soft=.4, flat=True)   # bow tie
    belt(s, ramp('#2a2430'), 40, P['gold'])
    arm(s, shirt, SKIN, (35, 30), (38.5, 36), (41, 40), r=2.6)
    arm(s, shirt, SKIN, (21, 30), (17.5, 34), (15, 37), r=2.6)
    with s.grp('armL'):   # a fan of cards
        for i, (dx, rot) in enumerate(((-4, -.5), (-1.5, -.2), (1, .1))):
            s.part(ramp('#fbf8f0', .7), [('poly', [(14 + dx, 36), (17 + dx, 35), (18.5 + dx + rot * 4, 28), (15.5 + dx + rot * 4, 29)])], soft=.5)
        s.mark(15, 32, (200, 30, 50)); s.mark(13, 33, (30, 30, 30))
    head(s)
    bangs(s, ramp('#2a2228', 1.2), 'swept', shine=10)
    s.part(ramp('#2a2430', 1.3), [('rect', 20, 3, 36, 12), ('ell', 28, 12.5, 12.5, 2.2)], soft=1, gloss=.6, cast=2)   # top hat
    s.part(red, [('rect', 20, 9.5, 36, 11.2)], soft=.4, cast=1)
    face(s, '#c03050', 'smile')
    return s


def fortuneteller():
    s = Spr()
    robe, scarf, gold = ramp('#8a3a8a', 1.2, 1.1), ramp('#e05aa0', 1.1), P['gold']
    back_hair(s, ramp('#3a1a3a', 1.2), 38, 12)
    legs(s, robe, ramp('#4a2040'), robe=True)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, gold, 47.8)
    for x in (22, 26, 30, 34):   # coins on the sash
        s.part(gold, [('ell', x, 39, 1.3, 1.3)], soft=.4, gloss=1, line=False)
    arm(s, robe, SKIN, (35, 30), (38.5, 35), (41, 32.5), r=3.3)
    arm(s, robe, SKIN, (21, 30), (17.5, 35), (15, 38), r=3.3)
    with s.grp('weapon'):   # a big die balanced over the raised hand
        die(s, 42, 27, 3.2, [(-1.5, -1.5), (0, 0), (1.5, 1.5)])
    die(s, 13.5, 34, 2.4, [(0, 0)])
    head(s)
    bangs(s, ramp('#3a1a3a', 1.2), 'long', shine=10)
    s.part(scarf, [('chord', 28, 15, 12.5, 9, 180, 360), ('rect', 15.5, 14, 40.5, 15.5)], soft=1, cast=2)   # head scarf
    for x in (19, 24, 29, 34):
        s.part(gold, [('ell', x, 16, .9, .9)], soft=.3, gloss=1, line=False)
    face(s, '#d06aa0', 'smile')
    for x, y in ((8, 24), (50, 18)):
        sparkle(s, x, y, (255, 220, 120))
    return s


def highroller():
    s = Spr()
    coat, gold, wine = ramp('#e8c050', 1.1), P['gold'], ramp('#6a1a3a', 1.2)
    cape(s, wine, 1.2, 52)
    legs(s, ramp('#3a2a3a'), ramp('#2a1a20'))
    torso(s, coat, hem=46)
    s.part(wine, [('poly', [(25, 29), (31, 29), (31, 46), (25, 46)])], soft=.8)
    for y in (32, 36, 40):
        s.part(gold, [('ell', 28, y, 1, 1)], soft=.3, gloss=1, line=False)
    belt(s, wine, 41, gold)
    arm(s, coat, SKIN, (35, 30), (39, 36), (42, 40), r=3)
    arm(s, coat, SKIN, (21, 30), (17.5, 34), (15, 37), r=3)
    with s.grp('armL'):   # two golden dice
        s.part(gold, [('rect', 9, 31, 15, 37), ('rect', 14, 26, 19, 31)], soft=.8, gloss=1.2)
        for x, y in ((11, 33), (13, 35), (16, 28)):
            s.mark(x, y, (90, 40, 20))
    head(s)
    bangs(s, ramp('#f0e0b0', 1.0), 'swept', shine=10)
    s.part(wine, [('poly', [(16, 14), (40, 14), (38, 9), (34, 4), (22, 4), (18, 9)])], soft=1.2, gloss=.6, cast=2)   # feathered cap
    s.part(ramp('#f8f4ff', .7), [('poly', [(34, 5), (46, 0), (44, 4), (38, 8)])], soft=.8)
    s.part(gold, [('rect', 16, 12.5, 40, 14.5)], soft=.4, gloss=1)
    face(s, '#d0a020', 'smile')
    s.part(gold, [('ell', 31, 21, 2.2, 2.2)], sub=[('ell', 31, 21, 1.4, 1.4)], soft=.3, gloss=1, line=False)   # monocle
    for x, y in ((6, 20), (8, 44), (50, 22)):
        sparkle(s, x, y, (255, 230, 140))
    return s


def glacierwarden():
    s = Spr()
    parka, fur, ice = ramp('#6aa0d0', 1.2), ramp('#f4f8fb', .7), ramp('#a8ecff', 1.2, 1.1)
    legs(s, ramp('#3a5070'), ramp('#2a3a50'))
    torso(s, parka, hem=46)
    hem_trim(s, fur, 44)
    belt(s, ramp('#2a3a50'), 39, ice)
    staff(s, ramp('#8ab0c8', 1.2), 42, 52, 43, 14, .9)
    s.part(ice, [('poly', [(43, 5), (46, 11), (43, 16), (40, 11)])], soft=.8, gloss=1.4)
    arm(s, parka, SKIN, (35, 30), (39, 36), (42.5, 40), r=3.1, glove=fur)
    arm(s, parka, SKIN, (21, 30), (18, 35), (17, 39), r=3.1, glove=fur)
    s.part(ice, [('poly', [(6, 30), (19, 28), (20, 47), (13, 52), (6, 46)])], soft=1.5, gloss=1.2)   # slab of ice as a shield
    s.part(ramp('#e8fbff', .8), [('poly', [(9, 32), (12, 31.5), (10, 44)])], soft=.4, line=False, flat=True, bias=.25)
    head(s)
    bangs(s, ramp('#e0eef8', 1.0), 'neat', shine=10)
    s.part(fur, [('chord', 28, 17, 13, 12.5, 180, 360), ('poly', [(15, 17), (19, 17), (19.5, 29), (14, 30)]),
                 ('poly', [(37, 17), (41, 17), (42, 30), (36.5, 29)])], sub=[('ell', 28, 19.5, 9.5, 8.5)], soft=2.5, cast=2)
    face(s, '#3a90d0')
    sparkle(s, 50, 28, (220, 245, 255))
    return s


GAMBLERS = dict(cardshark=cardshark, fortuneteller=fortuneteller, highroller=highroller, glacierwarden=glacierwarden)
