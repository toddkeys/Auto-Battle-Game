// Priority mixer. HTML media fallback keeps local-file play supported.
const SND=(()=>{
  const clamp=v=>Math.max(0,Math.min(1,Number(v)||0));
  let ready=false,musVol=.5,sfxVol=.7,want='prep',context=null,master=null,analyser=null;
  let voices=[],serial=0,rng=0x41c64e6d,focusPriority=0,dropped=0;
  const last=new Map(),bound=new WeakMap(),pool=new Map();
  const MAX_VOICES=10,MAX_POOL=3,SFX_VOL=.72,MUSIC_VOL=.42;
  const LIMIT={basic:3,support:2,cast:1,skill:3,critical:2,boss:2,ui:2,result:1};
  const CHANNEL_GAP={basic:.065,support:.24,cast:.16,critical:.09,boss:.12,ui:.04};
  const UI=new Set(['click','buy','sell','reroll','equip','slot']);
  const SUPPORT=new Set(['heal','bless','shield']);
  const BASIC=new Set(['hit','hit1','hit2','hit3','shoot','zapshot','hdie','mdie','slime']);
  const VOLUME={click:.35,buy:.65,sell:.6,reroll:.55,equip:.55,slot:.65,hit:.48,hit1:.48,hit2:.48,hit3:.48,shoot:.45,zapshot:.42,cast:.34,heal:.48,bless:.5,shield:.55,crit:.8,hdie:.4,mdie:.4,flurry:.52};
  const GAPS={hit:.08,shoot:.085,zapshot:.09,heal:.3,bless:.35,shield:.3,cast:.18,boom:.25,quake:.25,freeze:.22,shatter:.18,flurry:.16};
  const music={prep:new Audio('assets/audio/prep.mp3'),battle:new Audio('assets/audio/battle.mp3')};
  for(const m of Object.values(music)){m.loop=true;m.volume=0;m.preload='auto';m._level=0;}
  try{const p=JSON.parse(localStorage.getItem('ab_sound')||'{}');if(Number.isFinite(p.mus))musVol=clamp(p.mus);if(Number.isFinite(p.sfx))sfxVol=clamp(p.sfx);}catch(e){}
  const save=()=>{try{localStorage.setItem('ab_sound',JSON.stringify({mus:musVol,sfx:sfxVol}));}catch(e){}};
  const random=()=>{rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng/4294967296;};
  function attach(a,pan=0){
    if(!context)return null;if(bound.has(a))return bound.get(a);
    try{const gain=context.createGain(),panner=context.createStereoPanner?context.createStereoPanner():null,source=context.createMediaElementSource(a);
      gain.gain.value=0;if(panner){panner.pan.value=pan;source.connect(panner);panner.connect(gain);}else source.connect(gain);
      gain.connect(master);const link={gain,panner,source};bound.set(a,link);a.volume=1;return link;
    }catch(e){return null;}
  }
  function init(){
    if(ready){if(context?.state==='suspended')context.resume().catch(()=>{});return;}ready=true;
    // Local-file audio uses native media volumes, without CORS-dependent routing.
    if(location.protocol==='http:'||location.protocol==='https:')try{
      const AC=window.AudioContext||window.webkitAudioContext;if(AC){context=new AC();master=context.createGain();master.gain.value=.85;
        const compressor=context.createDynamicsCompressor();compressor.threshold.value=-12;compressor.knee.value=6;compressor.ratio.value=12;compressor.attack.value=.003;compressor.release.value=.14;
        analyser=context.createAnalyser();analyser.fftSize=1024;master.connect(compressor);compressor.connect(analyser);analyser.connect(context.destination);
        for(const m of Object.values(music))attach(m);context.resume().catch(()=>{});}
    }catch(e){context=null;master=null;analyser=null;}
  }
  function describe(k){
    if(k.startsWith('skill:'))return AUDIO_PROFILES[k.slice(6)]||null;
    let channel=UI.has(k)?'ui':SUPPORT.has(k)?'support':BASIC.has(k)?'basic':k==='cast'?'cast':k==='crit'?'critical':k.startsWith('roar')?'boss':k==='victory'||k==='defeat'||k==='start'||k==='star'?'result':'skill';
    return {file:'assets/audio/sfx/'+k+'.ogg',channel,priority:channel==='result'?6:channel==='ui'?2:channel==='boss'?4:channel==='critical'?3:channel==='skill'?2:channel==='basic'?0:1,
      gain:VOLUME[k]??.65,gap:GAPS[k]??.12,focus:channel==='boss'?.45:channel==='critical'?.15:channel==='skill'?.18:channel==='result'?.3:0,duration:channel==='result'?2.5:channel==='basic'?.6:1.7};
  }
  function stop(v){
    if(!voices.includes(v))return;
    voices=voices.filter(x=>x!==v);v.a.pause();try{v.a.currentTime=0;}catch(e){}
    const link=bound.get(v.a);if(link)link.gain.gain.setValueAtTime(0,context.currentTime);else v.a.volume=0;
  }
  function reap(){const now=performance.now()/1000;for(const v of [...voices])if(v.a.ended||(v.started&&v.a.paused)||now>v.expires)stop(v);}
  function channelGain(channel){
    if(focusPriority>=4)return {basic:.25,support:.4,cast:.4,skill:.7,critical:.85}[channel]??1;
    if(focusPriority>=3)return {basic:.4,support:.55,cast:.5,skill:.85}[channel]??1;
    return focusPriority>=2&&channel==='basic'?.7:1;
  }
  function target(v){const combat=voices.filter(x=>x.channel!=='ui'&&x.channel!=='result').length;
    const density=v.channel==='ui'||v.channel==='result'?1:1/Math.sqrt(Math.max(1,combat/3));
    return clamp(SFX_VOL*sfxVol*v.meta.gain*channelGain(v.channel)*density);
  }
  function level(v,value){const link=bound.get(v.a);if(link)link.gain.gain.setTargetAtTime(value,context.currentTime,.012);else v.a.volume=clamp(value);}
  function play(k,options={}){
    if(!ready||!sfxVol)return false;reap();const now=performance.now()/1000,meta=describe(k);if(!meta)return false;
    const channel=options.channel||meta.channel,priority=options.priority??meta.priority;
    if(k==='victory'||k==='defeat')for(const v of [...voices])if(v.channel!=='ui')stop(v);
    if(now-(last.get(k)??-99)<meta.gap||now-(last.get('group:'+channel)??-99)<(CHANNEL_GAP[channel]||0)){dropped++;return false;}
    const same=voices.filter(v=>v.channel===channel),full=voices.length>=MAX_VOICES||same.length>=(LIMIT[channel]||2);
    if(full){const candidates=(same.length>=(LIMIT[channel]||2)?same:voices).filter(v=>v.priority<priority).sort((a,b)=>a.priority-b.priority||a.serial-b.serial);
      if(!candidates.length){dropped++;return false;}stop(candidates[0]);}
    let file=meta.file;if(k==='hit')file='assets/audio/sfx/hit'+(1+(random()*3|0))+'.ogg';
    let clips=pool.get(file);if(!clips){clips=[];pool.set(file,clips);}
    let a=clips.find(x=>!voices.some(v=>v.a===x));if(!a){if(clips.length>=MAX_POOL){dropped++;return false;}a=new Audio(file);a.preload='auto';clips.push(a);}
    const pan=Number.isFinite(options.x)?Math.max(-.35,Math.min(.35,(options.x/8-.5)*.7)):0,link=attach(a,pan);
    if(link?.panner)link.panner.pan.setValueAtTime(pan,context.currentTime);
    const v={a,k,channel,priority,meta,serial:serial++,started:false,expires:now+meta.duration+.65,focusUntil:now+(meta.focus||0),level:0};
    voices.push(v);last.set(k,now);last.set('group:'+channel,now);focusPriority=Math.max(focusPriority,meta.focus?priority:0);
    v.level=target(v);level(v,v.level);try{a.currentTime=0;}catch(e){}
    if(context?.state==='suspended')context.resume().catch(()=>{});
    a.play().then(()=>{v.started=true;}).catch(()=>{stop(v);});return true;
  }
  function update(dt){
    reap();const now=performance.now()/1000;focusPriority=voices.reduce((n,v)=>v.focusUntil>now?Math.max(n,v.priority):n,0);
    for(const v of voices){const to=target(v);v.level+=(to-v.level)*Math.min(1,dt*(to<v.level?35:9));level(v,v.level);}
    const duck=focusPriority>=4?.35:focusPriority>=3?.52:focusPriority>=2?.75:1;
    for(const [k,m] of Object.entries(music)){
      const to=ready&&k===want?MUSIC_VOL*musVol*duck:0;m._level+=(to-m._level)*Math.min(1,dt*(to<m._level?18:3));
      const link=bound.get(m);if(link)link.gain.gain.setTargetAtTime(m._level,context.currentTime,.025);else m.volume=clamp(m._level);
      if(to>0&&m.paused)m.play().catch(()=>{});if(to===0&&m._level<.003&&!m.paused)m.pause();
    }
  }
  function reset(){for(const v of [...voices])stop(v);last.clear();focusPriority=0;}
  return {init,play,update,reset,
    skill(a){const key=AUDIO_PROFILES[a.type]?'skill:'+a.type:SKILL_SND[a.type]||'skill';return play(key,{x:a.x});},
    impact(src,t,crit){return play(crit?'crit':'hit',{x:t.x});},
    music(kind){if(kind!==want&&kind==='battle')try{music.battle.currentTime=0;}catch(e){}want=kind;},
    setMusic(v){musVol=clamp(v);save();if(!musVol)for(const m of Object.values(music)){m._level=0;const l=bound.get(m);if(l)l.gain.gain.setValueAtTime(0,context.currentTime);else m.volume=0;}},
    setSfx(v){sfxVol=clamp(v);save();if(!sfxVol)reset();},
    get musVol(){return musVol;},get sfxVol(){return sfxVol;},get musicOn(){return musVol>0;},
    inspect(){let peak=0;if(analyser){const samples=new Float32Array(analyser.fftSize);analyser.getFloatTimeDomainData(samples);for(const n of samples)peak=Math.max(peak,Math.abs(n));}
      return {ready,context:context?.state||'media',active:voices.length,focus:focusPriority,dropped,peak,musicLevel:music[want]._level,voices:voices.map(v=>({key:v.k,channel:v.channel,priority:v.priority,level:v.level,playing:!v.a.paused&&!v.a.ended}))};}
  };
})();
