"""Real touch selling, repeated rotation and non-top-ten run-over regressions.
Audio deliberately advertises no Ogg support and rejects HTML SFX play() calls.
This exercises Safari's codec/autoplay constraints in Chromium, not physical iOS.
"""
import asyncio,functools,http.server,json,shutil,threading,argparse
from pathlib import Path
from playwright.async_api import async_playwright
from check_progression import QuietHandler,ROOT
from check_touch_controls import Fingers

async def main(server,preview):
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
  context=await browser.new_context(viewport={'width':1024,'height':768},has_touch=True,is_mobile=True,device_scale_factor=2)
  await context.add_init_script('''
    window.blockedMediaSfx=0;
    const supports=HTMLMediaElement.prototype.canPlayType,play=HTMLMediaElement.prototype.play;
    HTMLMediaElement.prototype.canPlayType=function(type){return /ogg/i.test(type)?'':supports.call(this,type)};
    HTMLMediaElement.prototype.play=function(){if(/\\.(?:ogg|m4a)(?:$|\\?)/.test(this.src)){blockedMediaSfx++;return Promise.reject(new DOMException('User gesture required','NotAllowedError'));}return play.call(this)};
  ''')
  page=await context.new_page();page.set_default_timeout(10000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  requests=[];page.on('request',lambda r:requests.append(r.url))
  rows=[{'name':f'Champion {i+1}','round':1000-i,'bosses':100,'team':[{'t':'crownduelist','s':3},{'t':'fatekeeper','s':3}],'created_at':'2026-01-01T00:00:00Z'} for i in range(10)]
  await page.route('**/*.supabase.co/**',lambda route:route.fulfill(json=rows))
  await page.goto(f'http://127.0.0.1:{server.server_port}/ro-autobattler.html',wait_until='load',timeout=30000)
  await page.wait_for_function('Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))')
  await page.locator('.mode[data-m=normal]').tap()
  f=Fingers(page,await context.new_cdp_session(page))
  await page.evaluate('''() => {window.check=(v,m)=>{if(!v)throw Error(m)};window.ipadFixture=()=>{newGame();S.gold=200;S.inv=['fang'];S.shop=['archer','mage','thief','acolyte','swordsman'];S.units=[{uid:1,type:'swordsman',star:1,items:[],loc:{w:'board',cx:3,cy:5}}];S.uid=2;renderUI();render();};}''')
  # Effects scheduled OUTSIDE the gesture use the unlocked context, with AAC files.
  await page.evaluate("SND.setMusic(0);SND.setSfx(.8);SND.reset();setTimeout(()=>SND.play('skill:shogun'),50)")
  await page.wait_for_function("SND.inspect().voices.some(v=>v.key==='skill:shogun'&&v.playing)")
  await page.wait_for_timeout(100)
  audio=await page.evaluate('SND.inspect()')
  assert audio['codec']=='aac' and audio['peak']>.0001 and audio['context']=='running',audio
  assert await page.evaluate('blockedMediaSfx')==0
  assert any('/skills/shogun.m4a' in u for u in requests)
  # Every AAC alternative must decode, rather than just existing on disk.
  files=[str(f.relative_to(ROOT)) for folder in ['sfx','skills'] for f in sorted((ROOT/'assets/audio'/folder).glob('*.m4a'))]
  decoded=await page.evaluate('''async files=>{const ac=new AudioContext();let n=0;for(const file of files){const r=await fetch(file);if(!r.ok)throw Error(file);const b=await ac.decodeAudioData(await r.arrayBuffer());let peak=0;for(const x of b.getChannelData(0))peak=Math.max(peak,Math.abs(x));if(b.duration<=0||peak<.001||peak>=.98)throw Error('Bad AAC '+file+' '+peak);n++;}await ac.close();return n;}''',files)

  await page.evaluate('SND.setSfx(0)')
  # Drop on cards, odds and action buttons, far from the small gold display.
  for selector in ['#shop .su[data-k="0"]','#odds','#bReroll']:
   await page.evaluate('ipadFixture()');await page.locator('#cv').scroll_into_view_if_needed();await page.wait_for_timeout(100)
   start=await f.cell(3,5);end=await f.center(selector)
   await f.drag(start,end)
   await page.evaluate("check(!S.units.length&&S.gold===201,'full Shop is a sale target');check($('#confirm').hidden,'no sale confirmation');check(!shopCard.classList.contains('sellready'),'sale overlay removed')")
  await page.evaluate('ipadFixture()');await f.tap_cell(3,5);await page.locator('[data-unit-sell]').tap()
  await page.evaluate("check(!S.units.length&&S.gold===201&&$('#confirm').hidden,'tap hero sell immediately')")
  await page.locator('#items .it').tap();await page.locator('[data-item-sell]').tap()
  await page.evaluate("check(!S.inv.length&&S.gold===206&&$('#confirm').hidden,'tap item sell immediately')")
  # Start a drag, rotate mid-gesture: no stale release may move/buy/sell anything.
  await page.evaluate('ipadFixture()');await page.locator('#cv').scroll_into_view_if_needed();start=await f.cell(3,5)
  await f.send('touchStart',[(1,*start)]);await f.send('touchMove',[(1,start[0]+20,start[1])])
  await page.set_viewport_size({'width':768,'height':1024});await page.wait_for_timeout(400)
  await f.send('touchCancel')
  await page.evaluate("check(!dragU&&!itemDrag&&!shopDrag&&S.units.length===1&&S.gold===200,'rotation cancels active gestures')")
  rotations=[(1024,768),(768,1024),(1366,1024),(1024,1366),(1024,768),(768,1024)]
  for width,height in rotations:
   await page.set_viewport_size({'width':width,'height':height});await page.wait_for_timeout(250)
   await page.evaluate('''()=>{const r=cv.getBoundingClientRect();check(Math.abs(r.width/r.height-W/H)<.001,'board aspect after rotation');check(document.documentElement.scrollWidth<=innerWidth,'no rotation overflow');const l=cellAt({clientX:r.left+r.width*3.5/8,clientY:r.top+r.height*5.5*64/600});check(l&&l.cx===3&&l.cy===5,'rotated input maps to the drawn cell');}''')
  # End-of-run actions must remain visible with a full board and no qualifying name form.
  for width,height in [(1024,768),(768,1024),(1366,1024),(390,844)]:
   await page.set_viewport_size({'width':width,'height':height});await page.wait_for_timeout(200)
   await page.evaluate("ipadFixture();S.phase='over';S.round=4;showSummary()")
   await page.wait_for_function("$('#lb .lbt')&&$('#lb .lbt').querySelectorAll('tr:not(.lbteam)').length===11")
   assert await page.locator('#lbName').count()==0
   if preview:await page.screenshot(path=str(preview))
   await page.evaluate('''()=>{for(const id of ['sumClose','bAgain','bOther']){const r=document.getElementById(id).getBoundingClientRect();check(r.top>=0&&r.bottom<=innerHeight&&r.left>=0&&r.right<=innerWidth,'summary button visible '+id+' '+JSON.stringify({w:innerWidth,h:innerHeight,r:r.toJSON(),panel:$('.run-summary').getBoundingClientRect().toJSON()}));}const r=$('.run-summary').getBoundingClientRect();check(r.height<=innerHeight&&r.top>=0,'summary fits viewport');}''')
   if preview and width==1024:await page.screenshot(path=str(preview))
   await page.locator('#sumClose').tap();assert await page.locator('#modes').is_visible()
   await page.locator('.mode[data-m=normal]').tap()
  # A leaderboard outage must never trap the player behind loading/error text.
  await page.unroute('**/*.supabase.co/**')
  await page.route('**/*.supabase.co/**',lambda route:route.fulfill(status=503,body='offline'))
  await page.evaluate("S.phase='over';S.round=4;showSummary()")
  await page.wait_for_function("$('#lb').textContent.includes(\"Couldn't reach\")")
  await page.locator('#sumClose').tap();assert await page.locator('#modes').is_visible()
  await page.locator('.mode[data-m=normal]').tap()
  await page.evaluate("S.phase='over';S.round=4;showSummary()")
  await page.locator('#bAgain').tap();await page.evaluate("check(S.phase==='prep'&&S.round===1&&$('#summary').hidden,'play again without a top-ten score')")
  assert not errors,errors
  print(json.dumps({'shopSaleTargets':3,'touchSales':'no confirmation','rotationSizes':rotations,'nonTopTenDialogs':4,'aacDecoded':decoded,'effectsPeak':round(audio['peak'],4),'mediaSfxCalls':0},indent=2))
  await browser.close()
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--preview',type=Path);args=ap.parse_args()
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
 try:asyncio.run(main(server,args.preview))
 finally:server.shutdown();server.server_close()
