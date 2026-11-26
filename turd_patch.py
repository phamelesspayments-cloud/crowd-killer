s=open('index.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a));s=s.replace(a,b)
rep("  im.src=sec.src;\n});","""  im.src=sec.src;
  /* an animated room: a looping, muted video drawn over the still (the still shows until the video can play) */
  if(sec.video){try{var v=document.createElement('video');v.muted=true;v.defaultMuted=true;v.loop=true;v.playsInline=true;
    v.setAttribute('playsinline','');v.setAttribute('muted','');v.preload='auto';v.src=sec.video;
    v.style.cssText='position:fixed;left:0;top:0;width:2px;height:2px;opacity:0.01;pointer-events:none;z-index:-1';
    (document.body||document.documentElement).appendChild(v);sec.vid=v;}catch(e){}}
});
function syncSectionVideo(){SECTIONS.forEach(function(q){if(q.vid&&q!==SEC&&!q.vid.paused)q.vid.pause();});
  if(SEC&&SEC.vid&&SEC.vid.paused){try{var pr=SEC.vid.play();if(pr&&pr.catch)pr.catch(function(){});}catch(e){}}}""")
rep("  if(bg)ctx.drawImage(bg,cx,0,W,H,cx,0,W,H);","  if(bg)ctx.drawImage(bg,cx,0,W,H,cx,0,W,H);\n  if(SEC&&SEC.vid){if(SEC.vid.readyState>=2)ctx.drawImage(SEC.vid,0,SEC.oy||0,Math.round(SEC.vid.videoWidth*SEC.k),Math.round(SEC.vid.videoHeight*SEC.k));if((frames&31)===0)syncSectionVideo();}")
rep("ENC=SEC.enc;TRIG=SEC.trig;","syncSectionVideo();ENC=SEC.enc;TRIG=SEC.trig;")
i=s.index("  /* 3-2 PLACEHOLDER");j=s.index("cans:[{x:700,y:372,loot:'tenders'}],actors:[]}",i)+len("cans:[{x:700,y:372,loot:'tenders'}],actors:[]}")
s=s[:i]+"""  /* 3-2 Turd Processing: one screen, its machines animated by a looping video. Three grunts, then Ned Tugent comes
     out of the EXIT door. The angled right wall by the door and the machines along the back are off limits. */
  {name:'3-2',sub:'TURD PROCESSING',src:'turd_bg.jpg',video:'turd_bg.mp4',k:1,oy:0,ft:394,waveBase:9,startX:150,
   skins:[null,'grunt2','grunt3','grunt4','chad','kevin'],propSrc:[],
   walls:{left:[[0,394],[0,540]],right:[[818,394],[934,462],[934,540]],margin:24},
   spawnPts:[[70,452],[836,430],[70,512],[880,500]],
   enc:[{g:3,b:0,t:0},{g:2,b:0,t:0,boss:'ned'}],trig:[0,0],endOnClear:true,bossSpawn:[846,438],stageEnd:'STAGE 3 CLEAR',
   cans:[],actors:[]}"""+s[j:]
open('index.html','w').write(s)
