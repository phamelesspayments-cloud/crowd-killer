import asyncio,sys
from playwright.async_api import async_playwright
async def main(url,out,mobile):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(**(p.devices['iPhone 13'] if mobile else {'viewport':{'width':1100,'height':700}}))
        pg=await ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append('console:'+m.text) if m.type=='error' else None)
        pg.on('requestfailed',lambda r:errs.append('FAIL '+r.url[-40:]))
        await pg.goto(url);await pg.wait_for_timeout(3000)
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(400);await pg.keyboard.press('Enter');await pg.wait_for_timeout(400)
        try: await pg.click('#start',timeout=3000)
        except Exception as e: errs.append('nostart')
        await pg.wait_for_timeout(4000);await pg.screenshot(path=out)
        print(errs[:10]);await b.close()
asyncio.run(main(sys.argv[1],sys.argv[2],len(sys.argv)>3))
