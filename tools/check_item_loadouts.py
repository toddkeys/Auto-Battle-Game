"""Weighted equipment variety, compact item controls and four effects modes."""
import asyncio,functools,http.server,json,shutil,threading
from playwright.async_api import async_playwright
from check_progression import QuietHandler,ROOT
from check_touch_controls import Fingers

async def ready(page,url):
 await page.goto(url);await page.wait_for_function('Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))')
 await page.locator('.mode[data-m=normal]').click()

async def main(server):
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
  page=await browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));url=f'http://127.0.0.1:{server.server_port}/ro-autobattler.html'
  await ready(page,url)
  result=await page.evaluate('''()=>{
   const check=(v,m)=>{if(!v)throw Error(m)},old=Math.random;SND.setMusic(0);SND.setSfx(0);
   const added=['longbow','warwrap','lens','bulwarkcrest','mirrorcharm','seraphseal','scoutmantle','finisherbadge','soulrelic','callersigil'];
   try{
    Math.random=mulberry32(72819);newGame();const rates={};
    for(const rarity of ['common','rare']){let gems=0;const seen=new Set(),recent=[];for(let i=0;i<20000;i++){const k=rollEquipment(rarity,'sample-'+rarity);check(!recent.includes(k),'recent equipment repeated');recent.push(k);if(recent.length>3)recent.shift();check((rarity==='rare'?RARE:COMMON).includes(k)||k==='gem','wrong rarity '+k);seen.add(k);if(k==='gem')gems++;}rates[rarity]=gems/20000;check(rates[rarity]>.005&&rates[rarity]<.05,'gem weighting '+rarity);check(seen.size===(rarity==='rare'?RARE.length:COMMON.length+1),'pool not reachable '+rarity);}
    // Real reroll preserves enchantment, costs 30 once, and admits a rare gem.
    newGame();S.gold=1000;S.inv=['sword:4'];Math.random=()=>.999999;rerollItem(0);check(S.inv[0]==='gem:4'&&S.gold===970,'common reroll gem/level/cost');
    S.inv=['bell:3'];S.itemHistory={};Math.random=()=>0;rerollItem(0);check(S.inv[0]==='gem:3','rare reroll gem');
    const recent=[];Math.random=mulberry32(32);for(let i=0;i<15;i++){const old=S.inv[0].split(':')[0];rerollItem(0);const k=S.inv[0].split(':')[0];check(k!==old&&!recent.includes(k)&&ILV(S.inv[0])===3,'reroll repeat or lost level');recent.push(k);if(recent.length>3)recent.shift();}
    // Fused duplicate equipment can enchant the second slot when the first is maxed.
    const fused={type:'crownduelist',fuse:'grandmaster',items:['sword:6','sword:2']};S.inv=['sword:2'];check(!itemEquipError(fused,S.inv[0]),'valid second-slot enchant disabled');giveItem(fused,0);check(fused.items[0]==='sword:6'&&fused.items[1]==='sword:4'&&!S.inv.length,'wrong fused slot enchanted');
    // Merchant and chest actually award gems, rather than only exposing a helper.
    newGame();S.round=8;S.gold=30;Math.random=()=>0;openEvent();const wares=[...S.eventWares.keys];check(wares.includes('gem')&&new Set(wares).size===3,'merchant gem and uniqueness');$('#eventbox [data-e=merchant]').click();$('#eventbox [data-buy=gem]').click();check(S.inv.includes('gem')&&S.gold===24,'6g gem purchase');$('#eventbox [data-e=leave]').click();
    S.round=12;openEvent();check(S.eventWares.keys.every(k=>!wares.includes(k)),'merchant repeated prior offering');$('#eventbox [data-e=leave]').click();
    newGame();S.round=8;S.gold=30;openEvent();let n=0;Math.random=()=>n++===0?.5:0;$('#eventbox [data-e=chest]').click();check(S.inv.includes('gem')&&S.gold===26,'chest cannot award gem');$('#eventbox [data-e=leave]').click();
    newGame('daily');S.round=20;const draft=bossLootOptions(),history=JSON.stringify(S.itemHistory);check(JSON.stringify(bossLootOptions())===JSON.stringify(draft)&&JSON.stringify(S.itemHistory)===history,'same draft rerolled on reopening');check(draft.length===3&&new Set(draft).size===3&&draft.every(k=>RARE.includes(k)),'boss rare draft');
    const daily=()=>{newGame('daily');S.round=8;openEvent();return JSON.stringify(S.eventWares.keys)};check(daily()===daily(),'daily merchant seed changed');$('#event').hidden=true;
    // Every new item at every enchant level must produce finite combat stats.
    let levels=0;
    for(const k of added)for(let level=1;level<=MAX_ILV;level++){newGame();S.units=[{uid:1,type:'starcaller',star:3,items:[k+':'+level],loc:{w:'board',cx:3,cy:5}}];startFight();const a=S.fight.f[0];check(['max','hp','atk','asM','ms','skPow','skHeal','shield','mshield','dodge','manaAtk','sumBoost','leech'].every(n=>Number.isFinite(a[n]||0)),'invalid item '+k+'/'+level);check((a.dodge||0)<=.65&&a.hp>0,'item cap '+k);check(subOf(k+':4'),'missing sub-stat '+k);levels++;}
    // The summoner item really affects called creatures, not just its tooltip.
    const caller=key=>{newGame();S.units=[{uid:1,type:'starcaller',star:1,items:key?[key]:[],loc:{w:'board',cx:3,cy:5}}];startFight();return summon(S.fight.f[0],'drake',9)};
    const base=caller(null),boost=caller('callersigil');check(boost.max>base.max&&boost.atk>base.atk,'caller item did not boost pet');
    const raised=key=>{newGame();S.units=[{uid:1,type:'bonelord',star:1,items:key?[key]:[],loc:{w:'board',cx:3,cy:5}}];startFight();S.fight.graves=[{type:'swordsman',star:1,x:3,y:3,team:1,mult:1}];raise(S.fight.f[0],1,.6);return S.fight.f[S.fight.f.length-1]};
    const corpse=raised(null),boostedCorpse=raised('callersigil');check(boostedCorpse.max>corpse.max&&boostedCorpse.atk>corpse.atk,'caller item did not boost raised ally');
    // Visual detail must never alter combat or consume a different random stream.
    const simulate=mode=>{Math.random=mulberry32(9023);newGame();setEffectsMode(mode);S.round=40;S.units=['crownduelist','fatekeeper','starcaller'].map((type,i)=>({uid:i+1,type,star:3,items:[added[i]+':3'],loc:{w:'board',cx:2+i,cy:5}}));startFight();for(const a of S.fight.f){a.hp=a.max=a.hpLag=1e7;}for(let i=0;i<480;i++)step(1/60);const F=S.fight;return JSON.stringify({t:F.t,f:F.f.map(a=>[a.type,a.hp,a.mp,a.x,a.y,a.dd,a.dtk]),proj:F.proj.map(p=>[p.x,p.y,p.mult]),timers:F.timers.map(t=>t.t)})};
    const full=simulate('full');for(const mode of ['auto','tablet','minimal'])check(simulate(mode)===full,'effects changed combat/RNG '+mode);
    setEffectsMode('minimal');clearVisuals(S.fight);burst(2,2,'#fff',100);V({k:'anim',fx:'smoke',x:1,y:1});V({k:'sigilBloom',x:1,y:1});for(const k of ['rune','charge','reticle','meteor','arrowrain','beam'])V({k,x:1,y:1,r:1,c:'#fff'});check(!S.fight.parts.length&&!S.fight.vfx.some(v=>v.k==='anim'||v.k==='sigilBloom'),'minimal decoration survived');check(['rune','charge','reticle','meteor','arrowrain','beam'].every(k=>S.fight.vfx.some(v=>v.k===k)),'lost essential cue');popNum(S.fight.f[0],100,'#fff');check(!S.fight.fx.some(f=>!f.icon),'minimal still emits numbers');
    // Menus preserve an already paused boss fight and resist repeated opens.
    const F=S.fight;F.paused=false;openEffectsMenu();openEffectsMenu();closeEffectsMenu();check(!F.paused,'double menu open stranded fight');F.paused=true;openEffectsMenu();closeEffectsMenu();check(F.paused,'menu unpaused a boss decision');
    newGame();setEffectsMode('minimal');return {newItems:added.length,itemEnchantCases:levels,gemRates:rates,allEffectModesEquivalent:true};
   }finally{Math.random=old;newGame();}
  }''')
  await page.close()
  layouts=[]
  for width,height in [(1024,768),(768,1024),(844,390),(852,393)]:
   context=await browser.new_context(viewport={'width':width,'height':height},has_touch=True,is_mobile=True);q=await context.new_page();q.on('pageerror',lambda e:errors.append(str(e)));await ready(q,url)
   await q.evaluate("()=>{SND.setMusic(0);SND.setSfx(0);S.gold=100;S.units=[{uid:1,type:'swordsman',star:1,items:['sword'],loc:{w:'board',cx:3,cy:5}},{uid:2,type:'crownduelist',fuse:'grandmaster',star:3,items:['plate'],loc:{w:'board',cx:4,cy:5}},{uid:3,type:'mage',star:1,items:[],loc:{w:'bench',i:0}}];S.uid=4;S.inv=['sword','lens','longbow','scroll'];renderUI()}")
   f=Fingers(q,await context.new_cdp_session(q))
   assert await q.locator('#bTeamGear,.gear-row,[data-item-send]').count()==0
   for cx,cy,bench in [(3,5,False),(4,5,False),(0,0,True),(4,5,False)]:
    await q.locator('#items [data-i="0"]').tap()
    assert await q.locator('#itemCard .tipi').is_visible()
    await q.locator('[data-item-equip]').tap();await f.tap_cell(cx,cy,bench=bench)
   assert await q.evaluate("S.units[0].items[0]==='sword:2'&&S.units[1].items.length===0&&S.units[2].items[0]==='longbow'&&S.inv.includes('plate')&&S.inv.includes('lens')&&!S.inv.includes('scroll')")
   await q.locator('#bEffects').tap();assert await q.locator('[data-effects-mode]').evaluate_all('(es)=>es.map(e=>e.dataset.effectsMode)')==['auto','full','tablet','minimal']
   await q.locator('[data-effects-mode="minimal"]').tap();assert await q.evaluate('effectsMode')=='minimal'
   await q.reload();await q.wait_for_selector('.mode[data-m=normal]');assert await q.evaluate('effectsMode')=='minimal'
   await q.locator('.mode[data-m=normal]').tap();await q.locator('[data-quick-buy]').first.tap();assert await q.evaluate('S.units.length')==1
   await q.evaluate("startFight();renderUI()");await q.locator('#bEffects').tap();assert await q.evaluate('S.fight.paused')
   await q.locator('[data-effects-mode=tablet]').tap();assert not await q.evaluate('S.fight.paused')
   assert await q.evaluate('document.documentElement.scrollWidth<=innerWidth')
   layouts.append(f'{width}x{height}');await context.close()
  assert not errors,errors
  print(json.dumps({**result,'nativeTouchLayouts':layouts,'compactEquipEnchantScroll':True},indent=2));await browser.close()
if __name__=='__main__':
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
 try:asyncio.run(main(server))
 finally:server.shutdown();server.server_close()
