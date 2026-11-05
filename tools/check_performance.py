"""Reproducible late-round rendering benchmark and rendering correctness checks.

Optional --baseline serves a previously built HTML file through the same server.
Absolute times depend on the browser/graphics backend; compare on one machine.
"""
import argparse
import asyncio
import functools
import hashlib
import http.server
import json
import shutil
import threading
from pathlib import Path
from playwright.async_api import async_playwright
from check_progression import QuietHandler, ROOT

async def open_game(browser, server, source=None):
    page = await browser.new_page(viewport={'width': 1440, 'height': 1000})
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    if source:
        await page.route('**/ro-autobattler.html', lambda route: route.fulfill(
            status=200, content_type='text/html', body=source))
    await page.goto(f'http://127.0.0.1:{server.server_port}/ro-autobattler.html', wait_until='load')
    await page.wait_for_function('ARENA.naturalWidth&&Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))')
    await page.locator('.mode[data-m=normal]').click()
    await page.evaluate('''() => {
      window.perfRAF=requestAnimationFrame.bind(window);window.requestAnimationFrame=()=>0;
      SND.setMusic(0);SND.setSfx(0);
    }''')
    await page.wait_for_timeout(100)
    return page, errors

async def rendering_checks(browser, server):
    page, errors = await open_game(browser, server)
    result = await page.evaluate('''() => {
      const check=(ok,msg)=>{if(!ok)throw Error(msg)};
      const one={},two={},a=rigSurface(one),b=rigSurface(two);
      check(a===rigSurface(one)&&a!==b,'stable, separate per-unit tint surfaces');
      check(RIG_SURFACES instanceof WeakMap,'surface keys must not keep old fighters alive');
      const canvas=document.createElement('canvas');canvas.width=RIG.width;canvas.height=RIG.height;
      const g=canvas.getContext('2d',{willReadFrequently:true}),target={canvas,ctx:g};
      const pixels=()=>new Uint8ClampedArray(rg.getImageData(0,0,RIG.width,RIG.height).data);
      let tested=0,worst=0;
      for(const u of [...UNITS,...SUMMONS,...MONSTERS]){
        const r=SPR[u.id].rig;if(!r)continue;
        const rects=r.rects;check(rects&&rects.length>=r.layers.length,'all layer crops supplied '+u.id);
        const states=[{}, {atkT:ATK_T*.55}, {cast:CAST_T*.5}, {rel:REL_T}, {hurt:.6,hurtK:1,hurtX:1}];
        for(const state of states){
          ANIM=.5;const R=rigPose(state,u.id,U[u.id]);buildRig(r,R,[],exprOf(state));const cropped=pixels();
          r.rects=null;buildRig(r,R,[],exprOf(state));const full=pixels();r.rects=rects;
          let diff=0;for(let i=0;i<full.length;i++)diff+=Math.abs(full[i]-cropped[i]);
          const mean=diff/full.length;worst=Math.max(worst,mean);check(mean<.35,'cropping changed art '+u.id+': '+mean);
          // At native resolution the direct and isolated joint transforms coincide.
          g.setTransform(RES,0,0,RES,0,0);g.clearRect(0,0,168,162);
          buildRig(r,R,[],exprOf(state),null,{ctx:g,direct:true});
          const direct=g.getImageData(0,0,canvas.width,canvas.height).data;
          for(let i=0;i<direct.length;i++)check(direct[i]===cropped[i],'direct rig geometry differs '+u.id);
          // Status tinting stays on an independent surface, matching the scratch path.
          buildRig(r,R,[['#8453cd',.3]],exprOf(state));const tint=pixels();
          buildRig(r,R,[['#8453cd',.3]],exprOf(state),null,target);
          const isolated=g.getImageData(0,0,canvas.width,canvas.height).data;
          for(let i=0;i<isolated.length;i++)check(isolated[i]===tint[i],'isolated status tint differs '+u.id);
          tested++;
        }
      }
      // The old API without crop metadata must continue to support legacy rigs.
      const r=SPR.swordsman.rig,old=r.rects;r.rects=null;buildRig(r,rigPose({},'swordsman',U.swordsman),[],null);r.rects=old;
      return {rigStates:tested,worstCropChannelDifference:worst};
    }''')
    assert not errors, errors
    await page.close()
    return result

