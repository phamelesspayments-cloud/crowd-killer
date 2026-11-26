from PIL import Image
import numpy as np,json,glob,os
from scipy import ndimage
def keyed(arr,thr=(110,35,40)):
    r,g,b=arr[...,0].astype(int),arr[...,1].astype(int),arr[...,2].astype(int)
    green=(g>thr[0])&(g-r>thr[1])&(g-b>thr[2])
    a=np.where(green,0,255).astype(np.uint8);edge=(g-np.maximum(r,b)>14)&~green;a=np.where(edge,110,a).astype(np.uint8)
    a[:3,:]=0;a[-3:,:]=0;a[:,:3]=0;a[:,-3:]=0
    o=np.dstack([r,np.minimum(g,np.maximum(r,b)+6),b,a]).astype(np.uint8)
    m=o[...,3]>100;lab,n=ndimage.label(m)
    if n>1:
        sz=ndimage.sum(m,lab,range(1,n+1));keep=np.isin(lab,[i+1 for i in range(n) if sz[i]>=30]);o[...,3]=np.where(keep,o[...,3],0)
    return o
def vf(v,i):return keyed(np.array(Image.open('f%d/%03d.png'%(v,i+1)).convert('RGB')))
def bbox(o):
    ys,xs=np.where(o[...,3]>100);return xs.min(),ys.min(),xs.max()+1,ys.max()+1
def no_puddle(o,feet_y):
    """drop brown vomit on the floor (anything at foot level that isn't boot-dark)"""
    rgb=o[...,:3].astype(int);al=o[...,3]>100
    brown=al&(rgb[...,0]>70)&(rgb[...,0]-rgb[...,2]>25)&(rgb[...,1]>35)
    band=np.zeros_like(al);band[feet_y-30:,:]=True
    lab,n=ndimage.label(brown&band)
    o=o.copy()
    for i in range(1,n+1):
        ys,xs=np.where(lab==i)
        if len(xs)>15:o[lab==i,3]=0
    return o
# ---------- enemy atlas (drawn x1.9 like other grunts) ----------
G=108
def crop(o,S,ax,ay):
    x0,y0,x1,y1=bbox(o);im=Image.fromarray(o[y0:y1,x0:x1],'RGBA').resize((max(1,round((x1-x0)*S)),max(1,round((y1-y0)*S))),Image.LANCZOS)
    return [im,round((ax-x0)*S),round((ay-y0)*S)]
def ref(o):
    x0,y0,x1,y1=bbox(o);a=o[...,3]>100;feet=np.where(a[y1-12:y1].any(0))[0];return (feet.min()+feet.max())/2,y1,y1-y0
