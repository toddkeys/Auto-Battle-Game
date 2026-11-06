"""Run checkpoints, late boss counterplay, tablet effects and one-tap Shop buys."""
import asyncio,functools,http.server,json,shutil,threading
from playwright.async_api import async_playwright
from check_progression import QuietHandler,ROOT
from check_touch_controls import Fingers

async def ready(page,url):
 await page.goto(url);await page.wait_for_function('Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))')

async def main(server):
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1024,'height':768},has_touch=True,is_mobile=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  score_requests=[]
  async def scores(route):
   score_requests.append(route.request.url);await route.fulfill(status=200,json=[])
  await page.route('**/rest/v1/scores**',scores)
  url=f'http://127.0.0.1:{server.server_port}/ro-autobattler.html'
  await ready(page,url);await page.locator('.mode[data-m=normal]').tap()
  expected=await page.evaluate('''()=>{newGame();SND.setMusic(0);SND.setSfx(0);S.round=235;S.gold=1234;S.hp=67;S.extra=6;S.bigShop=true;S.streak=4;S.bounty=6;S.locked=true;S.freeRerolls=2;
   S.units=[{uid:1,type:'crownduelist',star:3,fuse:'grandmaster',items:['fang:2'],loc:{w:'board',cx:3,cy:5}},{uid:2,type:'mage',star:2,items:[],loc:{w:'bench',i:0}}];S.uid=3;S.buffs=['edge','edge','rhythm'];S.inv=['plate','grimoire:2'];S.shop=['mage',null,'archer','thief','acolyte','swordsman',null,'mage','hexbreaker','rapieradept'];S.bossOrder=[...BOSSES].reverse();S.pendingLoot=RARE.slice(0,3);S.offerQueue=['blessing','pact'];offerBossLoot();renderUI();if(!saveRunNow())throw Error('save failed');return readRunSave().state;}''')
  assert expected is not None
  await ready(page,url)
  assert await page.locator('#modesResume').count()==1
  assert await page.evaluate('readRunSave().state')==expected,'boot overwrote checkpoint'
  await page.locator('#modesResume').tap()
  restored=await page.evaluate('''()=>Object.fromEntries(['round','gold','hp','extra','bigShop','streak','bounty','locked','freeRerolls','units','buffs','inv','shop','bossOrder','pendingLoot','offerQueue'].map(k=>[k,S[k]]))''')
  assert all(restored[k]==expected[k] for k in restored),restored
  await page.locator('[data-loot]').first.tap();await page.wait_for_selector('#cards:not([hidden])')
  choices=await page.locator('#cardrow [data-k]').evaluate_all('(es)=>es.map(e=>e.dataset.k)')
  before=await page.evaluate('({gold:S.gold,inv:S.inv,buffs:S.buffs})');await page.evaluate('saveRunNow()')
  await ready(page,url);await page.locator('#modesResume').tap()
  assert await page.locator('#cardrow [data-k]').evaluate_all('(es)=>es.map(e=>e.dataset.k)')==choices
  assert await page.evaluate('({gold:S.gold,inv:S.inv,buffs:S.buffs})')==before
  await page.locator('#cardrow [data-k]').first.tap();await page.locator('[data-pact=standard]').tap()
  await page.locator('#bSaveExit').tap();assert await page.locator('#modesResume').is_visible()
  await page.locator('#modesResume').tap()
  checkpoint=await page.evaluate('saveRunNow();returnState=JSON.parse(JSON.stringify({round:S.round,hp:S.hp,gold:S.gold,units:S.units,inv:S.inv,buffs:S.buffs,bossPact:S.bossPact}));returnState')
  await page.locator('#bFight').tap();assert await page.evaluate('S.phase')=='fight'
  assert await page.evaluate('saveRunNow()') is False,'combat closures must not replace prep checkpoint'
  saved_before_fight=await page.evaluate("(()=>{const r=readRunSave().state;return Object.fromEntries(Object.keys(returnState).map(k=>[k,r[k]]))})()")
  assert all(saved_before_fight[k]==checkpoint[k] for k in checkpoint if k!='units')
  assert len(saved_before_fight['units'])==len(checkpoint['units'])
  assert all(u['loc']['w']=='board' for u in saved_before_fight['units']),'auto-filled bench is included in checkpoint'
  checkpoint=saved_before_fight
  await ready(page,url);await page.locator('#modesResume').tap()
  assert await page.evaluate('({round:S.round,hp:S.hp,gold:S.gold,units:S.units,inv:S.inv,buffs:S.buffs,bossPact:S.bossPact})')==checkpoint
  # A Daily resumed on a later date must keep the original seed and score board.
  await page.evaluate("newGame('daily');S.seed='daily-2020-01-01';S.round=51;saveRunNow()")
  await ready(page,url);await page.locator('#modesResume').tap()
  assert await page.evaluate('S.seed')=='daily-2020-01-01'
  await page.evaluate("S.hp=0;S.phase='over';showSummary()")
  await page.wait_for_selector('#lbName')
  assert any('board=eq.daily-2020-01-01' in u for u in score_requests)
  assert 'Daily 2020-01-01' in await page.locator('#lb').inner_text()
  assert await page.evaluate("!!localStorage.getItem('ab_daily_2020-01-01')")
  # A paid/resolved event cannot be bought/claimed again on resume.
  await page.evaluate("newGame();S.round=8;S.gold=100;openEvent()")
  await page.locator('[data-e=chest]').tap();event=await page.evaluate('saveRunNow();({gold:S.gold,inv:S.inv,eventDone:S.eventDone})')
  await ready(page,url);await page.locator('#modesResume').tap()
  assert await page.evaluate('({gold:S.gold,inv:S.inv,eventDone:S.eventDone})')==event
  assert await page.locator('#event [data-e=chest]').count()==0
  await page.locator('#event [data-e=leave]').tap()
  # pagehide flushes edits that arrived before the debounce fires.
  await page.evaluate("S.gold=4321;dispatchEvent(new Event('pagehide'))")
  assert await page.evaluate('readRunSave().state.gold')==4321
  quota=await page.evaluate('''()=>{const original=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===RUN_SAVE_KEY)throw new DOMException('Quota','QuotaExceededError');return original.call(this,k,v)};try{const saved=saveRunNow();saveAndExit();return {saved,phase:S.phase,message:$('#msg').textContent}}finally{Storage.prototype.setItem=original}}''')
  assert not quota['saved'] and quota['phase']=='prep' and 'Could not save' in quota['message']
  await page.evaluate("S.hp=0;S.phase='over';showSummary()")
  assert await page.evaluate('readRunSave()') is None
  # Corrupt/newer saves are ignored safely, not loaded as a partial team.
  await page.evaluate("localStorage.setItem(RUN_SAVE_KEY,JSON.stringify({version:99,state:{round:500}}));openModes()")
  assert await page.locator('#modesResume').count()==0
  await page.evaluate("localStorage.removeItem(RUN_SAVE_KEY);$('#modes').hidden=true")
  # Tablet budgets must not alter simulation or its random stream.
  mechanics=await page.evaluate('''()=>{const check=(v,m)=>{if(!v)throw Error(m)};const oldRandom=Math.random;
   const fixture=()=>{newGame();S.round=60;S.extra=6;S.units=[{uid:1,type:'crownduelist',star:3,items:[],loc:{w:'board',cx:2,cy:5}},{uid:2,type:'fatekeeper',star:3,items:[],loc:{w:'board',cx:4,cy:5}},{uid:3,type:'dawnoracle',star:3,items:[],loc:{w:'board',cx:3,cy:6}}];startFight();return S.fight};
   const simulate=mode=>{Math.random=mulberry32(9843);setEffectsMode(mode);const F=fixture();for(let i=0;i<480&&S.phase==='fight';i++)step(1/60);return JSON.stringify({f:F.f.map(a=>[a.type,a.hp,a.mp,a.x,a.y,a.dd]),timers:F.timers.map(t=>t.t),hazards:(F.hazards||[]).map(h=>[h.kind,h.t,h.x,h.y])})};
   try{check(simulate('auto')===simulate('tablet'),'tablet effects changed combat/RNG');
    const F=fixture();setEffectsMode('tablet');clearVisuals(F);burst(1,1,'#fff',2000);check(F.parts.length===80,'tablet particle budget');
    for(const k of ['reticle','meteor','charge','arrowrain','rune'])V({k,x:1,y:1,r:1,c:'#fff'});check(['reticle','meteor','charge','arrowrain','rune'].every(k=>F.vfx.some(v=>v.k===k)),'lost critical cue');
    S.round=39;F.hazards=[];tickBossPatterns(20);check(!F.hazards.length,'late patterns leaked into early rounds');S.round=60;
    let phases=0,avoided=0;
    for(const id of BOSSES){const boss=F.f.find(a=>a.team===1&&U[a.type].boss);boss.type=id;boss.hp=boss.max;boss.atk=1e12;boss.dmgM=1;const hero=F.f.find(a=>a.team===0);hero.hp=hero.max;hero.root=hero.frz=hero.stun=hero.ward=hero.taunt=hero.crs=0;hero.x=3;hero.y=5;
      F.f=F.f.filter(a=>a.team===0||a===boss);F.hazards=[];
      for(const pct of [1,.6,.3]){boss.hp=boss.max*pct;F.hazards=[];const h=prepareBossPattern(boss);check(h&&h.phase===bossPhase(boss)&&h.t>=1.6,'phase/tell '+id);phases++;}
      boss.hp=boss.max;F.hazards=[];const h=prepareBossPattern(boss);h.x=3;h.y=5;if(h.kind==='line'){h.x2=7;h.y2=5;}hero.x=h.kind==='ring'?4.7:3;hero.y=5;hero.ms=2.5;hero.evadeAt=0;hero.walk=0;F.t=10;
      const initial=hazardDepth(h,hero.x,hero.y);check(initial>0,'fixture in danger '+id);for(let n=0;n<100;n++){F.t+=1/60;evadeBossPattern(hero,1/60);}check(hazardDepth(h,hero.x,hero.y)<=0,'AI failed evasion '+id);avoided++;
      hero.x=h.kind==='ring'?4.7:3;hero.y=5;hero.hp=hero.max;hero.shield=hero.mshield=0;hero.red=0;hero.vuln=0;hero.root=9;check(!evadeBossPattern(hero,1/60),'root ignored during evasion');boss.patternAt=1e9;h.t=.2;const hp=hero.hp;tickBossPatterns(.1);check(hero.hp===hp,'pattern hit before warning '+id);tickBossPatterns(.11);check(hero.hp<hp&&hero.hp>hp*.5,'pattern one-shot '+id);
      F.hazards=[];const cancelled=prepareBossPattern(boss);boss.hp=0;hero.hp=hero.max;tickBossPatterns(3);check(hero.hp===hero.max&&!F.hazards.length,'dead boss hazard survived '+id);
    }
    F.hazards=[{kind:'ring',x:3,y:5,r:2.35,safe:1.05,t:1,duration:1.6,name:'Storm Eye',color:'#d3b0ff'}];
    const warningPixels=mode=>{setEffectsMode(mode);ctx.setTransform(RES,0,0,RES,0,0);ctx.clearRect(0,0,W,H);drawBossHazards();return ctx.getImageData(0,0,cv.width,cv.height).data};
    const full=warningPixels('full'),tablet=warningPixels('tablet');check(full.every((v,i)=>v===tablet[i]),'tablet mode changed warning geometry');check(tablet.some(v=>v>0),'warning invisible');
    setEffectsMode('tablet');return {bossPhases:phases,evadedPatterns:avoided,tabletParticles:80,simulationEquivalent:true};
   }finally{Math.random=oldRandom;newGame();}
  }''')
  await ready(page,url)
  assert await page.evaluate('effectsMode')=='tablet'
  await page.close()
  # Native touch buys on three layouts, with both standard and expanded shops.
  shops=[]
  for width,height in [(1024,768),(768,1024),(390,844)]:
   context=await browser.new_context(viewport={'width':width,'height':height},has_touch=True,is_mobile=True)
   q=await context.new_page();q.on('pageerror',lambda e:errors.append(str(e)));await ready(q,url);await q.locator('.mode[data-m=normal]').tap()
   for big in [False,True]:
    await q.evaluate("big=>{newGame();S.gold=100;S.bigShop=big;S.shop=Array.from({length:big?10:5},()=> 'swordsman');renderUI();}",big)
    target=await q.locator('[data-quick-buy="0"]').bounding_box();assert target['height']>=44,target
    f=Fingers(q,await context.new_cdp_session(q));start=await f.center('[data-quick-buy="0"]');await f.drag(start,(start[0]+18,start[1]),cancel=True)
    assert await q.evaluate('S.gold===100&&!S.units.length'),'cancelled Buy tap spent gold'
    await q.locator('[data-quick-buy="0"]').tap()
    await q.wait_for_timeout(150)
    assert await q.evaluate("S.gold===99&&S.units.length===1&&S.units[0].loc.w==='bench'&&S.shop[0]===null")
    assert not await q.locator('#heroCard').is_visible()
   await q.evaluate("()=>{newGame();S.gold=100;S.shop=['swordsman','mage','archer','thief','acolyte'];S.units=['swordsman','swordsman','archer','mage','acolyte','thief','knight','hunter'].map((type,i)=>({uid:i+1,type,star:1,items:[],loc:{w:'bench',i}}));S.uid=9;renderUI()}")
   await q.locator('[data-quick-buy="0"]').tap()
   assert await q.evaluate("S.gold===99&&S.units.length===7&&S.units.some(u=>u.type==='swordsman'&&u.star===2)"),'quick buy must preserve full-bench merges'
   if width>600:
    await q.evaluate("()=>{newGame();S.gold=100;S.shop=['swordsman','mage','archer','thief','acolyte'];renderUI();window.requestAnimationFrame=()=>0}")
    await q.wait_for_timeout(100)
    await q.evaluate("window.dragRenderCalls=0;window.originalDragRender=render;render=(...args)=>{dragRenderCalls++;return originalDragRender(...args)}")
    f=Fingers(q,await context.new_cdp_session(q));start=await f.center('#shop .su[data-k="0"]');end=await f.cell(3,5)
    await f.drag(start,end)
    assert await q.evaluate("S.units.some(u=>u.type==='swordsman'&&u.loc.w==='board')"),'native drag purchase'
    assert await q.evaluate('dragRenderCalls')<5,'shop pointermove redrew scene for every touch sample'
    await q.evaluate('render=originalDragRender')
   await q.locator('#shop .su[data-k="1"]').tap();assert await q.locator('#heroCard').is_visible();await q.locator('[data-hcclose]').tap()
   await q.evaluate("S.gold=0;renderUI()")
   assert await q.locator('[data-quick-buy="1"]').is_disabled()
   assert await q.evaluate('document.documentElement.scrollWidth<=innerWidth')
   shops.append(f'{width}x{height}');await context.close()
  ipad=await browser.new_context(viewport={'width':1024,'height':768},has_touch=True,user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15')
  await ipad.add_init_script("Object.defineProperty(navigator,'maxTouchPoints',{get:()=>5})")
  q=await ipad.new_page();await ready(q,url)
  assert await q.evaluate('effectsMode')=='tablet','detected iPad must default to lighter effects'
  await q.locator('.mode[data-m=normal]').tap();await q.locator('#bEffects').tap()
  assert await q.evaluate('effectsMode')=='full'
  await ready(q,url);assert await q.evaluate('effectsMode')=='full','explicit effect preference survives reload'
  await ipad.close()
  assert not errors,errors
  print(json.dumps({'checkpointRound':235,'unclaimedRewardsRestored':True,'paidEventNotRepeated':True,'midFightResumesPrep':True,'quickBuyLayouts':shops,**mechanics},indent=2))
  await browser.close()
if __name__=='__main__':
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
 try:asyncio.run(main(server))
 finally:server.shutdown();server.server_close()
