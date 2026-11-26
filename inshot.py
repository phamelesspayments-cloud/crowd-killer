import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900},device_scale_factor=2)
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit1')
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(1)"); await pg.wait_for_timeout(2600)
        await pg.evaluate("()=>{__toExit();var d=__dbg();d.p.x=2700;d.p.y=440;d.p.face=-1;d.p.inv=0;}")
        await pg.wait_for_timeout(700)
        await pg.locator('#game').screenshot(path='build/in_screen.png')
        await b.close()
asyncio.run(main())
