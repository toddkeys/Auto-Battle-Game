"""Reward exhaustion, new equipment/blessings and mana feedback browser checks."""
import asyncio
import functools
import http.server
import shutil
import threading
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

async def main(server):
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
          window.closeTo=(a,b,label)=>check(Math.abs(a-b)<1e-7,label+': '+a+' vs '+b);
          window.testBattle=(items=[],buffs=[])=>{
            newGame();S.buffs=[...buffs];S.round=15;
            S.units=[{uid:1,type:'priest',star:1,items:[...items],loc:{w:'board',cx:3,cy:5}}];
            startFight();return S.fight.f.find(a=>a.team===0);
          };
          // Partial/exhausted pools must remain selectable, without capped cards.
          newGame();
          S.buffs=Object.keys(BLESSINGS).filter(k=>!['renewal','precision'].includes(k)).flatMap(k=>Array(BLESS_MAX).fill(k));
          S.buffs.push('renewal','renewal','precision','precision');offerBlessings();
          check($('#cardrow').children.length===2,'two remaining rewards');
          check(!$('#cardrow').querySelector(':disabled'),'no dead reward cards');
        }''')
        assert not await page.locator('#bBlessSkip').is_visible()
        await page.locator('.bless[data-k=renewal]').click()
        await page.evaluate("check(blessOwned('renewal')===3,'third stack');offerBlessings();check($('#cardrow').children.length===1,'only one remaining reward')")
        await page.locator('.bless[data-k=precision]').click()
        await page.evaluate("offerBlessings();check($('#cardrow').children.length===0,'no capped rewards');window.beforeSkip=[S.round,S.gold,S.buffs.length]")
        assert await page.locator('#bBlessSkip').is_visible()
        await page.set_viewport_size({'width': 390, 'height': 844})
        assert await page.evaluate('''() => [...document.querySelectorAll('.cardsbox h2,.cardsbox p,#bBlessSkip')].every(e=>{
          const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth;
        })'''), 'exhausted rewards fit a phone'
        await page.locator('#bBlessSkip').click()
        await page.set_viewport_size({'width': 1440, 'height': 1000})
        await page.evaluate("check($('#cards').hidden,'exhausted reward dismissed');check(JSON.stringify(beforeSkip)===JSON.stringify([S.round,S.gold,S.buffs.length]),'skip preserves progression')")
        result = await page.evaluate('''() => {
          newGame();offerBlessings();const card=$('#cardrow').firstElementChild,k=card.dataset.k;
          card.click();card.click();check(blessOwned(k)===1,'double pick blocked below cap');
          const blessingChecks={
            renewal:['regen',v=>v+.0105],precision:['crit',v=>v+.18],pursuit:['ms',v=>v*1.1**3],
            hunger:['leech',v=>v+.105],retribution:['thorns',v=>v+.24],mending:['healOut',v=>v+.3],
            meditation:['manaAtk',v=>v+6]
          };
          const base={...testBattle()};
          for(const [k,[stat,expected]] of Object.entries(blessingChecks)){
            const a=testBattle([],Array(3).fill(k));closeTo(a[stat],expected(base[stat]),k);
          }
          const shielded=testBattle([],Array(3).fill('bastion'));
          closeTo(shielded.shield,base.shield+shielded.max*.3,'First Light shield');
          const items=['buckler','grimoire','heartwood','duelist','hourglass','stormcore'];
          for(const k of items){
            check(EQUIP.includes(k)&&(ITEMS[k].rare?RARE:COMMON).includes(k),'loot pool '+k);
            for(const lv of [1,6]){
              newGame();const u={uid:1,type:'priest',star:1,items:[],loc:{w:'board',cx:3,cy:5}};
              S.units=[u];S.inv=[k];giveItem(u,0);
              for(let n=1;n<lv;n++){S.inv.push(k);giveItem(u,0)}
              check(ILV(u.items[0])===lv&&S.inv.length===0,'equip/enchant '+k);
              S.inv=[k,k];combineItems(0,1);check(ILV(S.inv[0])===2,'combine '+k);
              startFight();const a=S.fight.f.find(x=>x.team===0),scale=IK(u.items[0]);
              for(const stat of ['hp','max','atk','asM','mp','shield','skPow','skHeal'])check(Number.isFinite(a[stat]),'finite '+k+' '+stat);
              check(!/NaN|undefined/.test(itemTip(u.items[0])),'tooltip '+k);
              if(k==='buckler')check(a.shield>=base.max*.22*scale,'buckler shield');
              if(k==='grimoire'){closeTo(a.skPow,base.skPow*(1+.2*scale),'grimoire damage');closeTo(a.skHeal,base.skHeal*(1+.15*scale),'grimoire healing')}
              if(k==='heartwood')check(a.max>base.max&&a.healOut>base.healOut,'heartwood stats');
              if(k==='duelist')check(a.dodge>0&&a.crit>base.crit,'duelist stats');
              if(k==='hourglass')check(a.mp>base.mp&&a.mp<a.mpMax&&a.cloak>=1,'hourglass stats');
              if(k==='stormcore')closeTo(a.quickcastK,.3*scale,'stormcore stat');
              // Pilfer must remove new equipment bonuses without removing hero stats.
              a.shield=0;strip(a);
              check(!a.items.length&&a.shield>=0&&a.mshield>=0,'strip consumed shield '+k);
              closeTo(a.skPow,base.skPow,'strip damage '+k);closeTo(a.skHeal,base.skHeal,'strip healing '+k);
              closeTo(a.quickcastK,0,'strip cast haste '+k);
            }
          }
          let a=testBattle(['stormcore']);a.castTgt=nearest(a,S.fight.f);releaseCast(a);
          closeTo(a.quickcastT,3,'cast activates Storm Core');const originalAS=a.asM;
          releaseCast(a);closeTo(a.quickcastT,3,'refresh timer');closeTo(a.asM,originalAS,'refresh does not stack');
          // Isolate cooldown progression, with both sides alive and no attacks/casts.
          const cooldown=active=>{a.quickcastT=active?3:0;a.cd=10;a.mp=0;a.castT=0;a.spawnT=0;a.sil=10;step(.1);return 10-a.cd};
          const ordinary=cooldown(false),boosted=cooldown(true);
          closeTo(boosted,ordinary*1.3,'Storm Core speeds actual cooldown');
          a.quickcastT=.05;step(.1);closeTo(a.quickcastT,0,'haste expires');
          a.quickcastT=3;dispel(a);closeTo(a.quickcastT,0,'haste dispelled');
          a=testBattle();a.mp=0;a.mg=0;a.drain=1;a.manaCut=.2;
          const fx=S.fight.fx.length;gainMp(a,20);closeTo(a.mp,8,'mana modifiers preserved');
          check(a.mg>0&&S.fight.fx.length===fx,'mana gain glows without numbers');
          a.mp=a.mpMax;a.mg=0;gainMp(a,20);closeTo(a.mg,0,'full mana does not glow');
          a.mp=0;a.drain=0;a.manaCut=0;cleanse(a);closeTo(a.mp,a.mpMax*.15,'cleanse mana');check(a.mg>0,'cleanse glow');
          S.fight.fx=[];pop(a,'+20 Mana','#aaddff');popNum(a,20,'#aaddff','+MP ');
          check(!S.fight.fx.length&&a.mg>0,'legacy mana labels replaced');
          popNum(a,25,'#ffffff');pop(a,'+2 gold','#ffdd77');check(S.fight.fx.length===2,'damage/gold numbers retained');
          a.mg=.05;a.mp=0;a.sil=10;a.cd=10;tickFx(.1);closeTo(a.mg,0,'mana glow fades in combat');
          S.phase='result';a.mg=.05;tickFx(.1);closeTo(a.mg,0,'mana glow fades after combat');
          // Daily choices stay reproducible and do not advance global random state.
          newGame('daily');offerBlessings();const first=$('#cardrow').innerHTML;
          offerBlessings();check(first===$('#cardrow').innerHTML,'seeded daily choices');
          newGame();return {blessings:Object.keys(BLESSINGS).length,newItems:items.length};
        }''')
        # Exercise the real boss reward timer, then continue to the next battle.
        await page.evaluate('''() => {
          testBattle();S.buffs=Object.keys(BLESSINGS).flatMap(k=>Array(BLESS_MAX).fill(k));
          for(const e of S.fight.f)if(e.team===1)e.hp=0;
          endFight(true);
        }''')
        await page.wait_for_function("S.phase==='prep'&&S.round===16&&!$('#cards').hidden", timeout=10000)
        await page.locator('#bBlessSkip').click()
        await page.evaluate("check($('#cards').hidden,'boss skip closes');startFight();check(S.phase==='fight','next battle starts after exhausted rewards')")
        print(result)
        print('Reward caps, exhaustion/continue, boss transition, equipment, haste and mana feedback passed.')
        assert not errors, errors
        await browser.close()

if __name__ == '__main__':
    server = http.server.ThreadingHTTPServer(
        ('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        asyncio.run(main(server))
    finally:
        server.shutdown()
        server.server_close()
