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
       'hexbreaker','barrierweaver','fatekeeper','soulcantor','covenantqueen','plaguesovereign','elixirempress','verdantempress',
       'thornweaver','gravecaller','bonelord','timekeeper','stonemonkey','wukong','eclipsewitch','voidsage'}
BOW={'watchkeeper','moonlance','archer','hunter','sniper','stormranger'}
SHIELD={'aegiscaptain','knight','bulwark','templar','axebrute','glacierwarden','aegispaladin'}

def spec(cid,size):
    w,h=size
    def part(poly,piv):return {'poly':[(x*w,y*h) for x,y in poly],'piv':(piv[0]*w,piv[1]*h)}
    # The forward hand is reserved before the weapon, keeping fingers above it.
    parts={
      'foreR':part([(.18,.6),(.34,.54),(.41,.61),(.35,.7),(.23,.73),(.16,.66)],(.37,.61)),
      'armR':part([(.23,.53),(.43,.48),(.5,.59),(.43,.71),(.23,.72),(.17,.64)],(.43,.54)),
      'armL':part([(.7,.5),(.85,.52),(.95,.69),(.85,.78),(.71,.69)],(.73,.53)),
    }
    if cid=='voidsage':
        # Her tall crescent staff must move as one piece; the old short-staff mask
        # cut off its top. Hair trails behind the head rather than taking the staff.
        parts={
          'foreR':part([(.22,.52),(.36,.51),(.40,.60),(.32,.66),(.22,.61)],(.38,.53)),
          'armR':part([(.34,.45),(.50,.43),(.54,.52),(.43,.62),(.34,.58)],(.48,.47)),
          'armL':part([(.69,.48),(.84,.52),(.90,.68),(.78,.72),(.68,.62)],(.70,.49)),
          'weapon':part([(0,0),(.28,0),(.32,.32),(.26,.40),(.44,.96),(.36,1),(.20,.43),(.08,.37),(0,.26)],(.29,.56)),
          'head':part([(.35,.06),(.73,.06),(.80,.27),(.71,.42),(.49,.44),(.35,.30)],(.56,.42)),
          'legL':part([(.30,.86),(.52,.86),(.52,1),(.26,1)],(.42,.87)),
          'legR':part([(.57,.86),(.80,.86),(.84,1),(.57,1)],(.68,.87)),
          'cape':part([(.75,.25),(1,.42),(1,.77),(.79,.77),(.72,.52)],(.77,.37)),
          'cloth':part([(.37,.65),(.73,.65),(.80,.94),(.33,.94)],(.55,.65)),
        }
        return {'parts':parts,'order':['cape','body','legL','legR','cloth','head','armL','weapon','foreR','armR'],
                'nofill':list(parts),'seams':{'foreR':5,'armR':8,'armL':7,'legL':7,'legR':7,'cloth':6},'fill':2}
    if cid=='shogun':
        # The katana extends far left, so anatomy sits to the right of frame centre.
        # Keep the gripping hand above the blade and pivot at the actual shoulder.
        parts={
          'foreR':part([(.36,.57),(.47,.57),(.49,.67),(.38,.68)],(.48,.60)),
          'armR':part([(.45,.43),(.62,.46),(.58,.60),(.47,.68),(.40,.61)],(.58,.48)),
          'armL':part([(.70,.43),(.83,.45),(.88,.64),(.78,.70),(.70,.58)],(.72,.47)),
          'weapon':part([(0,.85),(.37,.61),(.36,.57),(.43,.56),(.50,.64),(.44,.68),(.39,.68),(.02,.90)],(.41,.64)),
          'head':part([(.40,.08),(.73,.05),(.79,.27),(.67,.43),(.50,.40),(.40,.30)],(.61,.41)),
          'legL':part([(.56,.81),(.73,.81),(.73,1),(.54,1)],(.64,.82)),
          'legR':part([(.74,.81),(.91,.81),(.96,1),(.73,1)],(.82,.82)),
          'cape':part([(.78,.36),(1,.48),(1,.94),(.85,.90),(.76,.66)],(.79,.45)),
          'cloth':part([(.52,.63),(.78,.62),(.86,.85),(.51,.87)],(.65,.65)),
        }
        return {'parts':parts,'order':['cape','body','legL','legR','cloth','head','armL','weapon','foreR','armR'],
                'nofill':list(parts),'seams':{'foreR':5,'armR':8,'armL':7,'legL':7,'legR':7,'cloth':6},'fill':2}
    if cid in SHIELD:
        parts['armL']=part([(.68,.4),(.99,.3),(1,.9),(.82,.96),(.66,.67)],(.73,.53))
    if cid in STAFF|BOW:
        parts['weapon']=part([(0,.04),(.25,.04),(.3,.43),(.42,.94),(.28,1),(.15,.55)],(.28,.64))
    else:
        parts['weapon']=part([(0,.38),(.2,.31),(.29,.5),(.31,.68),(.22,.86),(0,.9)],(.28,.64))
    # A compact head mask leaves the trailing hair and cloak on the body.
    parts['head']=part([(.25,0),(.91,0),(.98,.28),(.84,.49),(.54,.53),(.3,.44),(.2,.24)],(.57,.49))
    parts['legL']=part([(.32,.78),(.57,.78),(.57,1),(.28,1)],(.47,.79))
    parts['legR']=part([(.6,.78),(.9,.78),(.95,1),(.59,1)],(.72,.79))
    parts['cape']=part([(.83,.42),(1,.48),(1,.94),(.85,.9),(.76,.66)],(.8,.5))
    parts['cloth']=part([(.44,.68),(.73,.68),(.8,.84),(.36,.85)],(.57,.69))
    return {'parts':parts,'order':['cape','body','legL','legR','cloth','head','armL','weapon','foreR','armR'],
            # Overlap at joints covers the area a limb exposes while turning. Keep the
            # weapon and outer cape empty so the rest silhouette cannot leave a ghost.
            'nofill':['weapon','foreR','armR','armL','legL','legR','cape','cloth'],
            'seams':{'foreR':5,'armR':8,'armL':7,'legL':7,'legR':7,'cloth':6},'fill':2}
