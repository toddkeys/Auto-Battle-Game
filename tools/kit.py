"""Shared body kit for the anime-style unit sprites (original characters).
Build everything with:  python tools/build_sprites.py"""
from pixel import Spr, ramp

SKIN = ramp('#ffd2b0', 0.8)


def grouped(g):
    """Helper decorator: everything the helper draws joins rig group g."""
    def deco(fn):
        def wrap(s, *a, **k):
            with s.grp(g):
                return fn(s, *a, **k)
        return wrap
    return deco
WHITE = (255, 255, 255)
BLUSH = (255, 150, 160)


# ====== body ======
@grouped('head')
def back_hair(s, rp, length=26, width=11.5):
    s.part(rp, [('ell', 28, 17, width, 10), ('poly', [(28 - width + .5, 18), (28 + width - .5, 18),
                                                      (28 + width - 2, length), (28 - width + 2, length)])], soft=2)


def legs(s, pants, boots, robe=False):
    # one group per leg so they can step; hips are the joints
    s.piv.update(legL=(24.7, 40), legR=(31.7, 40))
    for g, pant, boot in (('legL', [(22, 39), (27.5, 39), (27, 49), (22.5, 49)],
                           [(21.5, 46), (27.5, 46), (27.5, 53), (19, 53), (19.5, 50.5), (21.5, 49.5)]),
                          ('legR', [(29, 39), (34.5, 39), (34, 49), (29.5, 49)],
                           [(29.5, 46), (35, 46), (35.5, 53), (28, 53), (28.5, 50.5), (29.5, 49.5)])):
        with s.grp(g):
            if not robe:
                s.part(pants, [('poly', pant)], soft=1.2)
            s.part(boots, [('poly', boot)], soft=1.0, gloss=0.4)


@grouped('body')
def torso(s, rp, kind='tunic', hem=43, soft=2.2):
    if kind == 'tunic':
        sh = [('poly', [(21, 28), (35, 28), (36.5, hem), (19.5, hem)])]
    else:  # robe
        sh = [('poly', [(21, 28), (35, 28), (39, hem), (37, hem + 1), (28, hem + 1.5), (19, hem + 1), (17, hem)])]
    s.part(rp, sh, soft=soft, cast=1)


def arm(s, sleeve, skin, sh, el, hd, r=2.6, glove=None, hand_r=2.1):
    g = s.group or ('armR' if sh[0] > 28 else 'armL')
    s.piv.setdefault(g, sh)
    s.hands.setdefault(g, hd)
    with s.grp(g):
        _arm(s, sleeve, skin, sh, el, hd, r, glove, hand_r)


def _arm(s, sleeve, skin, sh, el, hd, r, glove, hand_r):
    s.part(sleeve, [('cap', *sh, *el, r), ('cap', *el, *hd, r * 0.85)], soft=1.1)
    s.part(glove or skin, [('ell', hd[0], hd[1] + 1.2, hand_r, hand_r)], soft=0.8)


@grouped('head')
def head(s, skin=SKIN):
    s.part(skin, [('ell', 28, 18, 10, 9.5), ('ell', 25.5, 22, 7.5, 6.5),
                  ('ell', 37.2, 20.5, 1.6, 2.2)], soft=2.5)


EXPR = None   # set by build_sprites.py to render a face variant (see EXPRESSIONS)
EXPRESSIONS = ('angry', 'hurt', 'dizzy', 'shock', 'sil', 'blind', 'sick', 'happy', 'ko')


@grouped('head')
def face(s, iris, mouth='smile', shift=0, blush=True):
    """Big anime eyes (3x4) with lashes and a shine, looking down-left. kit.EXPR swaps in an expression."""
    s.face_part = len(s.parts) - 1   # the face marks live on this part's layer
    r = ramp(iris, 1.1, 1.2)
    dark, mid, light = r[1], r[3], r[4]
    lash = (40, 26, 30)
    if EXPR:
        return _expression(s, EXPR, dark, mid, light, lash, mouth, shift, blush)
    for k, ex in enumerate((20 + shift, 27 + shift)):
        for dx in range(3):
            s.mark(ex + dx, 19, lash)
        s.mark(ex - 1 if k == 0 else ex + 3, 19 if k else 20, lash)  # outer lash flick
        s.mark(ex, 20, WHITE); s.mark(ex + 1, 20, dark); s.mark(ex + 2, 20, dark)
        s.mark(ex, 21, mid); s.mark(ex + 1, 21, mid); s.mark(ex + 2, 21, dark)
        s.mark(ex, 22, light); s.mark(ex + 1, 22, light); s.mark(ex + 2, 22, mid)
    if blush:
        for x in (19 + shift, 20 + shift, 30 + shift, 31 + shift):
            s.mark(x, 23, BLUSH)
    if mouth == 'smile':
        s.mark(24 + shift, 25, (150, 70, 70)); s.mark(25 + shift, 25, (190, 90, 90))
    elif mouth == 'open':
        s.mark(24 + shift, 25, (150, 60, 60)); s.mark(25 + shift, 25, (150, 60, 60))
        s.mark(24 + shift, 26, (230, 120, 120)); s.mark(25 + shift, 26, (230, 120, 120))


