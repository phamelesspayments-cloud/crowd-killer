from PIL import Image
import numpy as np,json,glob,os
from scipy import ndimage
TH=244   # Nicky's standing height in game px
def keyarr(im,thr=(120,45,45)):
    im=np.array(im.convert('RGB')).astype(int);r,g,b=im[...,0],im[...,1],im[...,2]
    green=(g>thr[0])&(g-r>thr[1])&(g-b>thr[2])
    a=np.where(green,0,255).astype(np.uint8)
    edge=(g-np.maximum(r,b)>18)&~green;a=np.where(edge,120,a).astype(np.uint8)
    return np.dstack([r,np.minimum(g,np.maximum(r,b)+6),b,a]).astype(np.uint8)
def clean(o):
    a=o[...,3]>100;lab,n=ndimage.label(a)
    if n>1:
        sz=ndimage.sum(a,lab,range(1,n+1));keep=np.isin(lab,[i+1 for i in range(n) if sz[i]>=40])
        o[...,3]=np.where(keep,o[...,3],0)
    o[:3,:,3]=0;o[-3:,:,3]=0;o[:,:3,3]=0;o[:,-3:,3]=0
    return o
def bbox(o):
    ys,xs=np.where(o[...,3]>100);return xs.min(),ys.min(),xs.max()+1,ys.max()+1
edges=[]
def vframes(v,idx,mode='ground',S=None,ref=None):
    out=[]
    for i in idx:
        o=clean(keyarr(Image.open('f%d/%03d.png'%(v,i+1))));x0,y0,x1,y1=bbox(o)
        if x0<=4 or x1>=o.shape[1]-4 or y0<=4 or y1>=o.shape[0]-4:edges.append((v,i,int(x0),int(y0),int(x1),int(y1)))
        gx,gy=ref
        crop=Image.fromarray(o[y0:y1,x0:x1],'RGBA').resize((max(1,round((x1-x0)*S)),max(1,round((y1-y0)*S))),Image.LANCZOS)
        out.append([crop,round((gx-x0)*S),round((gy-y0)*S)])
    return out
def clipref(v):
    o=clean(keyarr(Image.open('f%d/001.png'%v)));x0,y0,x1,y1=bbox(o)
    a=o[...,3]>100;feet=np.where(a[y1-12:y1].any(0))[0]
    return TH/(y1-y0),((feet.min()+feet.max())/2,y1)
anims={}
for v in (1,2,3):
    S,ref=clipref(v)
    if v==1:
        anims['idle']=vframes(1,list(range(0,23,2)),S=S,ref=ref)
        anims['charge']=vframes(1,list(range(24,53,2)),S=S,ref=ref)
        anims['windup']=vframes(1,list(range(54,77,2)),S=S,ref=ref)
        anims['punch']=vframes(1,list(range(78,107,2)),S=S,ref=ref)
    if v==2: anims['walk']=vframes(2,list(range(0,72,2)),S=S,ref=ref)
    if v==3:
        anims['guard']=vframes(3,list(range(0,21,4)),S=S,ref=ref)
        anims['lunge']=vframes(3,list(range(24,51,2)),S=S,ref=ref)
