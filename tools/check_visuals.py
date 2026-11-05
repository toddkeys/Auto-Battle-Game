"""Full roster and UI smoke checks. Requires Playwright and system Chromium."""
import asyncio,functools,http.server,threading,shutil
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent.parent
class QuietHandler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=shutil.which('chromium') or shutil.which('chromium-browser'),headless=True,args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1440,'height':1000});errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(f'http://127.0.0.1:{server.server_port}/ro-autobattler.html',wait_until='load')
  await page.wait_for_function('ARENA.naturalWidth && Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))')
  await page.locator('.mode[data-m=normal]').click()
  await page.locator('.su').first.click();await page.wait_for_function('S.units.length===1')
  await page.locator('#bLock').click();assert await page.evaluate('S.locked')
  await page.locator('#bPlan').click();assert await page.locator('#planner').is_visible()
  await page.evaluate("$('#planner').hidden=true")
  await page.locator('#bCodex').click();assert await page.locator('.codexgrid .cx').count()==72
  await page.evaluate("$('#codex').hidden=true")
  result=await page.evaluate('''() => {
    if(UNITS.some(u=>!DEFAULT_SPRITES[u.id].art||!SPR[u.id].rig))throw Error('Unreworked hero');
    let casts=0,states=0;
    for(const u of UNITS){
      newGame();S.round=15;S.bossOrder=['golem','lich','wyrm','thornmother','stormdjinn','colossus'];
      S.units=[{uid:1,type:u.id,star:2,items:[],loc:{w:'board',cx:3,cy:5}}];
      startFight();const a=S.fight.f.find(x=>x.team===0);a.castTgt=nearest(a,S.fight.f);releaseCast(a);casts++;
      for(let i=0;i<180&&S.phase==='fight';i++)step(1/60);
      if(S.fight.f.some(x=>!Number.isFinite(x.hp)))throw Error('Invalid HP: '+u.id);
      for(const face of [-1,1])for(const state of [{},{moving:true,walk:2},{cast:CAST_T*.5},{atkT:ATK_T*.5},{rel:REL_T*.5},{frz:1},{die:.5},{spin:1}]){
        drawUnit(u.id,2,100,100,{face,...state});states++;
      }
    }
    for(const u of [...SUMMONS,...MONSTERS])for(const face of [-1,1])for(const state of [{},{moving:true,walk:2},{cast:CAST_T*.5},{atkT:ATK_T*.5},{rel:REL_T*.5},{frz:1},{die:.5},{spin:1}]){
      drawUnit(u.id,1,100,100,{face,...state});states++;
    }
    newGame();$('#cards').hidden=true;
    S.units=UNITS.slice(0,3).map((u,i)=>({uid:i+1,type:u.id,star:1,items:[],loc:{w:'board',cx:2+i,cy:5}}));render();renderUI();
    return {heroes:UNITS.length,casts,renderStates:states};
  }''')
  await page.set_viewport_size({'width':390,'height':844});await page.wait_for_timeout(100)
  assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
  print(result);print('Shop purchase, lock, planner, 72-hero codex and mobile overflow checks passed.');print('Page errors:',errors);assert not errors
  await browser.close()
try:asyncio.run(main())
finally:server.shutdown();server.server_close()
