# Auto Battle Game

A single-file auto battler (original anime-style pixel art). Open `ro-autobattler.html` in a browser to play, or play online at https://toddkeys.github.io/Auto-Battle-Game/ (GitHub Pages serves `index.html`, which forwards to the game). Your best round is saved in your browser.

## Editing

- Game code: `tools/game_template.html` (do not edit `ro-autobattler.html` by hand, it is generated)
- Animation: every sprite is built from pieces (legs, body, arms + weapons, head, cape...). `build_sprites.py` also writes
  `assets/rig/<id>.png` (one layer per piece) + `<id>.json` (piece groups and joints); the game turns each piece on its
  joint (`rigPose` in the template) for walking, attacks, casting, hits, cheering and dying.
- Sprites: `tools/kit.py`, `tools/classes.py`, `tools/tier4.py`, `tools/crusaders.py`, `tools/occultists.py`, `tools/samurai.py`, `tools/frostkin.py`, `tools/gamblers.py`, `tools/newclasses.py`, `tools/newclasses2.py`, `tools/bosses.py`, `tools/summoners.py`, `tools/monsters.py`, `tools/creatures.py` (engine in `tools/pixel.py`; `R = 2` renders HD 112x108 sprites from the same 56x54 design grid, a full build takes ~12 min)
- Hand-made hero pictures: put one in `assets/art/<id>.png` (prepared from a sheet with `tools/prep_art.py`) and it replaces that hero's drawn sprite; it animates as one piece unless `tools/art_rig.py` cuts it into rig pieces (sword, arms, shield, head), as it does for the Aegis Paladin. The Aegis Paladin uses `assets/art/src/aegispaladin_sheet.webp`, prepared with `python tools/prep_art.py assets/art/src/aegispaladin_sheet.webp aegispaladin 40 110 860 912 0,0,232,256 205,0,300,224 556,0,620,205 0,240,165,335 515,100,560,140` and `... aegispaladin_back 978 922 1245 1226`.

Sound: `assets/audio` (credits in `assets/audio/CREDITS.txt`), rebuilt from the source packs with `python tools/build_audio.py <packs folder>` (needs ffmpeg).

Rebuild (needs Python with Pillow and numpy):

```bash
python tools/build_sprites.py   # redraw sprites -> assets/units/*.png, assets/preview.png
python tools/build_game.py      # embed sprites into ro-autobattler.html
```

## Coordinated hero skins

The first seven reworked skins live in `assets/art/src/hero_skins_atlas.png`:
Wukong (`stonemonkey`), Mythic Wukong (`wukong`), Eclipse Witch (`eclipsewitch`),
Stormweaver (`voidsage`), Crimson Ravager/Berserker (`chieftain`),
Worldbreaker (`grandmaster`), and Shadowstep (`shadowstep`). Gameplay names,
classes, and stats are unchanged. Paladin (`aegispaladin`) and Crimson Valkyrie
(`starwarden`) use the matching `assets/art/src/holy_skins_atlas.png`. Only front
artwork is used, mirrored for facing.

To extract the skins, copy them into the unit assets, rebuild their animation rigs,
and embed them into the game (requires ImageMagick plus the Python dependencies above):

```bash
python tools/prep_hero_skins.py
python tools/build_game.py
```

The atlas cell boundaries are in `tools/prep_hero_skins.py`; the matching animation
piece polygons are in `_SKIN_PARTS` in `tools/art_rig.py`. Adjust both when replacing
the atlas. The full sprite build also uses these rig definitions for these heroes.

## Sanctuary visual upgrade

Night Reaper and the six boss skins are extracted from
`assets/art/src/nightreaper_bosses_atlas.png`. Their animation pieces are defined
in `tools/art_rig.py`. The sanctuary battlefield is `assets/scenery/sanctuary.jpg`;
`build_game.py` embeds it with the sprites so the generated HTML still works
without a server (audio remains in the checked-in assets directory).

