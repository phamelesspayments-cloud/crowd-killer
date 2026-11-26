from PIL import Image
import numpy as np,json,os,pickle
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
p0=vf(1,0);px,py,ph=ref(p0);S1=G/ph
w0=vf(2,0);wx,wy,wh=ref(w0);S2=S1*609/566*566/609   # same pixel scale as the punch clip (both clips framed alike)
S2=G/ph*(609/609)
anims['walk']=[crop(vf(2,i),S1*(609/566)*(566/609),*ref(vf(2,i))[:2]) for i in range(0,34,2)]
# keep the walk frames anchored to the clip's own ground point (frame 0 feet), not per-frame feet, so the shuffle doesn't jitter
anims['walk']=[crop(vf(2,i),S1*609/566*566/609,wx,wy) for i in range(0,34,2)]
anims['act']=[crop(vf(1,i),S1,px,py) for i in (0,12,30,48,57,60,63,66,69)]
anims['hurt']=[crop(vf(1,i),S1,px,py) for i in (66,69,66,69)]
x0,y0,x1,y1=bbox(p0);gimg=Image.fromarray(p0[y0:y1,x0:x1],'RGBA').resize((round((x1-x0)*S1),round((y1-y0)*S1)),Image.LANCZOS)
def rot(a):
    r=gimg.rotate(a,expand=True,resample=Image.BICUBIC);r=r.crop(r.getbbox());return [r,r.width//2,r.height]
anims['down']=[rot(20),rot(50),rot(80),rot(90),rot(90),rot(90)]
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
at.save('../build/max_atlas.png',optimize=True);json.dump(out,open('../build/max_anims.json','w'),separators=(',',':'))
spans=[]
for i in range(0,34):
    o=vf(2,i);a=o[...,3]>100;bx0,by0,bx1,by1=bbox(o);xs=np.where(a[by1-40:by1].any(0))[0];spans.append(xs.max()-xs.min())
SPR=2.2
print('walk stride per anim frame',round(2*(max(spans)-min(spans))*S1*SPR/17,2),'spans',min(spans),max(spans))
# death sheet: 2 rows x 5, cut at the empty gaps; pieces stay with their frame
ds=keyed(np.array(Image.open('death.png').convert('RGB')),(120,45,45),20)
DF=[]
for (y0,y1),cs in (((0,268),[0,205,397,588,800,1024]),((268,572),[0,207,406,605,811,1024])):
    for ci in range(5):DF.append(ds[y0:y1,cs[ci]:cs[ci+1]].copy())
pickle.dump(DF,open('max_death.pkl','wb'))
im=Image.new('RGBA',(1100,620),(50,50,60,255));xx=yy=0
for k,c in enumerate(DF):
    t=Image.fromarray(c,'RGBA')
    if k==5:xx=0;yy=300
    im.alpha_composite(t,(xx,yy));xx+=t.width+8
im.save('cut_check.png')
