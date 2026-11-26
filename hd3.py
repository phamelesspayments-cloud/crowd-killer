import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit1')
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(2)"); await pg.wait_for_timeout(2400)
        await pg.evaluate("()=>{__toExit();var d=__dbg();d.p.x=1250;d.p.y=470;d.p.hp=60;d.p.inv=0;}")
        await pg.wait_for_timeout(500)
        print('before',await pg.evaluate("()=>{var d=__dbg();return [d.k.map(k=>k.kind+'@'+k.x+','+k.y),Math.round(d.p.hp)]}"))
        await pg.locator('#game').screenshot(path='build/hd3.png')
        await pg.evaluate("()=>{var d=__dbg();d.p.x=1405;d.p.y=440;}")
        await pg.wait_for_timeout(300)
        print('after',await pg.evaluate("()=>{var d=__dbg();return [d.k.length,Math.round(d.p.hp)]}"))
        print(errs); await b.close()
asyncio.run(main())
