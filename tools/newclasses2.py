"""Designs for the Ninja, Gravity, Druid and Berserker classes (original characters).
Berserkers are giants: drawn bulkier here and scaled up in the game (UNITS scale)."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import hem_trim, sparkle
from pixel import Spr, ramp


# ====== ninjas ======
def shadowstep():
    s = Spr()
    garb, red, steel = ramp('#2a2f4a', 1.2), ramp('#d8303a', 1.1), P['steel']
    with s.grp('cape'):   # long scarf trailing behind
        s.part(red, [('poly', [(32, 27), (36, 27), (50, 33), (52, 38), (46, 36), (38, 31)])], soft=1)
    legs(s, garb, ramp('#1a1e30'))
    torso(s, garb, hem=45)
    s.part(ramp('#3a405e', 1.2), [('poly', [(21, 29), (25, 29), (35, 42), (31, 43)])], soft=.6)
    belt(s, red, 39)
    sword(s, steel, ramp('#3a2a2a'), x0=42, y0=42, x1=45, y1=22, w=1.3, guard=3)
    arm(s, garb, SKIN, (35, 30), (38.5, 36), (41.5, 40), glove=ramp('#1a1e30'))
    arm(s, garb, SKIN, (21, 30), (18.5, 35), (18, 39), glove=ramp('#1a1e30'))
    head(s)
    bangs(s, ramp('#1a1a24', 1.3), 'spiky', shine=10)
    s.part(garb, [('poly', [(17, 22.5), (39, 22.5), (38, 29), (28, 31), (18, 29)])], soft=1, cast=1)   # mask over the mouth
    s.part(steel, [('rect', 21, 12, 35, 15)], soft=.5, gloss=1.2, cast=1)   # headband plate
    s.part(red, [('rect', 16.5, 12.5, 21, 14.5), ('rect', 35, 12.5, 39.5, 14.5), ('poly', [(16, 13), (9, 10), (10, 15)])], soft=.5)
    face(s, '#d8303a')
    return s


def phantomblade():
    s = Spr()
    garb, ghost, violet = ramp('#e8e4f4', .8), ramp('#b08aff', 1.2, 1.2), ramp('#5a3a9a', 1.2)
    back_hair(s, ramp('#f0f0ff', .8), 40, 10)
    legs(s, violet, ramp('#2a1a4a'))
    torso(s, garb, hem=46)
    s.part(violet, [('poly', [(21, 29), (25, 29), (35, 43), (31, 44)]), ('poly', [(22, 40), (34, 40), (35, 47), (21, 47)])], soft=.8)
    belt(s, ghost, 39)
    with s.grp('weapon'):   # spectral katana
        s.part(ghost, [('poly', [(41, 40), (43, 40), (47, 12), (46, 9), (44.5, 12)])], soft=.5, gloss=1.6)
        s.part(ramp('#3a2a4a'), [('cap', 39, 41.5, 45, 41, .9), ('cap', 42, 41.5, 41.6, 47, .9)], soft=.4)
    arm(s, garb, SKIN, (35, 30), (38.5, 36), (42, 41))
    arm(s, garb, SKIN, (21, 30), (18.5, 35), (18, 39))
    head(s)
    bangs(s, ramp('#f0f0ff', .8), 'swept', shine=10)
    s.part(violet, [('poly', [(28, 22.5), (39, 22.5), (38, 29), (30, 30)])], soft=.8, cast=1)   # half mask
    face(s, '#b08aff')
    for x, y in ((8, 22), (50, 28), (12, 44)):
        sparkle(s, x, y, (200, 170, 255))
    return s


# ====== gravity (crowd control) ======
def riftcaller():
    s = Spr()
    robe, star, gold = ramp('#2a2a6a', 1.2), ramp('#c8b8ff', 1.1, 1.2), P['gold']
    legs(s, robe, ramp('#1a1a40'), robe=True)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, star, 48)
    for x, y in ((24, 36), (31, 42), (27, 46), (33, 34)):
        s.mark(x, y, (220, 210, 255))
    belt(s, gold, 38, star)
    staff(s, ramp('#4a4a6a', 1.2), 42, 52, 43, 15, .9)
    s.part(ramp('#1a0a30', 1.3), [('ell', 43, 11, 4.2, 4.2)], soft=.6, gloss=.6)   # orb of swirling dark
    s.part(star, [('ell', 43, 11, 4.2, 4.2)], sub=[('ell', 43.6, 10.6, 3, 3)], soft=.3, line=False, flat=True, bias=.25)
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40))
    arm(s, robe, SKIN, (21, 30), (18, 35), (17, 38))
    head(s)
    bangs(s, ramp('#c8c8e8', .9), 'neat', shine=10)
    s.part(robe, [('chord', 28, 17, 13.5, 13.5, 180, 360), ('poly', [(14.5, 17), (18.5, 17), (19, 30), (14, 31)]),
                  ('poly', [(37.5, 17), (41.5, 17), (42, 31), (37, 30)])], sub=[('ell', 28, 20, 9.5, 8.5)], soft=2.5, cast=2)
    face(s, '#8a7aff')
    return s


def eclipsewitch():
    s = Spr()
    robe, gold, dark = ramp('#1a1428', 1.3), P['gold'], ramp('#0a0814', 1.2)
    back_hair(s, ramp('#2a1a3a', 1.2), 42, 12)
    cape(s, ramp('#3a1a5a', 1.2), 1.4, 53)
    legs(s, robe, dark, robe=True)
    torso(s, robe, 'robe', hem=51)
    hem_trim(s, gold, 49)
    belt(s, gold, 38, ramp('#b08aff', 1.2))
    staff(s, ramp('#3a2a4a', 1.2), 42, 52, 43, 14, 1)
    s.part(gold, [('ell', 43, 9.5, 5, 5)], soft=.5, gloss=1.4)   # eclipse: a black disc over a golden ring
    s.part(dark, [('ell', 43.8, 9, 4, 4)], soft=.4, line=False)
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40), glove=gold)
    arm(s, robe, SKIN, (21, 30), (18, 35), (17, 38), glove=gold)
    head(s)
    bangs(s, ramp('#2a1a3a', 1.2), 'long', shine=10)
    s.part(dark, [('poly', [(12, 13), (44, 13), (40, 10), (31, -1), (29, 0), (16, 10)])], soft=1.2, gloss=.6, cast=2)   # pointed hat
    s.part(gold, [('rect', 16, 11, 40, 13)], soft=.4, gloss=1)
    face(s, '#d0a020')
    for x, y in ((7, 20), (51, 24), (9, 42)):
        sparkle(s, x, y, (230, 200, 255))
    return s


# ====== druids (roots and wind) ======
def thornweaver():
    s = Spr()
    robe, leaf, bark = ramp('#4a8a3a', 1.1), ramp('#7ad66a', 1.2, 1.1), ramp('#6a4a2a', 1.1)
    legs(s, robe, P['leather'], robe=True)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, ramp('#3a6a2a'), 48)
    s.part(leaf, [('poly', [(22, 30), (26, 30), (24, 35)]), ('poly', [(30, 30), (34, 30), (32, 35)])], soft=.4)
    belt(s, bark, 38, leaf)
    staff(s, bark, 42, 52, 43, 13, 1.1)
    s.part(leaf, [('cap', 41, 14, 46, 20, .8), ('ell', 46, 13, 2.4, 1.6), ('ell', 40, 17, 2.2, 1.5)], soft=.5, gloss=.6)   # vines + leaves
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40))
    arm(s, robe, SKIN, (21, 30), (18, 35), (17, 38))
    head(s)
    bangs(s, ramp('#8a5a30', 1.0), 'swept', shine=10)
    for x, c in ((19, '#ff8ab8'), (24, '#ffe27a'), (29, '#ff8ab8'), (34, '#ffffff'), (38, '#ffe27a')):   # flower crown
        s.part(ramp(c, 1.1), [('ell', x, 11.5, 1.8, 1.8)], soft=.4, gloss=.8)
    face(s, '#3a9a5a', 'smile')
    return s


def galecaller():
    s = Spr()
    robe, sky, white = ramp('#5ab8d8', 1.1), ramp('#bfefff', .8), ramp('#f8fcff', .6)
    with s.grp('cape'):   # windblown sash
        s.part(white, [('poly', [(30, 30), (36, 30), (50, 24), (53, 28), (46, 33), (38, 36)])], soft=1)
    legs(s, robe, ramp('#3a7a9a'), robe=True)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, white, 48)
    belt(s, white, 38, sky)
    staff(s, ramp('#e8e0c8', 1.0), 42, 52, 43, 14, .9)
    s.part(white, [('poly', [(43, 14), (49, 6), (47, 13)]), ('poly', [(43, 14), (38, 7), (41, 14)])], soft=.5, gloss=.6)   # feathers
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40))
    arm(s, robe, SKIN, (21, 30), (17, 34), (14, 31))
    head(s)
    bangs(s, ramp('#e8f0f8', .9), 'swept', shine=10)
    s.part(sky, [('poly', [(16, 13), (40, 13), (44, 6), (36, 9), (28, 3), (20, 9), (12, 6)])], soft=1, gloss=.6, cast=2)   # feathered circlet
    face(s, '#2a90d0', 'smile')
    for x, y in ((7, 22), (9, 40)):
        sparkle(s, x, y, (220, 250, 255))
    return s


# ====== berserkers: giants with huge axes ======
def axe(s, haft, head_rp, x0, y0, x1, y1, big=1.0):
    with s.grp('weapon'):
        s.part(haft, [('cap', x0, y0 + 5, x1, y1, 1.1 * big)], soft=.5)
        # blade on the left of the haft: in the forward guard (and on the swing) the edge faces the enemy, not the sky
        s.part(head_rp, [('poly', [(x1 + 1, y1 + 1), (x1 - 8 * big, y1 - 5 * big), (x1 - 10 * big, y1 + 3 * big),
                                   (x1 - 8 * big, y1 + 11 * big), (x1 + 1, y1 + 7 * big)])], soft=.7, gloss=1.3)
        s.part(head_rp, [('poly', [(x1, y1 + 1), (x1 + 4 * big, y1 - 2 * big), (x1 + 4 * big, y1 + 7 * big), (x1, y1 + 6 * big)])], soft=.5, gloss=1)


def axebrute():
    s = Spr()
    fur, paint, skin = ramp('#8a6a4a', 1.1), ramp('#c03030'), ramp('#e0a880', .9)
    legs(s, ramp('#4a3a2a'), ramp('#3a2a1a'))
    torso(s, skin, hem=44)
    with s.grp('body'):
        s.part(skin, [('poly', [(18.5, 29), (37.5, 29), (37, 41), (19, 41)])], soft=2, cast=1)   # broad bare chest
        s.part(paint, [('cap', 23, 32, 26, 37, .7), ('cap', 33, 32, 30, 37, .7)], soft=.3, line=False)   # war paint
        s.part(fur, [('poly', [(19, 40), (37, 40), (38, 47), (28, 48.5), (18, 47)])], soft=1.4)   # fur kilt
    belt(s, ramp('#3a2a1a'), 40, P['steel'])
    axe(s, P['wood'], P['steel'], 42, 41, 45, 13)
    arm(s, skin, skin, (36, 30), (40, 36), (42.5, 40.5), r=3.4, glove=ramp('#5a3a2a'), hand_r=2.5)
    s.part(fur, [('chord', 36.5, 31, 6, 5, 180, 360)], soft=1.6, cast=1)
    arm(s, skin, skin, (20, 30), (16.5, 35), (16, 40), r=3.4, glove=ramp('#5a3a2a'), hand_r=2.5)
    s.part(fur, [('chord', 19.5, 31, 6, 5, 180, 360)], soft=1.6, cast=1)
    head(s)
    bangs(s, ramp('#a04a2a', 1.0), 'spiky', shine=9)
    s.part(P['steel'], [('chord', 28, 14, 12, 7, 180, 360), ('rect', 15.5, 12, 40.5, 14.5)], soft=1, gloss=1, cast=2)   # helmet
    s.part(ramp('#f0e8d0', .7), [('poly', [(16, 11), (9, 3), (8, 8), (14, 14)]), ('poly', [(40, 11), (47, 3), (48, 8), (42, 14)])], soft=.6, gloss=.8)   # horns
    face(s, '#3a7ab0')
    return s


def chieftain():
    s = Spr()
    pelt, gold, skin, paint = ramp('#5a4a3a', 1.2), P['gold'], ramp('#c88a60', .9), ramp('#3a7ad0', 1.1)
    cape(s, ramp('#6a6a72', 1.2), 1.5, 53)   # wolf pelt
    legs(s, ramp('#3a2a20'), ramp('#2a1a10'))
    torso(s, skin, hem=44)
    with s.grp('body'):
        s.part(skin, [('poly', [(18, 29), (38, 29), (37.5, 41), (18.5, 41)])], soft=2, cast=1)
        s.part(paint, [('poly', [(22, 31), (34, 31), (28, 37)])], soft=.4, line=False)
        s.part(pelt, [('poly', [(18.5, 40), (37.5, 40), (39, 48), (28, 49.5), (17, 48)])], soft=1.4)
        for i in range(6):   # bone necklace
            s.part(ramp('#f0e8d0', .7), [('ell', 22 + i * 2.4, 30 + abs(i - 2.5) * -.5 + 1.5, .9, 1.3)], soft=.3, line=False)
    belt(s, gold, 40, ramp('#d03030'))
    axe(s, ramp('#4a3020', 1.1), ramp('#d8dce8', 1.3), 42, 42, 45, 9, 1.25)
    arm(s, skin, skin, (36.5, 30), (40.5, 36), (42.5, 41), r=3.6, glove=gold, hand_r=2.6)
    s.part(pelt, [('chord', 37, 31, 6.5, 5.5, 180, 360)], soft=1.6, cast=1)
    arm(s, skin, skin, (19.5, 30), (16, 35), (15.5, 40), r=3.6, glove=gold, hand_r=2.6)
    s.part(pelt, [('chord', 19, 31, 6.5, 5.5, 180, 360)], soft=1.6, cast=1)
    head(s)
    bangs(s, ramp('#e8e0d0', .8), 'spiky', shine=10)
    s.part(ramp('#e8e0d0', .8), [('poly', [(21, 25), (35, 25), (33, 33), (30, 37), (28, 34), (26, 37), (23, 33)])], soft=1)   # braided beard
    s.part(gold, [('ell', 26, 34.5, .9, .9), ('ell', 30, 34.5, .9, .9)], soft=.2, line=False)
    s.part(paint, [('rect', 19, 17.5, 37, 18.6)], soft=.2, line=False)
    face(s, '#3a7ad0')
    for x, y in ((6, 22), (51, 30)):
        sparkle(s, x, y, (255, 210, 150))
    return s


NEWCLASSES2 = dict(shadowstep=shadowstep, phantomblade=phantomblade, riftcaller=riftcaller, eclipsewitch=eclipsewitch,
                   thornweaver=thornweaver, galecaller=galecaller, axebrute=axebrute, chieftain=chieftain)