def _expression(s, e, dark, mid, light, lash, mouth, shift, blush):
    """Pixel faces for battle moments. Eyes sit at x=ex..ex+2, y=19..22; the mouth near (24..25, 25..26)."""
    M = lambda pts, c: [s.mark(x, y, c) for x, y in pts]
    MOUTH = (110, 40, 50)
    for k, ex in enumerate((20 + shift, 27 + shift)):
        inner = ex + 2 if k == 0 else ex          # the eye corner nearer the nose
        outer = ex if k == 0 else ex + 2
        if e == 'angry':                          # narrowed, brows pulled down at the middle
            M([(ex, 19), (ex + 1, 19), (ex + 2, 19), (inner, 20)], lash)
            M([(ex + 1, 20)], lash)
            M([(ex, 21), (ex + 1, 21), (ex + 2, 21)], dark); M([(ex, 22), (ex + 1, 22), (ex + 2, 22)], mid)
            M([(outer, 21)], WHITE)
        elif e == 'hurt':                         # > <
            M([(outer, 19), (ex + 1, 20), (inner, 20), (outer, 21)], lash)
        elif e == 'dizzy':                        # @ @
            M([(ex, 19), (ex + 1, 19), (ex + 2, 19), (ex, 20), (ex + 2, 20), (ex, 21), (ex + 1, 21), (ex + 2, 21)], lash)
            M([(ex + 1, 20)], mid)
        elif e == 'shock':                        # wide white eyes, tiny pupils
            M([(ex, 19), (ex + 1, 19), (ex + 2, 19)], lash)
            M([(x, y) for x in range(ex, ex + 3) for y in (20, 21, 22)], WHITE); M([(ex + 1, 21)], (30, 30, 50))
        elif e == 'sil':                          # worried eyes (inner brow raised)
            M([(outer, 20), (ex + 1, 19), (inner, 18)], lash)
            M([(ex, 21), (ex + 1, 21), (ex + 2, 21)], dark); M([(ex, 22), (ex + 1, 22), (ex + 2, 22)], light)
        elif e == 'blind':                        # shut tight
            M([(ex, 21), (ex + 1, 21), (ex + 2, 21), (outer, 20)], lash)
        elif e == 'sick':                         # droopy, green under the eyes
            M([(ex, 20), (ex + 1, 20), (ex + 2, 20)], lash)
            M([(ex, 21), (ex + 1, 21), (ex + 2, 21)], mid); M([(ex, 22), (ex + 1, 22), (ex + 2, 22)], (120, 190, 110))
        elif e == 'happy':                        # ^ ^
            M([(ex, 21), (ex + 1, 20), (ex + 2, 21)], lash)
        elif e == 'ko':                           # x x
            M([(ex, 19), (ex + 2, 19), (ex + 1, 20), (ex, 21), (ex + 2, 21)], lash)
    if blush and e in ('angry', 'happy', 'hurt', 'shock'):
        M([(19 + shift, 23), (20 + shift, 23), (30 + shift, 23), (31 + shift, 23)], BLUSH if e != 'shock' else (170, 210, 240))
    if e == 'hurt':
        M([(35 + shift, 16), (35 + shift, 17), (36 + shift, 17)], (150, 210, 255))   # sweat drop
    if e == 'dizzy':
        M([(16 + shift, 14), (39 + shift, 13)], (255, 230, 120))
    if not mouth:                                 # masked face: only the eyes change
        return
    x = 24 + shift
    if e == 'angry':
        M([(x - 1, 25), (x, 25), (x + 1, 25), (x + 2, 25)], MOUTH); M([(x, 26), (x + 1, 26)], (230, 110, 110))
    elif e == 'hurt':
        M([(x - 1, 25), (x + 2, 25)], MOUTH); M([(x, 25), (x + 1, 25)], WHITE)
    elif e in ('dizzy', 'sick'):
        M([(x - 1, 26), (x, 25), (x + 1, 26), (x + 2, 25)], MOUTH)
    elif e == 'shock':
        M([(x, 25), (x + 1, 25), (x, 26), (x + 1, 26)], MOUTH)
    elif e == 'sil':
        M([(x - 1, 24), (x + 1, 24), (x, 25), (x - 1, 26), (x + 1, 26)], (120, 60, 160))
    elif e == 'blind':
        M([(x, 25), (x + 1, 25)], MOUTH)
    elif e == 'happy':
        M([(x - 1, 25), (x, 25), (x + 1, 25), (x + 2, 25)], MOUTH); M([(x, 26), (x + 1, 26)], (240, 130, 130))
    elif e == 'ko':
        M([(x - 1, 26), (x, 25), (x + 1, 25), (x + 2, 26)], MOUTH)


