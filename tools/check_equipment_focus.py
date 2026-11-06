"""Compact item details and real touch equipment inspection on field, bench and combat."""
import asyncio,functools,http.server,json,shutil,threading
from playwright.async_api import async_playwright
from check_progression import QuietHandler,ROOT
from check_touch_controls import Fingers

async def main(server):
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);errors=[];layouts=[]
  for width,height in [(1024,768),(768,1024),(844,390),(852,393)]:
   c=await browser.new_context(viewport={'width':width,'height':height},has_touch=True,is_mobile=True,device_scale_factor=2)
   q=await c.new_page();q.set_default_timeout(10000);q.on('pageerror',lambda e:errors.append(str(e)))
   await q.goto(f'http://127.0.0.1:{server.server_port}/ro-autobattler.html');await q.wait_for_function('Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))');await q.locator('.mode[data-m=normal]').tap()
   await q.evaluate("SND.setSfx(0);SND.setMusic(0);S.gold=200;S.units=[{uid:1,type:'swordsman',star:1,items:['sword:4'],loc:{w:'board',cx:3,cy:5}},{uid:2,type:'crownduelist',fuse:'grandmaster',star:3,items:['sword:2','plate'],loc:{w:'board',cx:4,cy:5}},{uid:3,type:'mage',star:1,items:['sword:6'],loc:{w:'bench',i:0}},{uid:4,type:'archer',star:1,items:[],loc:{w:'board',cx:5,cy:5}}];S.inv=['sword','gem'];renderUI();render()")
   assert await q.locator('#bTeamGear,[data-item-send],.gear-list').count()==0
   before=await q.evaluate('JSON.stringify({units:S.units,inv:S.inv,gold:S.gold})')
   await q.locator('#items [data-i="0"]').tap()
   assert await q.locator('#itemCard .tipi').is_visible();assert await q.evaluate("$('#itemCard').scrollTop===0")
   # Spy on actual canvas painting: every holder uses its own enchantment.
   painted=await q.evaluate('''()=>{const icon=cvCtx.drawImage,sword=iconImg(ITEMS.sword.icon),text=cvCtx.fillText,icons=[],labels=[];try{cvCtx.drawImage=function(im,...args){if(im===sword)icons.push(args[2]);return icon.call(this,im,...args)};cvCtx.fillText=function(s,...args){if(/^\\+[0-5]$/.test(s))labels.push(s);return text.call(this,s,...args)};render();return {icons,labels,large:EQUIPMENT_HITS.slice(0,equipmentHitCount).filter(h=>h.large).map(h=>h.key)};}finally{cvCtx.drawImage=icon;cvCtx.fillText=text;}}''')
   assert sorted(painted['large'])==['sword:2','sword:4','sword:6'],painted
   assert all(n==30 for n in painted['icons']) and all(n in painted['labels'] for n in ['+1','+3','+5']),painted
   assert await q.evaluate('JSON.stringify({units:S.units,inv:S.inv,gold:S.gold})')==before
   await q.locator('[data-item-close]').tap()
   f=Fingers(q,await c.new_cdp_session(q))
   async def held_point(uid,key):
    await q.locator('#cv').scroll_into_view_if_needed();await q.wait_for_timeout(120)
    pos=await q.evaluate('''([uid,key])=>{render();const h=EQUIPMENT_HITS.slice(0,equipmentHitCount).find(h=>(h.owner.uid===uid||h.owner.unitUid===uid)&&h.key===key);if(!h)throw Error('missing held item');const r=cv.getBoundingClientRect();return {x:r.left+h.x*r.width/W,y:r.top+h.y*r.height/H};}''',[uid,key])
    return await f.visual_point(pos['x'],pos['y'])
   # Direct taps on equipped canvas icons bypass hero detail scrolling.
   for uid,key,name in [(1,'sword:4','Iron Sword +3'),(3,'sword:6','Iron Sword +5'),(2,'sword:2','Iron Sword +1')]:
    await q.touchscreen.tap(*await held_point(uid,key));assert await q.locator('#itemCard').is_visible()
    assert await q.evaluate('itemCardContext.key')==key
    assert await q.locator('[data-item-equip],[data-item-sell]').count()==0,'held gear acquired free actions'
    await q.locator('[data-item-close]').tap()
   # A cancelled drag starting on equipment must not open details or move a hero.
   point=await held_point(1,'sword:4');await f.drag(point,(point[0]+20,point[1]),cancel=True)
   assert await q.locator('#itemCard').is_hidden();assert await q.evaluate('canvasTap===null&&dragU===null')
   # Real battle equipment may differ from the owned inventory (Pilfer).
   await q.evaluate("startFight();S.fight.paused=true;for(const a of S.fight.f)a.spawnT=0;S.fight.f.find(a=>a.unitUid===1).items=['gem:2'];renderUI();render()")
   await q.touchscreen.tap(*await held_point(1,'gem:2'));assert await q.evaluate("itemCardContext.key==='gem:2'&&S.phase==='fight'")
   live=await q.evaluate("()=>{render();return EQUIPMENT_HITS.slice(0,equipmentHitCount).filter(h=>h.large).map(h=>h.key)}")
   assert live==['gem:2'],live
   # Combat inspection has no equip/use actions and closes without changing pause.
   assert await q.locator('[data-item-equip]').count()==0
   await q.locator('[data-item-close]').tap();assert await q.evaluate('S.fight.paused&&equipmentFocusKey===null')
   await q.set_viewport_size({'width':height,'height':width});await q.wait_for_timeout(200)
   await q.touchscreen.tap(*await held_point(3,'sword:6'));assert await q.evaluate("itemCardContext.key==='sword:6'")
   await q.locator('[data-item-close]').tap();assert await q.evaluate('document.documentElement.scrollWidth<=innerWidth')
   # Base +0 remains explicit; fused duplicates and edge bench badges stay inside canvas.
   extra=await q.evaluate("()=>{newGame();S.units=[{uid:1,type:'crownduelist',fuse:'grandmaster',star:3,items:['sword','sword:6'],loc:{w:'bench',i:7}}];S.inv=['sword'];openItemCard(0);const text=cvCtx.fillText,labels=[];try{cvCtx.fillText=function(s,...a){if(/^\\+[0-5]$/.test(s))labels.push(s);return text.call(this,s,...a)};render();return {labels,hits:EQUIPMENT_HITS.slice(0,equipmentHitCount).filter(h=>h.large).map(h=>({x:h.x,y:h.y}))};}finally{cvCtx.fillText=text;}}")
   assert '+0' in extra['labels'] and '+5' in extra['labels'],extra
   assert all(22<=h['x']<=490 and h['y']+25<=600 for h in extra['hits']),extra
   await q.locator('[data-item-close]').tap();await q.evaluate('newGame();render()');assert await q.evaluate('EQUIPMENT_HITS.every(h=>h.owner===null)'),'old fighter references retained'
   layouts.append(f'{width}x{height}');await c.close()
  assert not errors,errors
  print(json.dumps({'nativeTouchLayouts':layouts,'paintedEnchantLevels':[0,1,3,5],'fieldBenchCombat':True,'cancelAndRotation':True,'inspectionPreservesInventory':True},indent=2));await browser.close()
if __name__=='__main__':
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
 try:asyncio.run(main(server))
 finally:server.shutdown();server.server_close()
