import asyncio,sys,base64,io
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://127.0.0.1:8765/dbg.html'); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit2')
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(2)"); await pg.wait_for_timeout(2600)
        await pg.evaluate("""()=>{__hold();var d=__dbg();d.q.length=0;d.A.forEach(a=>a.state='done');
          var g=null;d.en.forEach((e,i)=>{if(e.type==='grunt'&&!g){g=e;}else{e.hp=0;e.gone=true;}});
          d.p.x=500;d.p.y=470;d.p.face=1;d.p.inv=999;d.p.state='free';
          g.x=d.p.x+70;g.y=d.p.y;g.state='walk';g.cd=999;g.inn=true;g.face=-1;}""")
        tiles=[];log=[]
        async def snap(tag):
            url=await pg.evaluate("()=>__step(2)")
            st=await pg.evaluate("()=>{var d=__dbg();return [d.p.state,d.p.tt||0,d.en.map(e=>e.state+'@'+Math.round(e.x))]}")
            log.append((tag,st));im=Image.open(io.BytesIO(base64.b64decode(url.split(',')[1])));return im,st
        await pg.evaluate("()=>document.dispatchEvent(new KeyboardEvent('keydown',{code:'ArrowRight'}))")
        for i in range(14):
            im,st=await snap('walk')
            if st[0]=='hold':break
        await pg.evaluate("()=>document.dispatchEvent(new KeyboardEvent('keyup',{code:'ArrowRight'}))")
        for i in range(8):
            im,st=await snap('hold')
            if i in (0,3,7):tiles.append(im)
        await pg.evaluate("()=>document.dispatchEvent(new KeyboardEvent('keydown',{code:'KeyL'}))")
        for i in range(24):
            im,st=await snap('throw')
            if i in (2,5,7,9,13):tiles.append(im)
        await pg.evaluate("()=>document.dispatchEvent(new KeyboardEvent('keyup',{code:'KeyL'}))")
        for l in log[::3]:print(l)
        print(errs); await b.close()
        crops=[t.crop((330,170,800,540)).resize((300,236)) for t in tiles]
        o=Image.new('RGB',(300*4,236*2));[o.paste(c,((i%4)*300,(i//4)*236)) for i,c in enumerate(crops)];o.save('build/grabgrid.png')
asyncio.run(main())
