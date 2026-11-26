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
        await pg.evaluate("()=>{__hold();__sec(6);__inv();}");await snap(130)
        print('start',await pg.evaluate("()=>__st()"))
        await pg.evaluate("()=>__key('right',1)")
        for i in range(30):
            await pg.evaluate("()=>__step(5)");st=await pg.evaluate("()=>__st()")
            if st['px']>300:break
        print('down stairs',st);await snap(1)
        await pg.evaluate("()=>__step(40)");print('landing',await pg.evaluate("()=>__st()"))
        await pg.evaluate("()=>__key('right',0)");await snap(30)
        await pg.evaluate("()=>__killAll()");await snap(20)
        print('cleared',await pg.evaluate("()=>__st()"))
        # walk to the lower flight and down to the door
        await pg.evaluate("()=>__key('down',1)");await pg.evaluate("()=>__step(40)");await pg.evaluate("()=>__key('down',0)")
        await pg.evaluate("()=>__key('left',1)")
        for i in range(80):
            await pg.evaluate("()=>__step(5)");st=await pg.evaluate("()=>__st()")
            if st['ph']=='enter':break
        await pg.evaluate("()=>__key('left',0)")
        print('door',st);await snap(1)
        await pg.evaluate("()=>__step(30)");await snap(1)
        await pg.evaluate("()=>__step(250)")
        print('over',await pg.locator('#over').is_visible(),await pg.locator('#over h3').text_content(),errs)
        await b.close()
        o=Image.new('RGB',(960*3,540*2))
        for i,im in enumerate(shots[:6]):o.paste(im,((i%3)*960,(i//3)*540))
        o.resize((1920,720)).save('build/sec23grid.png')
asyncio.run(main())
