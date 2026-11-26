import re,sys
p=sys.argv[1];s=open(p).read()
def R(a,b):
    global s
    n=s.count(a)
    if n!=1: raise SystemExit('expected 1 got %d: %s'%(n,a[:90]))
    s=s.replace(a,b)
def RX(pat,b):
    global s
    s2,n=re.subn(pat,b,s,count=1,flags=re.S)
    if n!=1: raise SystemExit('regex miss: '+pat[:80])
    s=s2
R('Prototype 0.3 · Stage 1 · Bergie Block','Prototype 0.4 · Stage 1-1 · Bergie Block')
R('var bg=null,TILES=3,OVL=56,TW=0;','var bg=null,TILES=1,OVL=56,TW=0;')
R("    bg=c;WORLD=c.width;","    bg=t;WORLD=t.width;")
R('<div><dt>Area</dt><dd id="r-wave">1</dd></div>','<div><dt>Reached</dt><dd id="r-wave">1</dd></div>')
RX(r"var ENC=\[.*?\];\nvar TRIG=\[.*?\];",
"""/* Section 1-1: the camera stops halfway for three skinheads, then the Foreman hops out at the far right. */
var ENC=[{g:3,b:0,t:0},{g:0,b:0,t:1}];
var TRIG=[.5,1];
var fadeT=0;""")
R("""      if(encIdx>=ENC.length-1){phase='clear';phaseT=210;stageWon=true;score+=lives*1000;}
      else{
        if(encIdx===1||encIdx===3){var pk={kind:'burrito',x:clamp(player.x+player.face*140,camX+60,camX+W-60),y:clamp(player.y,FT+10,FB-10),t:0};pickups.push(pk);}
        encIdx++;phase='walk';
      }""",
"""      if(encIdx>=ENC.length-1){phase='exit';stageWon=true;score+=lives*1000;}
      else{encIdx++;phase='walk';}""")
R("  if(phase==='clear'){phaseT--;if(phaseT<=0&&mode==='play')endGame(true);}",
"""  if(phase==='exit'){if(player.hp>0&&player.x>=camX+W-24*CS-6){phase='fade';fadeT=0;}return;}
  if(phase==='fade'){fadeT++;if(fadeT>=110&&mode==='play')endGame(true);}""")
# foreman hops in
R("be.boss=true;bossE=be;alertT=150;sfx('heavy');}",
  "be.boss=true;bossE=be;alertT=150;sfx('heavy');be.x=camX+W+30*CS;be.y=clamp(player.y,FT+30,FB-10);be.state='hop';be.air=true;be.z=40*CS;be.vz=10*JV;be.vx=-3.2*JV;be.face=-1;be.t=0;}")
R("  if(e.state==='held'){\n    e.vx=0;e.vy=0;\n  }else if(e.state==='walk'){",
"""  if(e.state==='held'){
    e.vx=0;e.vy=0;
  }else if(e.state==='hop'){
    e.vy=0;
    if(!e.air&&e.t>2){e.state='walk';e.inn=true;e.cd=50;shake=Math.max(shake,9*(REDUCE?.3:1));sfx('heavy');burst(e.x,e.y-6,18,5,['#8a8a92','#5a5a62',INK.w]);}
  }else if(e.state==='walk'){""")
R("    if(e.z<=0){e.z=0;e.vz=0;e.air=false;e.vx=0;}\n  }\n  if(e.thrown){",
  "    if(e.z<=0){e.z=0;e.vz=0;e.air=false;e.vx=0;}\n  }\n  if(e.state==='hop')e.face=-1;\n  if(e.thrown){")
R("  if(st==='held')return A.hurt[2];","  if(st==='held')return A.hurt[2];\n  if(st==='hop')return e.air?A.act[0]:A.act[6]||A.act[0];")
# banners
R("""  }else if(phase==='clear'){
    var b=phaseT>190?(210-phaseT)/20:1;
    misreg('STAGE CLEAR',W/2,190,64,clamp(b,0,1));
  }else if(phase==='walk'&&encIdx>0&&camX<trigX(encIdx-1)+90&&((frames>>4)&1)){""",
"""  }else if((phase==='exit'||(phase==='walk'&&encIdx>0))&&((frames>>4)&1)){""")
R("""    misreg('STAGE 1',W/2,180,72,clamp(a,0,1));""","""    misreg('STAGE 1-1',W/2,180,72,clamp(a,0,1));""")
R("""    misreg('THE FOREMAN',W/2,180,44,clamp(al,0,1));
  }""","""    misreg('THE FOREMAN',W/2,180,44,clamp(al,0,1));
  }
  if(phase==='fade'){ctx.fillStyle='rgba(0,0,0,'+clamp(fadeT/80,0,1)+')';ctx.fillRect(0,0,W,H);}""")
R("ctx.fillText('STAGE 1 \u00b7 AREA',W/2,26);","ctx.fillText('STAGE',W/2,26);")
R("ctx.fillText(Math.max(1,wave)+'/'+ENC.length,W/2,54);","ctx.fillText('1-1',W/2,54);")
# results text
R("return 'Best run: <b>'+best.score+'</b> points, area <b>'+best.wave+'/'+ENC.length+'</b>'+(best.won?' (cleared)':'')+', '+best.time+' as '+best.who;",
  "return 'Best run: <b>'+best.score+'</b> points, '+(best.won?'<b>1-1 cleared</b>':'stopped at <b>'+(best.wave>1?'the Foreman':'the skinheads')+'</b>')+', '+best.time+' as '+best.who;")
R("overEl.querySelector('h3').textContent=win?'Stage clear':'Knocked out';","overEl.querySelector('h3').textContent=win?'Section 1-1 clear':'Knocked out';")
R("$('r-wave').textContent=wave+'/'+ENC.length;","$('r-wave').textContent=win?'Exit':(encIdx>=1?'Foreman':'Skinheads');")
R("'Best run: '+best.score+' points, area '+best.wave+'/'+ENC.length;","'Best run: '+best.score+' points';")
open(p,'w').write(s);print('ok')
