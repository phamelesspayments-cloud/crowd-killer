import asyncio,base64,io
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1100,'height':900})
        await pg.goto('http://127.0.0.1:8765/dbg.html');await pg.wait_for_timeout(2500)
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(300);await pg.keyboard.press('Enter');await pg.wait_for_timeout(300)
        await pg.click('#start');await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>{__hold();__sec(4);__inv();}")
        await pg.evaluate("()=>__step(100)")
        for i in range(40):
            st=await pg.evaluate("()=>__st().A[0]")
            if st=='kevin:intro':break
            await pg.evaluate("()=>__step(2)")
        ims=[]
        for t in (25,20,25,30):
            url=await pg.evaluate("(n)=>__step(n)",t);ims.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB').crop((40,80,360,440)))
        o=Image.new('RGB',(1280,360));[o.paste(im,(i*320,0)) for i,im in enumerate(ims)];o.save('build/vomitzoom.png')
        await b.close()
asyncio.run(main())
