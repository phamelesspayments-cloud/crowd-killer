import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1100,'height':900})
        await pg.goto('http://127.0.0.1:8765/dbg.html');await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(300);await pg.keyboard.press('Enter');await pg.wait_for_timeout(300)
        await pg.click('#start');await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(2)");await pg.wait_for_timeout(2600)
        await pg.evaluate("()=>{__o().opt.blood=10;__fight();}");await pg.wait_for_timeout(200)
        for k in range(2):
            await pg.evaluate("()=>__hit()");await pg.wait_for_timeout(330)
        await pg.evaluate("()=>__hit()");await pg.wait_for_timeout(90)
        await pg.locator('#game').screenshot(path='build/blood10b.png')
        await b.close()
asyncio.run(main())
