"""Extract the coordinated hero skins and rebuild their rigs (requires ImageMagick).
Run from any directory: python tools/prep_hero_skins.py && python tools/build_game.py
"""
from pathlib import Path
import shutil
import subprocess
import art_rig

ROOT = Path(__file__).resolve().parent.parent
# Atlas cell boundaries are explicit: weapons and scarves stay with their owner.
CELLS = [('stonemonkey',0,294),('wukong',294,592),('eclipsewitch',592,883),
         ('voidsage',883,1177),('chieftain',1177,1544),
         ('grandmaster',1544,1867),('shadowstep',1867,2172)]

def main():
    for cid,left,right in CELLS:
        dest=ROOT/'assets/art'/f'{cid}.png'
        subprocess.run(['magick',str(ROOT/'assets/art/src/hero_skins_atlas.png'),
                        '-crop',f'{right-left}x724+{left}+0','+repage','-channel','A','-threshold','8%','+channel','-trim','+repage',
                        '-resize','x162',str(dest)],check=True)
        # Remove two isolated fragments at the edges of adjacent atlas cells.
        if cid in ('eclipsewitch','grandmaster'):
            subprocess.run(['magick',str(dest),'-alpha','on','-region',
                            '10x35+0+68' if cid=='eclipsewitch' else '8x46+0+35',
                            '-channel','A','-evaluate','set','0','+channel','+region',str(dest)],check=True)
        shutil.copyfile(dest,ROOT/'assets/units'/f'{cid}.png')
        art_rig.build(cid,str(ROOT/'assets/art'),str(ROOT/'assets/rig'))
        print('Prepared',cid)

if __name__=='__main__':
    main()
