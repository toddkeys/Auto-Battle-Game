"""Real Chromium touch gestures in iPad/phone layouts (not physical iPad Safari).

Uses CDP touch injection so pointer capture, scrolling and pointer cancellation
are handled by the browser, rather than synthetic DOM PointerEvents.
"""
import argparse
import asyncio
import functools
import http.server
import json
import shutil
import threading
from pathlib import Path
from playwright.async_api import async_playwright
from check_progression import QuietHandler, ROOT

class Fingers:
    def __init__(self,page,cdp):self.page,self.cdp=page,cdp
    async def send(self,kind,points=()):
        await self.cdp.send('Input.dispatchTouchEvent',{'type':kind,'touchPoints':[{'x':x,'y':y,'id':i,'radiusX':3,'radiusY':3,'force':1} for i,x,y in points]})
    async def drag(self,start,end,cancel=False):
        x,y=start;tx,ty=end
        await self.send('touchStart',[(1,x,y)])
        for n in range(1,16):
            await self.send('touchMove',[(1,x+(tx-x)*n/15,y+(ty-y)*n/15)])
            await self.page.wait_for_timeout(12)
        await self.send('touchCancel' if cancel else 'touchEnd')
    async def center(self,selector):
        target=self.page.locator(selector).first
        await target.scroll_into_view_if_needed();await self.page.wait_for_timeout(70)
        b=await target.bounding_box();return b['x']+b['width']/2,b['y']+b['height']/2
    async def cell(self,cx,cy=None,bench=False):
        b=await self.page.locator('#cv').bounding_box()
        x=(cx+.5)*64;y=532+32 if bench else (cy+.5)*64
        return b['x']+b['width']*x/512,b['y']+b['height']*y/600
    async def tap_cell(self,cx,cy=None,bench=False):
        await self.page.locator('#cv').scroll_into_view_if_needed();await self.page.wait_for_timeout(250)
        await self.page.touchscreen.tap(*await self.cell(cx,cy,bench))

