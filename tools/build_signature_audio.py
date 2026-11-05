"""Build hero/boss skill remixes from the shipped, credited SFX (FFmpeg required).
Two-pass loudness normalization preserves headroom. No source packs required.
Usage: python tools/build_signature_audio.py [--only nightreaper]
"""
from pathlib import Path
import argparse,json,re,subprocess,math
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent.parent
SFX=ROOT/'assets/audio/sfx';OUT=ROOT/'assets/audio/skills'
# Main transient, quiet texture, duration. Identity comes from timbre and timing.
RECIPES={
 'sentinel':('trap','shield',.65),'abjurer':('bless','shield',.8),
 'duelist':('steal','flurry',.55),'soulbinder':('curse','teleport',.75),
 'warrior':('flurry','bash',.58),'archer':('arrows','shoot',.55),
 'holy':('bless','heal',.8),'rogue':('steal','hit3',.48),
 'magic':('fire','cast',.7),'gambler':('reroll','star',.55),
 'samurai':('steal','flurry',.58),'frost':('ice','shatter',.78),
 'occultist':('curse','poison',.8),'crusader':('bash','shield',.72),
 'summoner':('summon','cast',.82),'bard':('bless','equip',.72),
 'alchemist':('poison','heal',.65),'necro':('summon','curse',.85),
 'engineer':('zapshot','equip',.55),'monk':('hit2','slam',.48),
 'chrono':('teleport','cast',.7),'ninja':('flurry','teleport',.48),
 'mimic':('teleport','shatter',.65),'mesmer':('curse','bless',.8),
 'monkey':('flurry','bash',.58),'gunner':('snipe','shoot',.48),
 'grapple':('trap','bash',.65),'gravity':('teleport','boom',.85),
 'druid':('summon','heal',.75),'berserker':('flurry','bash',.65),
}
SPECIAL={
 'shogun':('steal','flurry',.8),'phantomblade':('teleport','flurry',.6),
 'nightreaper':('flurry','steal',.52),'aegispaladin':('bash','bless',.8),
 'starwarden':('bash','flurry',.68),'grandmaster':('slam','hit2',.58),
 'voidsage':('zap','shatter',.68),'eclipsewitch':('boom','teleport',.85),
 'wukong':('bash','flurry',.65),'chieftain':('flurry','slam',.72),
 'shadowstep':('steal','teleport',.55),'highwizard':('fire','boom',.8),
 'glacierwarden':('shield','ice',.75),'frostoracle':('ice','shield',.8),
 'winterqueen':('freeze','shatter',.9),
 'golem':('quake','roar_golem',1.0),'lich':('ice','roar_lich',1.0),
 'wyrm':('flame','roar',1.0),'thornmother':('trap','poison',.95),
 'stormdjinn':('zap','boom',.9),'colossus':('bash','quake',.95),
}

def build_one(u):
 cid,cls,cost=u;boss=cid in {'golem','lich','wyrm','thornmother','stormdjinn','colossus'}
 lead,texture,dur=SPECIAL.get(cid,RECIPES.get(cls,('skill','cast',.7)))
 # Stable recipe differences; never consume the game's random number generator.
 seed=sum((i+1)*ord(c) for i,c in enumerate(cid))
 pitch=(seed%7-3)*.32 + (-1.3 if boss else .18*(cost-2))
 if cid=='nightreaper':pitch=1.7
 if cid=='grandmaster':pitch=-2.5
 rate=2**(pitch/12);delay=25+seed%45
 filters=[]
 for i,(gain,shift) in enumerate([(1,0),(.26 if not boss else .34,delay)]):
  filters.append(f'[{i}:a]aresample=44100,asetrate={44100*rate:.6f},aresample=44100,highpass=f={55 if boss or cls in ("monk","berserker") else 100},lowpass=f={9500 if cls in ("frost","magic","archer") else 8200},volume={gain},adelay={shift}:all=1[a{i}]')
 base=';'.join(filters)+';[a0][a1]amix=inputs=2:normalize=0,apad,atrim=duration='+str(dur)
 if cls in ('holy','chrono','gravity','mesmer'):base+=',aecho=0.8:0.6:35|75:0.12|0.06'
 base+=f',atrim=duration={dur},afade=t=in:d=0.008,afade=t=out:st={dur-.12}:d=0.12'
 ins=['-i',str(SFX/(lead+'.ogg')),'-i',str(SFX/(texture+'.ogg'))]
 target=-22 if not boss else -21
 first=subprocess.run(['ffmpeg','-hide_banner','-nostdin',*ins,'-filter_complex',base+f',loudnorm=I={target}:TP=-5:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
 stats=json.JSONDecoder().raw_decode(first.stderr[first.stderr.rfind('{'):])[0]
 norm=f'loudnorm=I={target}:TP=-5:LRA=7:measured_I={stats["input_i"]}:measured_TP={stats["input_tp"]}:measured_LRA={stats["input_lra"]}:measured_thresh={stats["input_thresh"]}:offset={stats["target_offset"]}:linear=true'
 subprocess.run(['ffmpeg','-v','error','-nostdin','-y',*ins,'-filter_complex',base+','+norm+',aresample=44100,alimiter=limit=0.562:level=false','-ac','1','-ar','44100','-c:a','libvorbis','-q:a','4',str(OUT/(cid+'.ogg'))],check=True)
 return cid,{'file':'assets/audio/skills/'+cid+'.ogg','duration':dur,'priority':4 if boss else 3 if cost>=3 else 2,'focus':.5 if boss else .32 if cost>=3 else .18,'gap':.22 if boss else .14,'gain':.92 if boss else .85,'channel':'boss' if boss else 'skill','sources':[lead,texture],'pitch_semitones':round(pitch,2)}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--only');args=ap.parse_args();OUT.mkdir(parents=True,exist_ok=True)
 text=(ROOT/'tools/game_template.html').read_text();block=text.split('const UNITS = [',1)[1].split('\n];',1)[0]
 units=[(cid,cls,int(cost)) for cid,cls,cost in re.findall(r"\{id:'(\w+)'.*?cls:'(\w+)'.*?cost:(\d+)",block)]
 units += [(cid,'monster',5) for cid in ['golem','lich','wyrm','thornmother','stormdjinn','colossus']]
 manifest=OUT/'profiles.json';profiles=json.loads(manifest.read_text()) if manifest.exists() else {}
 selected=[u for u in units if not args.only or u[0]==args.only]
 if not selected:raise SystemExit('Unknown hero/boss')
 with ThreadPoolExecutor(max_workers=4) as pool:
  for cid,profile in pool.map(build_one,selected):profiles[cid]=profile
 from build_safari_audio import convert
 with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(convert,[OUT/(u[0]+'.ogg') for u in selected]))
 manifest.write_text(json.dumps(profiles,indent=2,sort_keys=True)+'\n')
 print('Built',len(selected),'skill signatures with two-pass loudness matching')
if __name__=='__main__':main()
