s=open('index.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
FJ=open('font2.json').read()
code=r'''
/* ---------- body font: the white chiselled letters (font2.png) for all other text, on the game screen and the page ---------- */
var BF_G=%s,BF_IMG=new Image(),bfOk=false,BF_CH=77,BF_BASE=66,bfTints={};
var bfWait=[];BF_IMG.onload=function(){bfOk=true;var w=bfWait;bfWait=[];w.forEach(function(f){f();});};BF_IMG.src='font2.png';
function bfKey(ch){if(BF_G[ch])return ch;if(ch==='×')return 'x';if(ch==='’'||ch==='‘')return "'";if(ch==='“'||ch==='”')return '"';if(ch==='–'||ch==='—'||ch==='·'||ch==='‹'||ch==='›')return ch==='·'?'·':ch==='‹'?'<':ch==='›'?'>':'-';var u=ch.toUpperCase();return BF_G[u]?u:ch;}
/* white letters come straight from the atlas; any other colour gets a tinted copy (multiply keeps the chisel shading) */
function bfAtlas(col){
  if(!col||typeof col!=='string')return BF_IMG;var k=col.replace(/\s/g,'').toLowerCase();
  if(k==='#fff'||k==='#ffffff'||k==='#f4f2fa'||k==='white'||k==='rgb(255,255,255)')return BF_IMG;
  if(bfTints[k])return bfTints[k];
  var c=document.createElement('canvas');c.width=BF_IMG.width;c.height=BF_IMG.height;var g=c.getContext('2d');
  g.drawImage(BF_IMG,0,0);g.globalCompositeOperation='multiply';g.fillStyle=col;g.fillRect(0,0,c.width,c.height);
  g.globalCompositeOperation='destination-in';g.drawImage(BF_IMG,0,0);bfTints[k]=c;return c;
}
function bfAdv(ch,sc){var k=bfKey(ch),G=BF_G[k];if(G)return (G[2]-7)*sc;if(k===' ')return 24*sc;if(k==='·')return 26*sc;return 30*sc;}
function bfWidth(txt,size){var sc=size*1.25/BF_CH,w=0;for(var i=0;i<txt.length;i++)w+=bfAdv(txt[i],sc);return w+7*sc;}
/* size: the CSS-style px size the text was meant to be; baseline: 'alphabetic' | 'middle' | 'top' */
function bfText(g,txt,x,y,size,align,baseline,col){
  txt=String(txt);var sc=size*1.25/BF_CH,tw=bfWidth(txt,size),img=bfAtlas(col);
  var cx=align==='right'||align==='end'?x-tw:align==='center'?x-tw/2:x;
  var top=baseline==='middle'?y-36*sc:baseline==='top'||baseline==='hanging'?y-3*sc:y-BF_BASE*sc;
  for(var i=0;i<txt.length;i++){
    var k=bfKey(txt[i]),G=BF_G[k];
    if(G)g.drawImage(img,G[0],G[1],G[2],BF_CH,cx,top,G[2]*sc,BF_CH*sc);
    else if(k==='·'){var d=BF_G['.'];if(d)g.drawImage(img,d[0],d[1],d[2],BF_CH,cx,top-22*sc,d[2]*sc,BF_CH*sc);}
    cx+=bfAdv(txt[i],sc);
  }
}
/* every fillText on the game screen goes through the letters (their outline and shadow are built in, so strokeText is skipped) */
(function(){
  var oF=ctx.fillText.bind(ctx),oS=ctx.strokeText.bind(ctx);
  ctx.fillText=function(t,x,y){if(!bfOk)return oF(t,x,y);var m=/(\d+(?:\.\d+)?)px/.exec(ctx.font),sz=m?+m[1]:16;
    var prev=ctx.imageSmoothingEnabled;ctx.imageSmoothingEnabled=true;bfText(ctx,t,x,y,sz,ctx.textAlign,ctx.textBaseline,ctx.fillStyle);ctx.imageSmoothingEnabled=prev;};
  ctx.strokeText=function(t,x,y){if(!bfOk)return oS(t,x,y);};
})();
/* page text: each text node becomes a row of small canvases, one per word, so the browser still wraps lines.
   A visually hidden copy of the text stays for screen readers, copy-paste and textContent. */
var BF_SKIP={SCRIPT:1,STYLE:1,TITLE:1,OPTION:1,SELECT:1,TEXTAREA:1,CANVAS:1,NOSCRIPT:1};
function bfWordCanvas(w,px,col){
  var dpr=Math.min(3,window.devicePixelRatio||1),sc=px*1.25/BF_CH,wd=Math.max(1,Math.ceil(bfWidth(w,px))),ht=Math.ceil(BF_CH*sc);
  var c=document.createElement('canvas');c.width=wd*dpr;c.height=ht*dpr;c.style.width=wd+'px';c.style.height=ht+'px';
  c.style.verticalAlign=(-(BF_CH-BF_BASE)*sc).toFixed(1)+'px';c.setAttribute('aria-hidden','true');c.className='bfw';
  var g=c.getContext('2d');g.scale(dpr,dpr);g.imageSmoothingEnabled=true;bfText(g,w,0,BF_BASE*sc,px,'left','alphabetic',col);return c;
}
function bfNode(tn){
  var el=tn.parentNode;if(!el||el.nodeType!==1||BF_SKIP[el.nodeName]||el.closest('.fhead,.bfsr,.bfwrap'))return;
  var raw=tn.nodeValue;if(!raw||!raw.trim())return;
  var cs=getComputedStyle(el),px=parseFloat(cs.fontSize)||16,col=cs.color,txt=raw.replace(/\s+/g,' ');
  if(cs.textTransform==='uppercase')txt=txt.toUpperCase();
  var wrap=document.createElement('span');wrap.className='bfwrap';
  var sr=document.createElement('span');sr.className='bfsr';sr.textContent=raw;wrap.appendChild(sr);
  var parts=txt.split(/( )/);
  parts.forEach(function(p){if(p===' ')wrap.appendChild(document.createTextNode(' '));else if(p)wrap.appendChild(bfWordCanvas(p,px,col));});
  el.replaceChild(wrap,tn);
}
function bfScan(root){
  if(!bfOk)return;var tw=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,null),list=[],n;
  while((n=tw.nextNode()))list.push(n);list.forEach(bfNode);
}
function bfStart(){
  bfScan(document.body);
  try{new MutationObserver(function(ms){ms.forEach(function(m){
    if(m.type==='characterData'){var p=m.target.parentNode;if(p&&p.classList&&p.classList.contains('bfsr')){var w=p.parentNode;if(w&&w.parentNode){var t=document.createTextNode(m.target.nodeValue);w.parentNode.replaceChild(t,w);bfNode(t);}}else if(m.target.nodeType===3)bfNode(m.target);return;}
    m.addedNodes.forEach(function(a){if(a.nodeType===3)bfNode(a);else if(a.nodeType===1&&!(a.classList&&(a.classList.contains('bfwrap')||a.classList.contains('bfw')||a.classList.contains('bfsr'))))bfScan(a);});
  });}).observe(document.body,{childList:true,subtree:true,characterData:true});}catch(e){}
}
if(bfOk)bfStart();else bfWait.push(bfStart);
'''%FJ
rep("var cv=$('game'),ctx=cv.getContext('2d');\n","var cv=$('game'),ctx=cv.getContext('2d');\n"+code)
rep(".fhead{text-shadow:none!important;line-height:0!important}",".fhead{text-shadow:none!important;line-height:0!important}\n.bfsr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap}\n.bfwrap{text-shadow:none}\ncanvas.bfw{display:inline-block}")
open('index.html','w').write(s)
