# Auto Battle Game

A single-file auto battler (original anime-style pixel art). Open `ro-autobattler.html` in a browser to play, or play online at https://toddkeys.github.io/Auto-Battle-Game/ (GitHub Pages serves `index.html`, which forwards to the game). Your best round is saved in your browser.

## Editing

- Game code: `tools/game_template.html` (do not edit `ro-autobattler.html` by hand, it is generated)
- Animation: every sprite is built from pieces (legs, body, arms + weapons, head, cape...). `build_sprites.py` also writes
  `assets/rig/<id>.png` (one layer per piece) + `<id>.json` (piece groups and joints); the game turns each piece on its
  joint (`rigPose` in the template) for walking, attacks, casting, hits, cheering and dying.
- Sprites: `tools/kit.py`, `tools/classes.py`, `tools/tier4.py`, `tools/crusaders.py`, `tools/occultists.py`, `tools/samurai.py`, `tools/frostkin.py`, `tools/gamblers.py`, `tools/newclasses.py`, `tools/newclasses2.py`, `tools/bosses.py`, `tools/summoners.py`, `tools/monsters.py`, `tools/creatures.py` (engine in `tools/pixel.py`; `R = 2` renders HD 112x108 sprites from the same 56x54 design grid, a full build takes ~12 min)
- Custom hero pictures: `tools/prep_art.py` can import a pose into `assets/art/<id>.png`.
  Shipped heroes should be rebuilt from the coordinated roster atlases below;
  the original reference sheets remain archived in `assets/art/src`.


Sound: `assets/audio` (credits in `assets/audio/CREDITS.txt`), rebuilt from the source packs with `python tools/build_audio.py <packs folder>` (needs ffmpeg).

Rebuild (needs Python with Pillow and numpy):

```bash
python tools/build_sprites.py   # redraw sprites -> assets/units/*.png, assets/preview.png
python tools/build_game.py      # embed sprites into ro-autobattler.html
```

## Coordinated hero skins

All 88 heroes now use the same compact chibi roster style and articulated rig
format. `assets/art/src/roster/champions.png` replaces the ten earlier designs:
Wukong, Mythic Wukong, Eclipse Witch, Stormweaver, Crimson Ravager, Worldbreaker,
Shadowstep, Aegis Paladin, Crimson Valkyrie and Night Reaper. Their head/body
proportions are drawn to match the other heroes; the earlier head-enlargement
and per-character size overrides are removed. They turn left/right like the roster.

```bash
python tools/prep_roster.py --group champions
python tools/prep_roster.py --group tactics_reworks  # latest Stormweaver / Shogun override
python tools/build_game.py
```

`python tools/prep_hero_skins.py` is a compatibility entry point for the same
champions group. The old seven-hero and holy-hero atlases remain archived and are
not used by the standard rebuild commands. Atlas order is in
`assets/art/src/roster/manifest.json`; animation masks are in `tools/roster_rigs.py`.

## Sanctuary visual upgrade

The six boss skins are extracted from
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

All 88 playable heroes now have individual reworked skins and use eleven
coordinated source sheets in `assets/art/src/roster/`; the
manifest records their exact cell order. `tools/roster_rigs.py` defines their
animation masks, and `art_rig.py` builds the same rig format used by the earlier
reworks. The tactical expansion below adds classes and skills on top of this art pipeline.

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
bows draw, guns recoil, punches extend, and casters raise their staffs. All 88
heroes share the articulated lower-body, elbow and trailing-cloth rig format. Wolves,
wisps, drakes, turrets and bosses have species-specific motion. Summons and small
monsters use their native silhouettes and individual scale, rather than the hero
height normalization. Combat definitions are unchanged.

Optional browser smoke checks use Python Playwright and system Chromium:

```bash
python tools/check_visuals.py
```

These exercise all 88 skill casts and idle, walking, attack, casting, release,
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

All 88 heroes and six bosses have remixed skill signatures, built from the
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

## Ice Wall appearance by price

`assets/vfx/ice_walls.js` renders the 2-gold Glacier Warden's frosted rampart,
3-gold Frost Oracle's tall rune prisms, and 4-gold Winter Queen's crowned bastion.
Damage adds branching cracks; walls rise into place and fade as they expire.
Snowmender (1 gold) keeps its existing healing skill. All three raise one wall, 3 cells wide for 6 seconds; higher tiers keep their
stronger HP, shielding and shatter effects. `build_game.py` embeds
this renderer into the generated HTML.

