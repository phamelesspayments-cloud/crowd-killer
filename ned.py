from PIL import Image
import numpy as np,json,pickle
exec(open('../tools/dan.py').read().split('anims={}')[0])
anims={}
w0=vf(2,0);wx,wy,wh=ref(w0);S1=G/wh
anims['walk']=[crop(vf(2,i),S1,wx,wy) for i in range(0,72,3)]
g0=vf(3,0);gx,gy,gh=ref(g0);S2=G/gh
anims['act']=[crop(vf(3,i),S2,gx,gy) for i in (0,30,36,42,48,51,54,57,60,63,69)]
h0=vf(1,0);hx,hy,hh=ref(h0);SH=G/hh
anims['hurt']=[crop(vf(1,i),SH,hx,hy) for i in (30,33,36,33)]
u0=vf(4,0);ux,uy,uh=ref(u0);SU=G/uh
GUN=(18,21,24,42,27,30,45,48,51,54,57,60,63,66)
anims['gun']=[crop(vf(4,i),SU,ux,uy) for i in GUN]
# muzzle: the flash centre in clip-4 frame 27, relative to the anchor, in atlas px
o=vf(4,27);rgb=o[...,:3].astype(int);fl=(o[...,3]>100)&(rgb[...,0]>235)&(rgb[...,1]>200)&(rgb[...,2]<170)
ys,xs=np.where(fl);MZ=[round((xs.min()+4-ux)*SU),round((ys.mean()-uy)*SU)];print('muzzle',MZ,len(xs))
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
out['muzzle']=MZ
at=Image.new('RGBA',(RW,y))
for im,qx,qy in items:at.alpha_composite(im,(qx,qy))
at.save('../build/ned_atlas.png',optimize=True);json.dump(out,open('../build/ned_anims.json','w'),separators=(',',':'))
spans=[]
for i in range(0,72):
    o=vf(2,i);a=o[...,3]>100;bx0,by0,bx1,by1=bbox(o);xs=np.where(a[by1-40:by1].any(0))[0];spans.append(xs.max()-xs.min())
print('stride',round(2*(max(spans)-min(spans))*S1*1.85/24,2))
bg=Image.new('RGBA',at.size,(40,40,50,255));bg.alpha_composite(at);bg.save('atlas_check.png')
# death sheet: 5 + 4 + 4 cells
ds=keyed(np.array(Image.open('death.png').convert('RGB')),(120,45,45),15)
cells=[((0,197),[0,212,410,600,800,1024]),((197,400),[0,226,476,748,1024]),((400,572),[0,250,507,760,1024])]
DF=[]
for (r0,r1),cs in cells:
    for ci in range(len(cs)-1):
        c=ds[r0:r1,cs[ci]:cs[ci+1]].copy();DF.append(c)
pickle.dump(DF,open('ned_death.pkl','wb'))
im=Image.new('RGBA',(1200,640),(50,50,60,255));xx=yy=0
for k,c in enumerate(DF):
    t=Image.fromarray(c,'RGBA')
    if k in(5,9):xx=0;yy+=210
    im.alpha_composite(t,(xx,yy));xx+=t.width+8
im.save('cut_check.png')
