"""Designs for the other 14 units (all original characters)."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from pixel import Spr, ramp


# ====== headwear & extras ======
def wizard_hat(s, rp, band=None, tip=(41, 1), brim=15):
    s.part(rp, [('ell', 28, 12.5, brim, 3.6)], soft=1.2, cast=2)
    s.part(rp, [('poly', [(19.5, 12.5), (36.5, 12.5), (35, 6), tip, (31, 3.5), (25, 5)])], soft=1.8, cast=2)
    if band:
        s.part(band, [('poly', [(19.8, 10), (36.2, 10), (36.5, 12.6), (19.5, 12.6)])], soft=0.6, gloss=0.5, cast=2)


def scarf(s, rp, tail=True):
    s.part(rp, [('ell', 28, 28.5, 8, 2.8)], soft=1, cast=1)
    if tail:
        s.part(rp, [('poly', [(33, 28), (36, 28.5), (45, 34), (47, 39), (43, 37), (38, 33)])], soft=1)


def mask(s, rp):
    s.part(rp, [('poly', [(18.3, 22.5), (37.5, 22.5), (36, 26), (28, 28.5), (20, 26.5)])], soft=1.2)


def ring(s, rp, cx, cy, rx, ry, t=1.2):
    s.part(rp, [('ell', cx, cy, rx, ry)], sub=[('ell', cx, cy, rx - t, ry - t)], soft=0.5, gloss=0.8, line=False)


def sparkle(s, x, y, c):
    for dx, dy, a in ((0, 0, 255), (1, 0, 150), (-1, 0, 150), (0, 1, 150), (0, -1, 150)):
        s.glow(x + dx, y + dy, c, a)


def hem_trim(s, rp, y=47.6):
    s.part(rp, [('poly', [(17.5, y), (38.5, y), (39, y + 1.4), (28, y + 2.9), (17, y + 1.4)])], soft=.6)


# ====== tier 1 ======
def archer():
    s = Spr()
    hair = ramp('#e8c35a')
    s.part(ramp('#7a5235'), [('poly', [(30, 25), (35, 23), (41, 39), (37, 41)])], soft=1)  # quiver
    s.part(ramp('#d9d2c0'), [('poly', [(33, 22.5), (36, 20), (38, 23)]), ('poly', [(35.5, 23), (39, 20.5), (40, 24)])], soft=.6)
    s.part(hair, [('line', [(36, 15), (41, 19), (42, 26), (40, 31)], 2.2)], soft=1.2)  # ponytail
    legs(s, ramp('#6b5338'), ramp('#5e3f2a'))
    torso(s, ramp('#4f9a4a'), hem=44)
    s.part(ramp('#3d6f39'), [('poly', [(19.6, 41), (36.4, 41), (37, 45), (19, 45)])], soft=1)
    belt(s, P['leather'], buckle=P['gold'])
    s.part(P['leather'], [('poly', [(34, 28.5), (36.5, 29.5), (22, 39.5), (20.8, 38)])], soft=.7)
    arm(s, ramp('#4f9a4a'), SKIN, (35, 30), (37.5, 36), (38, 40), glove=P['leather'])
    bow(s, P['wood'], P['string'], x=16, top=24, bot=52, bulge=5)
    arm(s, ramp('#4f9a4a'), SKIN, (21, 30), (18.5, 35), (16.5, 38.5), glove=P['leather'])
    head(s)
    bangs(s, hair, 'neat')
    s.part(ramp('#3d7f39'), [('chord', 28, 15, 12.2, 8, 180, 360), ('poly', [(16, 15), (40, 15), (42, 17), (14, 17)])], soft=1.6, cast=2)
    s.part(ramp('#e06a3a'), [('line', [(37, 11), (43, 4), (46, 1.5)], 1.1)], soft=.6)  # feather
    face(s, '#3c8a3c')
    return s


def acolyte():
    s = Spr()
    robe, trim = ramp('#eee6d6', 0.9), ramp('#2aa39a')
    legs(s, robe, ramp('#6b4a3a'), robe=True)
    staff(s, P['wood'], 41, 50, 42.5, 16)
    ring(s, P['gold'], 42.6, 13.5, 3.2, 3.2, 1.3)
    torso(s, robe, 'robe', hem=49)
    s.part(trim, [('rect', 26.5, 33, 29.5, 50)], soft=.8)
    hem_trim(s, trim)
    s.part(ramp('#d8cfbd', .9), [('ell', 28, 31, 9.5, 4.5)], soft=1.5, cast=1)  # mantle
    s.part(P['gold'], [('ell', 28, 32.5, 1.6, 1.6)], soft=.5, gloss=1)
    arm(s, robe, SKIN, (35, 30), (38, 36), (41.5, 39.5), r=3)
    arm(s, robe, SKIN, (21, 30), (18.5, 36), (21, 40), r=3)
    head(s)
    bangs(s, ramp('#3b3046'), 'neat')
    face(s, '#6d4c9f')
    return s


def thief():
    s = Spr()
    band = ramp('#b8333a')
    legs(s, ramp('#3e3a4a'), ramp('#6b4b33'))
    torso(s, ramp('#3e3a4a'))
    s.part(ramp('#c79a5a'), [('poly', [(20.6, 29), (26.5, 29), (24, 42), (19.6, 43)]),
                             ('poly', [(29.5, 29), (35.4, 29), (36.4, 43), (32, 42)])], soft=1.3)  # vest
    belt(s, P['darkleather'], 39)
    dagger(s, P['steel'], P['darkleather'], 40.5, 41, 'down')
    arm(s, ramp('#3e3a4a'), SKIN, (35, 30), (38, 35), (40.5, 39.5), r=2.4, glove=ramp('#d6cbb5'))
    dagger(s, P['steel'], P['darkleather'], 17, 40, 'up')
    arm(s, ramp('#3e3a4a'), SKIN, (21, 30), (18, 35), (17, 38.5), r=2.4, glove=ramp('#d6cbb5'))
    scarf(s, ramp('#2f8f7f'))
    head(s)
    bangs(s, ramp('#2b2b3a'), 'swept')
    s.part(band, [('poly', [(17, 11.5), (39, 11.5), (39.6, 14.5), (16.6, 14.5)])], soft=.6, cast=1)
    s.part(band, [('poly', [(38.5, 12), (45, 14), (46, 18), (42, 16), (38.5, 14.5)])], soft=.6)
    face(s, '#a0522d')
    return s


def mage():
    s = Spr()
    robe = ramp('#7a4fc4')
    cape(s, ramp('#4a2f80'), .6, 50)
    back_hair(s, ramp('#e0884a'), 30)
    legs(s, robe, ramp('#4a3a5a'), robe=True)
    torso(s, robe, 'robe', hem=49)
    hem_trim(s, P['gold'])
    s.part(P['gold'], [('rect', 27, 29, 29, 48)], soft=.6, gloss=.5)
    belt(s, ramp('#3a2a50'), 37)
    s.part(P['wood'], [('cap', 41, 41, 45.5, 29, .8)], soft=.5)
    orb(s, ramp('#ff6a9a', 1.2), 46, 27.5, 2.2)
    arm(s, robe, SKIN, (35, 30), (38, 36), (41.5, 39.5), r=3)
    arm(s, robe, SKIN, (21, 30), (18.5, 36), (21, 40.5), r=3)
    head(s)
    bangs(s, ramp('#e0884a'), 'long')
    wizard_hat(s, ramp('#6a3fb4'), band=P['gold'])
    face(s, '#d0457a')
    sparkle(s, 49, 24, (255, 200, 230))
    return s


# ====== tier 2 ======
def knight():
    s = Spr()
    plate, tab = ramp('#aab6cc', 1.4), ramp('#2c5fb0')
    legs(s, plate, ramp('#7c879b', 1.3))
    torso(s, plate, hem=44)
    s.part(tab, [('poly', [(24, 31), (32, 31), (32.5, 46), (28, 48), (23.5, 46)])], soft=1.2)
    belt(s, P['darkleather'], 39, P['gold'])
    sword(s, P['steel'], ramp('#c9a24a', 1.2), x0=41.5, y0=43, x1=50, y1=14, w=2.0, guard=4.5)
    arm(s, plate, plate, (35, 30), (38.5, 36), (41.5, 40.5), r=2.8)
    s.part(plate, [('chord', 35.5, 31, 4.6, 4, 180, 360)], soft=1.2, gloss=.8, cast=1)
    arm(s, plate, plate, (21, 30), (18.5, 35), (18, 39), r=2.8)
    kite = [(10, 31), (21, 31), (21, 40), (15.5, 48), (10, 40)]
    s.part(tab, [('poly', kite)], soft=2, gloss=.3)
    s.part(plate, [('poly', kite)], sub=[('poly', [(11.4, 32.3), (19.6, 32.3), (19.6, 39.6), (15.5, 46), (11.4, 39.6)])],
           soft=.6, gloss=.8, line=False)
    s.part(P['gold'], [('rect', 14.8, 33.5, 16.2, 43), ('rect', 12.3, 36, 18.7, 37.4)], soft=.5, flat=True, bias=.1)
    head(s)
    s.part(plate, [('chord', 28, 17, 12, 11, 180, 360), ('rect', 16, 14, 19.5, 26), ('rect', 36.5, 14, 40, 26)],
           soft=2, gloss=1, cast=2)
    s.part(ramp('#5c6780', 1.2), [('rect', 16, 14.5, 40, 16)], soft=.5, cast=1)
    s.part(ramp('#d2394a'), [('line', [(28, 6), (32, 1.5), (38, 1), (42, 4), (44, 8)], 2)], soft=1)  # plume
    face(s, '#3c5aa0')
    return s


def hunter():
    s = Spr()
    coat = ramp('#9a6a42')
    cape(s, ramp('#3f6b3a'), .9, 50)
    legs(s, ramp('#4a4a3a'), ramp('#4f3626'))
    torso(s, coat, hem=46)
    s.part(ramp('#6e4a30'), [('rect', 26.5, 29, 29.5, 46)], soft=.6)
    belt(s, P['darkleather'], 38, P['steel'])
    arm(s, coat, SKIN, (35, 30), (38, 36), (40, 40), glove=P['darkleather'])
    bow(s, ramp('#6b4226', 1.2), P['string'], x=15, top=18, bot=53, bulge=6)
    s.part(P['gold'], [('rect', 9.5, 34, 11.5, 37)], soft=.4, gloss=.8)
    arm(s, coat, SKIN, (21, 30), (18.5, 35), (15.5, 37.5), glove=P['darkleather'])
    scarf(s, ramp('#3f6b3a'), tail=False)
    head(s)
    bangs(s, ramp('#6b3f2a'), 'swept')
    s.part(ramp('#7a5a3a'), [('ell', 28, 13.5, 15.5, 3.4)], soft=1.2, cast=2)
    s.part(ramp('#7a5a3a'), [('chord', 28, 13.5, 9.5, 9, 180, 360)], soft=1.6, cast=2)
    s.part(ramp('#5a3d24'), [('rect', 18.6, 11, 37.4, 13.4)], soft=.5)
    s.part(ramp('#d7d2c8'), [('line', [(35, 12), (40, 6), (44, 3)], 1.0)], soft=.5)
    face(s, '#4a7a3a')
    return s


def priest():
    s = Spr()
    robe, stole = ramp('#f2efe8', .85), ramp('#3a6fc0')
    legs(s, robe, ramp('#8a7a6a'), robe=True)
    staff(s, P['gold'], 41.5, 51, 42.5, 12, .9)
    ring(s, P['gold'], 42.5, 9.5, 4, 4, 1.4)
    orb(s, ramp('#7fd4ff', 1.1), 42.5, 9.5, 1.6)
    torso(s, robe, 'robe', hem=49)
    s.part(stole, [('rect', 23, 29, 25.5, 48), ('rect', 30.5, 29, 33, 48)], soft=.8)
    s.part(P['gold'], [('rect', 23, 46, 25.5, 48), ('rect', 30.5, 46, 33, 48)], soft=.4, flat=True)
    hem_trim(s, P['gold'])
    arm(s, robe, SKIN, (35, 30), (38.5, 36), (42, 40), r=3.2)
    arm(s, robe, SKIN, (21, 30), (18.5, 36), (21.5, 40), r=3.2)
    head(s)
    bangs(s, ramp('#c4a76a'), 'neat')
    s.part(robe, [('chord', 28, 16, 12.5, 11.5, 180, 360), ('rect', 15.5, 15, 19, 29), ('rect', 37, 15, 40.5, 29)],
           sub=[('ell', 28, 19.5, 9.5, 8)], soft=2, cast=2)  # coif
    s.part(P['gold'], [('poly', [(18.5, 11.5), (37.5, 11.5), (37.5, 13), (18.5, 13)])], soft=.5, gloss=.6)
    s.part(ramp('#3a6fc0'), [('ell', 28, 12, 1.3, 1.3)], soft=.4, gloss=1)
    face(s, '#3a6fc0')
    return s


def assassin():
    s = Spr()
    suit, red = ramp('#4b3a6e'), ramp('#b3243a')
    s.part(red, [('poly', [(33, 27), (37, 28), (48, 37), (50, 46), (45, 41), (42, 44), (39, 36)])], soft=1)  # scarf tail
    legs(s, suit, ramp('#2e2840'))
    torso(s, suit)
    s.part(ramp('#352a52'), [('poly', [(21, 32), (35, 32), (36, 34), (20, 34)])], soft=.6)
    belt(s, red, 38)
    dagger(s, P['steel'], ramp('#2e2840'), 41, 41, 'down', 9)
    arm(s, suit, SKIN, (35, 30), (38.5, 35), (41, 39.5), r=2.4, glove=ramp('#2e2840'))
    dagger(s, P['steel'], ramp('#2e2840'), 17, 40, 'up', 9)
    arm(s, suit, SKIN, (21, 30), (18, 35), (17, 38.5), r=2.4, glove=ramp('#2e2840'))
    s.part(red, [('ell', 28, 28.5, 8.5, 3)], soft=1, cast=1)
    head(s)
    bangs(s, ramp('#c9cde0', 1.2), 'spiky')
    mask(s, ramp('#2e2840'))
    face(s, '#c03048', mouth=False)
    return s


def wizard():
    s = Spr()
    robe = ramp('#2b3f8f')
    back_hair(s, ramp('#cfd6f0'), 33)
    legs(s, robe, ramp('#2a2a40'), robe=True)
    staff(s, ramp('#5a3a6a'), 41, 52, 43, 11, 1)
    s.part(P['gold'], [('poly', [(40, 10), (43, 5.5), (46, 10), (43, 13)])], soft=.4, gloss=.8, line=False)
    orb(s, ramp('#5fd0ff', 1.2), 43, 8.5, 2.6)
    torso(s, robe, 'robe', hem=49)
    hem_trim(s, P['gold'])
    s.part(ramp('#c9b37a'), [('poly', [(24.5, 29), (31.5, 29), (30, 48), (26, 48)])], soft=1)
    s.part(robe, [('poly', [(19.5, 27.5), (24, 28.5), (32, 28.5), (36.5, 27.5), (36.5, 31), (19.5, 31)])], soft=1.2, cast=1)  # collar
    arm(s, robe, SKIN, (35, 30), (38.5, 36), (42, 40), r=3.3)
    arm(s, robe, SKIN, (21, 30), (18, 36), (20.5, 41), r=3.3)
    head(s)
    bangs(s, ramp('#cfd6f0'), 'long')
    wizard_hat(s, ramp('#22357a'), band=ramp('#c9b37a'), tip=(43, 0.5), brim=15.5)
    for x, y in ((25, 7), (32, 5), (29, 9)):
        s.glow(x, y, (255, 240, 160))
    face(s, '#2f6fd0')
    sparkle(s, 47, 5, (200, 240, 255))
    return s


# ====== tier 3 ======
def lordknight():
    s = Spr()
    plate, red, gold = ramp('#c4ccdc', 1.4), ramp('#b3202f'), P['gold']
    cape(s, red, 1.1, 52)
    legs(s, plate, ramp('#8a93a8', 1.3))
    torso(s, plate, hem=44)
    s.part(red, [('poly', [(24, 33), (32, 33), (32.5, 47), (28, 49), (23.5, 47)])], soft=1.2)
    s.part(gold, [('poly', [(21, 29), (35, 29), (34, 33), (28, 35), (22, 33)])], soft=1, gloss=.8)
    belt(s, gold, 39, red)
    # glowing greatsword
    s.part(ramp('#d8f2ff', 1.2), [('poly', [(40, 38), (44, 38), (51, 7), (49.5, 3), (47.5, 7)])], soft=.7, gloss=1.2)
    s.part(ramp('#7fd4ff', 1.1), [('poly', [(41.6, 37), (42.4, 37), (49.6, 8), (49, 7)])], soft=.3, line=False, flat=True, bias=.2)
    s.part(gold, [('poly', [(36, 38), (48, 38.8), (48, 41), (36, 40.2)]), ('cap', 42, 40, 41.6, 46, 1),
                  ('ell', 41.5, 47, 1.5, 1.5)], soft=.6, gloss=.8)
    arm(s, plate, plate, (35, 30), (39, 36), (42, 41), r=2.8)
    s.part(gold, [('chord', 36, 31, 5.2, 4.5, 180, 360)], soft=1.2, gloss=1, cast=1)
    arm(s, plate, plate, (21, 30), (18.5, 35), (20, 40), r=2.8)
    s.part(gold, [('chord', 20, 31, 5.2, 4.5, 180, 360)], soft=1.2, gloss=1, cast=1)
    head(s)
    bangs(s, ramp('#b0482e'), 'swept')
    s.part(plate, [('chord', 28, 16.5, 12, 10.5, 180, 360), ('rect', 16, 14, 19, 24), ('rect', 37, 14, 40, 24)],
           soft=2, gloss=1, cast=2)
    s.part(gold, [('rect', 16, 14, 40, 15.6), ('poly', [(26.5, 6), (29.5, 6), (28, 14.5)])], soft=.5, gloss=.8, cast=1)
    wing = ramp('#f4f4f4', .9)
    s.part(wing, [('poly', [(15.5, 14), (8, 6), (10, 12), (5, 10), (10, 16), (16, 18)])], soft=1)
    s.part(wing, [('poly', [(40.5, 14), (48, 6), (46, 12), (51, 10), (46, 16), (40, 18)])], soft=1)
    face(s, '#2f6fb8')
    for y in (10, 18, 26):
        sparkle(s, 52, y, (190, 240, 255))
    return s


def sniper():
    s = Spr()
    coat = ramp('#2f6f6a')
    cape(s, ramp('#7a2a2a'), 1.0, 51)
    legs(s, ramp('#3a3a48'), ramp('#3a2a22'))
    torso(s, coat, hem=47)
    s.part(ramp('#245752'), [('poly', [(28, 29), (29.5, 29), (29.5, 47), (28, 47)])], soft=.5)
    s.part(P['gold'], [('rect', 19.6, 45, 36.4, 47)], soft=.4, flat=True)
    belt(s, P['darkleather'], 38, P['gold'])
    s.part(P['darkleather'], [('poly', [(34, 28.5), (36.5, 29.5), (22, 39.5), (20.8, 38)])], soft=.7)
    arm(s, coat, SKIN, (35, 30), (38, 36), (40, 40), glove=P['darkleather'])
    # recurve bow, gold-trimmed, with a glowing arrow
    pts = [(17, 17), (13, 20), (11.5, 28), (11, 35), (11.5, 42), (13, 50), (17, 53)]
    s.part(P['string'], [('cap', 17, 17.5, 17, 52.5, .45)], soft=.4, line=False, thr=.3)
    s.part(ramp('#2a2a34', 1.3), [('line', pts, 1.3)], soft=.7, gloss=.7)
    s.part(P['gold'], [('ell', 17, 17, 1.5, 1.5), ('ell', 17, 53, 1.5, 1.5), ('rect', 10, 33, 13, 37)], soft=.5, gloss=1)
    s.part(ramp('#8fe8ff', 1.2), [('cap', 10, 35, 24, 35, .5)], soft=.3, line=False, flat=True, bias=.2)
    arm(s, coat, SKIN, (21, 30), (18, 35), (13.5, 36), glove=P['darkleather'])
    head(s)
    bangs(s, ramp('#b9c2cf', 1.2), 'swept')
    s.part(ramp('#4a3a2a'), [('rect', 17, 11.5, 39, 14)], soft=.6, cast=1)
    for gx in (22.5, 32):  # goggles
        s.part(P['gold'], [('ell', gx, 12.5, 3, 2.6)], soft=.6, gloss=1)
        s.part(ramp('#ff9a3a', 1.2), [('ell', gx, 12.5, 1.8, 1.5)], soft=.6, gloss=1.4, line=False)
    face(s, '#2a8a8a')
    sparkle(s, 8, 35, (180, 240, 255))
    return s


def highpriest():
    s = Spr()
    robe, gold = ramp('#f7f4ee', .8), P['gold']
    cape(s, ramp('#e8e0cc', .8), 1.0, 52)
    back_hair(s, ramp('#7a4632'), 36, 12)
    legs(s, robe, ramp('#a08a6a'), robe=True)
    staff(s, gold, 42, 52, 43.5, 13, 1)
    s.part(gold, [('poly', [(38.5, 12), (43.5, 3), (48.5, 12), (43.5, 16)])],
           sub=[('poly', [(40.5, 12), (43.5, 6.5), (46.5, 12), (43.5, 14.2)])], soft=.5, gloss=1, line=False)
    orb(s, ramp('#ffe07a', 1.1), 43.5, 10.5, 2)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, gold, 47.8)
    s.part(ramp('#c23a4a'), [('poly', [(25, 29), (31, 29), (30.5, 47.5), (25.5, 47.5)])], soft=.8)
    s.part(gold, [('rect', 27.3, 31, 28.7, 46), ('rect', 25.5, 34, 30.5, 35.4)], soft=.4, flat=True, bias=.1)
    s.part(gold, [('ell', 28, 30.5, 10, 4)], sub=[('ell', 28, 29.5, 7.5, 2.8)], soft=1, gloss=.8, cast=1)  # collar
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40), r=3.4)
    arm(s, robe, SKIN, (21, 30), (18, 36), (21.5, 41), r=3.4)
    head(s)
    bangs(s, ramp('#7a4632'), 'long')
    s.part(gold, [('rect', 18, 11.5, 38, 13), ('poly', [(26, 12), (28, 6.5), (30, 12)])], soft=.5, gloss=1)
    orb(s, ramp('#5fa8ff', 1.2), 28, 10.5, 1.2)
    face(s, '#d4a020')
    for x in range(18, 39):  # halo
        for y in range(0, 6):
            dx, dy = (x + .5 - 28) / 10.5, (y + .5 - 3) / 2.3
            r = dx * dx + dy * dy
            if 0.62 <= r <= 1.0:
                s.glow(x, y, (255, 236, 140), 230)
            elif 1.0 < r <= 1.35:
                s.glow(x, y, (255, 220, 110), 90)
    sparkle(s, 49, 4, (255, 245, 190))
    return s


def assassincross():
    s = Spr()
    suit, red = ramp('#26222e', 1.2), ramp('#c01f35')
    s.part(red, [('poly', [(32, 26), (37, 27), (47, 31), (53, 40), (51, 46), (48, 41), (46, 47), (43, 39), (39, 34)])], soft=1)
    cape(s, ramp('#3a3442', 1.2), 1.0, 52)
    legs(s, suit, ramp('#18151d'))
    torso(s, suit, hem=45)
    s.part(red, [('poly', [(21, 30), (24, 29.5), (35.6, 42), (33.5, 43)])], soft=.7)
    belt(s, ramp('#4a4452', 1.2), 39, red)
    blade = ramp('#ff5a6a', 1.2)
    s.part(blade, [('poly', [(40, 42), (43, 42), (46, 54), (43.5, 51)])], soft=.5, gloss=1)
    s.part(blade, [('poly', [(15.5, 39), (18, 38), (12, 25), (12.5, 30)])], soft=.5, gloss=1)
    arm(s, suit, SKIN, (35, 30), (38.5, 35.5), (41.5, 39.5), r=2.4, glove=red)
    arm(s, suit, SKIN, (21, 30), (18, 35), (16.5, 37.5), r=2.4, glove=red)
    head(s)
    bangs(s, ramp('#e6e6f0', 1.1), 'swept', cast=1)
    s.part(suit, [('chord', 28, 17, 13, 12.5, 180, 360), ('poly', [(15, 17), (19, 17), (19.5, 30), (14, 31)]),
                  ('poly', [(37, 17), (41, 17), (42, 31), (36.5, 30)]), ('poly', [(24, 5.5), (32, 5.5), (38, 1.5), (34, 6)])],
           sub=[('ell', 28, 19, 9.5, 8.5)], soft=2, cast=2)  # hood
    mask(s, red)
    face(s, '#ff3040', mouth=False)
    for y in (27, 33, 41):
        s.glow(11 + (y % 3), y, (255, 120, 140), 160)
    sparkle(s, 47, 51, (255, 150, 160))
    return s


def highwizard():
    s = Spr()
    robe, gold = ramp('#a3263a', 1.1), P['gold']
    cape(s, ramp('#2a1a3a', 1.2), 1.2, 52)
    back_hair(s, ramp('#f2f2fa', 1.1), 38, 12)
    legs(s, robe, ramp('#3a2030'), robe=True)
    staff(s, ramp('#3a2a3a', 1.2), 41, 52, 43, 13, 1.1)
    s.part(gold, [('poly', [(38.5, 14), (40, 6), (43, 10), (46, 6), (47.5, 14), (43, 16)])], soft=.5, gloss=1)
    s.part(ramp('#ff4060', 1.3), [('poly', [(43, 2), (46, 8), (43, 14), (40, 8)])], soft=1, gloss=1.4)  # crystal
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, gold, 47.8)
    s.part(ramp('#2a1a3a', 1.2), [('poly', [(25, 30), (31, 30), (31.5, 48), (24.5, 48)])], soft=.8)
    s.part(gold, [('rect', 25, 30, 26, 48), ('rect', 30, 30, 31, 48)], soft=.4, flat=True, bias=.05)
    s.part(robe, [('poly', [(17.5, 26), (24, 28.5), (32, 28.5), (38.5, 26), (38, 31), (18, 31)])], soft=1.2, cast=1)  # collar
    s.part(gold, [('poly', [(17.5, 26), (19, 26.5), (19, 30.5), (18, 31)]), ('poly', [(38.5, 26), (37, 26.5), (37, 30.5), (38, 31)])],
           soft=.4, flat=True)
    arm(s, robe, SKIN, (35, 30), (38.5, 36), (42, 40), r=3.4)
    arm(s, robe, SKIN, (21, 30), (17.5, 35), (15, 38), r=3.4)
    orb(s, ramp('#ff7a3a', 1.2), 13.5, 34, 2.4)  # fireball in hand
    head(s)
    bangs(s, ramp('#f2f2fa', 1.1), 'long')
    s.part(gold, [('rect', 17.5, 11.5, 38.5, 13), ('poly', [(25.5, 12), (28, 5.5), (30.5, 12)])], soft=.5, gloss=1)
    orb(s, ramp('#ff4060', 1.2), 28, 10.5, 1.3)
    face(s, '#c0283c')
    for x, y, c in ((9, 26, (255, 170, 80)), (7, 31, (255, 120, 60)), (11, 29, (255, 210, 120)), (51, 9, (255, 140, 170))):
        sparkle(s, x, y, c)
    return s


CLASSES = dict(archer=archer, acolyte=acolyte, thief=thief, mage=mage,
               knight=knight, hunter=hunter, priest=priest, assassin=assassin, wizard=wizard,
               lordknight=lordknight, sniper=sniper, highpriest=highpriest, assassincross=assassincross,
               highwizard=highwizard)
