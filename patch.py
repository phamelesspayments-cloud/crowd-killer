import re,sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src).read()
def R(a,b,count=1):
    global s
    n=s.count(a)
    if n!=count: raise SystemExit('expected %d got %d for: %s'%(count,n,a[:90]))
    s=s.replace(a,b)
def RX(pat,b):
    global s
    s2,n=re.subn(pat,b,s,count=1,flags=re.S)
    if n!=1: raise SystemExit('regex miss: '+pat[:80])
    s=s2

R('<title>Crowd Killer</title>','<title>Crowd Killer Streets</title>')
R('Prototype 0.2 · Last as long as you can','Prototype 0.3 · Stage 1 · Bergie Block')
R('aria-label="Game arena: a punk basement show"','aria-label="Game stage: a city street at night"')
R('<div><dt>Wave</dt><dd id="r-wave">1</dd></div>','<div><dt>Area</dt><dd id="r-wave">1</dd></div>')

# floor + camera
R('var W=960,H=540,FT=372,FB=514,GRAV=0.55,WALL=300;','var W=960,H=540,FT=404,FB=528,GRAV=0.55,WALL=300;')
RX(r"var WM=40,SPK_L=.*?\n\} /\* character scale",
"""/* Side-scrolling street: the walkable band is the sidewalk and the road; the screen edges are the walls. */
var camX=0,WORLD=W*4;
function floorRange(y){return [camX+24*CS,camX+W-24*CS];}
function walkClamp(o){o.x=clamp(o.x,camX+24*CS,camX+W-24*CS);}
/* character scale""")

# background strip
RX(r"var bg=buildBG\(\),bgPhoto=false;.*?bgImg\.src='arena_bg\.jpg';",
r"""var bg=null,TILES=3,OVL=56,TW=0;
function drawPole(g,x){
  /* a utility pole hides each seam where the street repeats */
  var top=0,bot=Math.round(H*0.765);
  g.fillStyle='rgba(0,0,0,.35)';g.beginPath();g.ellipse(x,bot+2,18,5,0,0,Math.PI*2);g.fill();
  g.fillStyle='#2a1e18';g.fillRect(x-9,top,18,bot-top);
  g.fillStyle='#4a362a';g.fillRect(x-7,top,8,bot-top);
  g.fillStyle='#5c4434';g.fillRect(x-5,top,2,bot-top);
  g.fillStyle='#8f949e';g.fillRect(x-10,Math.round(H*.27),20,4);g.fillRect(x-10,Math.round(H*.5),20,4);
  g.fillStyle='#1c1512';g.fillRect(x-28,Math.round(H*.06),56,5);
  g.strokeStyle='rgba(10,8,10,.85)';g.lineWidth=1.5;
  g.beginPath();g.moveTo(x-26,Math.round(H*.06)+3);g.quadraticCurveTo(x-120,Math.round(H*.13),x-260,Math.round(H*.09));g.stroke();
  g.beginPath();g.moveTo(x+26,Math.round(H*.06)+3);g.quadraticCurveTo(x+120,Math.round(H*.13),x+260,Math.round(H*.09));g.stroke();
}
var bgImg=new Image();
bgImg.onload=function(){
  try{
    var tw=Math.round(bgImg.naturalWidth*H/bgImg.naturalHeight);TW=tw-OVL;
    var t=document.createElement('canvas');t.width=tw;t.height=H;var tgc=t.getContext('2d');tgc.imageSmoothingQuality='high';tgc.drawImage(bgImg,0,0,tw,H);
    var m=document.createElement('canvas');m.width=tw;m.height=H;var mg=m.getContext('2d');
    mg.drawImage(t,0,0);mg.globalCompositeOperation='destination-in';
    var gr=mg.createLinearGradient(0,0,OVL,0);gr.addColorStop(0,'rgba(0,0,0,0)');gr.addColorStop(1,'rgba(0,0,0,1)');
    mg.fillStyle=gr;mg.fillRect(0,0,OVL,H);mg.fillStyle='#000';mg.fillRect(OVL,0,tw-OVL,H);
    var c=document.createElement('canvas');c.width=TW*TILES+OVL;c.height=H;var g=c.getContext('2d');
    g.drawImage(t,0,0);
    for(var i=1;i<TILES;i++)g.drawImage(m,i*TW,0);
    for(var j=1;j<TILES;j++)drawPole(g,j*TW+OVL/2);
    bg=c;WORLD=c.width;
  }catch(e){}
};
bgImg.src='street_bg.jpg';""")
R("var fl=document.createElement('canvas');fl.width=W;fl.height=H;","var fl=document.createElement('canvas');fl.width=W*4;fl.height=H;")

