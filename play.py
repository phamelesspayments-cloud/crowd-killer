import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(600)
        await pg.keyboard.press('Enter'); await pg.click('#start'); await pg.wait_for_timeout(2000)
        n=0
        for i in range(500):
            await pg.keyboard.down('ArrowRight'); await pg.wait_for_timeout(60); await pg.keyboard.up('ArrowRight')
            d='ArrowUp' if (i//15)%2 else 'ArrowDown'
            await pg.keyboard.down(d); await pg.wait_for_timeout(30); await pg.keyboard.up(d)
            await pg.keyboard.press('KeyJ'); await pg.wait_for_timeout(60)
            if i%60==0:
                await pg.locator('#game').screenshot(path='build/p%02d.png'%n);n+=1
            if await pg.locator('#over').is_visible():
                print('over at',i,await pg.locator('#over h3').text_content()); break
        await pg.locator('.stage').screenshot(path='build/pend.png')
        print('errors',errs)
        await b.close()
asyncio.run(main())
