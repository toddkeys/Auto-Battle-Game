"""Refresh-rate independent combat, adaptive decoration budgets and pooled effects."""
import asyncio
import functools
import http.server
import json
import shutil
import threading
from playwright.async_api import async_playwright
from check_progression import QuietHandler, ROOT
from check_performance import open_game

async def main(server):
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=shutil.which('chromium') or shutil.which('chromium-browser'),headless=True,args=['--no-sandbox'])
        page,errors=await open_game(browser,server)
        result=await page.evaluate('''() => {
          const check=(ok,msg)=>{if(!ok)throw Error(msg)};
          const originalStep=step,originalRender=render,originalObserve=observeFrameCost,random=Math.random;
          const resetClock=()=>{last=0;ANIM=0;simAccum=0;nextDrawAt=0;lastDrawAt=0;speed=1;};
          const fixture=()=>{newGame('daily');S.round=30;S.extra=6;
            const ids=['nightreaper','grandmaster','eclipsewitch','chieftain','bonelord','starcaller','mechanist','winterqueen','highpriest'];
            S.units=ids.map((type,i)=>({uid:i+1,type,star:3,fuse:UNITS[(i*7+5)%UNITS.length].id,items:['stormcore'],loc:{w:'board',cx:i%8,cy:5+Math.floor(i/8)}}));
            Math.random=mulberry32(1337);startFight();for(const a of S.fight.f){a.max*=20;a.hp=a.hpLag=a.max;}return S.fight;
          };
          try{
            let draws=0,ticks=0,elapsed=0;
            const clockResults=[];
            observeFrameCost=()=>{};
            for(const hz of [30,60,144,240])for(const unlocked of [false,true]){
              fixture();resetClock();unlockedFrames=unlocked;draws=ticks=elapsed=0;
              step=dt=>{ticks++;elapsed+=dt};render=()=>{draws++};
              for(let i=1;i<=hz;i++)frame(i*1000/hz);
              check(ticks===60,'60 simulation ticks at '+hz+' Hz');
              check(Math.abs(elapsed-PACE)<1e-7,'same battle time at '+hz+' Hz');
              check(unlocked?draws===hz:draws<=61,'drawing budget at '+hz+' Hz');
              clockResults.push({hz,unlocked,draws,ticks});
            }
            fixture();resetClock();speed=3;ticks=elapsed=0;
            for(let i=1;i<=240;i++)frame(i*1000/240);
            check(ticks===60&&Math.abs(elapsed-3*PACE)<1e-7,'speed x3 independent of refresh rate');
            fixture();resetClock();S.fight.paused=true;ticks=0;
            for(let i=1;i<=144;i++)frame(i*1000/144);check(ticks===0,'paused fight does not simulate');
            S.fight.paused=false;frame(1000+1000/144);check(ticks===0,'no catch-up from pause');
            step=originalStep;
            const run=(level,hz,unlocked)=>{
              fixture();resetClock();unlockedFrames=unlocked;FX_LOAD.level=level;
              for(let i=1;i<=hz*3;i++)frame(i*1000/hz);
              const F=S.fight;return JSON.stringify({t:F.t,f:F.f.map(a=>[a.type,a.hp,a.mp,a.x,a.y,a.dd,a.dtk,a.hl]),proj:F.proj.map(a=>[a.x,a.y,a.mult]),timers:F.timers.map(t=>t.t)});
            };
            const standard=run(0,60,false);
            check(run(2,144,false)===standard,'adaptive quality preserves combat and RNG at 144 Hz');
            check(run(2,240,true)===standard,'unlocked 240 Hz preserves combat and RNG');
            render=originalRender;observeFrameCost=originalObserve;
            newGame();FX_LOAD.level=0;FX_LOAD.ema=0;FX_LOAD.slow=FX_LOAD.fast=0;
            observeFrameCost(35,1/60,60);check(FX_LOAD.level===0,'single spike does not reduce detail');
            for(let i=0;i<120;i++)observeFrameCost(25,1/60,50);
            check(FX_LOAD.level===2,'sustained load reduces decorations');
            for(let i=0;i<900;i++)observeFrameCost(1,1/60,16.67);
            check(FX_LOAD.level===0,'sustained recovery restores decorations');
            fixture();clearVisuals(S.fight);FX_LOAD.level=2;
            const F=S.fight;const projectiles=F.proj,timers=F.timers;
            burst(1,1,'#fff',2000);check(F.parts.length===FX_BUDGETS[2].parts,'particle cap');
            for(let i=0;i<200;i++)V({k:'sigilBloom',x:1,y:1,r:1,c:'#fff'});
            for(const k of ['reticle','meteor','charge','arrowrain','rune'])V({k,x:1,y:1,r:1,c:'#fff'});
            check(F.vfx.filter(decorativeVfx).length===FX_BUDGETS[2].vfx,'decoration cap');
            check(['reticle','meteor','charge','arrowrain','rune'].every(k=>F.vfx.some(v=>v.k===k)),'telegraphs preserved');
            check(F.proj===projectiles&&F.timers===timers,'visual limits do not replace gameplay queues');
            // Dropping decorations consumes exactly the original random draws.
            const rngAfter=level=>{clearVisuals(F);FX_LOAD.level=level;Math.random=mulberry32(42);burst(1,1,'#fff',2000);for(let i=0;i<200;i++)V({k:'shards',x:1,y:1});for(let i=0;i<10;i++)wallBreakFx({src:{type:'glacierwarden'},team:0,x1:1,y1:1,x2:4,y2:1},true);return Math.random()};
            check(rngAfter(0)===rngAfter(2),'cosmetic drops preserve random sequence');
            clearVisuals(F);PARTICLE_POOL.length=0;FX_LOAD.level=0;burst(1,1,'#fff',100);
            const made=FX_STATS.particlesMade,reused=FX_STATS.particlesReused;
            tickFx(1);check(F.parts.length===0,'expired particles removed');burst(2,2,'#0f0',100,1,2,-1);
            check(FX_STATS.particlesMade===made&&FX_STATS.particlesReused>=reused+100,'particle storage reused');
            check(F.parts.every(p=>p.c==='#0f0'&&p.size===2&&p.g===-1&&p.x===2),'reused particle fields refreshed');
            clearVisuals(F);DEBRIS_POOL.length=0;F.debris=[];
            const wall={src:{type:'glacierwarden'},team:0,x1:1,y1:1,x2:4,y2:1};
            wallBreakFx(wall,true);const debrisMade=FX_STATS.debrisMade,debrisReused=FX_STATS.debrisReused;
            tickDebris(2);check(F.debris.length===0,'expired debris removed');wallBreakFx(wall,true);
            check(FX_STATS.debrisMade===debrisMade&&FX_STATS.debrisReused>=debrisReused+30,'debris storage reused');
            FX_LOAD.level=2;trimDecorations(F);check(F.parts.length<=140&&F.debris.length<=40,'quality change trims old decorations');
            clearVisuals(F);F.f=[];PARTICLE_POOL.length=0;FX_LOAD.level=0;
            const madeBefore=FX_STATS.particlesMade,reusedBefore=FX_STATS.particlesReused;
            for(let i=0;i<100;i++){burst(1,1,'#fff',100);tickFx(1);}
            const allocationCycles={emitted:10000,created:FX_STATS.particlesMade-madeBefore,reused:FX_STATS.particlesReused-reusedBefore};
            check(allocationCycles.created===100&&allocationCycles.reused===9900,'10,000 spark cycle allocates only 100 objects');
            newGame();check(PARTICLE_POOL.length<=700&&DEBRIS_POOL.length<=160,'pool memory bounded');
            return {clockResults,allocationCycles,poolReuse:{particles:FX_STATS.particlesReused,debris:FX_STATS.debrisReused}};
          }finally{step=originalStep;render=originalRender;observeFrameCost=originalObserve;Math.random=random;FX_LOAD.level=0;unlockedFrames=false;newGame();syncFrameButton();}
        }''')
        print(json.dumps(result,indent=2))
        await page.locator('#bFrames').click()
        assert await page.locator('#bFrames').inner_text()=='FPS: Unlocked'
        await page.reload(wait_until='load')
        await page.wait_for_function("document.querySelector('#bFrames').textContent==='FPS: Unlocked'")
        assert await page.evaluate('unlockedFrames')
        await page.locator('.mode[data-m=normal]').click()
        await page.locator('#bFrames').click()
        assert await page.evaluate("localStorage.getItem('ab_draw_unlocked')==='0'")
        assert not errors,errors
        print('Frame pacing, speed/pause, adaptive quality/recovery, combat/RNG equivalence, critical cues, pool reuse and saved FPS settings passed.')
        await browser.close()

if __name__=='__main__':
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:asyncio.run(main(server))
    finally:server.shutdown();server.server_close()
