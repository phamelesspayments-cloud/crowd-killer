from PIL import Image
import numpy as np, json
from scipy import ndimage
A=np.array(Image.open('sheet.png').convert('RGBA'));al=A[...,3]>12
lab,n=ndimage.label(al);cent=ndimage.center_of_mass(al,lab,range(1,n+1))
CW,CH=80,77
ROWS=["ABCDEFGHIJKL","MNOPQRSTUVWX","YZabcdefghij","klmnopqrstuv","wxyz01234567","89.,;:?!-#\"'","&()[]`\\/@~°+","=*$<>%"]
glyphs={}
for r,row in enumerate(ROWS):
    for c,ch in enumerate(row):
        m=np.zeros_like(al)
        for i,(cy,cx) in enumerate(cent):
            if int(cy//CH)==r and int(cx//CW)==c: m|=lab==(i+1)
        if not m.any():print('missing',ch);continue
        ys,xs=np.where(m);x0,x1=xs.min(),xs.max()+1
        g=np.zeros((CH,x1-x0,4),np.uint8);sub=A[r*CH:r*CH+CH,x0:x1].copy();mm=m[r*CH:r*CH+CH,x0:x1];sub[~mm]=0
        g[:sub.shape[0]]=sub;glyphs[ch]=Image.fromarray(g,'RGBA')
del glyphs['@'];del glyphs['~']   # the (c) and lightbulb symbols
RW=1024;x=y=0;out={}
for ch in sorted(glyphs):
    g=glyphs[ch]
    if x+g.width>RW:x=0;y+=CH
    out[ch]=[x,y,g.width];x+=g.width+2
at=Image.new('RGBA',(RW,y+CH))
for ch,(gx,gy,w) in out.items():at.alpha_composite(glyphs[ch],(gx,gy))
at.save('../build/font2.png',optimize=True);json.dump(out,open('../build/font2.json','w'),separators=(',',':'))
pv=Image.new('RGBA',(1000,170),(30,30,40,255))
for li,line in enumerate(['SCORE 12,345 Lives x3','Leather jacket, cool head! 50% (ok)?']):
    px=10
    for ch in line:
        if ch==' ':px+=22;continue
        g=glyphs.get(ch)
        if g is None:continue
        pv.alpha_composite(g,(px,8+li*80));px+=g.width-6
pv.save('preview.png');print(at.size,len(out))
