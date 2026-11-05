"""Extract Night Reaper and six boss skins. Requires ImageMagick, Pillow, NumPy, SciPy.
Run: python tools/prep_boss_skins.py && python tools/build_game.py
"""
from pathlib import Path
import subprocess
import shutil
import art_rig
ROOT=Path(__file__).resolve().parent.parent
CELLS=[('nightreaper',0,275),('golem',275,594),('lich',553,852),('wyrm',852,1244),
       ('thornmother',1244,1541),('stormdjinn',1541,1814),('colossus',1814,2172)]
def main():
    for cid,left,right in CELLS:
        dest=ROOT/'assets/art'/f'{cid}.png'
        subprocess.run(['magick',str(ROOT/'assets/art/src/nightreaper_bosses_atlas.png'),
                        '-crop',f'{right-left}x724+{left}+0','+repage','-channel','A','-threshold','8%',
                        '+channel','-trim','+repage','-resize','x162','-strip',str(dest)],check=True)
        if cid=='lich':
            subprocess.run(['magick',str(dest),'-region','11x110+0+45','-channel','A','-evaluate','set','0','+channel','+region','-strip',str(dest)],check=True)
        if cid=='golem':
            subprocess.run(['magick',str(dest),'-region','16x63+124+0','-channel','A','-evaluate','set','0','+channel','+region','-strip',str(dest)],check=True)
        shutil.copyfile(dest,ROOT/'assets/units'/f'{cid}.png')
        art_rig.build(cid,str(ROOT/'assets/art'),str(ROOT/'assets/rig'))
        print('Prepared',cid)
if __name__=='__main__': main()
