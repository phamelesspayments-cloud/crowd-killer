import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':1000})
        errs=[];fails=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.on('requestfailed',lambda r:fails.append(r.url[:60]))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(4000)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(400); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(500)
        await pg.screenshot(path='export/t_select.png')
        await pg.select_option('#testsec','3'); await pg.check('#testgod')
        await pg.keyboard.press('Digit2'); await pg.click('#start'); await pg.wait_for_timeout(4200)
        await pg.locator('#game').screenshot(path='export/t_14.png')
        imgs=await pg.evaluate("()=>{var n=0,bad=0;document.querySelectorAll('img').forEach(i=>{n++;if(!i.complete||!i.naturalWidth)bad++});return [n,bad]}")
        print('dom imgs',imgs,'failed requests',fails,'errors',errs)
        await b.close()
asyncio.run(main())
