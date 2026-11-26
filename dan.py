from PIL import Image
import numpy as np,json,pickle
from scipy import ndimage
def keyed(arr,thr=(110,35,40),minsz=30):
    r,g,b=arr[...,0].astype(int),arr[...,1].astype(int),arr[...,2].astype(int)
    green=(g>thr[0])&(g-r>thr[1])&(g-b>thr[2])
    a=np.where(green,0,255).astype(np.uint8);edge=(g-np.maximum(r,b)>14)&~green;a=np.where(edge,110,a).astype(np.uint8)
    a[:3,:]=0;a[-3:,:]=0;a[:,:3]=0;a[:,-3:]=0
    o=np.dstack([r,np.minimum(g,np.maximum(r,b)+6),b,a]).astype(np.uint8)
    m=o[...,3]>100;lab,n=ndimage.label(m)
    if n>1:
        sz=ndimage.sum(m,lab,range(1,n+1));keep=np.isin(lab,[i+1 for i in range(n) if sz[i]>=minsz]);o[...,3]=np.where(keep,o[...,3],0)
    return o
def vf(v,i):return keyed(np.array(Image.open('f%d/%03d.png'%(v,i+1)).convert('RGB')))
def bbox(o):
    ys,xs=np.where(o[...,3]>100);return xs.min(),ys.min(),xs.max()+1,ys.max()+1
def ref(o):
    x0,y0,x1,y1=bbox(o);a=o[...,3]>100;feet=np.where(a[y1-12:y1].any(0))[0];return (feet.min()+feet.max())/2,y1,y1-y0
G=108
def crop(o,S,ax,ay):
    x0,y0,x1,y1=bbox(o);im=Image.fromarray(o[y0:y1,x0:x1],'RGBA').resize((max(1,round((x1-x0)*S)),max(1,round((y1-y0)*S))),Image.LANCZOS)
    return [im,round((ax-x0)*S),round((ay-y0)*S)]
anims={}
w0=vf(2,0);wx,wy,wh=ref(w0);S1=G/wh
anims['walk']=[crop(vf(2,i),S1,wx,wy) for i in range(0,72,3)]
s0=vf(1,0);sx,sy,sh_=ref(s0);SS=G/sh_
anims['summon']=[crop(vf(1,i),SS,sx,sy) for i in (0,6,12,18,24,30,36,42,48,54,60,66)]
g0=vf(3,0);gx,gy,gh=ref(g0);S2=G/gh
anims['act']=[crop(vf(3,i),S2,gx,gy) for i in (0,12,24,36,45,51,54,57,60,66,69)]
# death sheet: 4 x 4
ds=keyed(np.array(Image.open('death.png').convert('RGB')),(120,45,45),15)
cells=[((0,189),[0,236,498,747,1024]),((189,381),[0,246,498,767,1024]),((381,572),[0,239,492,763,1024])]
DF=[]
for (y0,y1),cs in cells:
    for ci in range(4):DF.append(ds[y0:y1,cs[ci]:cs[ci+1]].copy())
dx,dy,dh=ref(DF[0]);SD=G/dh
anims['hurt']=[crop(vf(1,15),SS,sx,sy),crop(vf(3,24),S2,gx,gy),crop(vf(1,15),SS,sx,sy),crop(vf(3,24),S2,gx,gy)]
x0,y0,x1,y1=bbox(g0);gimg=Image.fromarray(g0[y0:y1,x0:x1],'RGBA').resize((round((x1-x0)*S2),round((y1-y0)*S2)),Image.LANCZOS)
def rot(a):
    r=gimg.rotate(a,expand=True,resample=Image.BICUBIC);r=r.crop(r.getbbox());return [r,r.width//2,r.height]
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
for im,qx,qy in items:at.alpha_composite(im,(qx,qy))
at.save('../build/dan_atlas.png',optimize=True);json.dump(out,open('../build/dan_anims.json','w'),separators=(',',':'))
spans=[]
for i in range(0,72):
    o=vf(2,i);a=o[...,3]>100;bx0,by0,bx1,by1=bbox(o);xs=np.where(a[by1-40:by1].any(0))[0];spans.append(xs.max()-xs.min())
print('stride',round(2*(max(spans)-min(spans))*S1*2.3/24,2))
# death frames: anchored at the shoes (lowest non-red pixels) and the cell's body centre
def anchor(c,k):
    rgb=c[...,:3].astype(int);a=c[...,3]>100;red=(rgb[...,0]>rgb[...,1]+50)
    ys,xs=np.where(a&~red);return xs
pickle.dump(DF,open('dan_death.pkl','wb'))
im=Image.new('RGBA',(1100,620),(50,50,60,255));xx=yy=0
for k,c in enumerate(DF):
    t=Image.fromarray(c,'RGBA')
    if k%4==0 and k:xx=0;yy+=200
    im.alpha_composite(t,(xx,yy));xx+=t.width+8
im.save('cut_check.png')
