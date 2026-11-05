"""Compatibility entry point for the ten harmonized champion skins.
The original user reference sheets remain archived in assets/art/src.
Run: python tools/prep_hero_skins.py && python tools/build_game.py
"""
import sys
from prep_roster import main
if __name__=='__main__':
    sys.argv[1:]=['--group','champions']
    main()
