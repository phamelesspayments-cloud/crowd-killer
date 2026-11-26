from PIL import Image
import numpy as np,json
B=json.load(open('bbox.json'))
TH=232  # Cody's standing height in game px (biggest fighter)
def key(path):
    im=np.array(Image.open(path).convert('RGB')).astype(int);r,g,b=im[...,0],im[...,1],im[...,2]
    green=(g>110)&(g-r>40)&(g-b>40)
    a=np.where(green,0,255).astype(np.uint8)
    edge=(g-np.maximum(r,b)>18)&~green;a=np.where(edge,120,a).astype(np.uint8)
    a[:4,:]=0;a[-4:,:]=0;a[:,:4]=0;a[:,-4:]=0
    return np.dstack([r,np.minimum(g,np.maximum(r,b)+6),b,a]).astype(np.uint8)
def clipscale(v):
    b=B[str(v)][0];return TH/(b[3]-b[1])
ANIMS={
 'idle':(3,list(range(0,72,3)),'ground'),
 'walk':(1,list(range(12,42))+[41,45,45,45],'ground'),
 'jab':(2,[10,12,14,16,18],'ground'),
 'hook':(2,[18,20,22,24,26],'ground'),
 'finish':(2,[26,28,30,32,34,36],'ground'),
 'heavy':(2,[44,46,48,50,52,54,56],'ground'),
 'jump':(6,list(range(21,55,3)),'air'),
 'airkick':(4,list(range(27,52,2)),'air'),
 'land':(6,[56,59,62,65],'ground'),
 'grab':(8,[18,21,24,27],'ground'),
 'hold':(8,[27,28,29,30,29,28],'ground'),
 'throw':(8,[42,45,48,50,52,54,57,60],'ground'),
 'hurt':(7,[3,5,7,9,11],'ground'),
 'fall':(7,list(range(12,34,2)),'body'),
 'down':(7,[33,36,39,42],'body'),
 'getup':(7,list(range(42,115,4)),'body'),
}
frames=[];meta={}
edges=[]
for name,(v,idx,mode) in ANIMS.items():
    S=clipscale(v);b0=B[str(v)][0]
    gx=(b0[0]+b0[2])/2;gy=b0[3]   # clip ground anchor from first (standing) frame
    hs=b0[3]-b0[1]
    lst=[]
    for i in idx:
        o=key('f%d/%03d.png'%(v,i+1));al=o[...,3]>100
        ys,xs=np.where(al);x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
        H,W=al.shape
        if x0<=5 or y0<=5 or x1>=W-5 or y1>=H-5: edges.append((name,i,int(x0),int(y0),int(x1),int(y1)))
        if mode=='air':
            bb=B[str(v)][i];ax=bb[4];ay=(bb[1]+bb[3])/2+hs/2   # head-x, hip-centred ground point
        elif mode=='body':
            ax=(x0+x1)/2;ay=y1
        else: ax,ay=gx,gy
        crop=Image.fromarray(o[y0:y1,x0:x1],'RGBA')
        w,h=round((x1-x0)*S),round((y1-y0)*S)
        crop=crop.resize((max(1,w),max(1,h)),Image.LANCZOS)
        lst.append([crop,round((ax-x0)*S),round((ay-y0)*S)])
    meta[name]=lst
# pack in rows per anim
rowsW=2048;x=y=0;rowh=0;placed={}
for name,lst in meta.items():
    placed[name]=[]
    for crop,ax,ay in lst:
        w,h=crop.size
        if x+w>rowsW:x=0;y+=rowh+2;rowh=0
        placed[name].append((x,y,w,h,ax,ay,crop));x+=w+2;rowh=max(rowh,h)
    x=0;y+=rowh+2;rowh=0
atlas=Image.new('RGBA',(rowsW,y))
out={}
for name,l in placed.items():
    out[name]=[]
    for (x,y2,w,h,ax,ay,crop) in l:
        atlas.alpha_composite(crop,(x,y2));out[name].append([x,y2,w,h,ax,ay,0,0])
atlas.save('../build/cody_atlas.png',optimize=True)
json.dump(out,open('../build/cody_anims.json','w'),separators=(',',':'))
import os;print('atlas',atlas.size,os.path.getsize('../build/cody_atlas.png'));print('edge-touching frames',edges)