# state
R("var BEST_KEY='pitbrawl.best';","var BEST_KEY='crowdkiller.streets.best';\nvar lives=3,encIdx=0,bossE=null,stageWon=false;")
R("player={c:c,x:W/2-120,","camX=0;player={c:c,x:220,")
R("  fg.clearRect(0,0,W,H);\n  startWave();","  fg.clearRect(0,0,fl.width,fl.height);\n  lives=3;encIdx=0;bossE=null;stageWon=false;phase='intro';phaseT=110;\n")

# encounters
RX(r"function startWave\(\)\{.*?\n\}\nfunction aliveCount",
r"""/* Stage 1: the camera locks at each area, the area's crew walks in from both edges, and GO opens the street again. */
var ENC=[{g:3,b:0,t:0},{g:4,b:1,t:0},{g:5,b:1,t:0},{g:4,b:3,t:0},{g:3,b:1,t:1}];
var TRIG=[0,.24,.5,.76,1];
function maxCam(){return Math.max(0,WORLD-W);}
function trigX(i){return Math.round(maxCam()*TRIG[Math.min(i,TRIG.length-1)]);}
function startWave(){
  var en=ENC[encIdx];wave=encIdx+1;phase='fight';spawnT=24;queue=[];
  for(var i=0;i<en.g;i++)queue.push('grunt');
  for(var j=0;j<en.b;j++)queue.splice(Math.floor(rnd(queue.length*.3,queue.length+1)),0,'brute');
  for(var t=0;t<en.t;t++)queue.unshift('tank');
}
function aliveCount""")
RX(r"function updateWave\(\)\{.*?\n\}\nfunction spawnEnemy",
r"""function updateWave(){
  if(phase==='intro'){phaseT--;if(phaseT<=0)phase='walk';return;}
  if(phase==='walk'){
    var lim=trigX(encIdx),target=player.x-W*.42;
    camX=Math.max(camX,Math.min(target,lim));
    if(camX>=lim-.5){camX=lim;startWave();}
    return;
  }
  if(phase==='fight'){
    spawnT--;
    if(spawnT<=0&&queue.length&&aliveCount()<Math.min(3+Math.floor(wave/2),5)){
      spawnEnemy(queue.shift());
      spawnT=rnd(Math.max(20,60-wave*4),Math.max(44,96-wave*6));
    }
    if(!queue.length&&enemies.length===0){
      score+=250*wave;
      if(encIdx>=ENC.length-1){phase='clear';phaseT=210;stageWon=true;score+=lives*1000;}
      else{
        if(encIdx===1||encIdx===3){var pk={kind:'burrito',x:clamp(player.x+player.face*140,camX+60,camX+W-60),y:clamp(player.y,FT+10,FB-10),t:0};pickups.push(pk);}
        encIdx++;phase='walk';
      }
    }
    return;
  }
  if(phase==='clear'){phaseT--;if(phaseT<=0&&mode==='play')endGame(true);}
}
function spawnEnemy""")
R("x:side<0?-36*CS:W+36*CS,y:rnd(432,FB),","x:side<0?camX-36*CS:camX+W+36*CS,y:rnd(FT+16,FB),")
R("  if(type==='tank'){alertT=130;sfx('heavy');}",
"  if(type==='tank'){var be=enemies[enemies.length-1];be.hp=be.maxhp=be.hp*1.5;be.boss=true;bossE=be;alertT=150;sfx('heavy');}")

