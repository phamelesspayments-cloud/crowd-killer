from PIL import Image
import numpy as np
from scipy import ndimage
def key(i):
    im=np.array(Image.open('vid2/f/%03d.png'%(i+1)).convert('RGB')).astype(int);r,g,b=im[...,0],im[...,1],im[...,2]
    green=(g>120)&(g-r>45)&(g-b>45)
    a=np.where(green,0,255).astype(np.uint8)
    edge=(g-np.maximum(r,b)>20)&~green;a=np.where(edge,140,a).astype(np.uint8)
    return np.dstack([r,np.minimum(g,np.maximum(r,b)+8),b,a]).astype(np.uint8)
WAIT=list(range(0,13,2));INTRO=list(range(19,50,2))
frames=[];canspr=None
for i in WAIT+INTRO:
    o=key(i);fg=o[...,3]>0
    lab,n=ndimage.label(fg)
    if n>1:
        sz=ndimage.sum(fg,lab,range(1,n+1));order=np.argsort(sz)[::-1];big=order[0]+1
        if i==31:
            k2=order[1]+1;sl=ndimage.find_objects(lab.astype(np.int32))[k2-1]
            c=o.copy();c[...,3]=np.where(lab==k2,c[...,3],0);canspr=Image.fromarray(c[sl],'RGBA')
        if i>=31: o[...,3]=np.where(lab==big,o[...,3],0)
    if 37<i<=45: o[:580,:85,3]=0
    frames.append(o)
al=np.maximum.reduce([f[...,3] for f in frames]);ys,xs=np.where(al>200)
x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
print('union',x0,y0,x1,y1,'edgeL',x0==0,'edgeR',x1>=720)
S=205/1147
fw,fh=round((x1-x0)*S),round((y1-y0)*S)
cols=8;rows=(len(frames)+cols-1)//cols
sheet=Image.new('RGBA',(fw*cols,fh*rows))
for k,f in enumerate(frames):
    sheet.alpha_composite(Image.fromarray(f[y0:y1,x0:x1],'RGBA').resize((fw,fh),Image.LANCZOS),((k%cols)*fw,(k//cols)*fh))
sheet.save('build/skin_wait.png',optimize=True)
last=frames[-1][...,3]>200;lx=np.where(last.any(0))[0];mid=(lx.min()+lx.max())/2
ax=round((mid-x0)*S);ay=round((1203-y0)*S)
cw,ch=canspr.size;canspr=canspr.resize((max(1,round(cw*S)),max(1,round(ch*S))),Image.LANCZOS);canspr.save('build/beer_can.png')
print('frame',fw,fh,'anchor',ax,ay,'n',len(frames),'release idx',len(WAIT)+INTRO.index(31),'can',canspr.size)
print('can rel',round(((18+175)/2-mid)*S),round((214-1203)*S))
v=Image.new('RGBA',(fw*6,fh),(40,40,50,255))
for j,k in enumerate([0,7,9,13,16,len(frames)-1]):
    v.alpha_composite(sheet.crop(((k%cols)*fw,(k//cols)*fh,(k%cols+1)*fw,(k//cols+1)*fh)),(j*fw,0))
v=v.resize((v.width*2,v.height*2),Image.NEAREST);v.save('build/wait_check.png')
