import json,re
s=open('index.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a));s=s.replace(a,b)
A=json.load(open('ned_anims.json'));MZ=A.pop('muzzle')
gd=open('grunt_deaths.json').read()
s=re.sub(r'var GDEATH=\{.*?\};\n',lambda m:'var GDEATH='+gd+';\n',s,count=1,flags=re.S)
rep("  /* Dan Glenzig: boss of 2-4;","""  /* Ned Tugent: boss of 3-2; punches up close, and now and then draws his revolver and fires along his lane */
  ned:{hp:250,spd:.95,dmg:26,range:62,wind:30,rec:36,scale:1.4,pts:6000,w:52,armor:true,poise:true,poiseMax:80,
    boss:true,title:'NED TUGENT',topY:200,walkIn:true,gunner:true,
    pal:{shirt:'#4b5232',print:INK.k,skin:'#d9a27b',hair:INK.k,head:'hair',pants:'#3a5a8a',shoe:INK.k}},
  /* Dan Glenzig: boss of 2-4;""")
rep("EN.dan.sprite=true;EN.dan.sprScale=1.17;","EN.dan.sprite=true;EN.dan.sprScale=1.17;EN.ned.sprite=true;EN.ned.sprScale=1.85;")
rep("type==='hoyle'||type==='gerry'||type==='dan'?type:null","type==='hoyle'||type==='gerry'||type==='dan'||type==='ned'?type:null")
rep("s==='summon'||s==='gcrouch'","s==='summon'||s==='shoot'||s==='gcrouch'")
rep("heavy:[150,40,.18,'sawtooth',.09],","heavy:[150,40,.18,'sawtooth',.09],gun:[1500,70,.16,'square',.16],")
rep("""  }else if(e.state==='summon'){""","""  }else if(e.state==='shoot'){
    /* Ned draws (the click is the warning), aims, fires twice along his lane, twirls the revolver and holsters it */
    e.vx=0;e.vy=0;
    if(e.t===14)sfx('pick');
    if(e.t===50||e.t===74)nedFire(e);
    if(e.t>=138){e.state='walk';e.cd=rnd(40,70);}
  }else if(e.state==='summon'){""")
rep("""      e.state='summon';e.t=0;e.vx=0;e.vy=0;e.face=p.x>e.x?1:-1;e.sumCd=420;
    }
""","""      e.state='summon';e.t=0;e.vx=0;e.vy=0;e.face=p.x>e.x?1:-1;e.sumCd=420;
    }
    else if(d.gunner&&pAlive&&e.inn&&e.cd<=0&&(e.sumCd||0)<=0&&Math.random()<(Math.abs(p.x-e.x)>160?.02:.006)&&p.state!=='down'){
      e.state='shoot';e.t=0;e.vx=0;e.vy=0;e.face=p.x>e.x?1:-1;e.sumCd=rnd(240,360);
    }
""")
code='''/* Ned Tugent: walk, wound-up punch, getting hit and the revolver draw from his clips */
var NED_ANIMS=%s,NED_MZ=%s;
ECFG.ned={wind:[0,1,2,3,4],atk:[5,6,7,8,9],rec:[10,0],stride:6.6};
/* gun frames: draw 0-2, aim 3, fire 4-5, twirl 6-10, holster 11-13 */
function nedGunIdx(t){
  if(t<8)return 0;if(t<16)return 1;if(t<24)return 2;if(t<50)return 3;if(t<54)return 4;if(t<58)return 5;if(t<74)return 3;
  if(t<78)return 4;if(t<82)return 5;if(t<90)return 3;if(t<120)return 6+Math.floor((t-90)/6);return Math.min(13,11+Math.floor((t-120)/6));
}
function nedFrame(e){if(e.state==='shoot')return NED_ANIMS.gun[nedGunIdx(e.t)];return enemyFrame(e);}
loadSet('ned','ned_atlas.png',null,NED_ANIMS,nedFrame);
/* a shot hits the player if they're roughly level with Ned (same depth) anywhere in front of him on screen */
var tracers=[];
function nedFire(e){
  var p=player,sc=e.d.sprScale*((SEC&&SEC.cs)||1),mx=e.x+e.face*NED_MZ[0]*sc,my=e.y+NED_MZ[1]*sc;
  sfx('gun');shake=Math.max(shake,4*(REDUCE?.3:1));
  var hit=p.hp>0&&p.state!=='down'&&Math.abs(p.y-e.y)<24&&(p.x-e.x)*e.face>20&&p.z<60*CS&&p.x>camX-10&&p.x<camX+W+10;
  var ex=hit?p.x-e.face*10:(e.face>0?camX+W+40:camX-40);
  tracers.push({tracer:true,x:(mx+ex)/2,y:e.y+2,x0:mx,x1:ex,my:my,t:7});
  if(hit){hurtPlayer(Math.round(22*DIFF().edmg),e.face,true);burst(p.x,my,10,5,['#ffe066','#ff9b3d',INK.w]);}
}
function tickTracers(){for(var i=tracers.length-1;i>=0;i--)if(--tracers[i].t<=0)tracers.splice(i,1);}
function drawTracer(T){
  ctx.save();ctx.globalAlpha=T.t/7;ctx.strokeStyle='#fff3b0';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(T.x0,T.my);ctx.lineTo(T.x1,T.my);ctx.stroke();
  ctx.strokeStyle='#ffb43d';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(T.x0,T.my-2);ctx.lineTo(T.x1,T.my-2);ctx.stroke();ctx.restore();
}
'''%(json.dumps(A,separators=(',',':')),json.dumps(MZ))
rep("/* Dan Glenzig: stomp-walk,",code+"/* Dan Glenzig: stomp-walk,")
rep("tickWolves();","tickWolves();tickTracers();")
rep("heads=[];wolves=[];","heads=[];wolves=[];tracers=[];")
rep("for(var wi=0;wi<wolves.length;wi++)list.push(wolves[wi]);","for(var wi=0;wi<wolves.length;wi++)list.push(wolves[wi]);for(var ti=0;ti<tracers.length;ti++)list.push(tracers[ti]);")
rep("else if(L.wolf)drawWolf(L);","else if(L.wolf)drawWolf(L);else if(L.tracer)drawTracer(L);")
i=s.index("  {name:'3-1',");j=s.index("doorFlash:true}",i)+len("doorFlash:true}")
s=s[:j]+""",
  /* 3-2 PLACEHOLDER: the 2-4 basement until the Turd Processing room's background arrives; Ned Tugent is the boss */
  {name:'3-2',sub:'NED TUGENT',src:'dan_bg.jpg',k:540/793,oy:0,ft:364,waveBase:9,startX:110,
   skins:[null,'grunt2','grunt3','grunt4','chad','kevin'],propSrc:[],
   enc:[{g:3,b:0,t:0},{g:2,b:0,t:0,boss:'ned'}],trig:[.25,1],endOnClear:true,stageEnd:'STAGE 3 CLEAR',
   cans:[{x:700,y:372,loot:'tenders'}],actors:[]}"""+s[j:]
open('index.html','w').write(s)
