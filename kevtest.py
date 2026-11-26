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
        await pg.evaluate("()=>{__hold();__sec(4);__inv();}")
        shots=[]
        async def snap(n,tag):
            url=await pg.evaluate("(n)=>__step(n)",n);shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'))
            print(tag,await pg.evaluate("()=>__st()"))
        await snap(70,'banner')
        await snap(60,'vomit-start')
        await snap(22,'vomiting')
        await snap(150,'handoff')
        await snap(60,'fighting')
        await pg.evaluate("()=>{__place();}");await pg.evaluate("()=>__step(2)")
        await pg.evaluate("()=>{__knock();}");await snap(14,'knocked')
        await snap(40,'down')
        await pg.evaluate("()=>{__place();__killK(false);}");await snap(60,'light death')
        await snap(70,'light death end')
        print(errs);await b.close()
        o=Image.new('RGB',(960*3,540*3))
        for i,im in enumerate(shots[:9]):o.paste(im,((i%3)*960,(i//3)*540))
        o.resize((1920,1080)).save('build/kevgrid.png')
asyncio.run(main())
