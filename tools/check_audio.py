"""Browser audio checks: decoding, voice pressure, ducking, mute and fallback."""
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
  page=await browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(f'http://127.0.0.1:{server.server_port}/ro-autobattler.html',wait_until='load')
  await page.locator('.mode[data-m=normal]').click()
  # Decode every exported signature to detect missing/corrupt files, silence and clipping.
  decoded=await page.evaluate('''async () => {
    const ac=new AudioContext(), results=[];
    for(const [id,p] of Object.entries(AUDIO_PROFILES)){
      const res=await fetch(p.file);if(!res.ok)throw Error('Missing '+id);
      const b=await ac.decodeAudioData(await res.arrayBuffer());let peak=0,energy=0;
      for(const x of b.getChannelData(0)){peak=Math.max(peak,Math.abs(x));energy+=x*x;}
      if(peak<.01||peak>=.98||!Number.isFinite(energy))throw Error('Bad audio '+id+' '+peak);
      if(Math.abs(b.duration-p.duration)>.06)throw Error('Wrong duration '+id);
      results.push({id,peak});
    }await ac.close();return {decoded:results.length,maxPeak:Math.max(...results.map(x=>x.peak))};
  }''')
  await page.evaluate('SND.setMusic(.5);SND.setSfx(.7);SND.reset()')
  await page.wait_for_timeout(700)
  bed=await page.evaluate('SND.inspect().musicLevel')
  await page.evaluate("SND.play('hit');SND.play('heal');SND.play('skill:nightreaper');SND.play('crit')")
  await page.wait_for_timeout(70)
  attack=await page.evaluate('SND.inspect()')
  assert attack['active']<=10 and attack['context']=='running',attack
  assert any(v['playing'] for v in attack['voices']),attack
  await page.wait_for_timeout(100)
  duck=await page.evaluate('SND.inspect()');assert duck['musicLevel']<bed, (bed,duck)
  # Force a busy mix. Important boss cues must be admitted while hits are throttled.
  stress=await page.evaluate('''async () => {
    SND.reset();let maxActive=0;
    for(let frame=0;frame<10;frame++){
      for(let i=0;i<30;i++){SND.play('hit');SND.play('heal');SND.play('shoot');}
      SND.play('shield');SND.play('cast');SND.play('crit');SND.play('buy');SND.play('sell');
      for(const u of UNITS.slice(0,8))SND.skill({type:u.id,x:2});
      const admitted=SND.skill({type:frame%2?'golem':'lich',x:5});
      const v=SND.inspect();maxActive=Math.max(maxActive,v.active);
      if(v.active>10)throw Error('Global voice cap exceeded');
      await new Promise(r=>setTimeout(r,80));
    }
    const v=SND.inspect();if(maxActive!==10||v.dropped<200)throw Error('Stress mix did not exercise the cap');return {...v,maxActive};
  }''')
  await page.wait_for_timeout(160)
  monitored=await page.evaluate('SND.inspect()')
  assert monitored['peak']>0 and monitored['peak']<1,monitored
  await page.evaluate('SND.setSfx(0)');assert await page.evaluate('SND.inspect().active')==0
  assert not await page.evaluate("SND.play('skill:nightreaper')")
  await page.evaluate('SND.setSfx(.6);SND.setMusic(.35)')
  await page.reload(wait_until='load')
  assert await page.evaluate('SND.sfxVol===.6&&SND.musVol===.35')
  # Exercise the same native-media fallback with Web Audio unavailable.
  local=await browser.new_page();local.on('pageerror',lambda e:errors.append(str(e)))
  await local.add_init_script('window.AudioContext=undefined;window.webkitAudioContext=undefined')
  await local.goto(f'http://127.0.0.1:{server.server_port}/ro-autobattler.html',wait_until='load')
  await local.locator('.mode[data-m=normal]').click();await local.evaluate("SND.play('skill:nightreaper')")
  await local.wait_for_timeout(100);fallback=await local.evaluate('SND.inspect()')
  assert fallback['context']=='media' and any(v['playing'] for v in fallback['voices']),fallback
  print({'files':decoded,'mixPeak':round(monitored['peak'],4),'musicBefore':round(bed,3),'musicDucked':round(duck['musicLevel'],3),'maxActive':stress['maxActive'],'dropped':stress['dropped'],'nativeMediaFallback':True})
  print('Page errors:',errors);assert not errors
  await browser.close()
try:asyncio.run(main())
finally:server.shutdown();server.server_close()