anims={}
w0=vf(1,0);fx,fy,h=ref(w0);S1=G/h
anims['walk']=[crop(vf(1,i),S1,fx,fy) for i in range(0,30,2)]
g0=vf(2,0);gx,gy,gh=ref(g0);S2=G/gh
anims['act']=[crop(vf(2,i),S2,gx,gy) for i in (0,16,18,20,24,28,32)]
# hurt: clutching stomach (death sheet frame 1, clean) and slumped (vomit clip 42 without puddle)
ds=np.array(Image.open('death.jpg').convert('RGB'))
dsk=keyed(ds,(120,40,40))
lab,n=ndimage.label(ndimage.binary_dilation(dsk[...,3]>100,iterations=6));objs=ndimage.find_objects(lab);sz=ndimage.sum(dsk[...,3]>100,lab,range(1,n+1))
big=sorted([(k+1,o) for k,(o,s) in enumerate(zip(objs,sz)) if s>3000],key=lambda t:(((t[1][0].start+t[1][0].stop)//2)//320,t[1][1].start))
DF=[]
for lid,o in big:
    c=dsk.copy();c[...,3]=np.where(lab==lid,c[...,3],0);DF.append(c[o[0],o[1]])
dx,dy,dh=ref(DF[0]);SD=G/dh
v42=no_puddle(vf(3,42),697);v3x,v3y,v3h=ref(vf(3,0));S3=G/644
anims['hurt']=[crop(DF[1],SD,*ref(DF[1])[:2]),crop(v42,S3,v3x,v3y),crop(DF[1],SD,*ref(DF[1])[:2]),crop(v42,S3,v3x,v3y)]
# knockdown (not lethal): his guard frame rotated over onto his back, and back up again
base=Image.fromarray(g0[slice(*bbox(g0)[1::2])] if False else g0,'RGBA')
x0,y0,x1,y1=bbox(g0);gimg=Image.fromarray(g0[y0:y1,x0:x1],'RGBA').resize((round((x1-x0)*S2),round((y1-y0)*S2)),Image.LANCZOS)
def rot(a):
    r=gimg.rotate(a,expand=True,resample=Image.BICUBIC);bb=r.getbbox();r=r.crop(bb);return [r,r.width//2,r.height]
anims['down']=[rot(25),rot(55),rot(80),rot(90),rot(90),rot(90)]
anims['getup']=[rot(70),rot(45),rot(20),rot(0)]
RW=1024;x=y=rowh=0;out={};items=[]
for nm,L in anims.items():
    out[nm]=[]
    for im,ax,ay in L:
        w,h=im.size
        if x+w>RW:x=0;y+=rowh+2;rowh=0
        items.append((im,x,y));out[nm].append([x,y,w,h,ax,ay,0,0]);x+=w+2;rowh=max(rowh,h)
    x=0;y+=rowh+2;rowh=0
at=Image.new('RGBA',(RW,y))
for im,px,py in items:at.alpha_composite(im,(px,py))
at.save('../build/kevin_atlas.png',optimize=True);json.dump(out,open('../build/kevin_anims.json','w'),separators=(',',':'))
# walk stride: one cycle (30 frames) covers two steps; measure foot spread at game scale (x1.9)
spans=[]
for i in range(0,30):
    o=vf(1,i);a=o[...,3]>100;x0,y0,x1,y1=bbox(o);band=a[y1-40:y1];xs=np.where(band.any(0))[0];spans.append(xs.max()-xs.min())
step=(max(spans)-min(spans))*S1*1.9;print('stride per anim frame',round(2*step/15,2))
# ---------- vomit intro sheet, at game size (205 tall) ----------
TH=205;SI=TH/644
fr=[vf(3,i) for i in range(0,73,2)]
al=np.maximum.reduce([f[...,3] for f in fr]);ys,xs=np.where(al>150);X0,Y0,X1,Y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
fw,fh=round((X1-X0)*SI),round((Y1-Y0)*SI);cols=8;rows=(len(fr)+cols-1)//cols
sh=Image.new('RGBA',(fw*cols,fh*rows))
for k,f in enumerate(fr):sh.alpha_composite(Image.fromarray(f[Y0:Y1,X0:X1],'RGBA').resize((fw,fh),Image.LANCZOS),((k%cols)*fw,(k//cols)*fh))
sh.save('../build/kevin_vomit.png',optimize=True)
print('intro frame',fw,fh,'anchor',round((v3x-X0)*SI),round((697-Y0)*SI),'n',len(fr))
# the puddle left behind (last frame), stamped on the floor when he joins the fight
last=fr[-1];p=last.copy();rgb=p[...,:3].astype(int);alp=p[...,3]>100
brown=alp&(rgb[...,0]>70)&(rgb[...,0]-rgb[...,2]>25)&(rgb[...,1]>35);band=np.zeros_like(alp);band[690:,:]=True
lab2,n2=ndimage.label(brown&band);keep=np.zeros_like(alp)
for i in range(1,n2+1):
    if (lab2==i).sum()>15:keep|=(lab2==i)
keep=ndimage.binary_dilation(keep,iterations=2)&alp
p[...,3]=np.where(keep,p[...,3],0);px0,py0,px1,py1=bbox(p)
pud=Image.fromarray(p[py0:py1,px0:px1],'RGBA').resize((round((px1-px0)*SI),max(1,round((py1-py0)*SI))),Image.LANCZOS);pud.save('../build/kevin_puddle.png')
print('puddle',pud.size,'offset',round((px0-v3x)*SI),round((py0-697)*SI))
# ---------- death frames for the grunt-death atlas ----------
import pickle;pickle.dump(DF,open('kevin_death.pkl','wb'))
print('death frames',len(DF))
