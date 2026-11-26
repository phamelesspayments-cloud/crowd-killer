import pickle,json,os
import numpy as np
from PIL import Image
J,D,E=pickle.load(open('deathcuts.pkl','rb'))
K=pickle.load(open('kevin/kevin_death.pkl','rb'));M=pickle.load(open('max/max_death.pkl','rb'));C=pickle.load(open('chad/chad_death.pkl','rb'))
HY=pickle.load(open('hoyle/hoyle_death.pkl','rb'));GE=pickle.load(open('gerry/gerry_death.pkl','rb'));DN=pickle.load(open('dan/dan_death.pkl','rb'));NT=pickle.load(open('ned/ned_death.pkl','rb'))
TH=205
def bbox(c):
    ys,xs=np.where(c[...,3]>100);return xs.min(),ys.min(),xs.max()+1,ys.max()+1
crops={}
for k,L in {'grunt2':J,'grunt4':D,'grunt3':E,'kevin':K}.items():
    x0,y0,x1,y1=bbox(L[0]);S=TH/(y1-y0)
    a=L[0][...,3]>100;feet=np.where(a[y1-12:y1].any(0))[0];fxs=(feet.min()+feet.max())/2-x0;fw0=x1-x0
    out=[]
    for c in L:
        bx0,by0,bx1,by1=bbox(c)
        im=Image.fromarray(c[by0:by1,bx0:bx1],'RGBA').resize((max(1,round((bx1-bx0)*S)),max(1,round((by1-by0)*S))),Image.LANCZOS)
        ax=round(fxs*S) if (by1-by0)>(y1-y0)*0.8 and abs((bx1-bx0)-fw0)<fw0*0.35 else round((bx1-bx0)*S/2)
        out.append([im,ax,round((by1-by0)*S)])
    crops[k]=out
def fixed(L,TH,ground_fn):
    x0,y0,x1,y1=bbox(L[0]);S=TH/(y1-y0);a=L[0][...,3]>100;feet=np.where(a[y1-12:y1].any(0))[0];off=(feet.min()+feet.max())/2-L[0].shape[1]/2
    out=[]
    for k,c in enumerate(L):
        bx0,by0,bx1,by1=bbox(c);axc=c.shape[1]/2+off;ayc=ground_fn(k,c,by1)
        im=Image.fromarray(c[by0:by1,bx0:bx1],'RGBA').resize((max(1,round((bx1-bx0)*S)),max(1,round((by1-by0)*S))),Image.LANCZOS)
        out.append([im,round((axc-bx0)*S),round((ayc-by0)*S)])
    return out
g1=bbox(M[0])[3];g2=bbox(M[5])[3]
crops['max']=fixed(M,230,lambda k,c,by1:g1 if k<5 else max(g2,by1-4))
def shoes(k,c,by1):
    rgb=c[...,:3].astype(int);a=c[...,3]>100;dark=a&(rgb.max(2)<90)
    ys=np.where(dark.any(1))[0];return ys.max() if len(ys) else by1
crops['chad']=fixed(C,205,shoes)
hg=bbox(HY[0])[3];crops['hoyle']=fixed(HY,250,lambda k,c,by1:hg if k<5 else by1-6)
gg=bbox(GE[0])[3];crops['gerry']=fixed(GE,215,lambda k,c,by1:gg if k<5 else by1-6)
dg=bbox(DN[0])[3];crops["dan"]=fixed(DN,127,lambda k,c,by1:dg if k<10 else by1-4)

# Ned: frames 0-8 stand on his shoes (the worm pile grows behind him); 9-12 he crawls and lies down, so the
# pile is kept where it was in frame 8
def ned_crops(L,TH):
    def parts(c):
        rgb=c[...,:3].astype(int);a=c[...,3]>100;red=a&(rgb[...,0]-rgb[...,1]>110)&(rgb[...,1]<110)
        dark=a&~red&(rgb.max(2)<70);return a,red,dark
    x0,y0,x1,y1=bbox(L[0]);S=TH/(y1-y0);out=[];pile_off=None
    for k,c in enumerate(L):
        a,red,dark=parts(c);bx0,by0,bx1,by1=bbox(c)
        if k<=8:
            ys,xs=np.where(dark);gy=ys.max();sel=xs[ys>gy-14];ax=(sel.min()+sel.max())/2;ay=gy
            if k==8:ry,rx=np.where(red);pile_off=ax-(rx.min()+rx.max())/2
        else:
            ry,rx=np.where(red);ax=(rx.min()+rx.max())/2+pile_off;ay=by1-4
        im=Image.fromarray(c[by0:by1,bx0:bx1],'RGBA').resize((max(1,round((bx1-bx0)*S)),max(1,round((by1-by0)*S))),Image.LANCZOS)
        out.append([im,round((ax-bx0)*S),round((ay-by0)*S)])
    return out
crops['ned']=ned_crops(NT,200)
RW=2048;x=y=rowh=0;meta={};items=[]
for k,L in crops.items():
    meta[k]=[]
    for im,ax,ay in L:
        w,h=im.size
        if x+w>RW:x=0;y+=rowh+2;rowh=0
        items.append((im,x,y));meta[k].append([x,y,w,h,ax,ay]);x+=w+2;rowh=max(rowh,h)
    x=0;y+=rowh+2;rowh=0
at=Image.new('RGBA',(RW,y))
for im,px,py in items:at.alpha_composite(im,(px,py))
at.save('build/grunt_deaths.png',optimize=True)
SEQ={'grunt2':{'fly':[1,2,3,4],'bleed':[7,8,9],'collapse':[5,6,7,8,9]},
     'grunt4':{'fly':[1,2,3,4],'bleed':[8],'collapse':[5,6,7,8]},
     'grunt3':{'fly':[1,2,3,4],'bleed':[6,7,8],'collapse':[1,2,5,6,7,8]},
     'kevin':{'fly':[4,6,9,13],'bleed':[15,16,17,18,19],'collapse':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]},
     'max':{'fly':[1,3,5,6],'bleed':[7,8,9],'collapse':[1,2,3,4,5,6,7,8,9]},
     'chad':{'inplace':1,'fly':[5,6,7,8],'bleed':[12,13,14,15],'collapse':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]},
     'hoyle':{'inplace':1,'fly':[1,2,3,4],'bleed':[9],'collapse':[1,1,2,2,3,3,4,4,5,6,7,8,9,9]},
     'dan':{'inplace':1,'fly':[1,2,3,4],'bleed':[11],'collapse':[1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11]},
     'ned':{'inplace':1,'fly':[1,2,3,4],'bleed':[12],'collapse':[1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12]},
     'gerry':{'inplace':1,'fly':[1,2,3,4],'bleed':[9],'collapse':[1,1,2,2,3,3,4,4,5,6,7,8,9,9]}}
json.dump({'F':meta,'S':SEQ},open('build/grunt_deaths.json','w'),separators=(',',':'))
print(at.size,os.path.getsize('build/grunt_deaths.png'))
