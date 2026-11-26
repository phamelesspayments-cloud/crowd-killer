import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page()
        await pg.goto('http://127.0.0.1:8765/dbg.html');await pg.wait_for_timeout(3000)
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(400);await pg.keyboard.press('Enter');await pg.wait_for_timeout(400)
        await pg.click('#start');await pg.wait_for_timeout(2000)
        print(await pg.evaluate("()=>__ev('[SEC.name,!!bg,!!SEC.bg,SEC.bg&&SEC.bg.width,WORLD,SECTIONS.map(function(q){return q.name+\":\"+(q.bg?q.bg.width:\"-\")}).join(\" \")]')"))
        await b.close()
asyncio.run(main())
