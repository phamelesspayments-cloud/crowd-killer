import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300)
        await pg.click('#start'); await pg.wait_for_timeout(2600)
        for k in ('KeyG','KeyO','KeyD'):await pg.keyboard.down(k.replace('Key',''))
        await pg.wait_for_timeout(400)
        await pg.locator('#game').screenshot(path='build/god_on.png')
        for k in ('G','O','D'):await pg.keyboard.up(k)
        await pg.wait_for_timeout(300)
        for k in ('G','O','D'):await pg.keyboard.down(k)
        await pg.wait_for_timeout(200)
        for k in ('G','O','D'):await pg.keyboard.up(k)
        await pg.wait_for_timeout(300)
        await pg.locator('#game').screenshot(path='build/god_off.png')
        print(errs);await b.close()
asyncio.run(main())
