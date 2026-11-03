"""Designs for the Samurai class (original characters)."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import sparkle
from pixel import Spr, ramp


def katana(s, blade, hilt, x0=41, y0=41, x1=47, y1=16):
    sword(s, blade, hilt, x0=x0, y0=y0, x1=x1, y1=y1, w=1.2, guard=2.2)


def ronin():
    s = Spr()
    kimono, sash, straw = ramp('#3a3a52', 1.2), ramp('#8a2a2a'), ramp('#c8a868', 1.1)
    legs(s, ramp('#2a2a3a'), ramp('#4a3a2a'))
    torso(s, kimono, hem=46)
    s.part(ramp('#e8e2d0', .8), [('poly', [(25, 28), (31, 28), (28, 35)])], soft=.6)   # under-robe collar
    belt(s, sash, 38)
    katana(s, ramp('#dfe6f0', 1.3), ramp('#2a2a30', 1.2))
    arm(s, kimono, SKIN, (35, 30), (38.5, 36), (41, 40), r=3)
    arm(s, kimono, SKIN, (21, 30), (18.5, 35), (19, 39), r=3)
    s.part(ramp('#2a2a30', 1.2), [('cap', 18, 40, 30, 41.5, 1)], soft=.5)   # sheathed short sword
    head(s)
    bangs(s, ramp('#2a2228', 1.2), 'neat', shine=10)   # neat, so no spikes poke through the hat
    s.part(straw, [('poly', [(10, 14.5), (28, 3), (46, 14.5), (43, 16), (28, 13), (13, 16)])], soft=1.5, cast=2)   # straw hat
    s.part(ramp('#9a7a40'), [('poly', [(27, 4), (29, 4), (28.5, 13), (27.5, 13)])], soft=.4, line=False)
    face(s, '#6a5a8a', 'smile')
    return s


def kensei():
    s = Spr()
    gi, hakama, red = ramp('#efe8dc', .8), ramp('#2a2a3a', 1.2), ramp('#b02a30')
    legs(s, hakama, ramp('#3a2a22'), robe=True)
    s.part(hakama, [('poly', [(20, 38), (36, 38), (39, 50), (17, 50)])], soft=1.5, cast=1)   # wide hakama
    torso(s, gi, hem=40)
    s.part(red, [('poly', [(22, 29), (26, 28.5), (33, 39), (30, 39.5)])], soft=.6)
    belt(s, red, 38)
    katana(s, ramp('#dfe6f0', 1.3), ramp('#3a2a2a', 1.2), x0=42, y0=40, x1=50, y1=18)
    arm(s, gi, SKIN, (35, 30), (39, 35.5), (42, 39), r=2.9)
    with s.grp('armL'):   # second blade held low
        s.part(ramp('#dfe6f0', 1.3), [('poly', [(15, 41), (16.5, 40), (8, 50), (7.5, 49)])], soft=.5, gloss=1)
    arm(s, gi, SKIN, (21, 30), (18, 35.5), (16.5, 39.5), r=2.9)
    head(s)
    bangs(s, ramp('#1e1a20', 1.2), 'swept', shine=10)
    s.part(ramp('#1e1a20', 1.2), [('ell', 28, 6.5, 3.2, 2.6), ('rect', 26.8, 7, 29.2, 10)], soft=1)   # topknot
    s.part(red, [('rect', 17, 12, 39, 13.6)], soft=.5, cast=1)   # headband
    face(s, '#8a3a30', 'smile')
    return s


def shogun():
    # warlord in black-and-crimson great armour: tiered shoulder plates, a tall golden crest, a long no-dachi
    s = Spr()
    black, crimson, gold, lace = ramp('#26222c', 1.3), ramp('#b0202c', 1.2, 1.1), P['gold'], ramp('#e04a3a', 1.1)
    cape(s, crimson, 1.5, 53)   # war cloak
    with s.grp('cape'):
        s.part(gold, [('poly', [(12, 51.5), (44, 51.5), (44.5, 52.8), (28, 54), (11.5, 52.8)])], soft=.4, gloss=1)
    legs(s, black, ramp('#16141a'))
    torso(s, black, hem=42)
    with s.grp('body'):
        for y in (30.5, 33.5, 36.5, 39.5):   # laced plates
            s.part(lace, [('rect', 20.5, y, 35.5, y + .7)], soft=.2, line=False, flat=True, bias=.1)
        s.part(gold, [('ell', 28, 34, 2.4, 2.4)], sub=[('ell', 28, 34, 1.4, 1.4)], soft=.3, gloss=1.2)   # family crest
        for k, y in enumerate((41, 44.5)):   # tiered armour skirt
            s.part(crimson if k else black, [('poly', [(19.5 - k, y), (36.5 + k, y), (37.5 + k, y + 4), (18.5 - k, y + 4)])], soft=.8, gloss=.5)
            s.part(gold, [('rect', 19 - k, y + 3.3, 37 + k, y + 4)], soft=.2, line=False)
    belt(s, crimson, 41, gold)
    sword(s, ramp('#eef2fa', 1.4), ramp('#2a1e1e'), x0=42, y0=43, x1=49, y1=4, w=1.4, guard=3)   # no-dachi
    arm(s, black, SKIN, (35, 30), (39, 36), (42, 41), r=3.1, glove=black)
    arm(s, black, SKIN, (21, 30), (18, 35), (17.5, 39.5), r=3.1, glove=black)
    for side in (1, -1):   # big tiered shoulder plates
        x = 28 + side * 10
        for k in range(3):
            y = 28 + k * 2.6
            s.part(crimson if k % 2 == 0 else black, [('poly', [(x - 5, y), (x + 5, y), (x + 5.5 * side + side * .5, y + 3), (x - 5.5 * side - side * .5, y + 3)])], soft=.8, gloss=.6, cast=1)
        s.part(gold, [('rect', x - 5, 28, x + 5, 28.8)], soft=.2, line=False)
    head(s)
    bangs(s, ramp('#1e1a20', 1.2), 'neat', shine=10)
    s.part(black, [('chord', 28, 16, 13, 11, 180, 360)], soft=2, gloss=1, cast=2)   # helmet bowl
    s.part(crimson, [('poly', [(14, 15), (20, 15), (18.5, 22), (12, 20.5)]), ('poly', [(42, 15), (36, 15), (37.5, 22), (44, 20.5)])], soft=1, gloss=.6)   # flared neck guard
    s.part(gold, [('rect', 15.5, 14, 40.5, 15.6)], soft=.4, gloss=1)
    s.part(gold, [('poly', [(28, 11), (17, 1), (13, -1), (19, 6), (26, 12)]), ('poly', [(28, 11), (39, 1), (43, -1), (37, 6), (30, 12)])], soft=.5, gloss=1.4)   # tall crest horns
    s.part(crimson, [('ell', 28, 11, 2, 2)], soft=.4, gloss=1)
    face(s, '#c03030')
    for x, y in ((7, 22), (51, 26), (9, 44)):
        sparkle(s, x, y, (255, 210, 140))
    return s


SAMURAI = dict(ronin=ronin, kensei=kensei, shogun=shogun)
