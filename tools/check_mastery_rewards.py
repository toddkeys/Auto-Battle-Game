"""Mastered-blessing reward claims, preparation-only rerolls and boss progression."""
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
        browser = await p.chromium.launch(
            executable_path=shutil.which('chromium') or shutil.which('chromium-browser'),
            headless=True, args=['--no-sandbox'])
        page = await browser.new_page(viewport={'width': 1440, 'height': 1000})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        await page.goto(f'http://127.0.0.1:{server.server_port}/ro-autobattler.html', wait_until='load')
        await page.locator('.mode[data-m=normal]').click()
        await page.evaluate('''() => {
          window.check=(ok,label)=>{if(!ok)throw Error(label)};
          window.mastered=(hp=90,mode='normal')=>{
            newGame(mode);S.hp=hp;S.buffs=Object.keys(BLESSINGS).flatMap(k=>Array(BLESS_MAX).fill(k));offerBlessings();
          };
          window.claim=k=>$('#cardrow').querySelector(`[data-reward="${k}"]`).click();
          newGame();offerBlessings();check(!$('#cardrow').querySelector('[data-reward]'),'no mastery rewards before cap');
          mastered();const before={gold:S.gold,hp:S.hp,buffs:S.buffs.length,round:S.round};
          const card=$('#cardrow [data-reward=gold]');card.click();card.click();
          check(S.gold===before.gold+3&&S.hp===before.hp,'gold once');
          check(S.buffs.length===before.buffs&&S.round===before.round&&S.freeRerolls===0,'no permanent growth or other reward');
          mastered(98);claim('recovery');check(S.hp===100,'recovery heals run');
          mastered(99);claim('recovery');check(S.hp===100,'recovery caps HP');
          mastered(100);check(!$('#cardrow [data-reward=recovery]'),'full HP replaces recovery');
          check($('#cardrow [data-reward=scoutpurse]'),'full HP purse present');
          let gold=S.gold;claim('scoutpurse');check(S.gold===gold+1&&S.freeRerolls===1,'hybrid reward');
          mastered();claim('scouting');check(S.freeRerolls===2,'two free rolls granted');
          S.gold=0;S.locked=true;renderUI();window.rollCount=S.rollN;
        }''')
        assert 'FREE ×2' in await page.locator('#bReroll').inner_text()
        await page.locator('#bReroll').click()
        await page.evaluate("check(S.gold===0&&S.freeRerolls===1&&S.rollN===rollCount+1&&!S.locked,'free roll works at zero gold and unlocks shop')")
        await page.locator('#bReroll').click()
        await page.evaluate("check(S.gold===0&&S.freeRerolls===0&&S.rollN===rollCount+2,'second roll consumes credit')")
        assert await page.locator('#bReroll').inner_text() == 'Reroll · 2'
        await page.locator('#bReroll').click()
        await page.evaluate("check(S.gold===0&&S.freeRerolls===0&&S.rollN===rollCount+2,'third roll denied without gold');S.gold=5;renderUI()")
        await page.locator('#bReroll').click()
        await page.evaluate('''() => {
          check(S.gold===3&&S.freeRerolls===0,'paid rolling resumes');
          mastered();claim('scouting');S.gold=7;S.units=[];startFight();
          check(S.phase==='prep'&&S.freeRerolls===2,'empty board cannot waste free rolls');
          S.units=[{uid:1,type:'priest',star:1,items:[],loc:{w:'board',cx:3,cy:5}}];
          startFight();S.fight.paused=true;check(S.freeRerolls===0,'unused credits expire when battle starts');
          const n=S.rollN;reroll();check(S.rollN===n&&S.gold===7,'cannot reroll during fight');
          // Daily shop sequence is unchanged by whether the reroll was paid or free.
          mastered(90,'daily');claim('scouting');reroll();const freeShop=JSON.stringify(S.shop);
          newGame('daily');reroll();check(JSON.stringify(S.shop)===freeShop,'daily shop seed preserved');
          mastered();const old=[S.hp,S.gold,S.buffs.length,S.freeRerolls,S.round];
          $('#bBlessSkip').click();check($('#cards').hidden&&JSON.stringify(old)===JSON.stringify([S.hp,S.gold,S.buffs.length,S.freeRerolls,S.round]),'skip gives no reward');
          // Credits and stale reward buttons do not leak into a restarted run.
          mastered();const stale=$('#cardrow [data-reward=gold]');newGame();stale.click();
          check(S.freeRerolls===0&&S.gold===10,'restart resets credits and rejects old rewards');
          // A partial blessing pool must continue to offer its last eligible card.
          mastered();S.buffs=S.buffs.filter(k=>k!=='rhythm');offerBlessings();
          check($('#cardrow [data-k=rhythm]')&&!$('#cardrow [data-reward]'),'partial cap still offers blessings');
          // Use the real boss-win transition, not only the offer helper.
          mastered(99);$('#cards').hidden=true;S.round=15;
          S.units=[{uid:1,type:'priest',star:1,items:[],loc:{w:'board',cx:3,cy:5}}];
          startFight();for(const e of S.fight.f)if(e.team===1)e.hp=0;endFight(true);
        }''')
        await page.wait_for_function("S.phase==='prep'&&S.round===16&&!$('#lootChoice').hidden", timeout=10000)
        await page.locator('#lootRow [data-loot]').first.click()
        await page.wait_for_function("!$('#cards').hidden", timeout=10000)
        await page.locator('[data-reward=recovery]').click()
        await page.evaluate("check(S.hp===100&&$('#cards').hidden,'actual boss recovery');startFight();S.fight.paused=true;check(S.phase==='fight','next battle remains playable');mastered(90)")
        assert await page.evaluate("[...document.querySelectorAll('.bless .bn')].every(e=>e.scrollWidth<=e.clientWidth)"), 'reward names fit their cards'
        if preview:
            await page.mouse.move(0, 0)
            await page.wait_for_timeout(650)
            await page.screenshot(path=str(preview))
        await page.set_viewport_size({'width': 390, 'height': 844})
        assert await page.evaluate("[...document.querySelectorAll('.bless')].every(e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth})"), 'mastery cards fit a phone'
        assert await page.evaluate("[...document.querySelectorAll('.bless .bn')].every(e=>e.scrollWidth<=e.clientWidth)"), 'reward names fit phone cards'
        await page.locator('[data-reward=scouting]').click()
        await page.locator('#bReroll').scroll_into_view_if_needed()
        await page.wait_for_timeout(100)
        assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth'), 'free-roll label fits a phone'
        await page.locator('#bReroll').click()
        await page.evaluate("check(S.freeRerolls===1&&S.gold===10,'phone free roll');mastered(100)")
        await page.locator('[data-reward=scoutpurse]').click()
        await page.evaluate("check(S.freeRerolls===1&&S.gold===11,'phone full-HP alternative')")
        print('Mastery gold, recovery, full-HP replacement, free/paid rerolls, expiry, skip, daily seed, restart, boss transition and phone checks passed.')
        assert not errors, errors
        await browser.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', type=Path)
    args = parser.parse_args()
    server = http.server.ThreadingHTTPServer(
        ('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        asyncio.run(main(server, args.preview))
    finally:
        server.shutdown()
        server.server_close()
