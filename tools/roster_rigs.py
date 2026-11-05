"""Animation masks for the coordinated roster sheets, in normalized sprite space.
Keep these masks separate from combat stats. All coordinates scale with the art.
"""
import json
from pathlib import Path
MANIFEST=Path(__file__).resolve().parent.parent/'assets/art/src/roster/manifest.json'
GROUPS=json.loads(MANIFEST.read_text())
HEROES={cid:g['key'] for g in GROUPS for cid in g['ids']}
STAFF={'acolyte','priest','highpriest','dawnoracle','snowmender','frostoracle','winterqueen',
       'mage','wizard','highwizard','hexer','bogwitch','doomherald','spiritcaller','stonebinder','starcaller',
       'thornweaver','gravecaller','bonelord','timekeeper'}
BOW={'archer','hunter','sniper','stormranger'}
SHIELD={'knight','bulwark','templar','axebrute','glacierwarden'}

def spec(cid,size):
    w,h=size
    def part(poly,piv):return {'poly':[(x*w,y*h) for x,y in poly],'piv':(piv[0]*w,piv[1]*h)}
    # The forward hand is reserved before the weapon, keeping fingers above it.
    parts={
      'armR':part([(.23,.53),(.43,.48),(.5,.59),(.43,.71),(.23,.72),(.17,.64)],(.43,.54)),
      'armL':part([(.7,.5),(.85,.52),(.95,.69),(.85,.78),(.71,.69)],(.73,.53)),
    }
    if cid in SHIELD:
        parts['armL']=part([(.68,.4),(.99,.3),(1,.9),(.82,.96),(.66,.67)],(.73,.53))
    if cid in STAFF|BOW:
        parts['weapon']=part([(0,.04),(.25,.04),(.3,.43),(.42,.94),(.28,1),(.15,.55)],(.28,.64))
    else:
        parts['weapon']=part([(0,.38),(.2,.31),(.29,.5),(.31,.68),(.22,.86),(0,.9)],(.28,.64))
    # A compact head mask leaves the trailing hair and cloak on the body.
    parts['head']=part([(.25,0),(.91,0),(.98,.28),(.84,.49),(.54,.53),(.3,.44),(.2,.24)],(.57,.49))
    parts['legL']=part([(.32,.86),(.57,.86),(.57,1),(.28,1)],(.47,.87))
    parts['legR']=part([(.6,.86),(.9,.86),(.95,1),(.59,1)],(.72,.87))
    return {'parts':parts,'order':['body','legL','legR','head','armL','weapon','armR'],
            'nofill':['weapon','armR','armL','legL','legR'],'fill':2}