```bash
python tools/check_ice_walls.py
```

This exercises all three actual caster skills, confirms their wall widths and
counts, checks rendering does not mutate wall state, and verifies enemy shots
are blocked while friendly shots pass through.

## Mana feedback and expanded rewards

Mana restoration now lights the mana bar blue instead of adding floating mana
numbers. The glow covers attacks, damage received, mana auras, cleansing and
Night Reaper's refund, and fades between fights. Damage and gold numbers remain.

Boss rewards draw up to three blessings that are below the three-stack cap.
Maxed blessings never take a card slot. Once every blessing is maxed, the reward
screen offers small mastery rewards (listed below) and a **Skip reward** button,
so the next round stays playable.
Daily-mode choices use the run seed.

Eight new blessings add regeneration (Living Roots), crit (True Aim), movement
(Trailblazers), lifesteal (Crimson Pact), reflection (Briar Oath), healing
(Gentle Hands), starting physical shields (First Light), and attack mana
(Patient Study).

Six new items enter the existing loot pools, with normal enchanting and sub-stats:

| Item | Rarity | Effect at +0 |
| --- | --- | --- |
| Dawn Buckler | Common | Starting physical shield: 22% max HP |
| Runebound Grimoire | Common | +20% skill damage, +15% skill healing |
| Heartwood Pendant | Common | +12% max HP and healing given |
| Duelist Sigil | Rare | +10% dodge, +8% crit; total dodge capped at 65% |
| Chrono Seal | Rare | +15% starting mana, block the first status effect |
| Storm Core | Rare | +30% attack speed for 3 seconds after casting |

Storm Core refreshes without stacking, expires during movement/channeling, and
can be dispelled. Pilfer removes the new equipment bonuses too.

```bash
python tools/check_progression.py
```

Checks partial/full blessing exhaustion, double-click protection, the actual boss
reward transition and next battle, new blessing stacks, loot pools, item
equipping/enchanting/combining/stripping, Storm Core cooldowns, and mana feedback.

## Conditional builds and grounded combat motion

Three additional blessings support distinct play styles using the existing items:

| Build | Blessing (per stack, up to three) | Useful pairings |
| --- | --- | --- |
| Spellweaver | Arcane Rhythm: after casting, the next three basic attacks each restore 3 extra mana | Storm Core speeds those attacks; Grimoire strengthens skills; Chrono Seal starts the loop sooner |
| Counterguard | Shield Riposte: shield absorption primes +20% damage on the next basic attack | Dawn Buckler, Spellward Charm, Warding Bell or First Light provide shields |
| Bloodbound | Crimson Reserve: excess lifesteal fills a physical shield up to 6% max HP | Vampire Fang or Crimson Pact supply lifesteal; Heartwood increases the HP-based reserve |

These effects work independently; owning a named set is not required. Rhythm
refreshes to three charges, Riposte holds one charge, and Reserve cannot grow
past its cap or reduce an existing larger shield. Mana gain reductions still
apply, wounds reduce lifesteal before conversion, and dispelling clears pending
Rhythm/Riposte charges. Spell damage does not consume Riposte. Pairing hints
appear on blessing cards and item tooltips; blue pips show remaining Rhythm
attacks and a gold bar outline indicates a ready Riposte.

Basic attacks keep their original strike time, with planted feet, a shorter
lunge, separate wind-up/strike/recovery poses and alternating arm accents.
Skill release starts on the strike pose rather than winding up after its damage
has already landed. Head, elbow, cape and cloth movement support the action;
short directional hit reactions are visual offsets and do not move combat
positions or interrupt actions. Reduced-motion preferences soften those offsets.
All 88 hero rigs have more overlap at joint seams to prevent gaps when pieces
turn, while artwork proportions and summon sizes retain their existing values.

```bash
python tools/check_builds_motion.py
# Optional visual review sheet and reward-screen capture:
python tools/check_builds_motion.py --preview /tmp/builds-motion.png
```

Checks real conditional procs, caps, dispelling, mana/wound reductions, actual
strike timing, all 88 heroes in 3,872 motion states, phone reward selection and
build tooltip layout. Regenerate rigs from the art using `tools/build_sprites.py`,
then run `tools/build_game.py` to embed the results.


