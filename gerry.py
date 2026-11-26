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
w0=vf(2,0);wx,wy,wh=ref(w0);S=G/wh   # walk clip sets the scale; the jump clip is framed the same way
j0=vf(1,0);jx,jy,jh=ref(j0);SJ=S*wh/615*615/wh*(615/539)*(539/615)  # both clips show him the same size
SJ=G/jh*(jh/539)*(539/615)*(615/wh)*(wh/615)
SJ=G/jh   # the jump clip frames him smaller, so scale it up to match his walking height
anims['walk']=[crop(vf(2,i),S,wx,wy) for i in range(0,72,3)]
anims['act']=[crop(j0,SJ,jx,jy)]
anims['crouch']=[crop(vf(1,i),SJ,jx,jy) for i in (3,6,9,12)]
# airborne frames: anchored at their own lowest point so the game's jump arc supplies the height
def air(i):
    o=vf(1,i);x0,y0,x1,y1=bbox(o);return crop(o,SJ,jx,y1)
anims['jump']=[air(i) for i in (15,18,21,24,27,30,33,36,39,42)]
anims['slide']=[crop(vf(1,i),SJ,jx,jy) for i in (45,48,51,54,57,60,63,66,69)]
ds=keyed(np.array(Image.open('death.png').convert('RGB')),(120,45,45),15)
DF=[]
for (y0,y1),cs in (((0,270),[0,187,390,612,808,1024]),((270,572),[0,195,400,605,815,1024])):
    for ci in range(5):DF.append(ds[y0:y1,cs[ci]:cs[ci+1]].copy())
dx,dy,dh=ref(DF[0]);SD=G/dh
anims['hurt']=[crop(DF[1],SD,*ref(DF[1])[:2]),crop(vf(1,6),SJ,jx,jy),crop(DF[1],SD,*ref(DF[1])[:2]),crop(vf(1,6),SJ,jx,jy)]
x0,y0,x1,y1=bbox(j0);gimg=Image.fromarray(j0[y0:y1,x0:x1],'RGBA').resize((round((x1-x0)*SJ),round((y1-y0)*SJ)),Image.LANCZOS)
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
at.save('../build/gerry_atlas.png',optimize=True);json.dump(out,open('../build/gerry_anims.json','w'),separators=(',',':'))
pickle.dump(DF,open('gerry_death.pkl','wb'))
im=Image.new('RGBA',(1100,620),(50,50,60,255));xx=yy=0
for k,c in enumerate(DF):
    t=Image.fromarray(c,'RGBA')
    if k==5:xx=0;yy=300
    im.alpha_composite(t,(xx,yy));xx+=t.width+8
im.save('cut_check.png')
print('SJ',SJ,'S',S,{k:len(v) for k,v in out.items()})