```bash
python tools/prep_boss_skins.py
python tools/build_game.py
```

The renderer adds class-colored casting sigils, radial impact bursts, crimson
Night Reaper effects, boss ground markings, floating motes, and assassin trails.
Reduced-motion mode freezes ambient drift and disables the new assassin trails.
The background has a quiet playable center and an existing meadow fallback while
its embedded image loads. This update changes presentation, not combat stats or skills.

Hero size is art-directed in `HERO_VISUAL_SCALE` and `HERO_HEAD_SCALE` in the game
template. These were tuned against side-by-side renders of the full hero roster;
heads, body presence, large hats and weapons are balanced visually rather than
forcing every image into the same outer bounding box. Feet stay anchored and
health bars follow the adjusted size. Bosses retain their separate larger scale.

## Full roster and interface

All 72 playable heroes now have individual reworked skins. The 62 remaining
heroes use eight coordinated source sheets in `assets/art/src/roster/`; the
manifest records their exact cell order. `tools/roster_rigs.py` defines their
animation masks, and `art_rig.py` builds the same rig format used by the earlier
reworks. Combat names, classes, stats and skills are unchanged.

```bash
python tools/prep_roster.py
python tools/build_game.py
```

Use `--group vanguard` (or another manifest group) to rebuild just one sheet.
The complete sprite builder also recognizes these art overrides. Keep each
figure within its atlas cell when replacing source artwork.

The original oak-and-brass interface, compact shop and wooden reserve bench are
restored. Narrow screens still stack the panels so controls remain reachable.

Animation uses separate torso, head, arms, elbow/wrist, boots, cape and clothing
pieces. Attacks have class-specific anticipation, action and recovery poses;
bows draw, guns recoil, punches extend, and casters raise their staffs. The ten
earlier skins also have animated lower-body and trailing-cloth pieces. Wolves,
wisps, drakes, turrets and bosses have species-specific motion. Summons and small
monsters use their native silhouettes and individual scale, rather than the hero
height normalization. Combat definitions are unchanged.

Optional browser smoke checks use Python Playwright and system Chromium:

```bash
python tools/check_visuals.py
```

These exercise all 72 skill casts and idle, walking, attack, casting, release,
frozen, death and spinning renders in both directions, plus buying, locking,
opening the planner/codex and checking a phone-width layout. Render checks also
cover all seven summons and nine monsters/bosses.

## Sound mixing and skill signatures

`assets/audio/mixer.js` supplies the priority mixer, embedded into the game by
`build_game.py`. It allows at most 10 active SFX voices with smaller channel
limits for basic hits, healing, casts, skills, critical hits and bosses. Important
sounds lower the music and background combat sounds briefly, with gradual
recovery. Music/SFX sliders keep their saved settings; muting SFX stops active
voices. HTTP(S) playback uses Web Audio compression and subtle stereo positioning;
opening the HTML from disk uses native media playback with the same voice limits
and volume controls. Sound variation uses a private random generator.

All 72 heroes and six bosses have remixed skill signatures, built from the
existing credited SFX. Night Reaper uses blade sounds, Worldbreaker uses a punch
impact, Paladin uses metal and holy textures, and Ice Wall users use ice/shatter
textures. The original music and SFX remain available for secondary impacts.
Signatures are matched with two-pass loudness normalization and peak headroom.

```bash
python tools/build_signature_audio.py
python tools/build_game.py
```

Use `--only nightreaper` to rebuild one signature. Recipe data is in the Python
builder; the generated `assets/audio/skills/profiles.json` records each source,
duration, pitch and runtime mix settings. Remix attribution and license are in
`assets/audio/skills/CREDITS.txt`.

Browser audio checks (Python Playwright and system Chromium):

```bash
python tools/check_audio.py
```

Checks decode every signature, reject silent/clipped samples, exercise the global
voice cap, verify music ducking and mute/preference persistence, and exercise the
native-media fallback with Web Audio unavailable.