## Rewards after mastering every blessing

When the entire blessing pool reaches three stacks, each blessing reward screen
offers one of these small bonuses instead of more permanent hero stats:

| Reward | Effect |
| --- | --- |
| Victory Purse | Gain 3 gold |
| Catch Your Breath | Restore 2 **player** HP, capped at 100 |
| Scout Ahead | Get 2 free shop rerolls for the current preparation phase |

At full player HP, recovery is replaced with **Scout's Purse**: 1 gold and 1 free
shop reroll for the current preparation phase. The player can also skip the
reward. Selecting a reward closes the screen before granting it, so double
clicks cannot claim multiple bonuses. Blessing stacks and normal boss loot stay
unchanged. Partially mastered runs still choose from their remaining blessings.

Free rolls use the normal shop reroll button, which displays the remaining
credits. Credits are spent before gold, preserve Daily-mode shop seeding, and
unlock the shop just like paid rolls. After they are spent, rerolls cost the
usual 2 gold. Unused credits expire when a battle successfully starts; an empty
board does not waste them. Starting a new run clears all credits.

```bash
python tools/check_mastery_rewards.py
# Optional reward screen capture:
python tools/check_mastery_rewards.py --preview /tmp/mastery-rewards.png
```

Checks reward amounts, HP caps/full-HP replacement, duplicate claims, free/paid
rolling at zero gold, shop locks, credit expiry, skipping, restarts, Daily seeds,
the real boss reward transition, next-battle progression and phone layout.

## Late-round rendering performance

Untinted, opaque articulated heroes now draw their limbs directly onto the board.
This avoids repeatedly reading/copying a shared scratch canvas between heroes.
Status tints, translucent spawns, ghosts and deaths use separate per-unit surfaces
so their compositing stays isolated. Those surfaces use weak object keys and are
released with their fighters; poses still update every frame.

`build_game.py` embeds tight source rectangles for every rig layer, including
expression frames, with transparent sampling margins. Drawing skips the empty
padding while retaining the original pivots and body proportions. Older rigs
without rectangle metadata still use the full-frame path. Fusion keeps its paired
auras, rings, partner weapon and cape; the constant whole-body colour wash is
removed to let fused teams use the direct path too.

```bash
python tools/build_game.py
python tools/check_performance.py
# Compare with a previously generated version on the same worker/browser:
python tools/check_performance.py --baseline /tmp/before.html --output /tmp/performance.json
```

The check covers 440 rig states, verifies cropped/full-frame rendering and
isolated tint output, then benchmarks deterministic round 15/30/60 fights with
nine heroes, summons and a full fused-team scenario. Benchmark fighters receive
extra HP only within the test to keep the workload alive. With `--baseline`, it
also requires exact matching combat state after the same simulation steps.

Sample on this cloud worker, headless Chromium, 120 frames per scenario,
compared with `69de6e8` (CPU time for simulation plus rendering, not an FPS promise):

| Scenario | Before mean | After mean | CPU reduction |
| --- | ---: | ---: | ---: |
| Round 15 | 20.4 ms | 5.5 ms | 73% |
| Round 30 | 17.8 ms | 5.6 ms | 69% |
| Round 30, fused team | 25.1 ms | 6.8 ms | 73% |
| Round 60 | 18.0 ms | 4.3 ms | 76% |

Frame-gap p95 on this worker fell from 50–67 ms to roughly 33 ms. Real frame rates
depend on the browser's graphics backend and hardware; rerun the comparison on
the same machine when investigating another performance issue.

## Boss spoils and optional risk

A boss victory now reserves its guaranteed rare-item slot for a **choose one of
three** draft. The other random equipment drop and the existing 35% scroll chance
are still awarded normally. Choosing completes the original two-equipment reward;
it does not add a third item. Offers are distinct rare items and reproducible in
Daily mode. A two-boss wave still grants one draft, matching its previous total
loot count. Partial boss kills on a lost fight keep their existing random loot.

Entering a boss preparation round opens an optional pact:

- **Standard battle:** normal enemies and rewards.
- **Reinforced guard:** two additional guards of the boss's existing minion type;
  victory awards 4 extra gold. Defeat awards no pact bonus.

The **Boss: Standard/Reinforced** HUD button lets the player change their choice
before starting. The battle captures that choice, and the pact resets next round.
No pact adds permanent stats or extra item drops.