async def benchmark(browser, server, frames, source=None):
    page, errors = await open_game(browser, server, source)
    result = await page.evaluate('''async frames => {
      const out=[],random=Math.random;
      try{
        for(const [round,fused] of [[15,false],[30,false],[30,true],[60,false]]){
          newGame('daily');S.round=round;S.extra=6;S.bossOrder=['golem','lich','wyrm','thornmother','stormdjinn','colossus'];
          const ids=['nightreaper','grandmaster','eclipsewitch','chieftain','bonelord','starcaller','mechanist','winterqueen','highpriest'];
          S.units=ids.map((type,i)=>({uid:i+1,type,star:fused?3:2,...(fused?{fuse:UNITS[(i*7+5)%UNITS.length].id}:{}),items:['stormcore:4'],loc:{w:'board',cx:i%8,cy:5+Math.floor(i/8)}}));
          Math.random=mulberry32(123456+round);ANIM=0;startFight();
          // Extend the fight so both builds exercise the same sustained workload.
          for(const a of S.fight.f){a.max*=20;a.hp=a.hpLag=a.max;a.mp=a.mpMax*.8;}
          for(let i=0;i<300;i++)step(1/60);
          const cpu=[],gaps=[];let previous=0;
          for(let i=0;i<frames;i++){
            const now=await new Promise(perfRAF);if(previous)gaps.push(now-previous);previous=now;ANIM+=1/60;
            const t=performance.now();step(1/60);render();cpu.push(performance.now()-t);
          }
          const pct=(a,p)=>[...a].sort((x,y)=>x-y)[Math.floor((a.length-1)*p)];
          const F=S.fight;
          if(F.f.some(a=>!Number.isFinite(a.hp)||!Number.isFinite(a.mp)))throw Error('Invalid late-round fighter');
          out.push({round,fused,fighters:F.f.length,particles:F.parts.length,vfx:F.vfx.length,
            cpuMeanMs:cpu.reduce((a,b)=>a+b)/cpu.length,cpuP95Ms:pct(cpu,.95),frameGapP95Ms:pct(gaps,.95),
            combat:JSON.stringify({t:F.t,f:F.f.map(a=>[a.type,a.team,a.star,a.x,a.y,a.hp,a.max,a.mp,a.dd,a.dtk,a.hl,a.items,a.fuse]),proj:F.proj.map(p=>[p.x,p.y,p.mult]),timers:F.timers.map(t=>t.t),walls:(F.walls||[]).map(w=>[w.hp,w.t,w.x1,w.y1,w.x2,w.y2])})});
        }
      }finally{Math.random=random}
      return out;
    }''', frames)
    assert not errors, errors
    await page.close()
    return result

async def main(server, args):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=shutil.which('chromium') or shutil.which('chromium-browser'),
            headless=True, args=['--no-sandbox'])
        checks = await rendering_checks(browser, server)
        baseline = await benchmark(browser, server, args.frames, args.baseline.read_text()) if args.baseline else None
        current = await benchmark(browser, server, args.frames)
        if baseline:
            for before, after in zip(baseline, current):
                assert before['combat'] == after['combat'], f"Combat changed in round {after['round']}, fused={after['fused']}"
                after['cpuReductionPercent'] = round(100 * (1-after['cpuMeanMs']/before['cpuMeanMs']), 1)
        for rows in [baseline, current]:
            for row in rows or []:
                row['combatSha256'] = hashlib.sha256(row.pop('combat').encode()).hexdigest()
        output = {'rendering': checks, 'framesPerScenario': args.frames, 'baseline': baseline, 'current': current}
        print(json.dumps(output, indent=2))
        if args.output:
            args.output.write_text(json.dumps(output, indent=2)+'\n')
        await browser.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--frames', type=int, default=120)
    args = parser.parse_args()
    if args.frames < 2:
        parser.error('--frames must be at least 2')
    server = http.server.ThreadingHTTPServer(
        ('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        asyncio.run(main(server, args))
    finally:
        server.shutdown()
        server.server_close()
