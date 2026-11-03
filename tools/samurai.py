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
    bangs(s, ramp('#2a2228', 1.2), 'spiky', shine=10)
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
    s = Spr()
    lacq, gold, dark = ramp('#a8202a', 1.2, 1.1), P['gold'], ramp('#2a2228', 1.3)
    cape(s, ramp('#3a1a2a', 1.2), 1.2, 52)
    legs(s, dark, ramp('#1e1a1e'))
    torso(s, lacq, hem=45)
    for y in (32, 36, 40):   # laced armour plates
        s.part(gold, [('rect', 20.5, y, 35.5, y + .8)], soft=.3, flat=True, bias=.05, line=False)
    s.part(lacq, [('poly', [(17, 29), (23, 28.5), (24, 36), (16, 37)]), ('poly', [(39, 29), (33, 28.5), (32, 36), (40, 37)])], soft=1.2, gloss=.6, cast=1)   # shoulder guards
    belt(s, dark, 41, gold)
    katana(s, ramp('#eef2fa', 1.3), gold, x0=42, y0=42, x1=50, y1=12)
    arm(s, dark, SKIN, (35, 30), (39, 36), (42, 41), r=3, glove=dark)
    arm(s, dark, SKIN, (21, 30), (18, 35), (17.5, 39.5), r=3, glove=dark)
    head(s)
    bangs(s, ramp('#1e1a20', 1.2), 'neat', shine=10)
    s.part(dark, [('chord', 28, 16.5, 12.5, 10.5, 180, 360), ('poly', [(15, 15), (20, 15), (19.5, 23), (13, 21)]), ('poly', [(41, 15), (36, 15), (36.5, 23), (43, 21)])],
           soft=2, gloss=.8, cast=2)   # kabuto
    s.part(gold, [('poly', [(14, 4), (20, 11), (28, 12.5), (36, 11), (42, 4), (38, 9.5), (28, 10.5), (18, 9.5)])], soft=.6, gloss=1.2)   # crescent crest
    s.part(gold, [('rect', 16, 13.6, 40, 15.2)], soft=.4, gloss=.8)
    face(s, '#a03030', 'smile')
    for x, y in ((8, 20), (50, 30)):
        sparkle(s, x, y, (255, 220, 140))
    return s


SAMURAI = dict(ronin=ronin, kensei=kensei, shogun=shogun)
