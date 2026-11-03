"""Designs for the 4-cost units (original characters), one per class."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import hem_trim, ring, sparkle
from pixel import Spr, ramp


def star(s, rp, cx, cy, r, ri=None):
    import math
    ri = ri or r * .42
    pts = [(cx + math.cos(math.pi * (-.5 + i / 5)) * (r if i % 2 == 0 else ri),
            cy + math.sin(math.pi * (-.5 + i / 5)) * (r if i % 2 == 0 else ri)) for i in range(10)]
    s.part(rp, [('poly', pts)], soft=.5, gloss=1, line=False)


def starwarden():
    s = Spr()
    plate, navy, gold = ramp('#3a4f9a', 1.2, 1.1), ramp('#1f2a5a', 1.2), P['gold']
    cape(s, navy, 1.25, 52)
    legs(s, plate, ramp('#22305e', 1.2))
    torso(s, plate, hem=44)
    s.part(gold, [('poly', [(21, 29), (35, 29), (33.5, 34), (28, 36), (22.5, 34)])], soft=1, gloss=.8)
    belt(s, gold, 39, ramp('#7fd4ff', 1.2))
    sword(s, ramp('#e6f0ff', 1.2), gold, x0=42, y0=43, x1=48, y1=16, w=1.9, guard=4.5)
    arm(s, plate, plate, (35, 30), (39, 36), (42, 41), r=2.9)
    s.part(gold, [('chord', 36, 31, 5.4, 4.6, 180, 360)], soft=1.2, gloss=1, cast=1)
    arm(s, plate, plate, (21, 30), (18.5, 35), (17, 39), r=2.9)
    # tower shield with a star crest
    s.part(ramp('#d8deea', 1.2), [('poly', [(8, 30), (20, 30), (20, 45), (14, 51), (8, 45)])], soft=1.5, gloss=.8)
    s.part(navy, [('poly', [(9.6, 31.6), (18.4, 31.6), (18.4, 44.3), (14, 49), (9.6, 44.3)])], soft=1.2)
    star(s, gold, 14, 39.5, 4.2)
    head(s)
    bangs(s, ramp('#d8e2f4', 1.1), 'swept', cast=1)
    s.part(plate, [('chord', 28, 16.5, 12, 10.5, 180, 360), ('rect', 16, 14, 19, 24), ('rect', 37, 14, 40, 24)],
           soft=2, gloss=1, cast=2)
    s.part(gold, [('rect', 16, 14, 40, 15.6)], soft=.5, gloss=.8, cast=1)
    star(s, ramp('#fff3a0', 1.1), 28, 7.5, 4.6)
    face(s, '#3a7ae0')
    for x, y in ((47, 32), (51, 40), (6, 26), (44, 48)):
        sparkle(s, x, y, (200, 225, 255))
    return s


def stormranger():
    s = Spr()
    cloak, steel, bolt = ramp('#4c5a6e', 1.2), P['steel'], ramp('#ffe45a', 1.2, 1.2)
    teal = ramp('#2fb3b0', 1.1)
    cape(s, cloak, 1.1, 52)
    legs(s, ramp('#33394a'), ramp('#262a36'))
    torso(s, ramp('#3b4658', 1.1), hem=46)
    s.part(teal, [('poly', [(21, 30), (23.5, 29.5), (35.5, 42), (33.5, 43)])], soft=.7)
    belt(s, P['darkleather'], 38, steel)
    arm(s, cloak, SKIN, (35, 30), (38, 36), (40, 40), glove=P['darkleather'])
    # long steel bow with a lightning arrow nocked
    pts = [(18, 14), (13.5, 19), (11, 28), (10.5, 35), (11, 42), (13.5, 50), (18, 54)]
    s.part(P['string'], [('cap', 18, 14.5, 18, 53.5, .45)], soft=.4, line=False, thr=.3)
    s.part(ramp('#8a96aa', 1.4), [('line', pts, 1.3)], soft=.7, gloss=1)
    s.part(teal, [('ell', 18, 14, 1.5, 1.5), ('ell', 18, 54, 1.5, 1.5), ('rect', 9.5, 33, 12.5, 37)], soft=.5, gloss=1)
    s.part(bolt, [('poly', [(10, 35), (15, 33.6), (17, 35.6), (22, 34), (26, 35.4), (21, 36.6), (17, 35.9), (14, 37)])],
           soft=.3, line=False, flat=True, bias=.25)
    arm(s, cloak, SKIN, (21, 30), (17.5, 35), (13, 36), glove=P['darkleather'])
    s.part(steel, [('chord', 35.5, 31, 4.2, 3.5, 180, 360)], soft=1.2, gloss=.8, cast=1)
    head(s)
    bangs(s, ramp('#2a3040', 1.2), 'neat', shine=10)
    s.part(cloak, [('chord', 28, 17, 13, 12.5, 180, 360), ('poly', [(15, 17), (19, 17), (19.5, 28), (14, 29)]),
                   ('poly', [(37, 17), (41, 17), (42, 29), (36.5, 28)])],
           sub=[('ell', 28, 19.5, 9.5, 8.5)], soft=2, cast=2)  # hood
    s.part(teal, [('rect', 17, 9, 39, 10.6)], soft=.4, flat=True, cast=1)
    face(s, '#2fb3b0')
    for x, y, c in ((7, 30, (255, 240, 120)), (6, 40, (255, 230, 90)), (27, 32, (255, 250, 180)), (48, 20, (160, 240, 240))):
        sparkle(s, x, y, c)
    return s


def dawnoracle():
    s = Spr()
    robe, gold, peach = ramp('#fff6e8', .8), P['gold'], ramp('#ffa860', 1.1, 1.1)
    # sun disc behind the head
    for x in range(10, 47):
        for y in range(0, 32):
            dx, dy = x + .5 - 28, y + .5 - 15
            r = (dx * dx + dy * dy) ** .5
            if 13 <= r <= 15:
                s.glow(x, y, (255, 200, 90), 220)
            elif 15 < r <= 18 and (int((x + y) * 1.3) % 3 == 0):
                s.glow(x, y, (255, 170, 70), 120)
    cape(s, peach, 1.0, 52)
    back_hair(s, ramp('#c8562a', 1.1), 40, 12.5)
    legs(s, robe, ramp('#c8a060'), robe=True)
    staff(s, gold, 42, 52, 43.5, 12, 1)
    ring(s, gold, 43.5, 8.5, 4, 4, 1.3)
    orb(s, ramp('#ffdc60', 1.1), 43.5, 8.5, 2.2)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, gold, 47.8)
    s.part(peach, [('poly', [(25, 29), (31, 29), (31, 47.5), (25, 47.5)])], soft=.8)
    s.part(gold, [('rect', 27.3, 31, 28.7, 46)], soft=.4, flat=True, bias=.1)
    s.part(gold, [('ell', 28, 30.5, 10, 4)], sub=[('ell', 28, 29.5, 7.5, 2.8)], soft=1, gloss=.8, cast=1)
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40), r=3.4)
    arm(s, robe, SKIN, (21, 30), (18, 36), (21.5, 41), r=3.4)
    head(s)
    bangs(s, ramp('#c8562a', 1.1), 'long', shine=10)
    s.part(gold, [('rect', 18, 11.5, 38, 13)], soft=.5, gloss=1)
    orb(s, ramp('#ff7a40', 1.2), 28, 11.5, 1.4)
    face(s, '#b86a10')
    sparkle(s, 49, 3, (255, 245, 190))
    sparkle(s, 8, 40, (255, 220, 150))
    return s


def nightreaper():
    s = Spr()
    suit, fur, green = ramp('#26302a', 1.2), ramp('#5a5e6a', 1.2), ramp('#5ee08a', 1.2, 1.1)
    # scythe held upright on the right, blade curling outward
    s.part(ramp('#4a3a2e', 1.2), [('cap', 45, 53, 46.5, 5, 1)], soft=.6)
    s.part(ramp('#cfe8d8', 1.3), [('poly', [(46, 3), (51, 2.5), (55, 7), (55.5, 15), (52.5, 9), (47, 7.5)])], soft=.6, gloss=1.2)
    s.part(green, [('poly', [(48, 4), (51.5, 4.2), (54, 8), (54.2, 12), (51.6, 6.6)])], soft=.3, line=False, flat=True, bias=.2)
    cape(s, ramp('#1c2420', 1.2), 1.1, 52)
    legs(s, suit, ramp('#16191a'))
    torso(s, suit, hem=45)
    s.part(green, [('poly', [(21, 30), (24, 29.5), (35.6, 42), (33.5, 43)])], soft=.7)
    belt(s, ramp('#4a4452', 1.2), 39, green)
    arm(s, suit, SKIN, (35, 30), (39, 35), (41.5, 38.5), r=2.4, glove=ramp('#3a3a3e'))
    dagger(s, ramp('#cfe8d8', 1.3), P['darkleather'], 18, 38)
    arm(s, suit, SKIN, (21, 30), (18, 35), (17.5, 37.5), r=2.4, glove=ramp('#3a3a3e'))
    head(s)
    bangs(s, ramp('#1e1e24', 1.2), 'spiky', cast=1)
    # wolf-pelt hood with ears
    s.part(fur, [('chord', 28, 16, 13, 12.5, 180, 360), ('poly', [(15, 16), (19, 16), (19.5, 29), (14, 30)]),
                 ('poly', [(37, 16), (41, 16), (42, 30), (36.5, 29)]),
                 ('poly', [(17, 9), (17.5, 0.5), (24.5, 5)]), ('poly', [(39, 9), (38.5, 0.5), (31.5, 5)])],
           sub=[('ell', 28, 19, 9.5, 8.5)], soft=2, cast=2)
    s.part(ramp('#d8a0a8'), [('poly', [(18.6, 7.5), (19, 3), (22.5, 5.5)]), ('poly', [(37.4, 7.5), (37, 3), (33.5, 5.5)])],
           soft=.4, line=False)
    s.part(ramp('#e8e8ee', .9), [('poly', [(19, 22.5), (37, 22.5), (35.5, 26), (28, 28.5), (20.5, 26)])], soft=1.2)  # muzzle mask
    face(s, '#5ee08a', mouth=False)
    for x, y in ((12, 22), (48, 30), (10, 46)):
        sparkle(s, x, y, (150, 255, 190))
    return s


def voidsage():
    s = Spr()
    robe, deep, silver = ramp('#4a2a7a', 1.2, 1.1), ramp('#1a1030', 1.3), ramp('#d8d4f0', 1.1)
    moon = ramp('#e8e0ff', 1.0)
    # crescent moon floating behind
    s.part(moon, [('ell', 13, 13, 8, 8)], sub=[('ell', 16.5, 10.5, 7, 7)], soft=1.2, gloss=1, line=False)
    cape(s, deep, 1.2, 52)
    back_hair(s, silver, 40, 12.5)
    legs(s, robe, ramp('#2a1a3a'), robe=True)
    staff(s, ramp('#2a1a3a', 1.2), 42, 52, 43.5, 12, 1.1)
    s.part(silver, [('ell', 43.5, 9, 4.6, 4.6)], sub=[('ell', 45.5, 7.5, 4, 4)], soft=.8, gloss=1, line=False)
    orb(s, ramp('#b070ff', 1.3), 42.5, 10, 1.8)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, silver, 47.8)
    s.part(deep, [('poly', [(25, 30), (31, 30), (31.5, 48), (24.5, 48)])], soft=.8)
    star(s, silver, 28, 38, 2.6)
    s.part(robe, [('poly', [(17.5, 26), (24, 28.5), (32, 28.5), (38.5, 26), (38, 31), (18, 31)])], soft=1.2, cast=1)
    arm(s, robe, SKIN, (35, 30), (38.5, 36), (42, 40), r=3.4)
    arm(s, robe, SKIN, (21, 30), (17.5, 35), (15, 38), r=3.4)
    orb(s, ramp('#7a3aff', 1.3), 13.5, 34, 2.4)  # void orb in hand
    head(s)
    bangs(s, silver, 'long', shine=10)
    s.part(deep, [('rect', 17.5, 11.5, 38.5, 13)], soft=.5)
    s.part(silver, [('ell', 28, 10.5, 2.2, 2.2)], sub=[('ell', 29.3, 9.6, 1.8, 1.8)], soft=.4, line=False)
    face(s, '#9a5aff')
    for x, y, c in ((9, 27, (190, 140, 255)), (7, 41, (150, 110, 255)), (50, 18, (230, 220, 255)), (22, 3, (230, 220, 255))):
        sparkle(s, x, y, c)
    return s


TIER4 = dict(starwarden=starwarden, stormranger=stormranger, dawnoracle=dawnoracle,
             nightreaper=nightreaper, voidsage=voidsage)
