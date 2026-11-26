import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900},device_scale_factor=2)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit1')
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(1)"); await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>{__dbg().p.inv=99999;__show();}")
        await pg.wait_for_timeout(900)
        await pg.evaluate("()=>__show()")
        await pg.locator('#game').screenshot(path='build/names.png')
        print(errs); await b.close()
asyncio.run(main())
