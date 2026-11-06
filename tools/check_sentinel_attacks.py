"""Sentinels must actually attack while guarding allies, including Paladin links."""
import asyncio,functools,http.server,json,shutil,threading
from playwright.async_api import async_playwright
from check_progression import QuietHandler,ROOT

async def main(server):
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
  page=await browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(f'http://127.0.0.1:{server.server_port}/ro-autobattler.html')
  await page.wait_for_function('Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))')
  await page.locator('.mode[data-m=normal]').click()
  result=await page.evaluate('''()=>{
   const check=(v,m)=>{if(!v)throw Error(m)},random=Math.random;Math.random=()=>.5;SND.setMusic(0);SND.setSfx(0);
   const sentinels=['watchkeeper','chainwarden','aegiscaptain'],paladins=[null,'bulwark','templar','aegispaladin'];
   const fixture=(id,paladin)=>{newGame();S.round=12;S.units=[{uid:1,type:id,star:1,items:[],loc:{w:'board',cx:3,cy:5}},{uid:2,type:'mage',star:1,items:[],loc:{w:'board',cx:3,cy:6}}];
    if(paladin)S.units.push({uid:3,type:paladin,star:1,items:[],loc:{w:'board',cx:2,cy:5}});startFight();
    const a=S.fight.f.find(b=>b.team===0&&b.type===id),ward=S.fight.f.find(b=>b.team===0&&b.type==='mage'),guardian=paladin&&S.fight.f.find(b=>b.team===0&&b.type===paladin),enemy=mkF('swordsman',1,3,1,1);
    S.fight.f=S.fight.f.filter(b=>b.team===0);S.fight.f.push(enemy);
    for(const b of S.fight.f){b.spawnT=0;b.cd=999;b.sil=999;b.mp=0;b.ms=0;b.leapDelay=0;b.hp=b.max=b.hpLag=100000;}
    a.ms=U[id].ms;a.cd=0;initTactics();return {a,ward,guardian,enemy};};
   const run=n=>{for(let i=0;i<n;i++)step(1/60)};
   let attacks=0,links=0;
   try{
    for(const id of sentinels)for(const paladin of paladins){
      let {a,ward,guardian,enemy}=fixture(id,paladin);check(a.sentryWard===ward,'real ward selection '+id);
      if(guardian){check(a.guard===guardian&&a.guardPct>0,'Paladin really links Sentinel '+id+'/'+paladin);links++;}
      run(480);check(a.attackN>=2&&a.dd>0&&enemy.hp<enemy.max,'Sentinel stood idle '+id+'/'+paladin+' attacks='+a.attackN);check(a.mp>0,'basic attacks restore mana '+id);attacks++;
      // Attacking an available foe must not be preempted by regrouping movement.
      ({a,ward,enemy}=fixture(id,paladin));a.x=3.5;a.y=4;ward.x=3.5;ward.y=6.5;enemy.x=3.5;enemy.y=2;ward.moving=1;
      run(25);check(a.attackN>0&&a.dd>0,'in-range shot blocked by escort '+id+'/'+paladin);attacks++;
    }
    for(const id of sentinels){
      // A first dive still readies the actual Sentinel skill with Guardian Link active.
      let {a,ward,guardian,enemy}=fixture(id,'aegispaladin');a.sil=0;a.cd=999;enemy.x=ward.x;enemy.y=ward.y-.7;enemy.recentDive=1;
      tickTactics(.12,S.fight.f);check(a.castT>0&&!a.firstIntercept,'reactive cast lost '+id);run(40);
      check(a.guard===guardian,'casting broke Guardian Link '+id);check(id==='aegiscaptain'?a.sentinelAuraUntil>S.fight.t:a.dd>0,'reactive skill did not resolve '+id);
      // Guard priority must respect forced targeting from taunt and mind control.
      for(const status of ['taunt','crs']){
        ({a,ward,enemy}=fixture(id,'aegispaladin'));a.x=3.5;a.y=5.5;ward.x=3.5;ward.y=6.5;enemy.x=3.5;enemy.y=6;
        const forced=mkF('swordsman',1,4,5,status==='crs'?0:1);forced.hp=forced.max=100000;forced.ms=0;forced.cd=forced.sil=999;S.fight.f.push(forced);
        a.firstIntercept=false;a[status]=2;if(status==='taunt')a.tauntBy=forced;else a.crsBy=forced;
        run(20);check(a.tgt===forced&&forced.hp<forced.max,'guard overrode '+status+' '+id);
      }
      // Losing the ward cannot strand the Sentinel with a stale dead reference.
      ({a,ward,enemy}=fixture(id,'aegispaladin'));ward.hp=0;run(240);check(a.attackN>0&&a.dd>0,'dead ward stranded '+id);
    }
    return {sentinelTiers:sentinels.length,linkedMatchups:links,attackScenarios:attacks,reactiveSkills:3,forcedTargetScenarios:6,deadWardScenarios:3};
   }finally{Math.random=random;newGame();}
  }''')
  assert not errors,errors
  print(json.dumps(result,indent=2));await browser.close()
if __name__=='__main__':
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
 try:asyncio.run(main(server))
 finally:server.shutdown();server.server_close()
