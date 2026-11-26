import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900},device_scale_factor=2)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit1')
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(3)"); await pg.wait_for_timeout(3400)
        await pg.evaluate("()=>{var d=__dbg();d.p.inv=9999;d.p.x=470;d.p.y=372;}")
        await pg.wait_for_timeout(400)
        await pg.locator('#game').screenshot(path='build/band1.png')
        await pg.wait_for_timeout(700)
        await pg.locator('#game').screenshot(path='build/band2.png')
        print(errs); await b.close()
asyncio.run(main())
