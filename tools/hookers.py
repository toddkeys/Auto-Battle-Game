"""Designs for the Hooker class (original characters): harbour folk who hook enemies and drag them in."""
from kit import *  # noqa: F401,F403  (shared body pieces + palettes)
from classes import sparkle
from pixel import Spr, ramp


def harpooner():
    # lanky harbour harpooner: yellow oilskin coat and sou'wester hat, a barbed harpoon on a rope
    s = Spr()
    oil, navy, rope, steel = ramp('#e8c23a', 1.1, 1.1), ramp('#2a3a5a', 1.1), ramp('#c8a06a', .9), P['steel']
    legs(s, navy, ramp('#3a2a20'))
    torso(s, oil, hem=46)
    with s.grp('body'):
        s.part(ramp('#d0aa2a', 1.1), [('rect', 27.3, 29, 28.7, 46)], soft=.4)   # coat seam
        for y in (32, 36, 40):
            s.part(ramp('#5a4a2a'), [('ell', 29.8, y, .7, .7)], soft=.2, line=False, flat=True)   # toggles
    belt(s, ramp('#5a3a22'), 41, steel)
    with s.grp('weapon'):   # harpoon held upright, rope coiled at the hand
        s.part(P['wood'], [('cap', 41, 50, 44.5, 14, .9)], soft=.5)
        s.part(steel, [('poly', [(43.2, 15), (45.8, 15), (45, 6), (44.3, 5)]), ('poly', [(43.4, 14.5), (40.6, 12), (43.6, 12.6)]),
                       ('poly', [(45.6, 14.5), (48.4, 12), (45.4, 12.6)])], soft=.4, gloss=1.2)
        s.part(rope, [('ell', 41.5, 44, 3.2, 2.2)], sub=[('ell', 41.5, 44, 2, 1.1)], soft=.4, line=False)
    arm(s, oil, SKIN, (35, 30), (38.5, 36), (41.5, 40), glove=ramp('#3a3a3a'))
    arm(s, oil, SKIN, (21, 30), (18.5, 35), (18, 39.5), glove=ramp('#3a3a3a'))
    head(s)
    bangs(s, ramp('#6a4a2a'), 'neat', shine=10)
    s.part(oil, [('ell', 28, 12.5, 14.5, 3.4)], soft=1, cast=2)   # sou'wester brim
    s.part(oil, [('chord', 28, 12.5, 10, 8, 180, 360)], soft=1.6, cast=2)
    s.part(ramp('#c8a02a'), [('rect', 18.5, 10.5, 37.5, 12.5)], soft=.4)
    face(s, '#3a6a8a')
    sparkle(s, 48, 8, (230, 240, 255))
    return s


def anchorbrute():
    # hulking dock brute: bald and red-bearded, striped sailor shirt, leather vest, an anchor-shaped hook on a chain
    s = Spr()
    shirt, stripe, vest, skin, beard = ramp('#e8e4dc', .8), ramp('#2a4a8a', 1.1), ramp('#6a4a32', 1.1), ramp('#e0a880', .9), ramp('#b04a2a', 1.0)
    iron = ramp('#7a8090', 1.3)
    legs(s, ramp('#2a3040'), ramp('#2a2018'))
    torso(s, shirt, hem=45)
    with s.grp('body'):
        s.part(shirt, [('poly', [(17.5, 29), (38.5, 29), (38, 42), (18, 42)])], soft=2, cast=1)   # barrel chest
        for y in (31, 34.5, 38):
            s.part(stripe, [('rect', 18, y, 38, y + 1.5)], soft=.3, line=False)
        s.part(vest, [('poly', [(17.5, 29), (24, 29), (22.5, 43), (17.5, 43)]), ('poly', [(32, 29), (38.5, 29), (38.5, 43), (33.5, 43)])], soft=1.2)
    belt(s, ramp('#3a2a1a'), 41, iron)
    with s.grp('weapon'):   # chain hanging from the hand down to an anchor-shaped hook
        for i in range(5):
            s.part(iron, [('ell', 43 + i * .4, 40 + i * 2.2, .9, 1.1)], sub=[('ell', 43 + i * .4, 40 + i * 2.2, .35, .5)], soft=.3, line=False)
        s.part(iron, [('cap', 45, 49, 45, 52, .8), ('line', [(40.5, 49.5), (41.5, 52.5), (45, 53.4), (48.5, 52.5), (49.5, 49.5)], .8),
                      ('poly', [(39.6, 49), (41.6, 48.8), (40.4, 47.2)]), ('poly', [(50.4, 49), (48.4, 48.8), (49.6, 47.2)])], soft=.4, gloss=1.2)
    arm(s, skin, skin, (36, 30), (40, 35.5), (42.5, 39.5), r=3.6, glove=ramp('#4a3a2a'), hand_r=2.6)
    arm(s, skin, skin, (20, 30), (16.5, 35), (16, 40), r=3.6, glove=ramp('#4a3a2a'), hand_r=2.6)
    s.part(ramp('#3a5a9a'), [('ell', 26.5, 34.8, 1.8, 1.2)], soft=.3, line=False, flat=True)   # anchor tattoo on the forearm area
    head(s, skin)
    s.part(skin, [('chord', 28, 15, 10.5, 9.5, 180, 360)], soft=2, gloss=.6, cast=1)   # bald head
    s.part(beard, [('poly', [(19, 21), (37, 21), (36, 27), (32, 30.5), (28, 31.5), (24, 30.5), (20, 27)])], sub=[('ell', 27, 24.6, 3, 1.4)], soft=1.6, cast=1)
    s.part(ramp('#2a2a32'), [('rect', 17.5, 13.5, 38.5, 15)], soft=.3)   # knotted headband
    s.part(ramp('#2a2a32'), [('poly', [(38, 13.5), (44, 12), (43, 16), (38, 15)])], soft=.4)
    face(s, '#5a7a9a', None, blush=False)
    return s


HOOKERS = dict(harpooner=harpooner, anchorbrute=anchorbrute)