async def run_device(browser,server,width,height,preview):
    context=await browser.new_context(viewport={'width':width,'height':height},has_touch=True,is_mobile=True,device_scale_factor=2)
    page=await context.new_page();page.set_default_timeout(8000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    await page.goto(f'http://127.0.0.1:{server.server_port}/ro-autobattler.html',wait_until='load',timeout=30000)
    await page.wait_for_function('ARENA.naturalWidth&&Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))')
    await page.locator('.mode[data-m=normal]').tap()
    await page.evaluate('''() => {
      SND.setSfx(0);SND.setMusic(0);
      window.check=(ok,msg)=>{if(!ok)throw Error(msg)};
      window.touchFixture=()=>{newGame();S.gold=200;S.shop=['swordsman','archer','mage','acolyte','thief'];renderUI();};touchFixture();
    }''')
    f=Fingers(page,await context.new_cdp_session(page));tablet=width>600
    # Reflow/compatibility clicks must not activate these controls twice.
    await page.locator('#bSpeed').tap();await page.wait_for_timeout(350)
    assert await page.locator('#bSpeed').inner_text()=='Speed x2'
    await page.locator('#bSpeed').tap();await page.locator('#bSpeed').tap()
    assert await page.locator('#bSpeed').inner_text()=='Speed x1'
    await page.locator('#bLock').tap();await page.wait_for_timeout(350)
    await page.evaluate("check(S.locked,'touch locks exactly once')")
    await page.locator('#bLock').tap()
    await page.evaluate("check(!S.locked,'touch unlock')")
    await page.locator('#shop .su[data-k="0"]').tap();await page.wait_for_timeout(450)
    assert await page.locator('#heroCard').is_visible()
    await page.evaluate("check(S.units.length===0&&S.gold===200,'tap inspects without purchasing');check($('#heroCard').textContent.includes('Swordsman'),'shop detail correct')")
    if preview and width==768:await page.screenshot(path=str(preview.with_name(preview.stem+'_hero.png')))
    await page.locator('[data-hcclose]').tap()
    await page.evaluate('S.gold=0;renderUI()')
    await page.locator('#shop .su[data-k="2"]').tap()
    assert await page.locator('[data-shop-buy]').is_disabled()
    assert await page.locator('#heroCard').is_visible()
    await page.locator('[data-hcclose]').tap()
    await page.evaluate('S.gold=200;renderUI()')
    await page.locator('#shop .su[data-k="1"]').tap()
    await page.locator('[data-shop-buy]').tap()
    await page.evaluate("check(S.units.length===1&&S.units[0].type==='archer'&&S.units[0].loc.w==='bench','explicit buy goes to bench')")
    if tablet:
        start=await f.center('#shop .su[data-k="0"]');end=await f.cell(3,5)
        await f.drag(start,end)
        await page.evaluate("check(S.units.some(u=>u.type==='swordsman'&&u.loc.w==='board'&&u.loc.cx===3&&u.loc.cy===5),'finger shop-to-board purchase');check(S.units.length===2,'no duplicate purchase after drag')")
        start=await f.cell(3,5);end=await f.cell(4,6);before=await page.evaluate('scrollY')
        await f.drag(start,end)
        await page.evaluate("check(S.units.find(u=>u.type==='swordsman').loc.cx===4&&S.units.find(u=>u.type==='swordsman').loc.cy===6,'finger moves owned hero')")
        assert abs(await page.evaluate('scrollY')-before)<2
    else:
        await page.locator('#shop .su[data-k="0"]').tap()
        await page.locator('[data-shop-place]').tap()
        await f.tap_cell(4,6)
        await page.evaluate("check(S.units.some(u=>u.type==='swordsman'&&u.loc.w==='board'&&u.loc.cx===4),'tap-to-place purchase')")
    await page.evaluate("const u=S.units.find(u=>u.type==='swordsman');u.star=2;u.items=['sword'];hoverId='mage';renderUI()")
    await f.tap_cell(4,6)
    await page.evaluate("check($('#heroCard').textContent.includes('Swordsman')&&$('#heroCard .stars').textContent==='★★','owned hero uses actual level, not stale shop hover');check($('#heroCard .held').textContent.includes('Iron Sword'),'owned equipment shown')")
    await page.locator('#heroCard .hi').tap()
    assert await page.locator('#itemCard').is_visible()
    assert await page.locator('[data-item-sell]').count()==0
    await page.locator('[data-item-close]').tap()
    await f.tap_cell(4,6)
    await page.locator('[data-unit-move]').tap()
    await f.tap_cell(2,5)
    await page.evaluate("check(S.units.find(u=>u.type==='swordsman').loc.cx===2&&!S.touchAction,'tap-to-move fallback')")
    # Equip, enchant, unbind and combine without dragging or right-click.
    await page.evaluate("S.units.find(u=>u.type==='swordsman').items=[];S.inv=['sword','sword','fang','fang','scroll'];renderUI()")
    for level in [1,2]:
        await page.locator('#items .it').first.tap()
        await page.locator('[data-item-equip]').tap()
        await f.tap_cell(2,5)
        await page.evaluate(f"check(ILV(S.units.find(u=>u.type==='swordsman').items[0])==={level},'touch equip/enchant level {level}')")
    await page.locator('#items .it').first.tap()
    await page.locator('[data-item-combine]').tap()
    await page.locator('#items .it[data-i="1"]').tap()
    await page.evaluate("check(S.inv[0]==='fang:2'&&!S.touchAction,'tap-to-combine')")
    await page.locator('#items .it').first.tap()
    await page.evaluate('window.goldBefore=S.gold')
    assert await page.locator('#itemCard').is_visible()
    await page.evaluate("check(!S.touchAction,'opening item detail cannot click through to combine')")
    await page.locator('[data-item-reroll]').tap()
    await page.evaluate("check(S.gold===goldBefore-30&&ILV(S.inv[0])===2&&IT(S.inv[0])!==IT('fang'),'touch reroll preserves enchant')")
    await page.locator('#items .it').first.tap()
    await page.locator('[data-item-sell]').tap()
    assert not await page.locator('#confirm').is_visible()
    await page.evaluate("check(S.gold===goldBefore-20,'touch item sells once without confirmation')")
    await page.locator('#items .it').first.tap()
    await page.locator('[data-item-equip]').tap()
    await f.tap_cell(2,5)
    await page.evaluate("check(!S.units.find(u=>u.type==='swordsman').items.length&&S.inv.includes('sword:2'),'touch unbinding scroll')")
    if tablet:
        # Real drag equip and cancel; cancellation must never mutate inventory.
        start=await f.center('#items .it');end=await f.cell(2,5)
        await f.drag(start,end)
        await page.evaluate("check(S.units.find(u=>u.type==='swordsman').items[0]==='sword:2'&&!S.inv.length,'finger drag equips item')")
    # Touch sales are immediate; fusion still requires confirmation.
    await f.tap_cell(2,5)
    await page.locator('[data-unit-sell]').tap()
    assert not await page.locator('#confirm').is_visible()
    await page.evaluate("check(!S.units.some(u=>u.type==='swordsman'),'touch hero sale without confirmation')")
    await page.evaluate("touchFixture();S.round=15;S.units=[{uid:1,type:'swordsman',star:3,items:[],loc:{w:'board',cx:3,cy:5}},{uid:2,type:'mage',star:3,items:[],loc:{w:'board',cx:4,cy:5}}];S.uid=3;renderUI();render()")
    await f.tap_cell(3,5);await page.locator('[data-unit-move]').tap();await f.tap_cell(4,5)
    await page.locator('#confirm [data-yes]').tap()
    await page.evaluate("check(S.units.length===1&&S.units[0].fuse&&S.gold===100,'touch fusion')")
    await page.evaluate("S.inv=['fang','fang'];startFight();S.fight.paused=true;renderUI();render()")
    await page.locator('#items .it').first.tap()
    assert await page.locator('[data-item-equip]').is_disabled()
    assert await page.locator('[data-item-sell]').is_disabled()
    await page.locator('[data-item-combine]').tap()
    await page.locator('#items .it[data-i="1"]').tap()
    await page.evaluate("check(S.inv[0]==='fang:2','touch combines during battle')")
    await page.locator('#cv').scroll_into_view_if_needed()
    await page.wait_for_timeout(100)
    b=await page.locator('#cv').bounding_box()
    enemy=await page.evaluate("(()=>{const a=S.fight.f.find(u=>u.team===1&&U[u.type].boss);return {x:a.x,y:a.y}})()")
    await page.touchscreen.tap(b['x']+b['width']*enemy['x']/8,b['y']+b['height']*(enemy['y']*64-5)/600)
    assert await page.locator('#heroCard').is_visible()
    assert await page.locator('[data-hcmark]').count()==0
    await page.locator('[data-hcclose]').tap()
    # Touch help/tooltips and Team Plan actions have alternatives to hover/native drag.
    await page.evaluate("touchFixture();S.buffs=['rhythm'];renderUI()")
    await page.locator('#bless .bl').tap()
    assert await page.locator('#bubble').is_visible()
    await page.touchscreen.tap(2,2)
    await page.locator('#bPlan').tap()
    await page.locator('#planPick [data-hero="swordsman"]').tap()
    await page.locator('[data-hcmark]').tap();await page.locator('[data-hcclose]').tap()
    await page.locator('#planPick [data-hero="mage"]').tap()
    await page.locator('[data-hcmark]').tap();await page.locator('[data-hcclose]').tap()
    await page.locator('[data-pup="1"]').tap()
    await page.evaluate("check(readMarks()[0]==='mage'&&readMarks()[1]==='swordsman','tap plan reorder')")
    await page.locator('[data-rm="1"]').tap()
    await page.locator('[data-pnew]').tap()
    await page.locator('#presetName').fill('Touch plan')
    await page.locator('[data-psave]').tap()
    await page.evaluate("check(readPresets().some(p=>p.name==='Touch plan'&&p.ids[0]==='mage'),'touch plan preset')")
    await page.locator('#planClose').tap()
    # Cancelled gestures and a second finger cannot spend gold or leave ghosts.
    await page.evaluate('touchFixture()')
    start=await f.center('#shop .su[data-k="0"]');end=(start[0]-50,start[1]+35)
    await f.drag(start,end,cancel=True)
    await page.evaluate("check(S.gold===200&&!S.units.length&&!shopDrag&&!document.querySelector('.dragghost'),'cancelled shop drag cleans up')")
    await f.send('touchStart',[(1,*start)])
    pointer=await page.evaluate('shopDrag.pointerId')
    await f.send('touchStart',[(1,*start),(2,start[0]+25,start[1]+5)])
    assert await page.evaluate('shopDrag.pointerId')==pointer
    await f.send('touchCancel')
    await page.evaluate("check(!shopDrag&&!itemDrag&&!dragU&&S.gold===200,'multi-touch cancellation')")
    if not tablet:
        # Hold a drag at the screen edge; the board can be reached from the lower shop.
        start=await f.center('#shop .su[data-k="0"]');old_y=await page.evaluate('scrollY')
        await f.send('touchStart',[(1,*start)])
        await f.send('touchMove',[(1,start[0],20)])
        await page.wait_for_timeout(450)
        assert await page.evaluate('scrollY')<old_y
        await f.send('touchCancel')
    # Empty board gestures still scroll the page in portrait layouts.
    if height>width:
        await page.evaluate('window.scrollTo(0,0)');await page.wait_for_timeout(120)
        start=await f.cell(1,2);end=(start[0],start[1]-100)
        before=await page.evaluate('scrollY');await f.drag(start,end);await page.wait_for_timeout(100)
        assert await page.evaluate('scrollY')>before,'empty board swipe scrolls page'
        await page.evaluate("check(!dragU&&!canvasTap,'scroll cancellation cleans canvas state')")
    # Long new skill descriptions and refreshed skins stay inspectable on tablets.
    await page.evaluate("touchFixture();S.shop=['watchkeeper','moonlance','voidsage','shogun','fatekeeper'];renderUI()")
    for index,name in enumerate(['Watchkeeper','Moonlance','Stormweaver','Shogun','Fatekeeper']):
        await page.locator(f'#shop .su[data-k="{index}"]').tap()
        assert await page.locator('#heroCard').is_visible()
        assert name in await page.locator('#heroCard').inner_text()
        await page.locator('[data-hcclose]').tap()
    await page.evaluate("check(S.gold===200&&!S.units.length,'new hero details never buy accidentally')")
    await page.evaluate('window.scrollTo(0,0)')
    assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth'),'tablet layout overflow'
    if preview and width==768:await page.screenshot(path=str(preview))
    assert not errors,errors
    await context.close()
    return {'viewport':f'{width}x{height}','touchDrag':tablet,'menus':True,'plan':True,'cancel':True}

async def main(server,preview):
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=shutil.which('chromium') or shutil.which('chromium-browser'),headless=True,args=['--no-sandbox'])
        results=[]
        for width,height in [(1024,768),(768,1024),(390,844)]:
            print(f'Testing {width}x{height}',flush=True)
            results.append(await run_device(browser,server,width,height,preview))
        print(json.dumps(results,indent=2));print('Real touch taps/drags, purchases, unit info/move/fusion, equipment, plan/presets, scrolling and cancellation passed.')
        await browser.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--preview',type=Path);args=parser.parse_args()
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:asyncio.run(main(server,args.preview))
    finally:server.shutdown();server.server_close()
