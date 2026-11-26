import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(600)
        await pg.keyboard.press('Enter'); await pg.click('#start'); await pg.wait_for_timeout(1500)
        await pg.keyboard.down('ArrowRight'); await pg.wait_for_timeout(3600); await pg.keyboard.up('ArrowRight')
        await pg.keyboard.down('ArrowUp'); await pg.wait_for_timeout(1500); await pg.keyboard.up('ArrowUp')
        await pg.keyboard.down('ArrowRight'); await pg.wait_for_timeout(1500); await pg.keyboard.up('ArrowRight')
        await pg.locator('#game').screenshot(path='build/c0.png')
        await pg.keyboard.press('KeyJ'); await pg.wait_for_timeout(500)
        await pg.locator('#game').screenshot(path='build/c1.png')
        await pg.keyboard.press('KeyJ'); await pg.wait_for_timeout(380)
        await pg.locator('#game').screenshot(path='build/c2.png')
        await pg.wait_for_timeout(1200)
        await pg.locator('#game').screenshot(path='build/c3.png')
        print(errs); await b.close()
asyncio.run(main())