# decapitation body sheet: each frame cut from its own blob (frames overlap the grid), anchored to its grid column
bs=Image.open('body_sheet.png');bo=keyarr(bs);CW=1024/5
A0=bo[...,3]>100;labB,nB=ndimage.label(ndimage.binary_dilation(A0,iterations=3));objB=ndimage.find_objects(labB);szB=ndimage.sum(A0,labB,range(1,nB+1))
blobs=[(k+1,o) for k,(o,sz) in enumerate(zip(objB,szB)) if sz>800]
headblob=[b for b in blobs if (b[1][1].stop-b[1][1].start)<80 and (b[1][0].stop-b[1][0].start)<80][0]
blobs=[b for b in blobs if b is not headblob]
blobs.sort(key=lambda b:(0 if b[1][0].stop<300 else 1,b[1][1].start))
body=[];bodyS=[]
for k,(lid,o) in enumerate(blobs):
    m=(labB==lid)&A0;c=bo.copy();c[...,3]=np.where(m,c[...,3],0)
    bx0,by0,bx1,by1=bbox(c);col=k%5
    if k==0:
        y1=by1;KB=TH/(by1-by0);feet=np.where(m[by1-12:by1].any(0))[0];FX=(feet.min()+feet.max())/2-col*CW
    gx=col*CW+FX;gy=by1
    if k==2:
        hl=headblob[0];ys,xs=np.where((labB==hl)&A0);headpos=[float(xs.mean()-gx),float(ys.mean()-gy)]
    crop=Image.fromarray(c[by0:by1,bx0:bx1],'RGBA').resize((round((bx1-bx0)*KB),round((by1-by0)*KB)),Image.LANCZOS)
    body.append([crop,round((gx-bx0)*KB),round((gy-by0)*KB)])
    bodyS.append((c[by0:by1,bx0:bx1],gx-bx0,gy-by0))
import pickle;pickle.dump([(b[0].shape,b[1],b[2]) for b in bodyS],open('bodyS.pkl','wb'))
for k,(arr,ax,ay) in enumerate(bodyS):Image.fromarray(arr,'RGBA').save('bodyf%d.png'%k)
neck=json.load(open('neck_manual.json')) if os.path.exists('neck_manual.json') else [None]*10
anims['hurt']=body[0:2];anims['decap']=body
# head sheet: 4 rows x 5, frames 0-17, fixed cells so the burst stays centred
hs=Image.open('head_sheet.png');ho=keyarr(hs);HCW=1024/5;HCH=143
h0=ho[0:HCH,0:int(HCW)];hx0,hy0,hx1,hy1=bbox(h0)
headH=(hy1-hy0)
# head in the body sheet is ~ 55px tall at 1024 scale -> match it
HK=(58*KB)/headH
heads=[]
for k in range(18):
    cx0=int(round((k%5)*HCW));cy0=(k//5)*HCH;c=clean(ho[cy0:cy0+HCH,cx0:int(round(cx0+HCW))].copy())
    if (c[...,3]>100).sum()<30: continue
    bx0,by0,bx1,by1=bbox(c);ccx=(hx0+hx1)/2;ccy=(hy0+hy1)/2
    crop=Image.fromarray(c[by0:by1,bx0:bx1],'RGBA').resize((max(1,round((bx1-bx0)*HK)),max(1,round((by1-by0)*HK))),Image.LANCZOS)
    heads.append([crop,round((ccx-bx0)*HK),round((ccy-by0)*HK)])
anims['head']=heads
# pack
RW=2048;x=y=rowh=0;placed={}
for name,lst in anims.items():
    placed[name]=[]
    for crop,ax,ay in lst:
        w,h=crop.size
        if x+w>RW:x=0;y+=rowh+2;rowh=0
        placed[name].append((x,y,w,h,ax,ay,crop));x+=w+2;rowh=max(rowh,h)
    x=0;y+=rowh+2;rowh=0
atlas=Image.new('RGBA',(RW,y))
out={}
for name,l in placed.items():
    out[name]=[]
    for (px,py,w,h,ax,ay,crop) in l:atlas.alpha_composite(crop,(px,py));out[name].append([px,py,w,h,ax,ay,0,0])
atlas.save('../build/nicky_atlas.png',optimize=True)
json.dump({'A':out,'neck':neck,'headpos':[round(headpos[0]*KB),round(headpos[1]*KB)],'KB':KB,'headH':round(58*KB)},open('../build/nicky_anims.json','w'),separators=(',',':'))
print('atlas',atlas.size,os.path.getsize('../build/nicky_atlas.png'));print('edges',edges);print('neck',neck);print('headpos',headpos,KB)
print({k:len(v) for k,v in anims.items()})