Preparation screens are queued: boss loot draft, then blessing/mastery reward.
Crossroads still appear on their normal eligible rounds, before the pact when
entering a boss round. A pending screen blocks battle start. Closing each screen
opens the next one, including when every blessing is maxed. Double claims and
result callbacks from an abandoned/restarted run are rejected.

```bash
python tools/check_boss_choices.py
```

## Adaptive effects, draw pacing and effect reuse

The HUD defaults to **FPS: 60**. Clicking it selects **FPS: Unlocked** for higher
refresh-rate displays; this preference is saved in the browser. The drawing
schedule retains its phase on 144/240 Hz displays instead of accidentally dropping
to 48 FPS. Input-driven refreshes remain immediate. Combat advances on a separate
60 Hz simulation clock, with the existing Speed x1/x2/x3 multipliers. Pause and
page visibility changes clear elapsed backlog rather than fast-forwarding it.

Effect density adjusts automatically after sustained expensive frames or missed
60 Hz frame deadlines. Three budgets reduce sparks, petals, motes, wall fragments,
decorative blooms and smoke. Downgrades require sustained load; restoring detail
requires five seconds of headroom per level, avoiding visible oscillation after
one slow frame. Target reticles, meteors, charge/arrow-rain cues, rune areas,
projectiles, Ice Walls and status indicators are kept.

Spark and wall-fragment objects return to bounded pools when they expire or a
round ends. Their arrays compact in place, and reused objects receive all fields
again. Pool capacities are 700 sparks and 160 fragments; expired objects do not
hold hero references. Existing tinted VFX frame caching continues to reuse image
frames. Reducing cosmetic density still consumes the original random draws, so
Daily-mode combat and random outcomes do not depend on graphics quality.

```bash
python tools/check_frame_pacing.py
python tools/check_performance.py
```

Frame-pacing checks cover 30/60/144/240 Hz, capped/unlocked drawing, Speed x3,
pause, saved settings, adaptive recovery, protected telegraphs, bounded storage
and particle/fragment reuse. Identical fights must produce the same combat state
at different refresh rates and effect budgets. Use the performance comparison
command above to measure CPU time on the same worker/browser.

A 10,000-spark reuse check (100 batches of 100, expired between batches) creates
100 particle objects and reuses them 9,900 times. Use `--stress` to compare full
and light decoration budgets in the performance check:

```bash
python tools/check_performance.py --stress --output /tmp/effect-stress.json
```

In a synthetic burst on this worker, decoration draw time fell from about 1.6 ms
to 0.8 ms, with all five tested warning cues retained. Normal-round per-frame CPU
time remains close to the previous direct-renderer version; these changes target
peak decoration load, allocation churn and unnecessary high-refresh draws.


## Tablet and touch controls

On iPad and other touch screens, tap a shop hero to keep its stats and skills
open. Use **Buy** to send it to the bench, **Buy and place** then tap a friendly
cell, or drag the shop card straight onto the field/bench. An unaffordable hero
can still be inspected. Desktop click-to-buy and right-click controls remain.

Tap an owned hero for its actual star level and equipment; use **Move / swap /
fuse** then tap a destination, or drag it. The detail card also provides **Sell**
immediately on touch screens; mouse sales retain confirmation. Fighters and bosses can be inspected during combat.

Tap a bag item for its description and equip/enchant, combine, reroll or sell
actions. Equip/use-scroll asks for a hero; combine asks for another matching bag
item. Combining works during combat; equipping, rerolling and selling wait for
preparation. Held equipment and blessings also have persistent touch details.

Team Plan supports tap-to-add, up/down ordering, remove and saved presets.
Touch drags can scroll at screen edges; empty board swipes still scroll the page.
Cancelled gestures, interrupted touches and extra fingers cannot buy a hero or
leave a drag ghost. Portrait shop actions wrap within the screen.

```bash
python tools/check_touch_controls.py
```

This uses Chromium's native touch input at 1024×768, 768×1024 and 390×844,
covering actual taps/drags, purchases, hero details, move/fuse, equipment actions,
plans/presets, cancellation and scrolling. It complements the desktop checks in
`tools/check_visuals.py`; it does not replace testing Safari on a physical iPad.


## Tactical roster expansion

The roster contains 88 heroes across 30 classes. All classes now have a 4-gold
hero. New content uses English names and descriptions throughout the game.