HAIR = {
    # wind-swept clumps leaning right instead of a crown of spikes
    'tousled': [('ell', 28, 15, 11.8, 9.5),
                ('poly', [(16.3, 13), (16.5, 22), (18.5, 16.5), (20.5, 18.5), (22, 15), (24.5, 18), (26.5, 14.5),
                          (29.5, 17.8), (31, 14.5), (34, 18), (35.5, 15), (38, 18.5), (39.8, 23), (39.8, 13)]),
                ('poly', [(18, 9), (19.5, 3), (24, 6)]), ('poly', [(23, 6), (27, 1.5), (30, 5.5)]),
                ('poly', [(29, 5.5), (35.5, 2.5), (35.5, 8)]), ('poly', [(35, 7.5), (42, 8), (39.5, 13)]),
                ('poly', [(39.5, 12.5), (44, 16.5), (39.8, 19)]), ('poly', [(17, 11), (12.5, 14), (16.5, 17.5)])],
    'spiky': [('chord', 28, 16.5, 12, 11.5, 175, 365),
              ('poly', [(16.5, 16), (18, 22), (20, 17.5), (22, 20.5), (24, 16.5), (26.5, 20), (28, 16.5),
                        (31, 20.5), (32, 16.5), (35, 20), (36, 16.5), (39.5, 22), (39.5, 15)]),
              ('poly', [(17, 12), (12, 8), (19.5, 8)]), ('poly', [(21, 7), (22, 1.5), (27, 5.5)]),
              ('poly', [(27, 5.5), (34, 2), (34, 7.5)]), ('poly', [(34, 7), (42, 6), (39.5, 12.5)]),
              ('poly', [(39, 12.5), (44, 16), (39.5, 18)])],
    'neat': [('chord', 28, 17, 11.5, 10.5, 175, 365),
             ('poly', [(16.5, 15), (17.5, 24), (19.5, 18.5), (22, 19.5), (25, 16.5), (29, 19), (31, 16.5),
                       (35, 19), (37.5, 17.5), (39.5, 24), (39.5, 15)])],
    'swept': [('chord', 28, 17, 11.5, 10.5, 175, 365),
              ('poly', [(16.5, 15), (17, 25), (19, 19), (21, 18.5), (31, 16.5), (36, 19), (38, 18.5),
                        (39.8, 25), (39.5, 14), (34, 7), (24, 7)])],
    'long': [('chord', 28, 17, 11.5, 10.5, 175, 365),
             ('poly', [(16.5, 15), (16, 30), (18.5, 26), (19.5, 18.5), (23, 19), (25.5, 16.5), (29, 19),
                       (33, 16.5), (36.5, 19), (37.5, 26), (40, 31), (39.8, 15)])],
}


@grouped('head')
def bangs(s, rp, style='neat', cast=2, shine=11):
    s.part(rp, HAIR[style], soft=2, cast=cast, shine=shine)


@grouped('cape')
def cape(s, rp, wide=1.0, hem=51):
    s.part(rp, [('poly', [(20, 28), (36, 28), (36 + 7 * wide, hem - 1), (33, hem + 1), (28, hem), (23, hem + 1),
                          (20 - 7 * wide, hem - 1)])], soft=2.5)


@grouped('body')
def belt(s, rp, y=38, buckle=None):
    s.part(rp, [('poly', [(19.7, y), (36.3, y), (36.4, y + 2), (19.6, y + 2)])], soft=0.6, gloss=0.3)
    if buckle:
        s.part(buckle, [('rect', 25.5, y - 0.3, 28.5, y + 2.3)], soft=0.5, gloss=0.6)


