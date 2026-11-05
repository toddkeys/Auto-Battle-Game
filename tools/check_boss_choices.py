"""Boss loot draft, optional guard pact and queued preparation offers."""
import argparse
import asyncio
import functools
import http.server
import shutil
import threading
from pathlib import Path
from playwright.async_api import async_playwright
from check_progression import QuietHandler, ROOT

async def main(server, preview):
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=shutil.which('chromium') or shutil.which('chromium-browser'),headless=True,args=['--no-sandbox'])
        page=await browser.new_page(viewport={'width':1440,'height':1000});errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        await page.goto(f'http://127.0.0.1:{server.server_port}/ro-autobattler.html',wait_until='load')
        await page.locator('.mode[data-m=normal]').click()
        await page.evaluate('''() => {
          window.check=(ok,msg)=>{if(!ok)throw Error(msg)};
          window.bossFixture=(round=15,mode='normal',maxed=false)=>{
            newGame(mode);speed=3;S.round=round;
            if(maxed)S.buffs=Object.keys(BLESSINGS).flatMap(k=>Array(BLESS_MAX).fill(k));
            S.units=[{uid:1,type:'priest',star:3,items:[],loc:{w:'board',cx:3,cy:5}}];
          };
          window.winFixture=()=>{for(const e of S.fight.f)if(e.team===1)e.hp=0;endFight(true)};
          bossFixture(14);startFight();winFixture();
        }''')
        await page.wait_for_function("S.round===15&&S.phase==='prep'&&!$('#bossPact').hidden")
        await page.locator('[data-pact=standard]').click()
        await page.evaluate("window.standardWave=genMonsters(15);check(S.bossPact.id==='standard','safe option');")
        await page.locator('#bBossPact').click()
        if preview:
            await page.wait_for_timeout(600)
            await page.screenshot(path=str(preview.with_name(preview.stem+'_pact.png')))
        await page.locator('[data-pact=reinforced]').click()
        await page.evaluate('''() => {
          const wave=genMonsters(15);check(wave.length===standardWave.length+2,'two extra guards');
          for(const old of standardWave)check(wave.some(e=>JSON.stringify(e)===JSON.stringify(old)),'original wave unchanged');
          startFight();check(S.fight.pact==='reinforced','pact captured at battle start');
          check(S.fight.f.filter(e=>e.team===1).length===wave.length,'extra guards actually spawn');
          const before=S.gold;winFixture();check(S.gold===before+5,'victory gold plus pact bonus');
          const after=[S.gold,S.inv.length];endFight(true);check(JSON.stringify(after)===JSON.stringify([S.gold,S.inv.length]),'duplicate win rejected');
          check(S.pendingLoot.length===3&&new Set(S.pendingLoot).size===3&&S.pendingLoot.every(k=>RARE.includes(k)),'unique rare choices');
          check(S.inv.filter(k=>!IT(k).use).length===1,'one ordinary drop, rare slot held for choice');
        }''')
        await page.wait_for_function("S.round===16&&!$('#lootChoice').hidden")
        if preview:
            await page.mouse.move(0,0);await page.wait_for_timeout(600)
            await page.screenshot(path=str(preview))
        await page.set_viewport_size({'width':390,'height':844})
        assert await page.evaluate("[...document.querySelectorAll('#lootRow .bless')].every(e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth})")
        await page.evaluate('''() => {
          const b=$('#lootRow [data-loot]'),key=b.dataset.loot;b.click();b.click();
          check(S.inv.filter(k=>!IT(k).use).length===2,'exactly two boss equipment drops after choice');
          check(S.inv.includes(key)&&!S.pendingLoot&&$('#lootChoice').hidden,'chosen item granted once');
          check(!$('#cards').hidden&&$('#cardrow [data-k]'),'blessing follows loot');
        }''')
        await page.locator('#cardrow [data-k]').first.click()
        await page.evaluate("check(S.offerQueue.length===0,'reward queue drained');startFight();check(S.phase==='fight','next battle playable');bossFixture(30,'daily',true);startFight();winFixture();window.dailyLoot=[...S.pendingLoot]")
        await page.wait_for_function("S.round===31&&!$('#lootChoice').hidden")
        await page.locator('#lootRow [data-loot]').first.click()
        await page.evaluate("check(S.inv.filter(k=>!IT(k).use).length===2,'two bosses still award two equipment total');check(!$('#cards').hidden&&$('#cardrow [data-reward]'),'mastery follows loot')")
        await page.locator('#bBlessSkip').click()
        await page.evaluate('''() => {
          check(S.offerQueue.length===0&&$('#cards').hidden,'mastery skip completes queue');
          bossFixture(30,'daily');startFight();winFixture();check(JSON.stringify(S.pendingLoot)===JSON.stringify(dailyLoot),'daily draft reproducible');
          // Losing a reinforced fight never pays its win-only gold or opens a draft.
          bossFixture();S.bossPact={round:15,id:'reinforced'};startFight();const gold=S.gold;
          for(const a of S.fight.f)if(a.team===0)a.hp=0;endFight(false);
          check(S.gold===gold&&!S.pendingLoot,'no risk payout on loss');
          newGame();window.freshRun=S;
        }''')
        await page.wait_for_timeout(650)
        await page.evaluate("check(S===freshRun&&S.round===1&&S.gold===10,'stale result timer cannot mutate restarted run');bossFixture(19);startFight();winFixture()")
        await page.wait_for_function("S.round===20&&!$('#event').hidden")
        await page.locator('#event [data-e=leave]').click()
        await page.wait_for_function("!$('#bossPact').hidden")
        assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth'), 'boss prep fits a phone'
        assert await page.evaluate("[...document.querySelectorAll('#pactRow .mode')].every(e=>e.scrollWidth<=e.clientWidth)"), 'pact text fits'
        if preview:
            await page.wait_for_timeout(600)
            await page.screenshot(path=str(preview.with_name(preview.stem+'_pact_mobile.png')))
        await page.locator('[data-pact=standard]').click()
        await page.evaluate("check($('#event').hidden&&$('#bossPact').hidden&&S.offerQueue.length===0,'crossroads then pact');startFight();check(S.phase==='fight'&&S.fight.pact==='standard','safe next boss starts')")
        assert not errors,errors
        print('Rare draft quantities/uniqueness, double claims, risk guards/payout, loss/restart, daily seeds, queued events/blessings/mastery and phone checks passed.')
        await browser.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--preview',type=Path);args=parser.parse_args()
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:asyncio.run(main(server,args.preview))
    finally:server.shutdown();server.server_close()
