import asyncio,base64,io
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://127.0.0.1:8765/dbg.html'); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit1')
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(2)"); await pg.wait_for_timeout(2600)
        await pg.evaluate("()=>{__hold();__setup();__kill();}")
        shots=[]
        for t in [2,10,18,30,60,120]:
            url=await pg.evaluate("(k)=>__step(k)",t if not shots else t-prev)
            prev=t;shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))))
        print(await pg.evaluate("()=>{var r=[];for(var i=0;i<6;i++){}return 1}"))
        print(errs);await b.close()
        o=Image.new('RGB',(960*2,540*3))
        for i,im in enumerate(shots):o.paste(im.convert('RGB'),((i%2)*960,(i//2)*540))
        o.resize((960,810)).save('build/deathgrid.png')
asyncio.run(main())
