"""Rebuild the 62 remaining hero skins and their animation rigs.
Requires ImageMagick and the Python dependencies documented in README.md.
Run: python tools/prep_roster.py && python tools/build_game.py
"""
from pathlib import Path
import subprocess,shutil,argparse
from PIL import Image
import art_rig
from roster_rigs import GROUPS
ROOT=Path(__file__).resolve().parent.parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--group',choices=[g['key'] for g in GROUPS]);args=ap.parse_args()
    for group in GROUPS:
        if args.group and group['key']!=args.group: continue
        src=ROOT/'assets/art/src/roster'/f"{group['key']}.png"
        with Image.open(src) as im: width,height=im.size
        for i,cid in enumerate(group['ids']):
            col,row=i%group['columns'],i//group['columns']
            left,top=round(col*width/group['columns']),round(row*height/group['rows'])
            right,bottom=round((col+1)*width/group['columns']),round((row+1)*height/group['rows'])
            dest=ROOT/'assets/art'/f'{cid}.png'
            subprocess.run(['magick',str(src),'-crop',f'{right-left}x{bottom-top}+{left}+{top}','+repage',
                            '-channel','A','-threshold','8%','+channel','-trim','+repage','-resize','x162','-strip',str(dest)],check=True)
            shutil.copyfile(dest,ROOT/'assets/units'/f'{cid}.png')
            art_rig.build(cid,str(ROOT/'assets/art'),str(ROOT/'assets/rig'))
            print('Prepared',cid)
if __name__=='__main__':main()
