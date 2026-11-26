import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(600)
        await pg.keyboard.press('Enter'); await pg.click('#start'); await pg.wait_for_timeout(300)
        await pg.evaluate("()=>{__cam(1488);var d=__dbg();d.p.x=d.c.x-110;d.p.y=d.c.y;d.p.face=1;}")
        await pg.wait_for_timeout(200)
        await pg.locator('#game').screenshot(path='build/d0.png')
        await pg.keyboard.press('KeyJ'); await pg.wait_for_timeout(600)
        await pg.locator('#game').screenshot(path='build/d1.png')
        await pg.keyboard.press('KeyJ'); await pg.wait_for_timeout(250)
        await pg.locator('#game').screenshot(path='build/d2.png')
        await pg.wait_for_timeout(1400)
        await pg.locator('#game').screenshot(path='build/d3.png')
        print(await pg.evaluate("()=>{var d=__dbg();return [d.c.hits,d.c.broken,d.k.length,d.k[0]&&d.k[0].kind]}"))
        print(errs); await b.close()
asyncio.run(main())
