import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://127.0.0.1:8765/dbg.html');await pg.wait_for_timeout(2500)
        print('loaded',errs,flush=True)
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(300);await pg.keyboard.press('Enter');await pg.wait_for_timeout(300)
        await pg.click('#start',timeout=5000);await pg.wait_for_timeout(1500)
        print('started',flush=True)
        await pg.evaluate("()=>{__hold();__sec(7);}");print('sec',await pg.evaluate("()=>__dst()"),flush=True)
        await pg.evaluate("()=>{for(var i=0;i<150;i++){mode='play';}}")
        print(await pg.evaluate("()=>{__step(10);return __dst()}"),flush=True)
        await b.close()
asyncio.run(main())