# camera-relative bounds
R("if(t.x<8||t.x>W-8){t.vx=-t.vx*.5;t.x=clamp(t.x,8,W-8);}","if(t.x<8||t.x>WORLD-8){t.vx=-t.vx*.5;t.x=clamp(t.x,8,WORLD-8);}")
R("else if(q.x<-30||q.x>W+30||q.t>120)","else if(q.x<camX-30||q.x>camX+W+30||q.t>120)")
R("x:clamp(e.x+rnd(-30,30),40,W-40),","x:clamp(e.x+rnd(-30,30),camX+40,camX+W-40),")
R("x:clamp(p.x+rnd(-24,24),30,W-30),","x:clamp(p.x+rnd(-24,24),camX+30,camX+W-30),")
R("x:clamp(x,90,W-90),","x:clamp(x,camX+90,camX+W-90),")
R("var ox=p.x,oy=p.y;p.x=clamp(p.x+p.vx,24*CS,W-24*CS);p.y=clamp(p.y+p.vy,FT,FB);walkClamp(p,ox,oy);",
  "p.x=p.x+p.vx;p.y=clamp(p.y+p.vy,FT,FB);walkClamp(p);")
R("if(!e.inn&&e.x>40*CS&&e.x<W-40*CS)e.inn=true;","if(!e.inn&&e.x>camX+40*CS&&e.x<camX+W-40*CS)e.inn=true;")
R("if(!e.inn){tx=W/2;ty=e.y;}","if(!e.inn){tx=camX+W/2;ty=e.y;}")
R("if(e.inn){e.x=clamp(e.x,22*CS,W-22*CS);walkClamp(e,ox,oy);}","if(e.inn)e.x=clamp(e.x,camX+22*CS,camX+W-22*CS);")

# lives
R("if(p.lt>(p.hp<=0?60:46)){if(p.hp<=0)p.gameOver=true;else{p.state='free';p.inv=80;}}",
  "if(p.lt>(p.hp<=0?60:46)){if(p.hp<=0){if(lives>1){lives--;respawn(p);}else p.gameOver=true;}else{p.state='free';p.inv=80;}}")
R("function updateEnemy(e){",
"""function respawn(p){
  p.hp=p.c.hp;p.hpShow=p.c.hp;p.state='free';p.inv=170;p.lt=0;p.vx=0;p.vy=0;
  burst(p.x,p.y-60*CS,22,7,[INK.c,INK.m,INK.y,INK.w]);sfx('pick');
  addFloater('BACK IN',lives+(lives===1?' LIFE LEFT':' LIVES LEFT'),INK.y,p.x,p.y-150*CS);
  for(var i=0;i<enemies.length;i++){var e=enemies[i];if(e.hp>0&&e.state!=='down'){if(e.state==='held')e.state='walk';knockEnemy(e,e.x>=p.x?1:-1,false);}}
  shake=Math.max(shake,6*(REDUCE?.3:1));
}
function updateEnemy(e){""")

# crowd removed
RX(r"var CROWD=\[\n.*?\n\];","var CROWD=[]; /* no spectators on the street */")

# render with camera
R("  ctx.drawImage(bg,0,0);ctx.drawImage(fl,0,0);\n  drawFan();",
"""  var cx=Math.round(camX);ctx.translate(-cx,0);
  if(bg)ctx.drawImage(bg,cx,0,W,H,cx,0,W,H);
  else{var bgr=ctx.createLinearGradient(0,0,0,H);bgr.addColorStop(0,'#141a28');bgr.addColorStop(.72,'#2a2630');bgr.addColorStop(.74,'#3a3d46');bgr.addColorStop(1,'#1c1d24');ctx.fillStyle=bgr;ctx.fillRect(cx,0,W,H);}
  ctx.drawImage(fl,cx,0,W,H,cx,0,W,H);""")

