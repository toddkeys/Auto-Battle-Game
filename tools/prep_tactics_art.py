"""Separate the generated two-character rework sheet without cutting the katana.
The two largest connected alpha components are the complete characters; a tiny
alpha fringe is retained. Only asset extraction/resizing happens here.
"""
import json
from pathlib import Path
import numpy as np
from scipy import ndimage
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent

def main():
    source=ROOT/'assets/art/src/tactics_reworks_source.png'
    pic=Image.open(source).convert('RGBA');pixels=np.asarray(pic).copy()
    labels,count=ndimage.label(pixels[:,:,3]>20)
    areas=np.bincount(labels.ravel());parts=sorted(np.argsort(areas[1:])[-2:]+1,key=lambda i:ndimage.center_of_mass(labels==i)[1])
    sheet=Image.new('RGBA',(400,180))
    for index,label in enumerate(parts):
        mask=ndimage.binary_dilation(labels==label,iterations=1)
        data=pixels.copy();data[:,:,3]=np.where(mask,data[:,:,3],0)
        sprite=Image.fromarray(data);sprite=sprite.crop(sprite.getbbox())
        sprite=sprite.resize((round(sprite.width*162/sprite.height),162),Image.Resampling.LANCZOS)
        sheet.alpha_composite(sprite,(index*200+(200-sprite.width)//2,9))
    sheet.save(ROOT/'assets/art/src/roster/tactics_reworks.png')
if __name__=='__main__':main()
