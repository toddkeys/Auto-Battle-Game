"""Designs for the Bard, Alchemist, Necromancer, Engineer, Monk and Chrono classes (original characters)
and the Engineer's turret."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import hem_trim, sparkle
from pixel import Spr, ramp


# ====== bards ======
def minstrel():
    s = Spr()
    coat, green, gold = ramp('#e07a3a', 1.1), ramp('#3a9a5a', 1.1), P['gold']
    legs(s, ramp('#3a5a4a'), P['leather'])
    torso(s, coat, hem=45)
    hem_trim(s, gold, 44)
    s.part(green, [('poly', [(25, 29), (31, 29), (30, 40), (26, 40)])], soft=.8)
    belt(s, P['darkleather'], 40, gold)
    with s.grp('weapon'):   # a lute held across the body
        s.part(P['wood'], [('ell', 38, 41, 5, 4.2)], soft=1.2, gloss=.8)
        s.part(ramp('#5a3020'), [('ell', 38, 41, 1.5, 1.5)], soft=.4, line=False)
        s.part(P['wood'], [('cap', 41, 38, 48, 28, 1.1)], soft=.6)
        s.part(P['string'], [('cap', 36, 43, 47, 29, .3)], soft=.3, line=False, thr=.3)
    arm(s, coat, SKIN, (35, 30), (38.5, 36), (40, 41))
    arm(s, coat, SKIN, (21, 30), (18.5, 35), (17.5, 39))
    head(s)
    bangs(s, ramp('#e8b860', 1.0), 'swept', shine=10)
    s.part(green, [('chord', 28, 12, 13, 5, 180, 360), ('rect', 15, 11, 41, 13)], soft=1, cast=2)   # feathered cap
    s.part(ramp('#ff5a4a'), [('poly', [(37, 10), (49, 2), (46, 8), (40, 12)])], soft=.6)
    face(s, '#3a9a5a', 'smile')
    for x, y in ((8, 20), (50, 16)):
        sparkle(s, x, y, (255, 220, 140))
    return s


def piper():   # 1-gold bard: a travelling flute player
    s = Spr()
    tunic, patch, gold = ramp('#3a8ab8', 1.1), ramp('#e8c45a', 1.0), P['gold']
    legs(s, ramp('#6a4a32'), P['leather'])
    torso(s, tunic, hem=44)
    s.part(patch, [('rect', 21.5, 33, 25.5, 37), ('rect', 30.5, 38, 34.5, 42)], soft=.6)   # patched tunic
    belt(s, P['darkleather'], 39, P['steel'])
    s.part(ramp('#b84a3a'), [('ell', 28, 28.5, 8, 2.6)], soft=1, cast=1)   # scarf
    with s.grp('weapon'):   # a wooden flute held out to the side
        s.part(P['wood'], [('cap', 33, 37, 47, 27, 1.0)], soft=.5, gloss=.5)
        for i in range(3):
            s.part(ramp('#3a2014'), [('ell', 39 + i * 2.3, 32.6 - i * 1.65, .5, .5)], soft=.2, line=False, flat=True)
    arm(s, tunic, SKIN, (35, 30), (37.5, 35.5), (39, 33.5))
    arm(s, tunic, SKIN, (21, 30), (18.5, 35), (18, 39))
    head(s)
    bangs(s, ramp('#b0602e', 1.0), 'neat', shine=9)
    s.part(ramp('#5a3a7a', 1.1), [('ell', 26, 10.5, 12.5, 4.5), ('rect', 16, 10, 37, 13)], soft=1.2, cast=2)   # floppy beret
    s.part(ramp('#f2f2f2', .8), [('poly', [(35, 9), (44, 1.5), (42, 7.5), (37, 11)])], soft=.5)   # feather
    face(s, '#3a8ab8', 'smile')
    for x, y in ((49, 22), (51, 30)):
        sparkle(s, x, y, (180, 230, 255))
    return s

def dancer():
    s = Spr()
    silk, rose, gold = ramp('#e84a8a', 1.1, 1.1), ramp('#ffc0d8', .8), P['gold']
    back_hair(s, ramp('#3a1a2a', 1.2), 40, 12)
    legs(s, silk, ramp('#c03a6a'), robe=True)
    torso(s, silk, 'robe', hem=50)
    hem_trim(s, gold, 48)
    s.part(rose, [('poly', [(14, 34), (21, 33), (20, 50), (12, 47)]), ('poly', [(35, 33), (42, 34), (44, 47), (36, 50)])], soft=1)   # trailing veils
    belt(s, gold, 38, ramp('#7fd4ff', 1.2))
    with s.grp('weapon'):   # folding fan
        s.part(ramp('#fff0f6', .7), [('poly', [(41, 40), (36, 30), (41, 28), (46, 29), (49, 33)])], soft=.6, gloss=.6)
        s.part(silk, [('poly', [(41, 40), (38, 31), (41, 30)])], soft=.3, line=False)
    arm(s, silk, SKIN, (35, 30), (38.5, 35.5), (41, 39.5), r=2.4)
    arm(s, silk, SKIN, (21, 30), (17, 33), (14, 30), r=2.4)
    head(s)
    bangs(s, ramp('#3a1a2a', 1.2), 'long', shine=10)
    s.part(gold, [('rect', 18, 12, 38, 13.4)], soft=.4, gloss=1, cast=1)
    s.part(ramp('#ff8ab8'), [('ell', 37, 11, 3, 2.5)], soft=.8, gloss=1)   # flower
    face(s, '#d04a8a', 'smile')
    return s


# ====== alchemists ======
def apothecary():
    s = Spr()
    coat, apron, glass = ramp('#4a7a5a', 1.1), ramp('#e8dcc0', .8), ramp('#7af06a', 1.2, 1.2)
    legs(s, ramp('#3a3a3a'), P['leather'])
    torso(s, coat, hem=46)
    s.part(apron, [('poly', [(23, 31), (33, 31), (34, 46), (22, 46)])], soft=.8)
    belt(s, P['darkleather'], 38, P['gold'])
    for x, c in ((24, '#ff6a6a'), (28, '#6ab0ff'), (32, '#ffd24a')):   # vials on the belt
        s.part(ramp(c, 1.2, 1.1), [('rect', x - .9, 38.5, x + .9, 42)], soft=.3, gloss=1, line=False)
    with s.grp('weapon'):   # round flask
        s.part(glass, [('ell', 42, 37, 3.6, 3.6), ('rect', 41, 31.5, 43, 34)], soft=.8, gloss=1.4)
        s.part(ramp('#c8a070'), [('rect', 40.6, 30.5, 43.4, 32)], soft=.3)
    arm(s, coat, SKIN, (35, 30), (38.5, 36), (41, 40.5))
    arm(s, coat, SKIN, (21, 30), (18.5, 35), (18, 39))
    head(s)
    bangs(s, ramp('#6a4a3a', 1.1), 'neat', shine=10)
    s.part(ramp('#c8e0ff', .8), [('ell', 24, 21, 2.6, 2.2), ('ell', 32, 21, 2.6, 2.2)], soft=.4, line=False, flat=True, bias=.3)   # goggles
    s.part(ramp('#8a6a3a'), [('rect', 16, 12, 40, 14.5)], soft=.5, cast=1)
    face(s, '#3a8a5a', 'smile')
    return s


def merchant():
    s = Spr()
    robe, gold, purple = ramp('#7a3a9a', 1.2, 1.1), P['gold'], ramp('#4a2a6a', 1.2)
    cape(s, purple, 1.2, 52)
    legs(s, robe, ramp('#3a2030'), robe=True)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, gold, 48)
    belt(s, gold, 39, ramp('#ff5a5a', 1.2))
    with s.grp('weapon'):   # a sack of gold
        s.part(ramp('#c8a060', 1.1), [('ell', 43, 41, 4.5, 4.8), ('poly', [(41, 36), (45, 36), (44, 38), (42, 38)])], soft=1, gloss=.4)
        s.part(gold, [('ell', 43, 41.5, 1.6, 1.6)], soft=.3, gloss=1, line=False)
    arm(s, robe, SKIN, (35, 30), (38.5, 35), (42, 37))
    arm(s, robe, SKIN, (21, 30), (17.5, 35), (15, 38))
    s.part(gold, [('ell', 14, 39, 2.2, 2.2), ('ell', 11, 37, 1.8, 1.8)], soft=.4, gloss=1.2)   # coins in the other hand
    head(s)
    bangs(s, ramp('#3a2a2a', 1.2), 'swept', shine=10)
    s.part(purple, [('chord', 28, 13, 12.5, 7, 180, 360), ('rect', 15.5, 11.5, 40.5, 14)], soft=1, gloss=.6, cast=2)   # turban
    s.part(gold, [('ell', 28, 10.5, 2, 2)], soft=.4, gloss=1.2)
    face(s, '#7a3a9a', 'smile')
    for x, y in ((7, 22), (50, 26)):
        sparkle(s, x, y, (255, 225, 120))
    return s


# ====== necromancers ======
def gravecaller():
    s = Spr()
    robe, bone, ghost = ramp('#3a3a4a', 1.2), ramp('#e8e0cc', .8), ramp('#8a7aff', 1.2, 1.2)
    legs(s, robe, ramp('#2a2a32'), robe=True)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, ghost, 48)
    belt(s, ramp('#5a4a3a'), 38, bone)
    staff(s, ramp('#6a5a4a', 1.1), 42, 52, 43, 14, .9)
    s.part(bone, [('ell', 43, 11, 3.6, 3.4), ('rect', 41.4, 12.5, 44.6, 15)], soft=.8, gloss=.6)   # skull on the staff
    s.part(ghost, [('ell', 41.8, 11, .9, .9), ('ell', 44.2, 11, .9, .9)], soft=.2, line=False, flat=True, bias=.3)
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40))
    arm(s, robe, SKIN, (21, 30), (18, 35), (17, 38))
    head(s)
    bangs(s, ramp('#d8d8e8', .9), 'long', shine=10)
    s.part(robe, [('chord', 28, 17, 13.5, 13.5, 180, 360), ('poly', [(14.5, 17), (18.5, 17), (19, 30), (14, 31)]),
                  ('poly', [(37.5, 17), (41.5, 17), (42, 31), (37, 30)])], sub=[('ell', 28, 20, 9.5, 8.5)], soft=2.5, cast=2)   # hood
    face(s, '#8a7aff')
    for x, y in ((8, 26), (50, 30)):
        sparkle(s, x, y, (180, 170, 255))
    return s


def bonelord():
    s = Spr()
    plate, bone, ghost, red = ramp('#2a2a3a', 1.3), ramp('#e8e0cc', .8), ramp('#8a7aff', 1.2, 1.2), ramp('#a02040')
    cape(s, ramp('#3a1a3a', 1.2), 1.5, 53)
    legs(s, plate, ramp('#1a1a24'))
    torso(s, plate, hem=46)
    s.part(bone, [('poly', [(22, 30), (34, 30), (32, 38), (24, 38)])], soft=1, gloss=.6)   # ribcage plate
    for y in (32, 34.5):
        s.part(plate, [('rect', 23.5, y, 32.5, y + .8)], soft=.2, line=False)
    belt(s, red, 40, bone)
    staff(s, ramp('#4a3a4a', 1.2), 42, 52, 43, 10, 1)
    s.part(ghost, [('ell', 43, 8, 3.4, 3.4)], soft=.6, gloss=1.4)   # soul orb
    s.part(bone, [('poly', [(39, 9), (40.5, 3), (42, 8)]), ('poly', [(44, 8), (45.5, 3), (47, 9)])], soft=.4)
    arm(s, plate, plate, (35, 30), (39, 36), (42.5, 40), r=2.9, glove=bone)
    s.part(bone, [('chord', 36, 31, 5.5, 4.6, 180, 360)], soft=1.2, gloss=.6, cast=1)
    arm(s, plate, plate, (21, 30), (18, 35), (17, 39), r=2.9, glove=bone)
    s.part(bone, [('chord', 20, 31, 5.5, 4.6, 180, 360)], soft=1.2, gloss=.6, cast=1)
    head(s)
    bangs(s, ramp('#1a1a24', 1.3), 'spiky', shine=10)
    s.part(bone, [('poly', [(17, 12), (20, 4), (23, 10), (28, 2), (33, 10), (36, 4), (39, 12)])], soft=.6, gloss=.6, cast=1)   # bone crown
    face(s, '#a02040')
    for x, y in ((6, 24), (50, 36), (9, 44)):
        sparkle(s, x, y, (170, 150, 255))
    return s


# ====== engineers ======
def tinkerer():
    s = Spr()
    overall, shirt, brass = ramp('#4a6aa0', 1.1), ramp('#e8d8b0', .8), ramp('#d8a040', 1.2, 1.1)
    legs(s, overall, P['darkleather'])
    torso(s, shirt, hem=44)
    s.part(overall, [('poly', [(22, 33), (34, 33), (35, 45), (21, 45)]), ('rect', 23, 29, 25, 33), ('rect', 31, 29, 33, 33)], soft=1)
    belt(s, P['leather'], 40, brass)
    with s.grp('weapon'):   # big wrench
        s.part(P['steel'], [('cap', 42, 43, 46, 28, 1.1), ('poly', [(43, 28), (49, 26), (49, 23), (46.5, 24.5), (45, 22), (43, 24.5)])], soft=.6, gloss=1)
    arm(s, shirt, SKIN, (35, 30), (38.5, 36), (42, 40), glove=P['leather'])
    arm(s, shirt, SKIN, (21, 30), (18.5, 35), (18, 39), glove=P['leather'])
    head(s)
    bangs(s, ramp('#d8703a', 1.0), 'neat', shine=9)
    s.part(brass, [('rect', 17, 12, 39, 14)], soft=.4, cast=1)
    s.part(ramp('#9ad8ff', 1.1), [('ell', 23, 11.5, 2.8, 2.6), ('ell', 33, 11.5, 2.8, 2.6)], soft=.5, gloss=1.2)   # goggles on the forehead
    face(s, '#3a7ad0', 'smile')
    return s


def engineer():
    s = Spr()
    coat, brass, dark = ramp('#8a5a2a', 1.1), ramp('#d8a040', 1.2, 1.1), ramp('#3a3a42', 1.2)
    legs(s, dark, P['darkleather'])
    torso(s, coat, hem=46)
    s.part(brass, [('rect', 27, 29, 29, 46)], soft=.4, gloss=1, line=False)
    belt(s, dark, 39, brass)
    with s.grp('weapon'):   # hand cannon, barrel pointing forward across the body
        s.part(P['steel'], [('rect', 33, 36, 44, 40)], soft=.6, gloss=1.2)
        s.part(brass, [('rect', 31, 35, 34, 41), ('rect', 40.5, 39, 43.5, 44)], soft=.4, gloss=1)
    arm(s, coat, SKIN, (35, 30), (38.5, 36), (42, 40), glove=dark)
    arm(s, coat, SKIN, (21, 30), (18.5, 35), (18, 39), glove=dark)
    head(s)
    bangs(s, ramp('#3a2a20', 1.2), 'neat', shine=10)
    s.part(dark, [('chord', 28, 13, 12, 6, 180, 360), ('rect', 14, 11.5, 42, 13.5)], soft=1, gloss=.6, cast=2)   # cap
    s.part(ramp('#9ad8ff', 1.1), [('ell', 32, 21, 2.6, 2.4)], soft=.4, gloss=1.2)   # monocle lens
    face(s, '#d0802a')
    return s


def turret():
    s = Spr()
    steel, brass, dark = P['steel'], ramp('#d8a040', 1.2, 1.1), ramp('#3a3a42', 1.2)
    s.piv.update(head=(28, 30))
    with s.grp('body'):   # tripod base
        s.part(dark, [('cap', 28, 38, 18, 52, 1.6), ('cap', 28, 38, 38, 52, 1.6), ('cap', 28, 38, 28, 52, 1.6)], soft=.6)
        s.part(brass, [('ell', 28, 38, 6, 3.2)], soft=1, gloss=1)
    with s.grp('head'):   # the gun turns with the head
        s.part(steel, [('ell', 28, 30, 8, 7)], soft=1.5, gloss=1.2, cast=1)
        s.part(steel, [('rect', 12, 27.5, 24, 32)], soft=.6, gloss=1)
        s.part(dark, [('rect', 10, 28, 13, 31.5)], soft=.3)
        s.part(ramp('#ff5a3a', 1.2, 1.2), [('ell', 30, 29, 2, 2)], soft=.4, gloss=1.4, line=False)
    return s


# ====== monks ======
def brawler():
    s = Spr()
    gi, sash = ramp('#f0e8d8', .8), ramp('#d84a2a', 1.1)
    legs(s, gi, ramp('#2a2a2a'))
    torso(s, gi, hem=44)
    s.part(SKIN, [('poly', [(26, 28.5), (30, 28.5), (28, 35)])], soft=.6, line=False)   # open collar
    belt(s, sash, 39)
    s.part(sash, [('poly', [(30, 40), (34, 40), (36, 46), (33, 45)])], soft=.6)
    arm(s, SKIN, SKIN, (35, 30), (38.5, 35.5), (41.5, 39), r=2.8, glove=ramp('#e8e0d0', .7), hand_r=2.5)
    arm(s, SKIN, SKIN, (21, 30), (18, 34.5), (17, 38.5), r=2.8, glove=ramp('#e8e0d0', .7), hand_r=2.5)
    head(s)
    bangs(s, ramp('#2a2a2a', 1.3), 'spiky', shine=10)
    s.part(sash, [('rect', 16.5, 12.5, 39.5, 14.5), ('poly', [(16, 13), (9, 17), (11, 19), (17, 15)])], soft=.6)   # headband
    face(s, '#8a4a2a', 'open')
    return s


def grandmaster():
    s = Spr()
    robe, gold, beads = ramp('#e8a030', 1.2, 1.1), P['gold'], ramp('#6a3a2a', 1.1)
    legs(s, robe, ramp('#5a3a2a'), robe=True)
    torso(s, robe, 'robe', hem=50)
    s.part(ramp('#a02a2a', 1.1), [('poly', [(21, 29), (25, 29), (35.5, 44), (31.5, 45)])], soft=.8)   # sash over the shoulder
    for i in range(7):   # prayer beads
        s.part(beads, [('ell', 22 + i * 2, 29.5 + i * .3 + (i % 2) * .4, 1.1, 1.1)], soft=.3, gloss=1, line=False)
    belt(s, ramp('#a02a2a', 1.1), 40, gold)
    arm(s, robe, SKIN, (35, 30), (38.5, 35.5), (41.5, 39), r=3, hand_r=2.5)
    arm(s, robe, SKIN, (21, 30), (18, 34), (19, 31), r=3, hand_r=2.5)
    head(s)
    s.part(SKIN, [('ell', 28, 15, 11, 9)], soft=2, gloss=.8, cast=2)   # shaved head
    s.part(ramp('#f0f0f0', .7), [('poly', [(23, 26), (33, 26), (31, 33), (28, 35), (25, 33)])], soft=1)   # long beard
    for x in (25, 28, 31):
        s.part(gold, [('ell', x, 9.5, .8, .8)], soft=.2, line=False)
    face(s, '#6a4a2a')
    for x, y in ((8, 22), (49, 20)):
        sparkle(s, x, y, (255, 220, 140))
    return s


# ====== chrono ======
def chronomancer():
    s = Spr()
    robe, teal, gold = ramp('#2a5a7a', 1.2), ramp('#7fe0e0', 1.2, 1.1), P['gold']
    legs(s, robe, ramp('#1a3040'), robe=True)
    torso(s, robe, 'robe', hem=50)
    hem_trim(s, teal, 48)
    belt(s, gold, 38, teal)
    staff(s, ramp('#c8b080', 1.1), 42, 52, 43, 15, .9)
    s.part(gold, [('ell', 43, 11, 4, 4)], sub=[('ell', 43, 11, 3, 3)], soft=.5, gloss=1)   # clock ring
    s.part(ramp('#f0fbff', .7), [('ell', 43, 11, 3, 3)], soft=.4, line=False)
    s.part(ramp('#2a3a4a'), [('cap', 43, 11, 43, 8.8, .35), ('cap', 43, 11, 44.8, 11.6, .35)], soft=.2, line=False)
    arm(s, robe, SKIN, (35, 30), (39, 36), (42.5, 40))
    arm(s, robe, SKIN, (21, 30), (18, 35), (17, 38))
    head(s)
    bangs(s, ramp('#e0e8f0', .9), 'swept', shine=10)
    s.part(teal, [('rect', 17, 12, 39, 13.5)], soft=.4, gloss=1, cast=1)
    face(s, '#2ab0b0')
    for x, y in ((8, 20), (50, 28), (10, 40)):
        sparkle(s, x, y, (180, 255, 255))
    return s


def timekeeper():
    s = Spr()
    coat, teal, gold = ramp('#1f3a5a', 1.2), ramp('#7fe0e0', 1.2, 1.1), P['gold']
    cape(s, ramp('#14283c', 1.2), 1.4, 53)
    legs(s, coat, ramp('#101c2a'))
    torso(s, coat, hem=47)
    hem_trim(s, gold, 46)
    s.part(gold, [('ell', 28, 35, 4.2, 4.2)], sub=[('ell', 28, 35, 3.2, 3.2)], soft=.5, gloss=1)   # clockface on the chest
    s.part(ramp('#f0fbff', .7), [('ell', 28, 35, 3.2, 3.2)], soft=.4, line=False)
    s.part(ramp('#2a3a4a'), [('cap', 28, 35, 28, 32.5, .35), ('cap', 28, 35, 30, 36, .35)], soft=.2, line=False)
    belt(s, gold, 41, teal)
    with s.grp('weapon'):   # hourglass held up
        s.part(gold, [('rect', 39, 30, 47, 31.5), ('rect', 39, 40, 47, 41.5)], soft=.4, gloss=1)
        s.part(ramp('#e8fbff', .6), [('poly', [(40, 31.5), (46, 31.5), (43.4, 35.7), (46, 40), (40, 40), (42.6, 35.7)])], soft=.6, gloss=1.2)
        s.part(ramp('#ffd27a', 1.1), [('poly', [(41.2, 38), (44.8, 38), (46, 40), (40, 40)]), ('rect', 42.7, 35.5, 43.3, 38)], soft=.3, line=False)
    arm(s, coat, SKIN, (35, 30), (39, 36), (43, 41), glove=gold)
    arm(s, coat, SKIN, (21, 30), (18, 35), (17, 39), glove=gold)
    head(s)
    bangs(s, ramp('#2a3a5a', 1.2), 'long', shine=10)
    s.part(gold, [('rect', 17, 11.5, 39, 13)], soft=.4, gloss=1, cast=1)
    s.part(teal, [('ell', 28, 11.5, 2, 2)], soft=.4, gloss=1.2)
    face(s, '#2ab0b0')
    for x, y in ((6, 24), (51, 20), (8, 44)):
        sparkle(s, x, y, (180, 255, 255))
    return s


NEWCLASSES = dict(piper=piper, minstrel=minstrel, dancer=dancer, apothecary=apothecary, merchant=merchant, gravecaller=gravecaller,
                  bonelord=bonelord, tinkerer=tinkerer, mechanist=engineer, brawler=brawler, grandmaster=grandmaster,
                  chronomancer=chronomancer, timekeeper=timekeeper, turret=turret)
