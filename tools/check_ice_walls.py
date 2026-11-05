"""Ice Wall visual tier and collision regression checks (Playwright/Chromium)."""
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
  browser=await p.chromium.launch(executable_path=shutil.which('chromium') or shutil.which('chromium-browser'),headless=True,args=['--no-sandbox']);page=await browser.new_page();errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(f'http://127.0.0.1:{server.server_port}/ro-autobattler.html',wait_until='load')
  await page.wait_for_function('ARENA.naturalWidth && Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))')
  result=await page.evaluate('''() => {
   const ids=['glacierwarden','frostoracle','winterqueen'],results=[];
   for(let j=0;j<ids.length;j++){
    const id=ids[j];newGame();S.round=15;S.bossOrder=['golem','lich','wyrm','thornmother','stormdjinn','colossus'];
    S.units=[{uid:1,type:id,star:1,items:[],loc:{w:'board',cx:3,cy:5}},{uid:2,type:'swordsman',star:1,items:[],loc:{w:'board',cx:5,cy:5}}];
    startFight();const F=S.fight,a=F.f.find(x=>x.type===id),enemy=F.f.find(x=>x.team===1);
    for(const x of F.f){x.ms=0;x.atk=1;x.mp=0;x.spawnT=0;}
    a.castTgt=enemy;releaseCast(a);const walls=F.walls||[];
    if(walls.length!==1)throw Error('Wrong wall count '+id);
    if(walls.some(w=>iceWallTier(w)!==j+2))throw Error('Wrong design tier '+id);
    const w=walls[0],expected=3;if(Math.abs(Math.hypot(w.x2-w.x1,w.y2-w.y1)-expected)>.001)throw Error('Wall width changed');
    if(w.t!==6)throw Error('Wall duration changed');
    const state=JSON.stringify([w.hp,w.t,w.x1,w.x2,w.y1,w.y2,w.shatter]);drawIceWall(w);
    if(state!==JSON.stringify([w.hp,w.t,w.x1,w.x2,w.y1,w.y2,w.shatter]))throw Error('Rendering changed wall state');
    const cx=(w.x1+w.x2)/2,cy=(w.y1+w.y2)/2,dx=w.x2-w.x1,dy=w.y2-w.y1,d=Math.hypot(dx,dy),nx=-dy/d,ny=dx/d;
    a.x=cx-nx*1.2;a.y=cy-ny*1.2;enemy.x=cx+nx*1.2;enemy.y=cy+ny*1.2;
    let hitAlly=false;const hp=w.hp;F.proj=[];shoot(enemy,a,1,undefined,false,()=>{hitAlly=true;});
    for(let i=0;i<120&&F.proj.length;i++)step(1/120);
    if(hitAlly||w.hp>=hp)throw Error('Enemy projectile did not hit wall '+id);
    let hitEnemy=false;F.proj=[];shoot(a,enemy,1,undefined,false,()=>{hitEnemy=true;});
    for(let i=0;i<120&&!hitEnemy;i++)step(1/120);
    if(!hitEnemy)throw Error('Friendly projectile blocked '+id);
    render();results.push({id,tier:iceWallTier(w),walls:walls.length,enemyBlocked:true,allyPassed:true});
   }
   cv.width=1440;cv.height=1000;ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#25333f';ctx.fillRect(0,0,720,500);S.fight.t=1;
   ids.forEach((id,col)=>[1,.25].forEach((hp,row)=>{
    const x=col*240;ctx.fillStyle='#ddd';ctx.font='12px sans-serif';ctx.textAlign='center';ctx.fillText((col+2)+' GOLD · '+ICE_WALL_STYLES[col+2].name,x+120,35+row*215);
    drawIceWall({src:{type:id},team:0,x1:(x+18)/CELL,y1:(140+row*215)/CELL,x2:(x+222)/CELL,y2:(140+row*215)/CELL,hp:hp*100,max:100,t:5,visualBorn:0});
    ctx.font='10px sans-serif';ctx.fillStyle='#9fb2c2';ctx.fillText(row?'DAMAGED':'FULL STRENGTH',x+120,180+row*215);
   }));window.wallPreview=cv.toDataURL();return results;
  }''')
  print(result);print('Page errors:',errors);assert not errors
  await browser.close()
try:asyncio.run(main())
finally:server.shutdown();server.server_close()
