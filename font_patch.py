import json
s=open('index.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
FJ=open('font.json').read()
code='''/* ---------- heading font: the orange bitmap letters (font.png), for names, level names and headings ---------- */
var FONT_G=%s,FONT_IMG=new Image(),fontOk=false,fontWait=[];
FONT_IMG.onload=function(){fontOk=true;var w=fontWait;fontWait=[];w.forEach(function(f){f();});};FONT_IMG.src='font.png';
function fontKey(ch){ch=ch.toUpperCase();if(ch==='×')return 'X';if(ch==='’'||ch==='‘')return "'";if(ch==='–'||ch==='—')return '-';return ch;}
/* size is roughly the cap height of the old display font at that px size; y is the vertical centre */
function fontWidth(txt,size){var sc=size/56,w=0;for(var i=0;i<txt.length;i++){var k=fontKey(txt[i]),G=FONT_G[k];w+=G?(G[2]-4)*sc:(k===' '?20*sc:size*.5);}return w+4*sc;}
function fontText(g,txt,x,y,size,align,maxW){
  txt=String(txt);var tw=fontWidth(txt,size);if(maxW&&tw>maxW){size*=maxW/tw;tw=maxW;}
  var sc=size/56,cx=align==='left'?x:align==='right'?x-tw:x-tw/2,top=y-27*sc;
  g.save();g.imageSmoothingEnabled=true;
  for(var i=0;i<txt.length;i++){
    var k=fontKey(txt[i]),G=FONT_G[k];
    if(G){g.drawImage(FONT_IMG,G[0],G[1],G[2],G[3],Math.round(cx),Math.round(top),G[2]*sc,G[3]*sc);cx+=(G[2]-4)*sc;}
    else if(k===' ')cx+=20*sc;
    else{ /* a character the sheet doesn't have: draw it in the old font, coloured to match */
      g.font=Math.round(size*.8)+'px '+DISPLAY;g.textAlign='left';g.textBaseline='middle';g.lineWidth=5*sc+2;g.strokeStyle='#fff';g.strokeText(k,cx,y);
      var gr=g.createLinearGradient(0,y-size*.4,0,y+size*.4);gr.addColorStop(0,'#ffd23f');gr.addColorStop(1,'#e8361c');g.fillStyle=gr;g.fillText(k,cx,y);cx+=size*.5;}
  }
  g.restore();
}
/* page headings drawn in the same letters (the text stays as the accessible name) */
function fontHead(el,txt,px){
  if(!el)return;el.setAttribute('aria-label',txt);el.classList.add('fhead');
  if(!fontOk){el.textContent=txt;fontWait.push(function(){fontHead(el,txt,px);});return;}
  var dpr=Math.min(3,window.devicePixelRatio||1),sz=px*1.15,w=Math.ceil(fontWidth(txt,sz))+4,h=Math.ceil(sz*1.05);
  var c=document.createElement('canvas');c.width=w*dpr;c.height=h*dpr;c.style.width=w+'px';c.style.maxWidth='100%%';c.style.height='auto';c.setAttribute('aria-hidden','true');
  var g=c.getContext('2d');g.scale(dpr,dpr);fontText(g,txt,2,h/2,sz,'left');
  el.textContent='';el.appendChild(c);
}
'''%FJ
rep("function misreg(txt,x,y,size,alpha){","""function misreg(txt,x,y,size,alpha){
  if(fontOk){ctx.save();ctx.globalAlpha=alpha;fontText(ctx,txt,x,y,size*1.05,'center',W-60);ctx.restore();return;}""")
rep("function misreg(txt,x,y,size,alpha){",code+"function misreg(txt,x,y,size,alpha){")
# HUD: player name, level name, boss names, bonus timer
rep("  ctx.font='22px '+DISPLAY;ctx.fillStyle=c.ink;ctx.fillText(c.name.toUpperCase(),24,38);","  if(fontOk)fontText(ctx,c.name,22,28,30,'left');else{ctx.font='22px '+DISPLAY;ctx.fillStyle=c.ink;ctx.fillText(c.name.toUpperCase(),24,38);}")
rep("  }else{ctx.font='28px '+DISPLAY;ctx.fillStyle=INK.w;ctx.fillText(SEC?SEC.name:'1-1',W/2,54);}","  }else if(fontOk)fontText(ctx,SEC?SEC.name:'1-1',W/2,45,38,'center');else{ctx.font='28px '+DISPLAY;ctx.fillStyle=INK.w;ctx.fillText(SEC?SEC.name:'1-1',W/2,54);}")
rep("    else{var secs=Math.max(0,Math.ceil(bonusT/60));ctx.font='40px '+DISPLAY;ctx.fillStyle=(phase==='bfight'&&secs<=8&&((frames>>3)&1))?'#ff4a4a':INK.w;ctx.fillText(String(secs),W/2,58);}",
    "    else{var secs=Math.max(0,Math.ceil(bonusT/60));if(fontOk){if(!(phase==='bfight'&&secs<=8&&((frames>>3)&1)))fontText(ctx,String(secs),W/2,46,44,'center');}else{ctx.font='40px '+DISPLAY;ctx.fillStyle=(phase==='bfight'&&secs<=8&&((frames>>3)&1))?'#ff4a4a':INK.w;ctx.fillText(String(secs),W/2,58);}}")
rep("    if(phase==='intro'){ctx.font='24px '+DISPLAY;ctx.fillStyle=INK.w;ctx.fillText('GET READY',W/2,52);}","    if(phase==='intro'){if(fontOk)fontText(ctx,'GET READY',W/2,45,30,'center');else{ctx.font='24px '+DISPLAY;ctx.fillStyle=INK.w;ctx.fillText('GET READY',W/2,52);}}")
rep("ctx.textAlign='left';ctx.font='18px '+DISPLAY;ctx.fillStyle=INK.y;ctx.fillText(be.d.title||'BOSS',bx2,by2-8);","if(fontOk)fontText(ctx,be.d.title||'BOSS',bx2-2,by2-17,24,'left');else{ctx.textAlign='left';ctx.font='18px '+DISPLAY;ctx.fillStyle=INK.y;ctx.fillText(be.d.title||'BOSS',bx2,by2-8);}")
# page headings
rep("  overEl.querySelector('h3').textContent=win?'Section '+SEC.name+' clear':'Knocked out';","  fontHead(overEl.querySelector('h3'),win?'Section '+SEC.name+' clear':'Knocked out',52);")
rep("var FONT_IMG=new Image(),fontOk=false,fontWait=[];","XX",0) if False else None
s=s.replace("FONT_IMG.src='font.png';","""FONT_IMG.src='font.png';
function fontHeads(){fontHead(document.querySelector('header.top h1'),'Crowd Killer',40);fontHead(document.getElementById('opt-h'),'Options',30);fontHead(document.getElementById('pick-h'),'Choose your fighter',30);
  fontHead(document.querySelector('#pause h3'),'Paused',52);fontHead(document.querySelector('#over h3'),'Knocked out',52);}
fontHeads();""",1)
rep(".overlay h3{margin:0;",".fhead{text-shadow:none!important;line-height:0!important}\n.fhead canvas{display:inline-block;vertical-align:middle}\n.overlay h3{margin:0;")
open('index.html','w').write(s)
