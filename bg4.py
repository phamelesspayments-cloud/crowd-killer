import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900},device_scale_factor=2)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit3')
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(3)"); await pg.wait_for_timeout(3400)
        await pg.evaluate("()=>{var d=__dbg();d.p.inv=0;d.en.forEach(e=>{e.hp=0;e.gone=true;});__at(330,385);}")
        await pg.wait_for_timeout(250)
        await pg.locator('#game').screenshot(path='build/bg4a.png')
        await pg.evaluate("()=>{__at(330,440);}")
        await pg.wait_for_timeout(250)
        await pg.locator('#game').screenshot(path='build/bg4b.png')
        print(errs); await b.close()
asyncio.run(main())
