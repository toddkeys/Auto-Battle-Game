"""Conditional build mechanics, impact timing and articulated roster motion checks."""
import asyncio
import base64
import functools
import http.server
import shutil
import threading
import argparse
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
        await page.wait_for_function('Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))')
        await page.locator('.mode[data-m=normal]').click()
        result = await page.evaluate('''() => {
          const check=(ok,label)=>{if(!ok)throw Error(label)};
          const near=(a,b,label)=>check(Math.abs(a-b)<1e-6,label+': '+a+' vs '+b);
          const fixture=(items=[],buffs=[])=>{
            newGame();S.buffs=[...buffs];S.round=15;
            S.units=[{uid:1,type:'swordsman',star:1,items:[...items],loc:{w:'board',cx:3,cy:5}}];
            startFight();const a=S.fight.f.find(x=>x.team===0),e=mkF('swordsman',1,4,5,1);
            e.max=e.hp=e.hpLag=100000;e.atk=10;e.cd=99;e.sil=99;e.ms=0;
            a.spawnT=0;a.cd=99;a.mp=0;a.crit=0;S.fight.f=[a,e];return {a,e};
          };
          const random=Math.random;Math.random=()=>.5;
          try{
            let {a,e}=fixture(['stormcore'],['rhythm','rhythm','rhythm']);
            a.castTgt=e;releaseCast(a);near(a.rhythmLeft,3,'rhythm primes three attacks');
            near(a.quickcastT,3,'item haste activates with rhythm');
            for(let i=0;i<3;i++){a.mp=0;beginAttack(a);near(a.mp,MANA_ATTACK+9,'rhythm mana')}
            a.mp=0;beginAttack(a);near(a.mp,MANA_ATTACK,'fourth attack no rhythm');
            releaseCast(a);releaseCast(a);near(a.rhythmLeft,3,'refresh does not add charges');
            a.mp=0;a.drain=1;a.manaCut=.2;beginAttack(a);near(a.mp,(MANA_ATTACK+9)*.4,'rhythm respects mana reduction');
            ({a,e}=fixture(['buckler'],['riposte','riposte','riposte']));
            deal(a,10,false,e);check(a.riposteReady===1,'physical shield primes counter');
            deal(a,10,false,e);near(a.riposteReady,1,'counter one charge');
            // A skill that happens to use mult=1 must not consume the basic-attack proc.
            CASTER=a;hit(a,e,1,false);CASTER=null;near(a.riposteReady,1,'skill keeps counter');
            e.hp=e.max;let hp=e.hp;hit(a,e,1,false);const counterDamage=hp-e.hp;
            near(a.riposteReady,0,'basic consumes counter');
            hp=e.hp;hit(a,e,1,false);near(counterDamage/(hp-e.hp),1.6,'three-stack counter damage');
            a.shield=a.mshield=0;deal(a,10,false,e);near(a.riposteReady,0,'unshielded damage does not prime');
            a.mshield=100;const magic=mkF('mage',1,4,5,1);deal(a,10,false,magic);near(a.riposteReady,1,'magic shield primes counter');
            a.riposteReady=0;a.ward=2;deal(a,10,false,e);near(a.riposteReady,0,'immune hit does not prime');
            a.riposteReady=1;a.rhythmLeft=3;dispel(a);near(a.riposteReady,0,'dispel removes counter');near(a.rhythmLeft,0,'dispel removes rhythm charges');
            ({a,e}=fixture(['fang'],['overflow','overflow','overflow']));
            const pos=[a.x,a.y,e.x,e.y], max=a.max, mp=a.mp;
            deal(e,100,false,a);near(a.shield,12,'excess lifesteal becomes shield');near(a.hp,max,'no overheal HP');
            for(let i=0;i<30;i++)deal(e,100,false,a);
            near(a.shield,max*.18,'reserve cap');
            a.shield=max*.3;deal(e,100,false,a);near(a.shield,max*.3,'does not truncate other shields');
            a.shield=0;a.hp=max-30;deal(e,100,false,a);near(a.hp,max-18,'missing HP heals first');near(a.shield,0,'no excess means no shield');
            a.hp=max;a.wnd=2;deal(e,100,false,a);near(a.shield,6,'wound reduces lifesteal reserve');
            check(JSON.stringify(pos)===JSON.stringify([a.x,a.y,e.x,e.y]),'hit feedback does not move combat positions');
            near(a.mp,mp,'lifesteal does not create mana');
            // Attack wind-up and strike use the original damage timer.
            ({a,e}=fixture());a.cd=0;a.sil=99;a.ms=0;const hpBefore=e.hp;
            step(.01);near(a.attackN,1,'attack starts');step(.125);near(e.hp,hpBefore,'wind-up has no early damage');
            step(.011);check(e.hp<hpBefore,'damage on strike frame');
            check(e.impactT>0&&e.impactK>0&&e.impactX>0,'directional recoil on hit');
            const hpAfter=e.hp;tickFx(.3);near(e.impactT,0,'recoil fades');near(e.hp,hpAfter,'visual fade cannot damage');
            for(const path of BUILD_PATHS){
              newGame();S.buffs=[path.bless];offerBlessings();
              check(itemTip(path.items[0]).includes(path.name)&&itemTip(path.items[0]).includes('owned ×1'),'owned build hint '+path.name);
            }
            newGame();S.buffs=Object.keys(BLESSINGS).filter(k=>k!=='rhythm').flatMap(k=>Array(3).fill(k));offerBlessings();
            check($('#cardrow').textContent.includes('Pairs with Storm Core'),'blessing pairing hint');
            $('#cards').hidden=true;
            // Finite, separate wind-up/strike/recovery poses across all heroes, both directions.
            let frames=0;
            for(const hero of UNITS){
              const poses=[];
              for(const face of [-1,1])for(const swing of [0,1])for(const state of [
                {},{moving:1,walk:1},{atkT:ATK_T*.72},{atkT:ATK_T*.55},
                {atkT:ATK_T*.15},{cast:CAST_T*.3},{rel:REL_T},{rel:REL_T*.2},
                {hurt:.65,hurtK:.8,hurtX:face,hurtY:.2},{frz:1,hurt:.65,hurtK:.8,hurtX:face},{spin:1}
              ]){
                const o={face,swing,ph:0,...state},P=pose(o,U[hero.id],true),R=rigPose(o,hero.id,U[hero.id]);
                for(const v of Object.values(P))check(Number.isFinite(v),'finite body motion '+hero.id);
                for(const joint of Object.values(R))if(typeof joint==='object')for(const v of Object.values(joint))check(Number.isFinite(v),'finite joint '+hero.id);
                drawUnit(hero.id,2,100,100,o);frames++;
                if(face===1&&swing===0&&state.atkT)poses.push(JSON.stringify(R));
              }
              check(new Set(poses).size===3,'distinct attack phases '+hero.id);
              const rest=pose({face:1},U[hero.id],true),hit=pose({face:1,hurt:.6,hurtK:1,hurtX:1},U[hero.id],true);
              check(hit.dx>rest.dx,'local impact recoil '+hero.id);
              const frozen=pose({face:1,frz:1,hurt:.6,hurtK:1,hurtX:1},U[hero.id],true);
              near(frozen.dx,0,'no frozen recoil '+hero.id);
            }
            // Release starts at strike, then settles; it must not wind up again after damage.
            near(releasePhase({rel:REL_T}),.52,'release strike pose');
            near(releasePhase({rel:0}),1,'release rests');
            const o={face:1,atkT:ATK_T*.55,walk:1},base=rigPose(o,'swordsman',U.swordsman),walking=rigPose({...o,moving:1},'swordsman',U.swordsman);
            near(base.legL.r,walking.legL.r,'feet planted during attacks');
            // Exercise the three builds together through real battle ticks and casts.
            ({a,e}=fixture(['fang','stormcore'],['rhythm','riposte','overflow','bastion','hunger']));
            for(let i=0;i<600&&S.phase==='fight';i++)step(1/60);
            check(S.fight.f.every(x=>Number.isFinite(x.hp)&&Number.isFinite(x.mp)&&x.shield>=0),'combined-build battle stable');
            newGame();return {builds:BUILD_PATHS.length,heroes:UNITS.length,motionFrames:frames};
          }finally{Math.random=random;CASTER=null}
        }''')
        await page.evaluate("S.buffs=Object.keys(BLESSINGS).filter(k=>!BUILD_PATHS.some(p=>p.bless===k)).flatMap(k=>Array(3).fill(k));offerBlessings()")
        assert await page.locator('.bless').count() == 3
        if preview:
            await page.wait_for_timeout(650)
            await page.screenshot(path=str(preview.with_name(preview.stem + '_rewards.png')))
        await page.set_viewport_size({'width': 390, 'height': 844})
        assert await page.evaluate("[...document.querySelectorAll('.bless')].every(e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth})"), 'build cards fit a phone'
        await page.locator('.bless[data-k=overflow]').click()
        assert await page.evaluate("$('#cards').hidden&&blessOwned('overflow')===1")
        await page.evaluate("S.inv=['stormcore'];S.buffs=['rhythm'];renderUI()")
        await page.locator('#items .it').first.scroll_into_view_if_needed()
        await page.wait_for_timeout(100)
        await page.mouse.move(0, 0)
        await page.locator('#items .it').first.hover()
        assert await page.locator('#bubble').is_visible()
        assert 'Spellweaver' in await page.locator('#bubble').inner_text()
        assert await page.evaluate("(()=>{const r=$('#bubble').getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight})()"), 'build tooltip fits a phone'
        await page.set_viewport_size({'width': 1440, 'height': 1000})
        await page.evaluate('hideBubble()')
        if preview:
            await page.evaluate("window.requestAnimationFrame=()=>0")
            await page.wait_for_timeout(100)
            # Contact sheet at the actual sprite proportions, drawn larger only for review.
            await page.evaluate('''() => {
              cv.width=1680;cv.height=1000;ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#25313c';ctx.fillRect(0,0,840,500);ANIM=0;
              const ids=['swordsman','nightreaper','grandmaster','eclipsewitch','chieftain','archer'];
              const states=[{}, {atkT:ATK_T*.72}, {atkT:ATK_T*.55}, {atkT:ATK_T*.15}, {rel:REL_T}, {hurt:.65,hurtK:1,hurtX:-1}];
              ids.forEach((id,row)=>{ctx.font='11px sans-serif';ctx.fillStyle='#e8dbc7';ctx.textAlign='left';ctx.fillText(U[id].name,8,row*80+43);
                states.forEach((st,col)=>{const x=160+col*120,y=43+row*80;drawUnit(id,2,x,y,{face:-1,ph:0,...st});});});
              ctx.font='11px sans-serif';ctx.textAlign='center';ctx.fillStyle='#e8dbc7';['GUARD','WIND-UP','STRIKE','RECOVER','SKILL RELEASE','HIT REACTION'].forEach((name,i)=>ctx.fillText(name,160+i*120,495));
            }''')
            preview.write_bytes(base64.b64decode((await page.evaluate('cv.toDataURL()')).split(',')[1]))
        print(result)
        print('Conditional builds, caps, mana reductions, strike timing, hit recovery and roster motion passed.')
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
