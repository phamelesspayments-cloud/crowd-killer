import sys;sys.path.insert(0,'.')
from PIL import Image
import numpy as np,json
exec(open('dan.py').read().split('def vf')[0])
def fr(i):return keyed(np.array(Image.open('../wolf/f/%03d.png'%i).convert('RGB')))
def bbox(o):
    ys,xs=np.where(o[...,3]>100);return xs.min(),ys.min(),xs.max()+1,ys.max()+1
H=62  # standing wolf height in game px (before scale)
o0=fr(68);x0,y0,x1,y1=bbox(o0);S=H/(y1-y0)
def crop(o):
    x0,y0,x1,y1=bbox(o);im=Image.fromarray(o[y0:y1,x0:x1],'RGBA').resize((round((x1-x0)*S),round((y1-y0)*S)),Image.LANCZOS)
    return [im,im.width//2,im.height]
anims={'run':[crop(fr(i)) for i in range(68,92,3)],
       'leap':[crop(fr(i)) for i in (116,120,124,130,136,144,152,158,162,166)]}
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
at.save('../build/wolf_atlas.png',optimize=True);json.dump(out,open('../build/wolf_anims.json','w'),separators=(',',':'))
bg=Image.new('RGBA',at.size,(40,40,50,255));bg.alpha_composite(at);bg.save('../wolf/check.png');print(at.size,S)
