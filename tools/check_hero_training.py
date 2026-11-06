"""Real skill previews, run/RNG isolation, bounded training and native touch controls."""
import asyncio,functools,http.server,json,shutil,threading
from playwright.async_api import async_playwright
from check_progression import QuietHandler,ROOT
from check_touch_controls import Fingers

async def main(server):
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1280,'height':900});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  url=f'http://127.0.0.1:{server.server_port}/ro-autobattler.html'
  await page.goto(url);await page.wait_for_function('Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))');await page.locator('.mode[data-m=normal]').click()
  result=await page.evaluate('''()=>{
   const check=(v,m)=>{if(!v)throw Error(m)};SND.setSfx(0);SND.setMusic(0);newGame('daily');S.gold=129;S.inv=['gem:3'];S.units=[{uid:1,type:'swordsman',star:2,items:['sword'],loc:{w:'board',cx:3,cy:5}}];saveRunNow();
   const original=S,state=JSON.stringify(S),save=localStorage.getItem(RUN_SAVE_KEY),codex=localStorage.getItem('ab_codex'),rng=Math.random,context=ctx;
   let cases=0,casts=0;
   for(const u of UNITS)for(const star of [1,2,3]){
    check(openHeroTraining(u.id),'open '+u.id);TRAINING.star=star;TRAINING.auto=false;TRAINING.ally=true;resetHeroTraining();$('#trainingCast').click();
    for(let i=0;i<360;i++){tickHeroTraining(1/60);if(i%120===0)drawHeroTraining();}
    let F=TRAINING.state.fight;check(F.trainingCasts>=1,'skill did not release '+u.id+'/'+star);casts+=F.trainingCasts;
    check(F.f.every(a=>['hp','max','x','y','atk','dd','hl'].every(k=>Number.isFinite(a[k]))),'nonfinite '+u.id+'/'+star);
    check(F.f.filter(a=>a.summon&&a.hp>0).length<=8,'summon cap '+u.id);check(F.parts.length<=effectBudget().parts,'particles unbounded');
    check(F.trainingHero.star===star,'wrong star');if(star===3&&U[u.id].cls==='summoner')check(F.f.some(a=>a.summon),'missing star starter '+u.id);cases++;closeHeroTraining();
    check(S===original&&JSON.stringify(S)===state&&Math.random===rng&&ctx===context,'run/RNG/context mutation '+u.id);
   }
   check(localStorage.getItem(RUN_SAVE_KEY)===save&&localStorage.getItem('ab_codex')===codex,'training changed persistence');
   // Healing and protective mechanics really resolve, not just a cosmetic preview.
   openHeroTraining('priest');TRAINING.ally=true;TRAINING.auto=false;resetHeroTraining();$('#trainingCast').click();for(let i=0;i<300;i++)tickHeroTraining(1/60);check(TRAINING.state.fight.trainingHero.hl>0,'no healing recorded');
   openHeroTraining('bonelord');TRAINING.auto=false;resetHeroTraining();let peak=0;for(let j=0;j<35;j++){$('#trainingCast').click();for(let i=0;i<100;i++)tickHeroTraining(1/60);peak=Math.max(peak,TRAINING.state.fight.f.length);}check(peak>=8&&peak<=11,'repeat summons grew or failed '+peak);
   const beforeFailure=S;try{withHeroTraining(()=>{throw Error('fixture')})}catch(e){check(e.message==='fixture','unexpected exception')}check(S===beforeFailure&&ctx===context&&Math.random===rng,'exception leaked training context');
   // Real auto attacks/skills, reset, hit tests, no main battle and disposal.
   openHeroTraining('swordsman');for(let i=0;i<600;i++)tickHeroTraining(1/60);check(TRAINING.state.fight.trainingDamage>0,'auto attack no damage');const hero=TRAINING.state.fight.trainingHero;$('#trainingHit').click();check(hero.hp<hero.max,'test hit no damage');
   startFight();check(S.phase==='prep'&&TRAINING,'battle started underneath training');$('#trainingReset').click();check(TRAINING.state.fight.trainingDamage===0&&TRAINING.state.fight.t===0,'reset not fresh');
   const F=TRAINING.state.fight;closeHeroTraining();check(!TRAINING&&$('#heroTraining').hidden&&trainingCanvas.width===0&&!F.parts.length&&!F.vfx.length,'training not disposed');
   // In-flight battle is never replaced/paused by a rejected preview.
   startFight();const battle=S.fight,before=JSON.stringify(S);check(S.phase==='fight','normal battle failed');check(openHeroTraining('mage')===false&&!TRAINING&&S.fight===battle&&JSON.stringify(S)===before,'preview opened during fight');openHeroCard('mage');check($('#heroCard [data-hero-training]').disabled,'combat try button enabled');closeHeroCard();
   newGame();openHeroTraining('mage');newGame();check(!TRAINING&&$('#heroTraining').hidden,'new run leaked training');
   return {heroes:UNITS.length,starCases:cases,releasedCasts:casts,peakSummonRoster:peak,runAndRandomIsolated:true};
  }''')
  layouts=[]
  for width,height in [(1024,768),(768,1024),(844,390),(852,393),(390,844)]:
   c=await browser.new_context(viewport={'width':width,'height':height},has_touch=True,is_mobile=True,device_scale_factor=2);q=await c.new_page();q.on('pageerror',lambda e:errors.append(str(e)));q.set_default_timeout(8000)
   await q.goto(url);await q.locator('.mode[data-m=normal]').tap();await q.evaluate("SND.setSfx(0);SND.setMusic(0);openCodex();openHeroCard('voidsage')")
   await q.locator('[data-hero-training]').tap();assert await q.locator('#heroTraining').is_visible()
   await q.locator('[data-training-star="3"]').tap();assert await q.evaluate('TRAINING.star')==3
   await q.locator('#trainingAuto').tap();assert not await q.evaluate('TRAINING.auto')
   await q.locator('#trainingCast').tap();await q.wait_for_timeout(1100);assert await q.evaluate('TRAINING.state.fight.trainingCasts')>=1
   await q.locator('#trainingAlly').tap();assert await q.evaluate('TRAINING.ally')
   await q.locator('#trainingHit').tap();assert await q.evaluate('TRAINING.state.fight.f.find(a=>a.trainingDummy&&a.team===0).hp<1100')
   f=Fingers(q,await c.new_cdp_session(q));await q.locator('#trainingCanvas').scroll_into_view_if_needed();await q.wait_for_timeout(80)
   box=await q.locator('#trainingCanvas').evaluate('e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}}')
   async def point(x,y):return await f.visual_point(box['x']+box['w']*x/8,box['y']+box['h']*y/8)
   await f.drag(await point(5.5,4.5),await point(6.5,3.5));assert await q.evaluate('TRAINING.state.fight.f.find(a=>a.trainingDummy&&a.team===1).x>6')
   await f.drag(await point(6.5,3.5),await point(5.5,3.5),cancel=True);assert await q.evaluate('TRAINING.drag===null')
   assert await q.evaluate('document.documentElement.scrollWidth<=innerWidth'),'page overflow'
   await q.set_viewport_size({'width':height,'height':width});await q.wait_for_timeout(200);assert await q.evaluate('document.documentElement.scrollWidth<=innerWidth'),'rotated overflow'
   await q.locator('#trainingClose').tap();assert await q.locator('#heroTraining').is_hidden();assert await q.evaluate('TRAINING===null')
   await q.evaluate("openHeroTraining('mage')");await q.locator('#trainingBack').tap();assert await q.locator('#codex').is_visible();assert await q.evaluate('TRAINING===null')
   layouts.append(f'{width}x{height}');await c.close()
  assert not errors,errors
  print(json.dumps({**result,'nativeTouchLayouts':layouts},indent=2));await browser.close()
if __name__=='__main__':
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
 try:asyncio.run(main(server))
 finally:server.shutdown();server.server_close()
