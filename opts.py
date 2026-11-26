import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://127.0.0.1:8765/dbg.html'); await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>localStorage.clear()")
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(400)
        print('after title',await pg.evaluate("()=>__o()"))
        await pg.screenshot(path='build/opt_screen.png')
        # keyboard: difficulty right (hard), down to music and left twice, down to blood right x5
        await pg.keyboard.press('ArrowRight');await pg.keyboard.press('ArrowDown');await pg.keyboard.press('ArrowLeft');await pg.keyboard.press('ArrowLeft')
        await pg.wait_for_timeout(500)
        print('after keys',await pg.evaluate("()=>__o()"))
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(400)
        print('after enter',await pg.evaluate("()=>__o()"))
        await pg.click('#start'); await pg.wait_for_timeout(1500)
        print('in game',await pg.evaluate("()=>__o()"))
        await pg.keyboard.press('KeyP'); await pg.wait_for_timeout(200)
        print('paused',await pg.evaluate("()=>__o().music"))
        await pg.keyboard.press('KeyP')
        # blood screenshots in the bar
        await pg.evaluate("()=>__sec(2)"); await pg.wait_for_timeout(2600)
        for lv in (1,5,10):
            await pg.evaluate("(lv)=>{var o=__o().opt;o.blood=lv;__fight();}",lv)
            await pg.wait_for_timeout(200)
            for k in range(3):
                await pg.evaluate("()=>__hit()");await pg.wait_for_timeout(260)
            await pg.wait_for_timeout(150)
            await pg.locator('#game').screenshot(path='build/blood%d.png'%lv)
        print(errs);await b.close()
asyncio.run(main())