# ====== weapons ======
def sword(s, blade, hilt, x0=40, y0=41, x1=44, y1=14, w=1.6, guard=4.0):
    s.part(blade, [('poly', [(x0 - w, y0 - 3), (x0 + w, y0 - 3), (x1 + w * .7, y1 + 2), (x1, y1 - 1), (x1 - w * .9, y1 + 2)])],
           soft=0.7, gloss=1.0)
    s.part(hilt, [('cap', x0 - guard, y0 - 2.6, x0 + guard, y0 - 3.4, 1.0), ('cap', x0, y0 - 2.5, x0 - .2, y0 + 3.5, 0.9),
                  ('ell', x0 - .3, y0 + 4.2, 1.3, 1.3)], soft=0.6, gloss=0.6)


def staff(s, wood, x0=40, y0=52, x1=42, y1=10, r=0.9):
    s.part(wood, [('cap', x0, y0, x1, y1, r)], soft=0.6)


def orb(s, rp, x, y, r):
    s.part(rp, [('ell', x, y, r, r)], soft=r * 0.6, gloss=1.2, bias=0.05)


def bow(s, wood, string, x=15, top=22, bot=52, bulge=5):
    mid = (top + bot) / 2
    pts = [(x, top), (x - bulge * .7, top + (mid - top) * .35), (x - bulge, mid),
           (x - bulge * .7, bot - (bot - mid) * .35), (x, bot)]
    s.part(string, [('cap', x, top, x, bot, 0.45)], soft=0.4, line=False, thr=0.3)
    s.part(wood, [('line', pts, 1.1), ('ell', pts[0][0], pts[0][1], 1.4, 1.4), ('ell', pts[-1][0], pts[-1][1], 1.4, 1.4)],
           soft=0.7, gloss=0.5)


def dagger(s, blade, hilt, x, y, ang='down', l=7):
    if ang == 'down':
        s.part(blade, [('poly', [(x - 1, y + 2), (x + 1, y + 2), (x + 2.5, y + 2 + l), (x + 0.2, y + 2 + l * .8)])], soft=0.6, gloss=1)
    else:  # reverse grip pointing up-left
        s.part(blade, [('poly', [(x - 1.3, y - 1), (x + 1, y - 1.5), (x - 3.5, y - l), (x - 2.5, y - l * .6)])], soft=0.6, gloss=1)
    s.part(hilt, [('cap', x - 2, y - .5, x + 2, y + .5, .8)], soft=.5)


P = dict(
    steel=ramp('#b4c0d8', 1.3), gold=ramp('#ffc94a', 1.2, 1.1), leather=ramp('#9a623a'),
    darkleather=ramp('#5e3d33'), wood=ramp('#a8703e'), string=ramp('#f0ead8'),
)


def swordsman():
    s = Spr()
    blue, red = ramp('#3f8ae8', 1, 1.1), ramp('#e8413a')
    legs(s, ramp('#4d556e'), P['leather'])
    torso(s, blue)
    s.part(P['darkleather'], [('poly', [(21.5, 29), (24.5, 28.5), (35, 38.5), (33, 39.5)])], soft=0.8)  # strap
    belt(s, P['darkleather'], buckle=P['gold'])
    sword(s, P['steel'], P['leather'], x0=41, y0=42, x1=49, y1=19)
    arm(s, blue, SKIN, (35, 30), (38.5, 36), (41, 40), glove=P['leather'])
    s.part(ramp('#8d97ab', 1.2), [('chord', 35.5, 31, 4, 3.4, 180, 360)], soft=1.2, gloss=0.6, cast=1)  # pauldron
    arm(s, blue, SKIN, (21, 30), (18.5, 35.5), (18, 39), glove=P['leather'])
    s.part(P['steel'], [('ell', 16, 38, 5, 5.5)], soft=1.5, gloss=0.8)  # buckler
    s.part(red, [('ell', 16, 38, 3.3, 3.8)], soft=1.2)
    s.part(P['gold'], [('ell', 16, 38, 1.2, 1.2)], soft=0.5, gloss=1)
    s.part(red, [('ell', 28, 28.5, 8, 2.8)], soft=1, cast=1)  # scarf
    s.part(red, [('poly', [(32, 28), (35, 28.5), (43, 31), (47, 36), (42, 35), (37, 32)])], soft=1)
    head(s)
    bangs(s, ramp('#8a5230'), 'tousled', shine=9)
    face(s, '#2f7fe0', 'open')
    return s
