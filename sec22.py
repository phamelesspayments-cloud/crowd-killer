import asyncio,base64,io
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://127.0.0.1:8765/dbg.html');await pg.wait_for_timeout(2500)
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(300);await pg.keyboard.press('Enter');await pg.wait_for_timeout(300)
        await pg.click('#start');await pg.wait_for_timeout(1500)
        shots=[]
        async def snap(n):
            url=await pg.evaluate("(n)=>__step(n)",n);shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'))
        await pg.evaluate("()=>{__hold();__sec(4);__inv();}");await pg.evaluate("()=>__step(140)")
        await pg.evaluate("()=>__end21()");await pg.evaluate("()=>__key('left',1)");await pg.evaluate("()=>__step(40)");await pg.evaluate("()=>__key('left',0)")
        await pg.evaluate("()=>__step(130)")
        print('2-2 loaded',await pg.evaluate("()=>__st()"))
        await snap(50)
        await snap(150)
        print('first fight',await pg.evaluate("()=>__st()"))
        await pg.evaluate("()=>{__inv();__clear();}");await pg.evaluate("()=>__step(5)")
        await pg.evaluate("()=>__key('right',1)")
        for k in range(3):
            for i in range(120):
                await pg.evaluate("()=>__step(10)");st=await pg.evaluate("()=>__st()")
                if st['ph'] in ('fight','fade'):break
            print('step',k,st)
            if st['ph']=='fight':
                await snap(1);await pg.evaluate("()=>{__clear();}")
            if st['ph']=='fade':break
        await pg.evaluate("()=>__key('right',0)")
        print(errs);await b.close()
        o=Image.new('RGB',(960*2,540*2))
        for i,im in enumerate(shots[:4]):o.paste(im,((i%2)*960,(i//2)*540))
        o.resize((1440,810)).save('build/sec22grid.png')
asyncio.run(main())
