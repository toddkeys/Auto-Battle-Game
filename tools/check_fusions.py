"""Fusion names, ordered joint casts, secondary traits and equipment rendering."""
import argparse,asyncio,base64,functools,http.server,json,shutil,threading
from pathlib import Path
from playwright.async_api import async_playwright
from check_progression import QuietHandler,ROOT

async def main(server,preview):
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(f'http://127.0.0.1:{server.server_port}/ro-autobattler.html',wait_until='load')
  await page.wait_for_function('Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))')
  await page.locator('.mode[data-m=normal]').click()
  result=await page.evaluate('''()=>{
    const check=(ok,m)=>{if(!ok)throw Error(m)},near=(a,b,m)=>check(Math.abs(a-b)<1e-6,m+': '+a+' / '+b),random=Math.random;
    const newClasses=new Set(['sentinel','abjurer','duelist','soulbinder']),isNew=id=>newClasses.has(U[id].cls),original=Object.fromEntries(Object.entries(SKILLS).map(([id,s])=>[id,s.cast]));let observed=[];
    SND.setMusic(0);SND.setSfx(0);Math.random=()=>.5;newGame();S.round=15;S.extra=6;
    S.units=[{uid:1,type:'swordsman',star:3,items:[],loc:{w:'board',cx:3,cy:5}}];startFight();
    const fixture=(lead,partner)=>{S.phase='fight';const a=mkF(lead,3,3,5,0);a.items=[];fuseFighter(a,partner);
      const enemy=mkF('golem',1,3,4,1),enemy2=mkF('swordsman',1,4,4,1),ally=mkF('mage',1,3,6,0);
      S.fight={f:[a,enemy,enemy2,ally],proj:[],fx:[],vfx:[],decorVfx:0,timers:[],parts:[],graves:[],holes:[],walls:[],t:1,kind:'pvp',stop:0,lastStop:-9,winner:null};
      applySynergy(S.fight.f);applyStars(a);initTactics();for(const b of S.fight.f){b.hp=b.max=b.hpLag=1e8;b.spawnT=0;b.cd=999;b.mp=0;b.sil=999;b.face=-1;b.ms=0;}a.sil=0;a.castTgt=enemy;return {a,enemy,enemy2,ally};};
    try{
      for(const cls of Object.keys(CLASSES))check(FUSE_WORDS[cls]?.length===2,'fusion words '+cls);
      for(const [id,k]of Object.entries(SKILLS))if(k.cast)k.cast=(a,t)=>{observed.push(id);return original[id](a,t)};
      let casts=0,names=0;
      for(const lead of UNITS)for(const partner of UNITS){if(lead.cls===partner.cls||!isNew(lead.id)&&!isNew(partner.id))continue;
        const {a}=fixture(lead.id,partner.id),name=fusedName(lead.id,partner.id),combo=comboName(lead.id,partner.id);
        check(name!==lead.name&&!name.includes('undefined')&&!/[\\u0e00-\\u0e7f]/.test(name),'English fused name '+lead.id+'/'+partner.id);check(combo.trim()===combo&&combo.includes(SKILLS[lead.id].name),'combo name '+name);names++;
        observed=[];releaseCast(a);const order=observed.filter(id=>id===lead.id||id===partner.id);check(order[0]===lead.id&&order[1]===partner.id,'lead then partner '+lead.id+'/'+partner.id+' '+order);
        for(let i=0;i<45&&S.phase==='fight';i++)step(1/60);
        check(S.fight.f.every(b=>Number.isFinite(b.hp)&&Number.isFinite(b.mp)),'finite joint skills '+name);check(CASTER===null&&CAST_TYPE===null,'context restored '+name);casts++;
      }
      // Monk's traits and the lead's own attack stats apply together.
      let {a,enemy}=fixture('crownduelist','grandmaster');check(a.comboStep>0&&a.dodge>0,'secondary Monk traits');near(a.range,U.crownduelist.range,'lead range retained');
      ({a,enemy}=fixture('hexbreaker','phantomblade'));a.root=2;a.mp=a.mpMax;check(!tryCast(a,enemy,true),'root blocks a moving SECONDARY skill');
      ({a,enemy}=fixture('crownduelist','gearmaster'));check(a.turrets>0,'secondary engineer starts turrets');const tower=build(a,3);check(tower?.type==='arctower','secondary Gearmaster builds its own tower');
      // Direct/delayed/shot damage belongs to the skill, not the lead's class.
      ({a,enemy}=fixture('crownduelist','hexbreaker'));enemy.shield=10000;enemy.mshield=10000;
      const physical=enemy.shield,magical=enemy.mshield;withSkill(a,'hexbreaker',()=>hit(a,enemy,1.8,false));check(enemy.shield===physical&&enemy.mshield<magical,'secondary magic hits magic shield');
      let seen=false;withSkill(a,'hexbreaker',()=>later(0,()=>{seen=isMagic(a)}));step(.001);check(seen,'timer retains secondary magic class');
      ({a,enemy}=fixture('hexbreaker','moonlance'));enemy.type='swordsman';enemy.max=enemy.hp=1e8;enemy.shield=10000;enemy.mshield=10000;const beforeMagic=enemy.mshield;withSkill(a,'moonlance',()=>shoot(a,enemy,1.4));check(S.fight.proj[0].arrow,'secondary archer fires its own projectile');for(let i=0;i<30;i++)step(1/60);check(enemy.shield<10000&&enemy.mshield===beforeMagic,'secondary arrow hits physical shield');
      // Trace every equipment layer: a Monk partner supplies NO pixels or limbs.
      const layer=rigLayer;let drawn=[],renders=0;
      rigLayer=(r,i,...args)=>{drawn.push({r,i,g:r.layers[i]});return layer(r,i,...args)};
      try{
        for(const lead of UNITS)for(const partner of UNITS){if(lead.cls===partner.cls||!isNew(lead.id)&&!isNew(partner.id)&&partner.cls!=='monk')continue;
          const rig=SPR[lead.id].rig;drawn=[];buildRig(rig,rigPose({fuse:partner.id,atkT:ATK_T*.55},lead.id,lead),[],null,fusionRig(lead.id,partner.id));
          if(partner.cls==='monk'){check(drawn.every(d=>(d.r.sourceRig||d.r)===rig),'no imported Monk body '+lead.id);check(drawn.some(d=>d.g==='weapon'),'lead keeps own weapon '+lead.id);check(drawn.every(d=>d.r===rig),'original arms and atlas '+lead.id);}
          else{const weapons=drawn.filter(d=>d.g==='weapon');check(weapons.length>0&&weapons.every(d=>(d.r.sourceRig||d.r)===SPR[partner.id].rig),'partner equipment '+lead.id+'/'+partner.id);}
          renders++;
        }
      }finally{rigLayer=layer;}
      // Monk-secondary rendering must preserve every original limb/equipment pixel,
      // including attack/cast/recovery poses; layer counts alone missed cut-out arms.
      let monkStates=0;
      for(const lead of UNITS.filter(u=>u.cls!=='monk'))for(const state of [{},{atkT:ATK_T*.55},{cast:CAST_T*.5},{rel:REL_T},{hurt:.6,hurtK:1,hurtX:1}]){
        const rig=SPR[lead.id].rig;buildRig(rig,rigPose(state,lead.id,lead),[],null);const expected=rg.getImageData(0,0,RIG.width,RIG.height).data;
        buildRig(rig,rigPose({...state,fuse:'grandmaster'},lead.id,lead),[],null,fusionRig(lead.id,'grandmaster'));const actual=rg.getImageData(0,0,RIG.width,RIG.height).data;
        check(expected.every((v,i)=>v===actual[i]),'Monk fusion preserves original silhouette '+lead.id);monkStates++;
      }
      // Prepared fusion crops must preserve the direct renderer's geometry.
      const surface=document.createElement('canvas');surface.width=RIG.width;surface.height=RIG.height;const brush=surface.getContext('2d',{willReadFrequently:true});let geometry=0;
      for(const [lead,partner]of [['shogun','grandmaster'],['aegiscaptain','grandmaster'],['crownduelist','hexbreaker'],['covenantqueen','aegiscaptain']])for(const state of [{},{atkT:ATK_T*.55},{cast:CAST_T*.5},{rel:REL_T},{hurt:.6,hurtK:1,hurtX:1}]){
        const rig=SPR[lead].rig,mix=fusionRig(lead,partner),pose=rigPose({...state,fuse:partner},lead,U[lead]);buildRig(rig,pose,[],null,mix);const pixels=rg.getImageData(0,0,RIG.width,RIG.height).data;
        brush.setTransform(RES,0,0,RES,0,0);brush.clearRect(0,0,168,162);buildRig(rig,pose,[],null,mix,{ctx:brush,direct:true});const direct=brush.getImageData(0,0,surface.width,surface.height).data;
        check(pixels.every((v,i)=>v===direct[i]),'fusion direct geometry '+lead+'/'+partner);geometry++;
      }
      const readPixels=CanvasRenderingContext2D.prototype.getImageData;let reads=0;
      CanvasRenderingContext2D.prototype.getImageData=function(...args){reads++;return readPixels.apply(this,args)};
      try{for(let i=0;i<60;i++)for(const [lead,partner]of [['shogun','grandmaster'],['aegiscaptain','grandmaster'],['crownduelist','hexbreaker']])buildRig(SPR[lead].rig,rigPose({fuse:partner,atkT:ATK_T*.55},lead,U[lead]),[],null,fusionRig(lead,partner));}finally{CanvasRenderingContext2D.prototype.getImageData=readPixels;}
      check(reads===0,'warmed fusion animation performs no pixel readback');
      check(FUSION_PART_LRU.size<=48,'fusion atlas cache bounded');
      for(const id of ['shogun','voidsage','watchkeeper','crownduelist']){const info=infoHTML(id,3,[],null,'grandmaster');check(info.includes('uses own weapon')&&!info.includes('bare-handed')&&info.includes(SKILLS.grandmaster.name),'details show Monk combo '+id);}
      newGame();check(FUSION_PART_LRU.size===0&&FUSED_THUMBS.size===0,'new run releases fusion pictures');
      return {names,orderedCombinedCasts:casts,equipmentRenders:renders,monkOriginalSilhouetteStates:monkStates,fusionGeometryStates:geometry,warmedAnimationReadbacks:reads,maxFusionCanvases:48};
    }finally{for(const[id,fn]of Object.entries(original))SKILLS[id].cast=fn;Math.random=random;CASTER=CAST_TYPE=null;}
  }''')
  if preview:
   data=await page.evaluate('''()=>{cv.width=1200*RES;cv.height=650*RES;ctx.setTransform(RES,0,0,RES,0,0);ctx.fillStyle='#211b18';ctx.fillRect(0,0,1200,650);ANIM=0;
    const pairs=[['crownduelist','hexbreaker'],['hexbreaker','crownduelist'],['aegiscaptain','covenantqueen'],['covenantqueen','aegiscaptain'],['fatekeeper','shogun'],['shogun','fatekeeper'],['shogun','grandmaster'],['voidsage','grandmaster'],['aegiscaptain','grandmaster'],['crownduelist','grandmaster'],['chieftain','grandmaster'],['moonlance','grandmaster'],['watchkeeper','grandmaster'],['chainwarden','grandmaster'],['threadwitch','grandmaster'],['covenantqueen','grandmaster'],['nightreaper','grandmaster'],['grandmaster','crownduelist']];
    pairs.forEach(([id,fuse],i)=>{const x=100+i%6*200,y=60+(i/6|0)*210;drawUnit(id,3,x,y,{face:-1,fuse,atkT:ATK_T*.55,ph:0});ctx.font='13px sans-serif';ctx.fillStyle='#eee';ctx.textAlign='center';ctx.fillText(fusedName(id,fuse),x,y+58);ctx.fillStyle='#b9a789';ctx.font='11px sans-serif';ctx.fillText(U[id].name+' + '+U[fuse].name,x,y+80);});return cv.toDataURL().split(',')[1];}''')
   preview.write_bytes(base64.b64decode(data))
  assert not errors,errors
  print(json.dumps(result,indent=2));print('New-class fusion names, ordered skills, passive traits, damage classes and Monk equipment checks passed.')
  await browser.close()
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--preview',type=Path);args=ap.parse_args();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
 try:asyncio.run(main(server,args.preview))
 finally:server.shutdown();server.server_close()