| Class | 2 gold | 3 gold | 4 gold |
| --- | --- | --- | --- |
| Sentinel | Watchkeeper | Chain Warden | Aegis Captain |
| Abjurer | Hexbreaker | Barrier Weaver | Fatekeeper |
| Duelist | Rapier Adept | Rose Cavalier | Crown Duelist |
| Soulbinder | Thread Witch | Soul Cantor | Covenant Queen |

Class bonuses use the existing two/three **different** heroes thresholds.
Sentinels select a nearby ranged ally to defend, remain near it and ready their
first skill when an enemy dives nearby. Aegis Captain intercepts two distinct
divers per perimeter cast; the same diver cannot consume both interceptions.
Abjurers weaken enemy spells and protect against burst. Reverse Fate absorbs
35% of nearby ally damage before lethal HP loss, converts absorbed/self damage
to healing for four seconds and has an eight-second recast cooldown. Absorption
has a 150% caster-max-HP budget. Only one Fatekeeper can absorb each hit, and the
transfer bypasses recursive damage/link triggers. Wounds reduce the healing.

Duelists build capped consecutive-target focus; switching targets resets stacks.
Their challenge cannot disable bosses. Soul links have at most four members,
share post-shield direct damage once, cannot recurse and stop when their source
dies. Multiple covenants replace rather than stack on the same enemy.

Moonlance is a new 3-gold Archer. Astral Arrow travels straight, can miss, hits
only the first enemy and stops at an enemy Ice Wall. Stun is based on travelled
distance: 0.5s + 0.4s/cell, capped at 3s and 0.65s against bosses.
Plague Sovereign, Elixir Empress and Verdant Empress complete Occultist,
Alchemist and Druid at 4 gold; Elixir Empress does not generate extra gold.

Stormweaver has a calm, long violet-haired mage design inspired by Fern, in the
same chibi proportions as the roster. Shogun is a female katana master with an
ivory/crimson/obsidian outfit and a delayed line-cut finisher, Moonfall: Final
Draw. Phantom Blade uses Phantom Cross: a dash, two inexpensive fading echoes
and a delayed crossing strike. Echoes share the adaptive decoration budget;
arrow collision, protection and link damage run on the existing simulation
clock independently of visual quality. Existing 60 FPS pacing/pooling remain.

New art source: `assets/art/src/roster/tactics.png`. The rework source is
`assets/art/src/tactics_reworks_source.png`; its separate characters are packed
into `assets/art/src/roster/tactics_reworks.png`. Manifest overrides deliberately
come last so a full rebuild preserves the latest Stormweaver and Shogun.

```bash
python tools/prep_tactics_art.py
python tools/prep_roster.py --group tactics
python tools/prep_roster.py --group tactics_reworks
python tools/build_signature_audio.py
python tools/build_game.py
python tools/check_tactical_roster.py --preview /tmp/tactical-roster.png
```

Checks cover pre-lethal protection, overlap/budget limits, damage-over-time,
barriers, reactive interceptions, bounded soul sharing/focus, arrow misses and
wall collisions, boss control caps and real combat ticks for all new/reworked
skills. Visual and motion checks dynamically cover the full roster; the touch
suite continues to cover tablet landscape/portrait and phone controls.


## iPad selling, rotation, audio and run-over fixes

Touch **Sell** actions now sell immediately; fusion keeps its confirmation.
Dragging a hero or bag item accepts the entire Shop panel, including cards, odds
and buttons. A large overlay shows the drop area without changing layout. The
release position is checked again, so scrolling while dragging cannot leave a
stale sell target. Cancelled/interrupted drags still cannot sell.

Board fitting sets both dimensions at the original aspect ratio. Resize,
orientation, visual viewport and HUD/container changes schedule a fresh fit;
rotation cancels active drags and removes temporary highlights. The Pages entry
also declares the device viewport. Run-over uses a scrollable content area with
an always-visible Close header and Play again / Other runs footer, regardless of
whether a score qualifies for the top ten or leaderboard loading succeeds.

Effects on HTTP(S) use decoded Web Audio buffers, sharing the context unlocked
by a real touch/keyboard gesture. This avoids needing a separate media autoplay
permission for each delayed combat effect. Resume is retried on touch release;
Safari's playback audio session is requested where supported. The decoded-file
LRU holds at most 48 entries and the existing ten-voice/priority limits remain.
Browsers without Ogg/Vorbis support select AAC `.m4a` alternatives; a decode
failure also tries the alternate codec. Native media remains the local-file /
no-Web-Audio fallback. AAC encoding includes a limiter and reconstruction
headroom, preserving the original sound attributions and remix license.

