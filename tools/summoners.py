"""Designs for the Summoner class (original characters), one per cost tier."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import hem_trim, sparkle
from pixel import Spr, ramp


def spiritcaller():
    s = Spr()
    robe, teal, gold = ramp('#eaf6f2', .8), ramp('#2fb8a0', 1.1), P['gold']
    back_hair(s, ramp('#b9a4e8', 1.1), 38, 12)
    legs(s, robe, ramp('#3a6a64'), robe=True)
    staff(s, P['wood'], 42, 52, 43, 14, .9)
    s.part(teal, [('ell', 43, 12, 2.6, 2.6)], soft=.6, gloss=1)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, teal, 47.8)
    s.part(teal, [('poly', [(25, 29), (31, 29), (30.5, 47.5), (25.5, 47.5)])], soft=.8)
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40), r=3.3)
    arm(s, robe, SKIN, (21, 30), (17.5, 35), (15, 38.5), r=3.3)
    # lantern held out in the near hand, a wisp glowing inside
    with s.grp('armL'):
        s.part(gold, [('rect', 11, 39, 17, 47), ('poly', [(12, 39), (14, 36.5), (16, 39)])], soft=.5, gloss=.8)
        s.part(ramp('#c8fff0', 1.0), [('rect', 12, 40.5, 16, 45.5)], soft=.4, flat=True, bias=.2, line=False)
    head(s)
    bangs(s, ramp('#b9a4e8', 1.1), 'long', shine=10)
    s.part(teal, [('rect', 18, 11.5, 38, 13)], soft=.5, gloss=.6)
    face(s, '#2fb8a0')
    for x, y in ((8, 30), (50, 22), (14, 20)):
        s.glow(x, y, (150, 255, 225), 230)
        sparkle(s, x, y, (190, 255, 235))
    return s


def beastmaster():
    s = Spr()
    leather, fur, bone = ramp('#7a4a2a'), ramp('#a87a4a', 1.1), ramp('#efe6d0', .8)
    cape(s, fur, 1.1, 50)
    legs(s, ramp('#4a3a2a'), P['darkleather'])
    torso(s, leather, hem=45)
    s.part(fur, [('ell', 28, 29, 9.5, 3.4)], soft=1.2, cast=1)   # fur collar
    for x in (24, 27, 30, 33):   # tooth necklace
        s.part(bone, [('poly', [(x, 31.5), (x + 1.4, 31.5), (x + .7, 34.5)])], soft=.3, line=False)
    belt(s, P['darkleather'], 39, P['gold'])
    with s.grp('weapon'):   # hand axe: haft and head turn together at the wrist
        s.part(P['wood'], [('cap', 41, 46, 44, 30, .9)], soft=.5)
        s.part(P['steel'], [('poly', [(43, 29), (49, 27), (50, 33), (44.5, 34)])], soft=.6, gloss=1)
    arm(s, leather, SKIN, (35, 30), (38.5, 36), (41.5, 40), glove=P['darkleather'])
    arm(s, leather, SKIN, (21, 30), (18, 35.5), (17.5, 39.5), glove=P['darkleather'])
    head(s)
    bangs(s, ramp('#9a3020', 1.1), 'spiky', shine=9)
    s.part(ramp('#c03a2a'), [('rect', 17, 12, 39, 14.2)], soft=.5, cast=1)   # headband
    s.part(fur, [('poly', [(19, 11), (21, 4), (24.5, 10)]), ('poly', [(37, 11), (35, 4), (31.5, 10)])], soft=.6)  # pelt ears
    face(s, '#c07a20', 'open')
    return s


def stonebinder():
    s = Spr()
    robe, stone, rune = ramp('#7a7068', 1.1), ramp('#9a948a', 1.25), ramp('#ffa040', 1.2, 1.2)
    cape(s, ramp('#4a443e', 1.1), 1.1, 52)
    legs(s, robe, ramp('#3a342e'), robe=True)
    staff(s, ramp('#5a4a3a', 1.2), 42, 52, 43, 15, 1)
    s.part(stone, [('ell', 43, 12, 4, 3.6)], soft=1.2, gloss=.3)
    s.part(rune, [('rect', 42.3, 10.5, 43.7, 13.5)], soft=.3, flat=True, bias=.25, line=False)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, ramp('#5a524a'), 47.8)
    for y in (33, 38, 43):   # glowing runes down the robe
        s.part(rune, [('rect', 27.3, y, 28.7, y + 2.6), ('rect', 26, y + 1, 30, y + 1.6)], soft=.3, flat=True, bias=.25, line=False)
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40), r=3.4)
    arm(s, robe, SKIN, (21, 30), (17.5, 34), (14.5, 36), r=3.4)
    with s.grp('armL'):   # a rock floating over the open hand
        s.part(stone, [('poly', [(10, 30), (14, 27), (18, 29.5), (17, 33), (12, 33.5)])], soft=1, gloss=.3)
        s.part(rune, [('rect', 13, 29.5, 15, 31)], soft=.3, flat=True, bias=.25, line=False)
    head(s)
    bangs(s, ramp('#3a3430', 1.1), 'neat', shine=10)
    s.part(ramp('#5a524a', 1.1), [('chord', 28, 17, 13, 12.5, 180, 360), ('poly', [(15, 17), (19, 17), (19.5, 29), (14, 30)]),
                                   ('poly', [(37, 17), (41, 17), (42, 30), (36.5, 29)])],
           sub=[('ell', 28, 19.5, 9.5, 8.5)], soft=2, cast=2)   # hood
    s.part(stone, [('poly', [(18.6, 22.6), (37.4, 22.6), (36, 26.5), (28, 28.6), (20.2, 26.5)])], soft=1)   # stone mask
    s.part(rune, [('rect', 27, 24, 29, 25.4)], soft=.3, flat=True, bias=.25, line=False)
    face(s, '#ff9a30', mouth=False)
    for x, y in ((9, 24), (20, 31)):
        s.glow(x, y, (255, 170, 80), 180)
    return s


def starcaller():
    s = Spr()
    robe, gold, sky = ramp('#22306a', 1.2, 1.1), P['gold'], ramp('#9ad0ff', 1.1)
    cape(s, ramp('#121a40', 1.3), 1.25, 52)
    back_hair(s, ramp('#f0e6ff', 1.0), 40, 12.5)
    legs(s, robe, ramp('#141a36'), robe=True)
    staff(s, gold, 42, 52, 43.5, 13, 1)
    s.part(gold, [('poly', [(43.5, 3), (45, 8), (50, 8.5), (46, 11.5), (47.5, 16.5), (43.5, 13.5), (39.5, 16.5), (41, 11.5), (37, 8.5), (42, 8)])],
           soft=.5, gloss=1.2)   # star on the staff
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, gold, 47.8)
    s.part(sky, [('poly', [(25, 29), (31, 29), (31.5, 48), (24.5, 48)])], soft=.8)
    for x, y in ((26.5, 34), (29.5, 38), (27, 43)):   # constellation on the robe
        s.mark(int(x), int(y), (255, 250, 220))
    s.part(gold, [('ell', 28, 30.5, 10, 4)], sub=[('ell', 28, 29.5, 7.5, 2.8)], soft=1, gloss=.8, cast=1)
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40), r=3.4)
    arm(s, robe, SKIN, (21, 30), (17.5, 35), (15, 38), r=3.4)
    orb(s, sky, 13.5, 34, 2.4)
    head(s)
    bangs(s, ramp('#f0e6ff', 1.0), 'long', shine=10)
    s.part(gold, [('rect', 17.5, 11.5, 38.5, 13), ('poly', [(21, 12), (22.5, 6.5), (24.5, 12)]), ('poly', [(26, 12), (28, 4.5), (30, 12)]),
                  ('poly', [(31.5, 12), (33.5, 6.5), (35, 12)])], soft=.5, gloss=1)   # star crown
    face(s, '#5a8aff')
    for x, y in ((8, 26), (51, 22), (6, 42), (50, 38), (12, 6)):
        sparkle(s, x, y, (230, 240, 255))
    return s


SUMMONERS = dict(spiritcaller=spiritcaller, beastmaster=beastmaster, stonebinder=stonebinder, starcaller=starcaller)
