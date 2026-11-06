"""Mock real PostgREST errors to test long-run score recovery without live writes."""
import asyncio,functools,http.server,json,shutil,threading
from playwright.async_api import async_playwright
from check_progression import QuietHandler,ROOT

async def main(server):
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1024,'height':768},has_touch=True,is_mobile=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  state={'posts':[],'gets':[],'reject':True,'legacy':False,'readfail':False,'fail_after_post':False,'status':400}
  async def scores(route):
   request=route.request
   if request.method=='POST':
    body=request.post_data_json;state['posts'].append(body)
    if state['reject']:
     await route.fulfill(status=state['status'],json={'code':'23514' if state['status']==400 else 'unavailable','message':'new row violates check constraint "scores_round_check"'});return
    if state['legacy'] and 'team' in body:
     await route.fulfill(status=400,json={'code':'PGRST204','message':"Could not find the 'team' column of 'scores' in the schema cache"});return
    await asyncio.sleep(.1)
    if state['fail_after_post']:state['readfail']=True
    await route.fulfill(status=201,body='');return
   state['gets'].append(request.url)
   if state['readfail']:await route.fulfill(status=503,json={'code':'unavailable'});return
   if state['legacy'] and ',team' in request.url:
    await route.fulfill(status=400,json={'code':'42703','message':'column scores.team does not exist'});return
   await route.fulfill(status=200,json=[{'name':'Earlier run','round':190,'bosses':34,'created_at':'2026-01-01T00:00:00Z','team':[]}])
  await page.route('**/rest/v1/scores**',scores)
  url=f'http://127.0.0.1:{server.server_port}/ro-autobattler.html'
  async def load():
   await page.goto(url);await page.wait_for_function('Object.values(SPR).every(s=>s.img.complete&&s.bounds&&(!s.rig||s.rig.img.complete))')
   await page.locator('.mode[data-m=normal]').tap()
  async def summary():
   await page.evaluate("newGame();SND.setSfx(0);SND.setMusic(0);S.round=235;S.bosses=43;S.phase='over';S.units=[{uid:1,type:'crownduelist',star:3,fuse:'grandmaster',items:[],loc:{w:'board',cx:3,cy:5}}];showSummary()")
   await page.locator('#lbName').wait_for();await page.locator('#lbName').fill('Long run')
  await load();await summary();await page.locator('#lbSend').tap()
  await page.wait_for_function("$('#lb .lbform b').textContent.includes('server update')")
  assert len(state['posts'])==1 and state['posts'][0]['round']==235 and state['posts'][0]['bosses']==43
  assert state['posts'][0]['team']==[{'t':'crownduelist','s':3,'f':'grandmaster'}]
  assert await page.evaluate('LB_TEAM') is True
  assert len(await page.evaluate('readPendingScores()'))==1
  # The original board, score, and fused lineup survive reload and a fresh run.
  await page.evaluate("savePendingScore({board:'hard',name:'Second run',round:1000,bosses:200,team:[{t:'mage',s:3}]})")
  state['reject']=False;await load();await page.locator('#bModes').tap();await page.locator('#modesPending').tap()
  await page.locator('[data-score-retry]').nth(0).tap();await page.wait_for_function("document.querySelector('[data-score-retry]').textContent==='Submitted'")
  assert state['posts'][1]==state['posts'][0]
  assert await page.evaluate('readPendingScores().length')==1
  await page.locator('[data-score-retry]').nth(1).tap();await page.wait_for_function("[...document.querySelectorAll('[data-score-retry]')].every(b=>b.disabled)")
  await page.wait_for_function('readPendingScores().length===0')
  assert state['posts'][-1]['round']==1000 and state['posts'][-1]['board']=='hard'
  assert await page.evaluate('readPendingScores().length')==0
  # A later GET outage must not re-enable a POST that was already accepted.
  await page.evaluate("$('#modes').hidden=true");state['fail_after_post']=True;await summary();before=len(state['posts'])
  await page.locator('#lbSend').tap();await page.wait_for_function("$('#lb .lbform b').textContent.startsWith('Score submitted.')")
  await page.wait_for_timeout(250)
  assert await page.locator('#lbSend').is_disabled()
  assert await page.evaluate('readPendingScores().length')==0
  await page.locator('#lbName').dispatch_event('keydown',{'key':'Enter'})
  assert len(state['posts'])==before+1
  # Real missing-column errors retain compatibility with old schemas.
  state.update(readfail=False,fail_after_post=False,legacy=True)
  legacy=await page.evaluate("async()=>{LB_TEAM=null;await lbFetch('normal');return LB_TEAM}")
  assert legacy is False
  await page.evaluate("async()=>{LB_TEAM=true;await lbSubmit('normal','Legacy',235,51,[{t:'mage',s:3}])}")
  assert 'team' in state['posts'][-2] and 'team' not in state['posts'][-1]
  # Transient/permission/constraint failures do not remove team support or POST twice.
  state.update(legacy=False,reject=True)
  for status in [400,403,429,503]:
   state['status']=status;before=len(state['posts'])
   result=await page.evaluate("async()=>{LB_TEAM=true;try{await lbSubmit('normal','Retry',1000,150,[{t:'mage',s:3}])}catch(e){return {status:e.status,team:LB_TEAM}}}")
   assert result=={'status':status,'team':True} and len(state['posts'])==before+1,(status,result)
  state['readfail']=True;before=len(state['gets'])
  await page.evaluate("async()=>{LB_TEAM=true;try{await lbFetch('normal')}catch(e){return e.status}}")
  assert len(state['gets'])==before+1 and await page.evaluate('LB_TEAM') is True
  assert not errors,errors
  print(json.dumps({'round':235,'bosses':43,'savedFusedLineup':True,'reloadRetry':True,'noDuplicatePostAfterRefreshFailure':True,'legacyTeamFallback':True,'errorStatuses':[400,403,429,503]}))
  await browser.close()
if __name__=='__main__':
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
 try:asyncio.run(main(server))
 finally:server.shutdown();server.server_close()