```bash
python tools/build_safari_audio.py
python tools/build_game.py
python tools/check_ipad_regressions.py --preview /tmp/ipad-run-over.png
python tools/check_touch_controls.py
python tools/check_audio.py
```

The audio builders refresh AAC alternatives when an effect changes. The iPad
regression check uses native touch input, rotates a running page repeatedly,
sells into three different Shop areas and checks full non-top-ten dialogs. It
also decodes all 141 AAC effects and checks audible output while Ogg support is
absent and HTML sound-effect playback is denied. These Chromium checks exercise
Safari's codec/autoplay constraints; they do not constitute physical iPad testing.


Fusion coverage includes Sentinel, Abjurer, Duelist and Soulbinder in both slots.
The lead casts first, followed by the partner; delayed hits, skill projectiles,
Soulbinder links and Eclipse fields retain their casting skill's physical/magic
identity. Class traits, Bard auras and Engineer/Summoner opening units also work
from the secondary slot. The lead still supplies basic attack range and stats.

A secondary Monk preserves the lead's original arms, equipment and attack motion,
without importing Monk limbs or capes. Fusion portraits, lineup
pictures and phantom echoes use the same equipment rules as the battlefield.
Prepared equipment atlases are created on demand and held in a 48-entry LRU,
large enough for two full nine-unit fused teams without rebuilding each frame;
portraits have separate bounded caches. New runs release these pictures.

```bash
python tools/build_game.py
python tools/check_fusions.py --preview /tmp/fusions.png
```

The fusion check covers 1,932 ordered new-class combinations, both skill releases,
secondary traits, delayed damage types, and 2,080 equipment render combinations.


For existing online leaderboards, run `tools/leaderboard_endless_runs.sql` in the
Supabase SQL Editor. The original schema rejected rounds above 200 and boss
counts above 50; endless runs now retain positive/nonnegative integer checks
without those gameplay caps. Updating the HTML alone cannot change live database
constraints. The complete `tools/leaderboard.sql` also includes this migration.

Failed score submissions are saved locally (the latest 20) before sending and
can be retried via **Runs → Retry saved scores**, including after reload. The
client retries without lineup data only for a confirmed missing `team` column;
constraint/network failures preserve the lineup. Successful submissions are not
retried just because the following ranking refresh fails. Browser storage must
be available to preserve failed submissions across reloads.


Runs now autosave preparation checkpoints on this browser/device. **Save & exit**
returns to Runs; **Continue** restores heroes (including fusions and equipment),
bench/field positions, blessings, gold/HP, shop/lock/upgrade state, boss order,
modifier, original Daily seed and pending item/blessing/pact choices. Leaving
mid-battle restores preparation for that round; live fighter references and
skill callbacks are never serialized. Paid crossroads outcomes cannot be claimed
again. Starting a new run replaces this device's checkpoint; a completed run
clears it. Browser storage failures are shown instead of claiming a successful save.

From round 40, bosses add distinct telegraphed ground patterns: Faultline circles,
Winter Crown rings, Scorching Run lanes, Briar Cross lanes, Storm Eye rings and
Siege Sweep beams. Shapes evolve below 66% and 33% health, with staggered extra
strikes for late circle/beam phases. Heroes automatically try to evade; roots,
channels and crowd control still matter. Pattern hits are capped before defense
modifiers at 16–21% of a target's max HP and cancel when their boss dies. Boss
warnings are separate from disposable effects, remain in every quality mode and
are clipped to the battlefield.

**Effects: Auto / iPad / Full** is saved separately from the run. iPad mode is the
default for detected iPads; it limits particles/debris, removes ambient decoration,
extra blooms and expensive cosmetic passes, while retaining projectiles, warning
geometry, statuses and hero animation. The Shop offers separate touch **Buy**
buttons beside each hero card, buying directly to the bench. Tapping the portrait
still opens details; dragging still buys onto the board. Shop pointer moves reuse
the regular frame renderer instead of drawing the whole scene per input event.

```bash
python tools/check_endless_features.py
python tools/check_touch_controls.py
python tools/check_frame_pacing.py
```
