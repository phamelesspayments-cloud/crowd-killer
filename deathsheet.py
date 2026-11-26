from PIL import Image,ImageDraw
import numpy as np,json,sys
from scipy import ndimage
def keyed(path):
    im=np.array(Image.open(path).convert('RGB')).astype(int);r,g,b=im[...,0],im[...,1],im[...,2]
    green=(g>120)&(g-r>40)&(g-b>40)
    a=np.where(green,0,255).astype(np.uint8);edge=(g-np.maximum(r,b)>18)&~green;a=np.where(edge,120,a).astype(np.uint8)
    return np.dstack([r,np.minimum(g,np.maximum(r,b)+6),b,a]).astype(np.uint8)
def cut(o,ysplit,cols):
    out=[]
    for ri,(y0,y1) in enumerate(ysplit):
        cs=cols[ri]
        for ci in range(len(cs)-1):
            c=o[y0:y1,cs[ci]:cs[ci+1]].copy();out.append(c)
    return out
def clean(c,minsz=30):
    m=c[...,3]>100;lab,n=ndimage.label(m)
    if n:
        sz=ndimage.sum(m,lab,range(1,n+1));keep=np.isin(lab,[i+1 for i in range(n) if sz[i]>=minsz]);c[...,3]=np.where(keep,c[...,3],0)
    return c
def erase_eyeballs(c,body_min=4000):
    """remove loose eyeballs: white blobs with an iris, plus anything not attached to the body that contains one"""
    rgb=c[...,:3].astype(int);al=c[...,3]>100
    white=al&(rgb.min(2)>185)
    lab,n=ndimage.label(white);hits=[]
    for i in range(1,n+1):
        ys,xs=np.where(lab==i)
        if len(xs)<18:continue
        w=xs.max()-xs.min()+1;h=ys.max()-ys.min()+1
        if w>40 or h>40:continue
        cx,cy=xs.mean(),ys.mean();R=max(w,h)*0.95+5
        Y,X=np.ogrid[:c.shape[0],:c.shape[1]];c[...,3]=np.where((X-cx)**2+(Y-cy)**2<=R*R,0,c[...,3]);hits.append((int(cx),int(cy),int(R)))
    # the trailing red streak left behind by a removed eyeball: drop small loose bits again
    return clean(c,60),hits
