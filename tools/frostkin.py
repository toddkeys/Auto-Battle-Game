"""Designs for the Frost Healer class (original characters): healers who mend slowly and ward allies in ice."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import hem_trim, sparkle
from pixel import Spr, ramp


def snowflake(s, x, y, c):
    for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (-2, 0), (0, 2), (0, -2), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        s.glow(x + dx, y + dy, c, 255 if dx == 0 or dy == 0 else 150)


def snowmender():
    s = Spr()
    robe, fur, ice = ramp('#cfe6f4', .8), ramp('#f6f8fa', .7), ramp('#8ad8ff', 1.2, 1.1)
    legs(s, robe, ramp('#7a9ab0'), robe=True)
    staff(s, ramp('#9ab0c0', 1.2), 41, 52, 42.5, 14, .9)
    s.part(ice, [('poly', [(42.5, 5), (45.5, 11), (42.5, 15), (39.5, 11)])], soft=.8, gloss=1.4)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, fur, 47.6)
    s.part(ice, [('poly', [(26.5, 29), (29.5, 29), (29.5, 46), (26.5, 46)])], soft=.5, flat=True, bias=.15)
    arm(s, robe, SKIN, (35, 30), (39, 36), (42, 40), r=3.4)
    arm(s, robe, SKIN, (21, 30), (18, 36), (20.5, 41), r=3.4)
    head(s)
    bangs(s, ramp('#a8c8e8', 1.1), 'long', shine=10)
    s.part(fur, [('chord', 28, 17, 13, 12.5, 180, 360), ('poly', [(15, 17), (19, 17), (19.5, 29), (14, 30)]),
                 ('poly', [(37, 17), (41, 17), (42, 30), (36.5, 29)])], sub=[('ell', 28, 19.5, 9.5, 8.5)], soft=2.5, cast=2)   # fur hood
    face(s, '#4aa8e0')
    snowflake(s, 9, 26, (220, 245, 255))
    snowflake(s, 50, 34, (200, 235, 255))
    return s


def frostoracle():
    s = Spr()
    robe, deep, ice = ramp('#4a78b8', 1.2, 1.1), ramp('#24406a', 1.3), ramp('#bff2ff', 1.1)
    cape(s, ramp('#e8f4fc', .8), 1.1, 52)
    back_hair(s, ramp('#e0eef8', 1.0), 40, 12.5)
    legs(s, robe, ramp('#1e3050'), robe=True)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, ice, 47.8)
    s.part(deep, [('poly', [(25, 30), (31, 30), (31.5, 48), (24.5, 48)])], soft=.8)
    arm(s, robe, SKIN, (35, 30), (38.5, 35), (40.5, 32), r=3.4)
    arm(s, robe, SKIN, (21, 30), (17.5, 35), (15, 38), r=3.4)
    with s.grp('armR'):   # a floating ice crystal over the raised hand
        s.part(ice, [('poly', [(42, 20), (45.5, 25), (42, 30), (38.5, 25)])], soft=1, gloss=1.4)
    orb(s, ramp('#8ad8ff', 1.2), 13.5, 34, 2.3)
    head(s)
    bangs(s, ramp('#e0eef8', 1.0), 'long', shine=10)
    s.part(ice, [('poly', [(20, 12), (22, 6), (24, 12)]), ('poly', [(25.5, 12), (28, 3), (30.5, 12)]), ('poly', [(32, 12), (34, 6), (36, 12)]),
                 ('rect', 19, 11.5, 37, 13)], soft=.6, gloss=1.3)   # crystal tiara
    face(s, '#3a8ad0')
    snowflake(s, 8, 22, (220, 245, 255))
    snowflake(s, 50, 14, (230, 250, 255))
    return s


def winterqueen():
    s = Spr()
    gown, white, ice = ramp('#d8ecf8', .8), ramp('#ffffff', .6), ramp('#9ae8ff', 1.2, 1.1)
    cape(s, ramp('#7ab8e0', 1.1), 1.35, 52)
    back_hair(s, ramp('#f4fbff', .9), 42, 13)
    legs(s, gown, ramp('#8ab0d0'), robe=True)
    staff(s, ramp('#c8e8f8', 1.2), 42, 52, 44, 12, 1)
    s.part(ice, [('poly', [(44, 1), (48, 7), (46, 13), (44, 9), (42, 13), (40, 7)])], soft=.8, gloss=1.4)   # ice scepter head
    torso(s, gown, 'robe', hem=51)
    hem_trim(s, ice, 48.2)
    s.part(white, [('poly', [(24, 30), (32, 30), (34, 49), (22, 49)])], soft=1)
    s.part(ice, [('ell', 28, 30.5, 10, 4)], sub=[('ell', 28, 29.5, 7.5, 2.8)], soft=1, gloss=1, cast=1)   # frost collar
    arm(s, gown, SKIN, (35, 30), (39, 36), (42.5, 40), r=3.4)
    arm(s, gown, SKIN, (21, 30), (17.5, 35), (15, 38), r=3.4)
    orb(s, ice, 13.5, 34, 2.5)
    head(s)
    bangs(s, ramp('#f4fbff', .9), 'long', shine=10)
    s.part(ice, [('poly', [(18, 12), (19, 4), (22, 10), (24, 1), (27, 9), (28, -1), (29, 9), (32, 1), (34, 10), (37, 4), (38, 12)])], soft=.6, gloss=1.4)   # ice crown
    face(s, '#2a90d8')
    for x, y in ((7, 18), (51, 26), (9, 44), (49, 46)):
        snowflake(s, x, y, (225, 248, 255))
    return s


FROSTKIN = dict(snowmender=snowmender, frostoracle=frostoracle, winterqueen=winterqueen)
