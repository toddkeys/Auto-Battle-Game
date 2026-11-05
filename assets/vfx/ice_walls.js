// Visual tiers only. Collision, HP, shatter damage and lifetime stay in iceWall().
const ICE_WALL_STYLES={
  2:{name:'Glacier Rampart',edge:'#397890',face:'#93c7d9',side:'#5796b4',cap:'#e2f6f6',height:25},
  3:{name:'Oracle Prism',edge:'#4159a3',face:'#8cbded',side:'#5279c0',cap:'#e3efff',height:34},
  4:{name:'Royal Bastion',edge:'#547aa5',face:'#b6e0f1',side:'#72add0',cap:'#f3fcff',height:43},
};
const iceWallTier=w=>Math.max(2,Math.min(4,U[w.src?.type]?.cost||2));
function drawIceWall(w){
  const tier=iceWallTier(w),s=ICE_WALL_STYLES[tier],len=Math.hypot(w.x2-w.x1,w.y2-w.y1)*CELL;
  const n=Math.max(3,Math.min(24,Math.ceil(len/23))),half=len/n*.52,hp=Math.max(0,Math.min(1,w.hp/w.max));
  const age=Number.isFinite(w.visualBorn)?Math.max(0,S.fight.t-w.visualBorn):1;
  const grow=calmMotion?1:easeOut(Math.min(1,age/.22)),fade=Math.min(1,w.t/.35);
  ctx.save();ctx.globalAlpha=fade;
  ctx.strokeStyle=w.team===0?'rgba(136,218,244,.55)':'rgba(235,147,197,.7)';ctx.lineWidth=4;
  ctx.beginPath();ctx.moveTo(w.x1*CELL,w.y1*CELL+8);ctx.lineTo(w.x2*CELL,w.y2*CELL+8);ctx.stroke();
  for(let i=0;i<n;i++){
    const q=(i+.5)/n,x=(w.x1+(w.x2-w.x1)*q)*CELL,y=(w.y1+(w.y2-w.y1)*q)*CELL;
    const h=s.height+(tier===2?(i%3)*3:tier===3?(i%2)*8:(i===0||i===n-1||i===Math.floor(n/2)?12:0));
    ctx.save();ctx.translate(x,y+8);ctx.scale(1,grow);ctx.globalAlpha=fade*.94;
    const polygon=points=>{ctx.beginPath();points.forEach(([px,py],j)=>j?ctx.lineTo(px,py):ctx.moveTo(px,py));ctx.closePath();};
    ctx.fillStyle='rgba(12,36,69,.24)';ctx.beginPath();ctx.ellipse(2,3,half+3,4,0,0,Math.PI*2);ctx.fill();
    // Wide frosted blocks, pointed oracle prisms, and crowned royal battlements.
    const tip=tier===2?5:tier===3?11:8;
    polygon([[-half,0],[-half,-h+tip],[-half*.22,-h],[half,-h+tip-2],[half,0]]);
    ctx.fillStyle=hp<.3?s.side:s.face;ctx.fill();ctx.strokeStyle=s.edge;ctx.lineWidth=.9;ctx.stroke();
    polygon([[0,0],[0,-h+4],[half,-h+tip-2],[half,0]]);ctx.fillStyle=s.side;ctx.fill();
    polygon([[-half,-h+tip],[-half*.22,-h],[half,-h+tip-2],[0,-h+8]]);ctx.fillStyle=s.cap;ctx.fill();
    ctx.strokeStyle='rgba(245,255,255,.76)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(-half+3,-h+tip+4);ctx.lineTo(-half+3,-5);ctx.stroke();
    if(tier===2){
      ctx.strokeStyle='#d3edf0';ctx.globalAlpha=fade*.55;ctx.beginPath();ctx.moveTo(-half,-h*.45);ctx.lineTo(half,-h*.51);ctx.stroke();
      ctx.fillStyle='#c3e4e7';ctx.fillRect(-half+2,-5,half*2-4,2);
    }else{
      // Refraction and glyphs make the Oracle tier distinct even in monochrome.
      polygon([[-half*.6,-h*.75],[half*.55,-h*.43],[-half*.15,-h*.12]]);ctx.fillStyle='rgba(230,244,255,.3)';ctx.fill();
      ctx.globalAlpha=fade*(hp<.3?.35:.8);ctx.strokeStyle=tier===4?'#fff0b6':'#d8d8ff';ctx.lineWidth=1.2;
      const cy=-h*.5;ctx.beginPath();ctx.moveTo(0,cy-5);ctx.lineTo(3.5,cy);ctx.lineTo(0,cy+5);ctx.lineTo(-3.5,cy);ctx.closePath();ctx.stroke();
      if(tier===4){
        // Gold inlays, connecting frost arches and three-prong crown finials.
        ctx.strokeStyle='#e4d5a4';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(-half+1,-8);ctx.lineTo(half-1,-8);ctx.stroke();
        if(i%3===0){polygon([[-6,-h+6],[-7,-h-4],[-2,-h],[0,-h-9],[2,-h],[7,-h-4],[6,-h+6]]);ctx.fillStyle='#e7f8ff';ctx.fill();ctx.strokeStyle='#d8c99a';ctx.stroke();}
      }else if(i%2===0){ctx.strokeStyle='#d7dcff';ctx.beginPath();ctx.arc(0,-h*.5,8,-.4,Math.PI+.4);ctx.stroke();}
    }
    // Damage is signalled by branching cracks rather than a color swap alone.
    if(hp<.7){ctx.globalAlpha=fade*.85;ctx.strokeStyle='#365470';ctx.lineWidth=hp<.3?1.5:.8;ctx.beginPath();ctx.moveTo(-half*.55,-h*.82);ctx.lineTo(half*.2,-h*.58);ctx.lineTo(-half*.15,-h*.35);ctx.lineTo(half*.5,-h*.13);ctx.moveTo(half*.2,-h*.58);ctx.lineTo(half*.8,-h*.68);ctx.stroke();}
    ctx.restore();
  }
  ctx.restore();
}
