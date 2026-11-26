from PIL import Image
import numpy as np,glob,sys,json
res={}
for i in range(1,7):
    out=[]
    for f in sorted(glob.glob('f%d/*.png'%i)):
        im=np.array(Image.open(f).convert('RGB')).astype(int);r,g,b=im[...,0],im[...,1],im[...,2]
        fg=~((g>110)&(g-r>40)&(g-b>40))
        # drop thin border noise
        fg[:4,:]=False;fg[-4:,:]=False;fg[:,:4]=False;fg[:,-4:]=False
        ys,xs=np.where(fg)
        top=ys.min();rows=np.where(fg[top:top+40].any(0))[0]
        out.append([int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()),int(rows.mean())])
    res[i]=out
json.dump(res,open('bbox.json','w'))
for i in res:
    b=res[i];print(i,len(b),'h0',b[0][3]-b[0][1],'bottoms',[x[3] for x in b[::3]])
