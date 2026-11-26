from PIL import Image, ImageDraw, ImageFilter
import numpy as np, json
from scipy import ndimage
im=Image.open('sheet.png').convert('RGBA');A=np.array(im)
al=A[...,3]>20
lab,n=ndimage.label(al)
cent=ndimage.center_of_mass(al,lab,range(1,n+1))
def cell(r,c):
    m=np.zeros_like(al)
    for i,(cy,cx) in enumerate(cent):
        if int(cy//50)==r and int(cx//50)==c: m|=lab==(i+1)
    return m
MAP={}
for i,ch in enumerate('0123456789'):MAP[ch]=(1,i)
MAP[':']=(1,10);MAP[';']=(1,11);MAP['?']=(1,15);MAP['!']=(0,1);MAP["'"]=(0,12)
for i,ch in enumerate('ABCDEFGHIJKLMNO'):MAP[ch]=(2,i+1)
for i,ch in enumerate('PQRSTUVWXYZ'):MAP[ch]=(3,i)
TOP=-2;H=54  # each glyph keeps its row position: rows are 50px, glyphs sit in a 54px box from the row top-2
glyphs={}
for ch,(r,c) in MAP.items():
    m=cell(r,c)
    if not m.any():
        # touching a neighbour on the sheet: cut by the 50px grid cell instead
        m=np.zeros_like(al);m[r*50:r*50+50,c*50:c*50+50]=al[r*50:r*50+50,c*50:c*50+50]
        lb,nn=ndimage.label(m)
        if nn>1:
            sz=ndimage.sum(m,lb,range(1,nn+1));keep=[i+1 for i,v in enumerate(sz) if v>40];m=np.isin(lb,keep)
        print('grid cut',ch)
    ys,xs=np.where(m);x0,x1=xs.min(),xs.max()+1
    y0=r*50+TOP
    g=np.zeros((H,x1-x0,4),np.uint8)
    sub=A[max(0,y0):y0+H,x0:x1].copy();mm=m[max(0,y0):y0+H,x0:x1]
    sub[~mm]=0
    g[max(0,-y0):max(0,-y0)+sub.shape[0]]=sub
    glyphs[ch]=Image.fromarray(g,'RGBA')
# synthesize '-' and '.' in the same style: white outline, orange-to-red fill sampled from the O
O=np.array(glyphs['O']);col=[]
for y in range(H):
    row=O[y];ok=(row[...,3]>200)&(row[...,0]>200)&(row[...,2]<120)
    col.append(tuple(int(v) for v in row[ok][:,:3].mean(0)) if ok.any() else None)
def fillcol(y):
    for d in range(H):
        for yy in (y-d,y+d):
            if 0<=yy<H and col[yy]:return col[yy]
def synth(w,box,rad):
    g=Image.new('RGBA',(w,H),(0,0,0,0));d=ImageDraw.Draw(g)
    x0,y0,x1,y1=box
    d.rounded_rectangle((x0-4,y0-4,x1+4,y1+4),rad+4,fill=(255,255,255,255))
    inner=Image.new('RGBA',(w,H),(0,0,0,0));di=ImageDraw.Draw(inner)
    mask=Image.new('L',(w,H),0);ImageDraw.Draw(mask).rounded_rectangle(box,rad,fill=255)
    grad=Image.new('RGBA',(w,H));
    for y in range(H):ImageDraw.Draw(grad).line([(0,y),(w,y)],fill=fillcol(y)+(255,))
    g.paste(grad,(0,0),mask)
    sh=Image.new('RGBA',(w,H),(0,0,0,0));
    return g
glyphs['-']=synth(30,(5,24,25,32),4)
glyphs['.']=synth(18,(5,38,13,46),4)
# pack
RW=1024;x=y=0;out={}
order=sorted(glyphs)
at=Image.new('RGBA',(RW,H*((sum(g.width+2 for g in glyphs.values())//RW)+1)))
for ch in order:
    g=glyphs[ch]
    if x+g.width>RW:x=0;y+=H
    at.alpha_composite(g,(x,y));out[ch]=[x,y,g.width,H];x+=g.width+2
at=at.crop((0,0,RW,y+H))
at.save('../build/font.png',optimize=True);json.dump(out,open('../build/font.json','w'),separators=(',',':'))
# preview
pv=Image.new('RGBA',(900,140),(30,30,40,255));px=10
for ch in 'STAGE 1-1':
    if ch==' ':px+=18;continue
    g=glyphs[ch];pv.alpha_composite(g,(px,10));px+=g.width-2
px=10
for ch in 'XI 2; MAX GERRY 22':
    if ch==' ':px+=18;continue
    g=glyphs[ch];pv.alpha_composite(g,(px,74));px+=g.width-2
pv.save('preview.png');print(at.size,len(out))
