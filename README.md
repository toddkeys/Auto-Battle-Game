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

The seven reworked skins live in `assets/art/src/hero_skins_atlas.png`:
Wukong (`stonemonkey`), Mythic Wukong (`wukong`), Eclipse Witch (`eclipsewitch`),
Stormweaver (`voidsage`), Crimson Ravager/Berserker (`chieftain`),
Worldbreaker (`grandmaster`), and Shadowstep (`shadowstep`). Gameplay names,
classes, and stats are unchanged. Only front artwork is used, mirrored for facing.

To extract the skins, copy them into the unit assets, rebuild their animation rigs,
and embed them into the game (requires ImageMagick plus the Python dependencies above):

```bash
python tools/prep_hero_skins.py
python tools/build_game.py
```

The atlas cell boundaries are in `tools/prep_hero_skins.py`; the matching animation
piece polygons are in `_SKIN_PARTS` in `tools/art_rig.py`. Adjust both when replacing
the atlas. The full sprite build also uses these rig definitions for these heroes.