# HUD
R("""  ctx.textAlign='center';ctx.font='700 16px '+UI;ctx.fillStyle='#a6a1bb';ctx.fillText('WAVE',W/2,26);
  ctx.font='28px '+DISPLAY;ctx.fillStyle=INK.w;ctx.fillText(String(wave),W/2,54);""",
"""  ctx.textAlign='right';ctx.font='700 18px '+UI;ctx.fillStyle=INK.w;ctx.fillText('LIVES ×'+lives,bx+bw,38);
  ctx.textAlign='center';ctx.font='700 16px '+UI;ctx.fillStyle='#a6a1bb';ctx.fillText('STAGE 1 · AREA',W/2,26);
  ctx.font='28px '+DISPLAY;ctx.fillStyle=INK.w;ctx.fillText(Math.max(1,wave)+'/'+ENC.length,W/2,54);
  if(bossE&&bossE.hp>0){
    var bw2=360,bx2=(W-bw2)/2,by2=H-34;
    ctx.fillStyle='rgba(8,7,14,.7)';ctx.fillRect(bx2-12,by2-30,bw2+24,52);
    ctx.textAlign='left';ctx.font='18px '+DISPLAY;ctx.fillStyle=INK.y;ctx.fillText('THE FOREMAN',bx2,by2-8);
    ctx.fillStyle='#0c0b12';ctx.fillRect(bx2-3,by2-3,bw2+6,16);
    ctx.fillStyle=INK.m;ctx.fillRect(bx2,by2,bw2*clamp(bossE.hp/bossE.maxhp,0,1),10);
  }""")

# banners
RX(r"function banner\(\)\{.*?\n\}\n/\* ---------- crowd",
r"""function banner(){
  if(phase==='intro'){
    var a=phaseT>90?(110-phaseT)/20:phaseT<20?phaseT/20:1;
    misreg('STAGE 1',W/2,180,72,clamp(a,0,1));
    misreg('BERGIE BLOCK',W/2,250,30,clamp(a,0,1));
  }else if(phase==='clear'){
    var b=phaseT>190?(210-phaseT)/20:1;
    misreg('STAGE CLEAR',W/2,190,64,clamp(b,0,1));
  }else if(phase==='walk'&&encIdx>0&&camX<trigX(encIdx-1)+90&&((frames>>4)&1)){
    misreg('GO',W-190,250,60,1);
    ctx.save();ctx.translate(W-112,250);ctx.lineJoin='round';
    ctx.beginPath();ctx.moveTo(-26,-14);ctx.lineTo(4,-14);ctx.lineTo(4,-30);ctx.lineTo(34,0);ctx.lineTo(4,30);ctx.lineTo(4,14);ctx.lineTo(-26,14);ctx.closePath();
    ctx.lineWidth=7;ctx.strokeStyle=OUT;ctx.stroke();ctx.fillStyle=INK.y;ctx.fill();ctx.restore();
  }
  if(alertT>0){
    var al=alertT>130?(150-alertT)/20:alertT<20?alertT/20:1;
    misreg('THE FOREMAN',W/2,180,44,clamp(al,0,1));
  }
}
/* ---------- crowd""")

# end screens
R("return 'Best run: <b>'+best.score+'</b> points, wave <b>'+best.wave+'</b>, '+best.time+' as '+best.who;",
  "return 'Best run: <b>'+best.score+'</b> points, area <b>'+best.wave+'/'+ENC.length+'</b>'+(best.won?' (cleared)':'')+', '+best.time+' as '+best.who;")
RX(r"function endGame\(\)\{.*?\n  overEl\.hidden=false;\n\}",
r"""function endGame(win){
  mode='over';win=!!win;
  var t=fmtTime(frames),isBest=!best||score>best.score;
  if(isBest){best={score:score,wave:wave,time:t,who:player.c.name,won:win};saveBest(best);}
  overEl.querySelector('h3').textContent=win?'Stage clear':'Knocked out';
  $('r-wave').textContent=wave+'/'+ENC.length;$('r-time').textContent=t;$('r-kos').textContent=String(kills);$('r-score').textContent=String(score);
  $('r-best').textContent=isBest?'New best run!':'Best run: '+best.score+' points, area '+best.wave+'/'+ENC.length;
  overEl.hidden=false;
}""")
open(dst,'w').write(s)
print('ok',len(s))
