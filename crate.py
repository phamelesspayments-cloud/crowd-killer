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
        await pg.evaluate("()=>{__hold();__sec(4);}");await pg.evaluate("()=>__step(130)")
        print(await pg.evaluate("()=>__goCrate()"))
        shots=[]
        async def snap(n):
            url=await pg.evaluate("(n)=>__step(n)",n);shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'))
        await snap(3)
        await pg.evaluate("()=>__hitC()");await snap(20)
        await pg.evaluate("()=>__hitC()");await snap(30)
        print('after break',await pg.evaluate("()=>__pk()"))
        await pg.evaluate("()=>__grab()");await snap(15)
        print('after grab',await pg.evaluate("()=>__pk()"),errs)
        await b.close()
        o=Image.new('RGB',(960*2,540*2))
        for i,im in enumerate(shots):o.paste(im,((i%2)*960,(i//2)*540))
        o.resize((1440,810)).save('build/crategrid.png')
asyncio.run(main())
