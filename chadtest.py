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
        await pg.evaluate("()=>{__hold();__sec(4);}");await pg.evaluate("()=>__step(100)")
        print('2-1 opening',await pg.evaluate("()=>__ens()"))
        print('2-1 grunt mix',await pg.evaluate("()=>__skins()"))
        shots=[];log=[]
        async def snap(n,tag):
            url=await pg.evaluate("(n)=>__step(n)",n);shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'));log.append((tag,await pg.evaluate("()=>__cst()")))
        await pg.evaluate("()=>__setupC()")
        await snap(25,'walk')
        for i in range(80):
            await pg.evaluate("()=>__step(2)");st=await pg.evaluate("()=>__cst()")
            if st[0]=='attack':await snap(4,'swing');break
        await snap(30,'after')
        await pg.evaluate("()=>{__pinv();__killC(false);}");await snap(30,'death a');await snap(30,'death b');await snap(40,'death c')
        for l in log:print(l)
        await pg.evaluate("()=>{__sec(1);}");await pg.evaluate("()=>__step(5)")
        print('1-2 grunt mix (James stays)',await pg.evaluate("()=>__skins()"))
        print(errs);await b.close()
        o=Image.new('RGB',(960*3,540*2))
        for i,im in enumerate(shots[:6]):o.paste(im,((i%3)*960,(i//3)*540))
        o.resize((1920,720)).save('build/chadgrid.png')
asyncio.run(main())
