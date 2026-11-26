import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit3')
        await pg.click('#start'); await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>__sec(1)"); await pg.wait_for_timeout(3000)
        await pg.evaluate("()=>{enemies.length=0;}") if False else None
        await pg.evaluate("()=>__toExit()")
        await pg.evaluate("()=>{var d=__dbg();d.p.x=2700;d.p.y=500;}")
        await pg.keyboard.down('ArrowRight'); await pg.wait_for_timeout(900); await pg.keyboard.up('ArrowRight')
        st=await pg.evaluate("()=>{var d=__dbg();return [d.ph,Math.round(d.p.x),Math.round(d.p.y),Math.round(d.cam)]}");print('blocked by fg can?',st)
        await pg.locator('#game').screenshot(path='build/e0.png')
        await pg.evaluate("()=>{var d=__dbg();d.p.y=330;d.p.x=2600;}")
        await pg.keyboard.down('ArrowRight'); await pg.wait_for_timeout(900); await pg.keyboard.up('ArrowRight')
        print('blocked by barrier?',await pg.evaluate("()=>{var d=__dbg();return [Math.round(d.p.x),Math.round(d.p.y)]}"))
        await pg.evaluate("()=>{var d=__dbg();d.p.y=430;}")
        await pg.keyboard.down('ArrowRight'); await pg.wait_for_timeout(2400); await pg.keyboard.up('ArrowRight')
        await pg.wait_for_timeout(2200)
        print('over visible',await pg.locator('#over').is_visible(),await pg.locator('#over h3').text_content(),await pg.locator('#r-wave').text_content())
        print(errs); await b.close()
asyncio.run(main())
