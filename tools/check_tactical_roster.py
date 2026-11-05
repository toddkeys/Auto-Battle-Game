"""Tactical roster, lethal-hit protection, bounded links and real arrow collision."""
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
  result=await page.evaluate('''() => {
    const check=(v,m)=>{if(!v)throw Error(m)},near=(a,b,m)=>check(Math.abs(a-b)<1e-5,m+': '+a+' vs '+b);
    const random=Math.random;Math.random=()=>.5;SND.setMusic(0);SND.setSfx(0);
    const fixture=(ids=['fatekeeper','mage'])=>{newGame();S.round=15;S.units=[{uid:1,type:'swordsman',star:1,items:[],loc:{w:'board',cx:3,cy:5}}];startFight();
      const fs=ids.map((id,i)=>mkF(id,1,2+i,5,0)),enemy=mkF('golem',1,3,3,1);S.fight.f=[...fs,enemy];S.fight.t=1;S.fight.timers=[];S.fight.holes=[];S.fight.walls=[];
      for(const a of S.fight.f){a.face=-1;a.red=0;a.mp=0;a.sil=99;a.cd=99;a.spawnT=0;a.ms=0;}initTactics();return {fs,enemy};};
    try{
      check(UNITS.length===88,'88 complete heroes');
      for(const cls of Object.keys(CLASSES))check(UNITS.some(u=>u.cls===cls&&u.cost===4),'4-gold class '+cls);
      for(const cls of ['sentinel','abjurer','duelist','soulbinder']){check(UNITS.filter(u=>u.cls===cls).length===3,'three tiers '+cls);check(CLASS_STAR[cls],'star perks '+cls);}
      for(const u of UNITS){check(SPR[u.id].rig&&DEFAULT_SPRITES[u.id].art,'art+rig '+u.id);check(AUDIO_PROFILES[u.id],'audio '+u.id);check(!/[\\u0e00-\\u0e7f]/.test(u.name+SKILLS[u.id].name+SKILLS[u.id].desc),'English text '+u.id);}
      let {fs:[a,b],enemy}=fixture();startReverseFate(a);a.hp=500;b.hp=100;deal(b,120,false,enemy);
      near(b.hp,22,'redirect BEFORE lethal loss');near(a.hp,542,'absorbed damage becomes healing');near(a.fateBudget,a.max*1.5-42,'absorption pays budget');
      b.hp=100;S.fight.t=6;deal(b,120,false,enemy);check(b.hp<0,'outside ultimate still lethal');
      ({fs:[a,b],enemy}=fixture());startReverseFate(a);a.hp=500;a.fateBudget=20;b.hp=100;deal(b,100,false,enemy);near(b.hp,20,'bounded absorption');near(a.fateBudget,0,'budget exhausted');
      a.hp=100;deal(a,120,false,enemy);check(a.hp<0,'no infinite self immunity');
      ({fs:[a,b],enemy}=fixture());a.sil=0;a.mp=a.mpMax;a.hp=100;deal(a,150,false,enemy);check(a.hp>0&&a.fateUntil>S.fight.t&&a.mp<a.mpMax,'emergency ultimate before lethal damage');a.mp=a.mpMax;check(!tryCast(a,enemy,true),'mana cannot bypass ultimate cooldown');
      ({fs:[a,b],enemy}=fixture(['fatekeeper','fatekeeper']));const ally=mkF('mage',1,3,5,0);S.fight.f.push(ally);startReverseFate(a);startReverseFate(b);const total=a.fateBudget+b.fateBudget;ally.hp=100;deal(ally,100,false,enemy);near(ally.hp,35,'overlapping Fatekeepers do not stack');near(total-a.fateBudget-b.fateBudget,35,'one budget pays redirect');
      ({fs:[a,b],enemy}=fixture());startReverseFate(a);b.hp=100;dotTick(b,{src:enemy},100,'#fff');near(b.hp,35,'damage-over-time also redirects');
      // Barriers reduce skills, not ordinary basic attacks, and do not stack.
      ({fs:[a,b],enemy}=fixture(['barrierweaver','mage']));a.castTgt=enemy;releaseCast(a);b.hp=1000;CASTER=enemy;deal(b,100,false,enemy);CASTER=null;near(b.hp,930,'30 percent skill barrier');deal(b,100,false,enemy);near(b.hp,830,'basic hit bypasses spell barrier');
      b.perimeterUntil=S.fight.t+4;b.barrierUntil=S.fight.t-1;b.hp=1000;CASTER=enemy;deal(b,100,false,enemy);CASTER=null;near(b.hp,915,'expired strong barrier does not extend through perimeter');b.perimeterUntil=0;
      b.heavyWard=.25;b.heavyCd=0;b.barrierUntil=0;b.hp=b.max=1000;deal(b,250,false,enemy);near(b.hp,750,'heavy first hit unchanged');deal(b,100,false,enemy);near(b.hp,675,'heavy protection after trigger');
      // The hex is consumed by a real skill release.
      ({fs:[a,b],enemy}=fixture(['hexbreaker','mage']));a.castTgt=enemy;releaseCast(a);check(enemy.hexUntil>S.fight.t,'hex marked');enemy.castTgt=b;releaseCast(enemy);check(enemy.hexUntil===0&&enemy.hexCastUntil>S.fight.t,'next spell consumes hex');
      // Shared damage is finite, cannot recursively spread, and ends with the caster.
      ({fs:[a,b],enemy}=fixture(['threadwitch','swordsman']));const e2=mkF('golem',1,4,3,1);e2.hp=e2.max=10000;e2.red=0;e2.face=-1;enemy.hp=enemy.max=10000;S.fight.f.push(e2);enemy.type=e2.type='swordsman';
      bindSouls(a,2,0,4);const hp1=enemy.hp,hp2=e2.hp;deal(enemy,100,false,b);near(hp1-enemy.hp,100,'primary link damage once');near(hp2-e2.hp,12,'one non-recursive share');
      a.hp=0;const before=e2.hp;deal(enemy,100,false,b);near(e2.hp,before,'dead caster ends link');
      // Consecutive-hit focus caps and resets when changing target.
      ({fs:[a,b],enemy}=fixture(['rapieradept','mage']));enemy.type='swordsman';enemy.hp=enemy.max=100000;a.atk=100;a.duelStep=.06;
      let first=enemy.hp;hit(a,enemy,1,false);first-=enemy.hp;for(let i=0;i<10;i++)hit(a,enemy,1,false);near(a.duelStacks,5,'focus bounded at five');const old=enemy.hp;hit(a,enemy,1,false);near((old-enemy.hp)/first,1.3/1.06,'focus bounded at 30 percent');
      b.team=1;b.hp=10000;hit(a,b,1,false);near(a.duelStacks,1,'new foe resets focus');
      // Arrow uses actual flight, first collision and exact duration (not fixed STATUS.stun duration).
      const arrow=(distance,boss=false,blocker=false,miss=false,wall=false)=>{const q=fixture(['moonlance']);a=q.fs[0];enemy=q.enemy;a.x=.5;a.y=1;enemy.x=.5;enemy.y=1+distance;enemy.type=boss?'golem':'swordsman';enemy.hp=enemy.max=10000;moonArrow(a);
        let front;if(blocker){front=mkF('swordsman',1,0,2,1);front.x=.5;front.y=2;S.fight.f.push(front);}
        if(miss)enemy.x=4;
        if(wall)S.fight.walls=[{team:1,x1:0,y1:2,x2:1,y2:2,hp:1000,t:5}];
        for(let i=0;i<100;i++)tickMoonArrows(1/60);return {stun:enemy.stun,hp:enemy.hp,front,remaining:S.fight.arrows.length};};
      const close=arrow(1),far=arrow(5),boss=arrow(5,true),blocked=arrow(5,false,true),miss=arrow(5,false,false,true),wall=arrow(5,false,false,false,true);
      check(far.stun>close.stun&&far.stun<=3,'distance increases stun');near(boss.stun,.65,'boss stun cap');near(blocked.hp,10000,'first foe intercepts arrow');check(blocked.front.stun>0,'interceptor stunned');near(miss.hp,10000,'straight arrow can miss');near(wall.hp,10000,'wall blocks arrow');check(!far.remaining&&!miss.remaining,'arrow expires');
      // Captain intercepts two DIFFERENT divers, leaving the third actionable.
      ({fs:[a,b],enemy}=fixture(['aegiscaptain','mage']));a.x=3;a.y=5;b.x=3;b.y=5.5;const divers=Array.from({length:3},(_,i)=>{const e=mkF('assassin',1,3+i*.1,5,1);e.recentDive=1;return e;});S.fight.f=[a,b,...divers];initTactics();SKILLS.aegiscaptain.cast(a);tickTactics(.12,S.fight.f);check(a.intercepted.size===2,'captain stops two');check(divers.filter(e=>e.stun>0).length===2,'third diver not stopped');
      // First intrusion readies a real cast without requiring a mouse interaction.
      ({fs:[a,b],enemy}=fixture(['watchkeeper','mage']));a.sil=0;enemy.x=b.x;enemy.y=b.y-.5;enemy.recentDive=1;tickTactics(.12,S.fight.f);check(a.castT>0&&!a.firstIntercept,'reactive sentinel cast');
      // All new/reworked skills survive real simulated combat and cannot grow queues forever.
      const ids=['watchkeeper','chainwarden','aegiscaptain','hexbreaker','barrierweaver','fatekeeper','rapieradept','rosecavalier','crownduelist','threadwitch','soulcantor','covenantqueen','plaguesovereign','elixirempress','verdantempress','moonlance','phantomblade','shogun'];
      let ticks=0;for(const id of ids){const q=fixture([id]);a=q.fs[0];enemy=q.enemy;a.sil=0;a.mp=a.mpMax;a.castTgt=enemy;enemy.max=enemy.hp=100000;a.max=a.hp=100000;releaseCast(a);for(let i=0;i<300&&S.phase==='fight';i++){step(1/60);ticks++;}check(S.fight.f.every(x=>Number.isFinite(x.hp)&&Number.isFinite(x.mp)),'finite battle '+id);check(S.fight.timers.length<100&&(S.fight.arrows||[]).length<20,'bounded queues '+id);}
      newGame();return {heroes:UNITS.length,classes:Object.keys(CLASSES).length,arrowStun:{close:close.stun,far:far.stun,boss:boss.stun},combatTicks:ticks};
    }finally{Math.random=random;CASTER=null;}
  }''')
  if preview:
   encoded=await page.evaluate('''() => {cv.width=1200*RES;cv.height=520*RES;ctx.setTransform(RES,0,0,RES,0,0);ctx.fillStyle='#211b18';ctx.fillRect(0,0,1200,520);
    const ids=['watchkeeper','chainwarden','aegiscaptain','hexbreaker','barrierweaver','fatekeeper','rapieradept','rosecavalier','crownduelist','threadwitch','soulcantor','covenantqueen','plaguesovereign','elixirempress','verdantempress','moonlance','voidsage','shogun','kensei','phantomblade','swordsman','dawnoracle','starwarden','nightreaper'];
    ids.forEach((id,i)=>{const x=100+(i%6)*200,y=60+Math.floor(i/6)*130;drawUnit(id,1,x,y,{face:-1});ctx.font='14px sans-serif';ctx.fillStyle='#f3e7cf';ctx.textAlign='center';ctx.fillText(U[id].name,x,y+52);ctx.fillStyle='#b9a789';ctx.fillText(U[id].cost+' gold',x,y+72);});return cv.toDataURL().split(',')[1];}''')
   preview.write_bytes(base64.b64decode(encoded))
  assert not errors,errors
  print(json.dumps(result,indent=2));print('Tactical defenses, bounded sharing/focus, arrow collision, tiers and new combat skills passed.')
  await browser.close()
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--preview',type=Path);args=ap.parse_args()
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
 try:asyncio.run(main(server,args.preview))
 finally:server.shutdown();server.server_close()
