import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300)
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(2)"); await pg.wait_for_timeout(2600)
        await pg.evaluate("()=>{__hold();__setup();__kill();}")
        out=[]
        for i in range(12):out.append((i*20+20,await pg.evaluate("()=>__step(20)")))
        print(out,errs);await b.close()
asyncio.run(main())
