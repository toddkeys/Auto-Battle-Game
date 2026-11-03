"""Builds assets/audio/ from the downloaded sound packs (see assets/audio/CREDITS.txt).
Each game sound is trimmed, loudness-matched and saved as a small mono OGG.
Run:  python tools/build_audio.py <folder with the extracted packs>   (needs ffmpeg on PATH)"""
import os
import shutil
import subprocess
import sys

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'audio')
A = 'a/RPG Sound Pack/'          # artisticdude, CC0
R = 'r/'                          # rubberduck 80 CC0 RPG SFX
B = 'b/'                          # rubberduck 25 CC0 bang SFX
P = 'sp/'                         # p0ss Spell Sounds Starter Pack, CC-BY-SA 3.0
K = 'k/OGG/'                      # Kenney RPG sounds, CC0

# game sound -> (source file or list of files to layer, max seconds, gain dB)
SFX = {
    # combat
    'hit1': (R + 'blade_01.ogg', .5, 0), 'hit2': (R + 'blade_02.ogg', .5, 0), 'hit3': (K + 'knifeSlice.ogg', .5, 0),
    'crit': (K + 'chop.ogg', .6, 3), 'shoot': (A + 'battle/swing2.wav', .4, -4), 'zapshot': (P + 'zap2.ogg', .5, -4),
    'cast': (R + 'spell_01.ogg', .8, -3), 'skill': (A + 'battle/magic1.wav', 1.2, 0),
    'hdie': (A + 'inventory/armor-light.wav', .8, 0), 'mdie': (R + 'creature_die_01.ogg', 1.0, 0),
    'shatter': (R + 'item_gem_03.ogg', .7, 2), 'freeze': (P + 'freeze2.ogg', 1.0, 0),
    'boom': (P + 'explode3.ogg', 1.4, 0), 'slam': (B + 'cannon_02.ogg', 1.0, -2), 'quake': (R + 'stones_02.ogg', 1.0, 2),
    'heal': (P + 'heal.ogg', 1.2, -2), 'bless': (P + 'blessing.ogg', 1.6, -2), 'shield': (P + 'magicshield.ogg', 1.2, -2),
    'fire': (R + 'spell_fire_02.ogg', 1.2, 0), 'flame': (P + 'flamethrower.ogg', 1.4, -2), 'ice': (P + 'freeze.ogg', 1.4, 0),
    'zap': (P + 'zap10.ogg', 1.0, -2), 'curse': (P + 'curse2.ogg', 1.2, -2), 'poison': (P + 'insect.ogg', 1.0, -2),
    'teleport': (P + 'teleport.ogg', 1.0, -2), 'summon': (P + 'warp2.ogg', 1.2, -2), 'stun': (P + 'forcepush.ogg', .9, 0),
    'arrows': (P + 'wind2.ogg', 1.4, 0), 'snipe': (P + 'shot2.ogg', .8, -6), 'steal': (A + 'battle/sword-unsheathe2.wav', .8, 0),
    'flurry': (R + 'blade_03.ogg', .6, 0), 'trap': (R + 'chain_01.ogg', .8, 0), 'slime': (A + 'NPC/slime/slime3.wav', .8, 0),
    'roar_golem': (A + 'NPC/giant/giant2.wav', 1.6, 0), 'roar_lich': (A + 'NPC/shade/shade6.wav', 1.6, 0), 'roar': (R + 'creature_roar_01.ogg', 1.6, 0),
    # shop / ui
    'click': (A + 'interface/interface1.wav', .3, -6), 'buy': (R + 'item_coins_01.ogg', .6, -2), 'sell': (K + 'handleCoins.ogg', .7, -2),
    'reroll': (K + 'bookFlip2.ogg', .5, 0), 'star': (P + 'cheer.ogg', 1.6, -2), 'equip': (A + 'inventory/chainmail1.wav', .7, -2),
    'slot': (R + 'lock_01.ogg', .6, 0),
    'bash': ([R + 'metal_02.ogg', B + 'cannon_01.ogg', A + 'inventory/metal-ringing.wav'], 1.1, 2),   # heavy shield slam: clang + thump + ring 'start': (A + 'battle/sword-unsheathe.wav', 1.0, -2),
    'victory': (P + 'cheer-crowd.ogg', 2.2, -4), 'defeat': (P + 'magicfail.ogg', 1.6, -2),
}
MUSIC = {'prep': 'TownTheme.mp3', 'battle': 'jrpg_battle_loop.mp3'}


def ff(args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + args, check=True)


if __name__ == '__main__':
    os.makedirs(os.path.join(OUT, 'sfx'), exist_ok=True)
    total = 0
    for name, (src, dur, gain) in SFX.items():
        out = os.path.join(OUT, 'sfx', name + '.ogg')
        fade = max(.05, dur * .25)
        srcs = src if isinstance(src, list) else [src]
        ins = sum((['-i', os.path.join(SRC, x)] for x in srcs), [])
        mix = ''   # several sources: trim each, layer them, then run the shared chain below
        if len(srcs) > 1:
            mix = ''.join(f'[{i}:a]silenceremove=start_periods=1:start_threshold=-50dB[s{i}];' for i in range(len(srcs)))
            mix += ''.join(f'[s{i}]' for i in range(len(srcs))) + f'amix=inputs={len(srcs)}:normalize=0[m];[m]'
        ff(ins + ['-t', str(dur), '-ac', '1', '-ar', '44100',
            '-filter_complex' if mix else '-af', mix + f'silenceremove=start_periods=1:start_threshold=-50dB,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100,volume={gain}dB,afade=t=out:st={dur - fade}:d={fade},alimiter=limit=0.8:level=false,volume=-1dB',
            '-c:a', 'libvorbis', '-q:a', '4', out])
        total += os.path.getsize(out)
    for name, src in MUSIC.items():
        out = os.path.join(OUT, name + '.mp3')
        shutil.copyfile(os.path.join(SRC, src), out)
        total += os.path.getsize(out)
    print(f'built {len(SFX)} sounds + {len(MUSIC)} music tracks, {total // 1024} KB')
