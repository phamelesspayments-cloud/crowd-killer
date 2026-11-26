s=open('index.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
anims=open('../dyehard/car_anims.js').read().strip()
car=open('../dyehard/car_code.js').read()
# --- the car bonus, ported from DYE Hard's "Break the car!" ---
code='''/* ---------- bonus stage: break the car (ported from DYE Hard). Two hit points, front and rear; 30 seconds. ---------- */
'''+anims+'''
var car=null,puffs=[],dbris=[],bonusT=0,bonusMsg='',bonusPts=0,CSC=2.2;
loadSet('car','car_atlas.png',null,CAR_ANIMS,null);
var BRKW=['break_glass.wav','metal_clang.wav','break_metal.wav'].map(function(f){var a=new Audio();a.preload='auto';a.src=f;return a;});
function breakSnd(){if(muted)return;try{var a=BRKW[Math.floor(Math.random()*BRKW.length)].cloneNode();a.volume=Math.min(1,.9*OPT.sfx/8);var pr=a.play();if(pr&&pr.catch)pr.catch(function(){});}catch(e){sfx('heavy');}}
function hitSnd(heavy){sfx(heavy?'heavy':'hit');}
'''+car.split('/* ---------- bonus stage: smash the car (two hit points, front and rear) ---------- */\n')[1]+'''
function startBonus(){car={x:W/2,y:420,w:Math.round(168*CSC),l:0,hp:420,maxhp:420,stage:0,dead:false,shk:0,flash:0,hit:[0,0],t:0,ej:{},isCar:true};car.l=car.x-car.w/2;
  puffs.length=0;dbris.length=0;bonusMsg='';bonusPts=0;bonusT=30*60;}
function finishBonus(win){
  phase='bclear';phaseT=260;
  if(win){var sl=Math.ceil(bonusT/60);bonusPts=3000+sl*150+(sl>=20?2000:0);score+=bonusPts;bonusMsg=sl>=20?'PERFECT!':'BONUS CLEAR!';sfx('pick');}
  else{bonusPts=0;bonusMsg='TIME UP';}
  player.inv=Math.max(player.inv,400);
}
function updateBonus(){
  if(phase==='walk'){phase='bfight';return;}
  if(phase==='bfight'){bonusT--;if(car.dead)finishBonus(true);else if(bonusT<=0)finishBonus(false);return;}
  if(phase==='bclear'){phaseT--;if(phaseT<=0){phase='fade';fadeT=0;}}
}
'''
# DYE Hard checks phase==='fight' for hits; here the bonus fight phase is 'bfight'
code=code.replace("if(!car||car.dead||phase!=='fight')return;","if(!car||car.dead||phase!=='bfight')return;")
assert code.count("phase!=='bfight'")==2
rep("var IN=new Image(),inOk=false;",code+"var IN=new Image(),inOk=false;")
# level flow
rep("  if(phase==='walk'){\n    var lim=trigX(encIdx);","  if(SEC.bonus&&(phase==='walk'||phase==='bfight'||phase==='bclear')){updateBonus();return;}\n  if(phase==='walk'){\n    var lim=trigX(encIdx);")
rep("wolves=[];tracers=[];","wolves=[];tracers=[];car=null;if(SEC.bonus)startBonus();")
# hits, car tick, player can't walk through the car
rep("hitCan(cn,p.face,heavy);}\n  if(wm){","hitCan(cn,p.face,heavy);}\n  strikeCar(p,dmg,reach,heavy,both,big);\n  if(wm){")
rep("  updatePickups();updateItems();updateProjs();updateCan();updateLeaner();","  updatePickups();updateItems();updateProjs();updateCan();updateLeaner();\n  if(car){updateCar();var pp=player;if(pp.z<12&&Math.abs(pp.y-car.y)<24&&pp.x>car.l+6&&pp.x<car.l+car.w-6)pp.x=pp.x<car.x?car.l+6:car.l+car.w-6;}")
# draw
rep("for(var ti=0;ti<tracers.length;ti++)list.push(tracers[ti]);","for(var ti=0;ti<tracers.length;ti++)list.push(tracers[ti]);if(car)list.push(car);")
rep("else if(L.wolf)drawWolf(L);","else if(L.isCar)drawCar();else if(L.wolf)drawWolf(L);")
rep("  drawBeers();drawDrops();drawTeeth();drawNickyFX();","  drawBeers();drawDrops();drawTeeth();drawNickyFX();\n  if(car){drawCarFx();drawZoneMarks();}")
# HUD: timer and car damage instead of the stage number
rep("  ctx.textAlign='center';ctx.font='700 16px '+UI;ctx.fillStyle='#a6a1bb';ctx.fillText('STAGE',W/2,26);\n  ctx.font='28px '+DISPLAY;ctx.fillStyle=INK.w;ctx.fillText(SEC?SEC.name:'1-1',W/2,54);",
"""  ctx.textAlign='center';ctx.font='700 16px '+UI;ctx.fillStyle='#a6a1bb';ctx.fillText(SEC&&SEC.bonus?'BONUS STAGE':'STAGE',W/2,26);
  if(SEC&&SEC.bonus){
    if(phase==='intro'){ctx.font='24px '+DISPLAY;ctx.fillStyle=INK.w;ctx.fillText('GET READY',W/2,52);}
    else{var secs=Math.max(0,Math.ceil(bonusT/60));ctx.font='40px '+DISPLAY;ctx.fillStyle=(phase==='bfight'&&secs<=8&&((frames>>3)&1))?'#ff4a4a':INK.w;ctx.fillText(String(secs),W/2,58);}
    var cb=W/2-220,cy2=80;ctx.fillStyle='#0c0b12';ctx.fillRect(cb-3,cy2-3,446,24);
    var dmgf=car?clamp(1-car.hp/car.maxhp,0,1):0;ctx.fillStyle='#e9e6f2';ctx.fillRect(cb,cy2,440,18);
    ctx.fillStyle=dmgf>.66?'#ff4a4a':INK.y;ctx.fillRect(cb,cy2,440*dmgf,18);
    ctx.textAlign='left';ctx.font='700 14px '+UI;ctx.fillStyle='#14141c';ctx.fillText('CAR DAMAGE',cb+8,cy2+14);ctx.textAlign='center';
  }else{ctx.font='28px '+DISPLAY;ctx.fillStyle=INK.w;ctx.fillText(SEC?SEC.name:'1-1',W/2,54);}""")
rep("    misreg('STAGE '+SEC.name,W/2,180,72,clamp(a,0,1));","    misreg(SEC.bonus?'BONUS STAGE':'STAGE '+SEC.name,W/2,180,72,clamp(a,0,1));")
rep("  if(godMsgT>0){godMsgT--;","  if(phase==='bclear'){var bb=phaseT>240?(260-phaseT)/20:phaseT<20?phaseT/20:1;misreg(bonusMsg,W/2,190,64,clamp(bb,0,1));if(bonusPts)misreg('+'+bonusPts,W/2,260,38,clamp(bb,0,1));}\n  if(godMsgT>0){godMsgT--;")
# music: the bonus has its own track
rep("var MUSIC=new Audio('music_stage1.mp3');MUSIC.loop=true;MUSIC.preload='auto';","var MUSIC=new Audio('music_stage1.mp3');MUSIC.loop=true;MUSIC.preload='auto';\nvar BMUS=new Audio('music_bonus.mp3');BMUS.loop=true;BMUS.preload='auto';")
rep("function musicStop(){try{MUSIC.pause();MUSIC.currentTime=0;}catch(e){}}","""function musicStop(){try{MUSIC.pause();MUSIC.currentTime=0;BMUS.pause();BMUS.currentTime=0;}catch(e){}}
/* on a new section: the bonus stage swaps to its own track; a section with no music is silent */
function musicSection(){try{if(SEC.music==='bonus'){MUSIC.pause();BMUS.currentTime=0;BMUS.volume=musicVol();var pr=BMUS.play();if(pr&&pr.catch)pr.catch(function(){});}else if(!SEC.music)musicStop();else{BMUS.pause();}}catch(e){}}""")
rep("function musicVol(){","function musicVolSync(){try{BMUS.volume=musicVol();}catch(e){}}\nfunction musicVol(){")
rep("loadSection(secIdx+1,false);phase='intro';phaseT=110;fadeIn=FADE_IN;if(!SEC.music)musicStop();","loadSection(secIdx+1,false);phase='intro';phaseT=110;fadeIn=FADE_IN;musicSection();")
# the section: between 2-4 and 3-1, in DYE Hard's parking lot
rep("  /* 3-1 the sewer:","""  /* BONUS: break the car (from DYE Hard), between stage 2 and stage 3 */
  {name:'BONUS',bonus:'car',music:'bonus',sub:'BREAK THE CAR!',src:'bonus_bg.jpg',k:540/572,oy:0,ft:340,fb:476,waveBase:0,startX:180,startY:420,
   skins:[null],propSrc:[],enc:[],trig:[0],cans:[],actors:[]},
  /* 3-1 the sewer:""")
open('index.html','w').write(s)
