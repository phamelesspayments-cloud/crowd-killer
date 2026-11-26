from PIL import Image
import numpy as np,glob,json,os
def key(path):
    im=np.array(Image.open(path).convert('RGB')).astype(int);r,g,b=im[...,0],im[...,1],im[...,2]
    green=(g>100)&(g-r>28)&(g-b>45)
    a=np.where(green,0,255).astype(np.uint8)
    edge=(g-np.maximum(r,b)>14)&~green;a=np.where(edge,110,a).astype(np.uint8)
    a[:3,:]=0;a[-3:,:]=0;a[:,:3]=0;a[:,-3:]=0
    return np.dstack([r,np.minimum(g,np.maximum(r,b)+6),b,a]).astype(np.uint8)
out={}
for v in 'ab':
    fs=sorted(glob.glob('f%s/*.png'%v));fr=[key(f) for f in fs]
    al=np.maximum.reduce([f[...,3] for f in fr]);ys,xs=np.where(al>150)
    x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
    H=y1-y0;S=190/H
    fw,fh=round((x1-x0)*S),round(H*S)
    cols=6;rows=(len(fr)+cols-1)//cols
    sh=Image.new('RGBA',(fw*cols,fh*rows))
    for k,f in enumerate(fr):sh.alpha_composite(Image.fromarray(f[y0:y1,x0:x1],'RGBA').resize((fw,fh),Image.LANCZOS),((k%cols)*fw,(k//cols)*fh))
    sh.save('../build/bar_crowd_%s.png'%v,optimize=True)
    d0=np.abs(fr[0][...,:3].astype(int)-fr[-1][...,:3].astype(int)).mean()
    out[v]=dict(fw=fw,fh=fh,n=len(fr),cols=cols)
    print(v,'bbox',x0,y0,x1,y1,'frame',fw,fh,'n',len(fr),'loop diff first/last',round(d0,2),'bytes',os.path.getsize('../build/bar_crowd_%s.png'%v))
    v2=Image.new('RGBA',(fw,fh),(70,120,170,255));v2.alpha_composite(sh.crop((0,0,fw,fh)));v2.save('../build/crowd_check_%s.png'%v)
json.dump(out,open('crowd.json','w'))
