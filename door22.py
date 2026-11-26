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
        await pg.evaluate("()=>{__hold();__sec(5);}");await pg.evaluate("()=>__step(120)")
        await pg.evaluate("()=>__toLast()");await pg.evaluate("()=>__step(60)")
        await pg.evaluate("()=>__killAll()")
        shots=[]
        for n in (30,9):
            url=await pg.evaluate("(n)=>__step(n)",n);shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'))
        print('after bosses',await pg.evaluate("()=>__ph()"))
        await pg.evaluate("()=>__px(2620)");await pg.evaluate("()=>__key('up',1)")
        for i in range(40):
            await pg.evaluate("()=>__step(5)");st=await pg.evaluate("()=>__ph()")
            if st[0]=='enter':break
        await pg.evaluate("()=>__key('up',0)")
        url=await pg.evaluate("()=>__step(25)");shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'))
        print('entering',await pg.evaluate("()=>__ph()"))
        for i in range(60):
            await pg.evaluate("()=>__step(5)");st=await pg.evaluate("()=>__ph()")
            if st[0]=='fade':break
        print('fade',st)
        await pg.evaluate("()=>__step(200)")
        print('over',await pg.locator('#over').is_visible(),await pg.locator('#over h3').text_content(),errs)
        await b.close()
        best=max(shots[:2],key=lambda im:sum(1 for px in im.crop((780,120,960,330)).getdata() if px[0]>220 and px[1]>190 and px[2]<90))
        o=Image.new('RGB',(1920,540));o.paste(best,(0,0));o.paste(shots[2],(960,0));o.resize((1440,405)).save('build/door22.png')
asyncio.run(main())
