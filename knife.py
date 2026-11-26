import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(600)
        await pg.keyboard.press('Enter'); await pg.click('#start'); await pg.wait_for_timeout(300)
        await pg.evaluate("()=>{__cam(1908);var d=__dbg();d.p.x=d.c.x-110;d.p.y=d.c.y;d.p.face=1;}")
        await pg.wait_for_timeout(200)
        await pg.keyboard.press('KeyJ'); await pg.wait_for_timeout(500)
        await pg.keyboard.press('KeyJ'); await pg.wait_for_timeout(600)
        print('items',await pg.evaluate("()=>__dbg().it.map(i=>[i.type,Math.round(i.x),Math.round(i.y)])"))
        await pg.evaluate("()=>{var d=__dbg();var k=d.it[0];d.p.x=k.x;d.p.y=k.y;}")
        await pg.wait_for_timeout(200)
        print('weapon',await pg.evaluate("()=>__dbg().p.weapon"))
        await pg.locator('#game').screenshot(path='build/k0.png')
        # wait for enemies, face the nearest, throw
        await pg.wait_for_timeout(2500)
        await pg.evaluate("()=>{var d=__dbg();var e=d.en.filter(e=>e.hp>0)[0];if(e){d.p.y=e.y;d.p.face=e.x>d.p.x?1:-1;}}")
        before=await pg.evaluate("()=>__dbg().en.filter(e=>e.hp>0).length")
        await pg.keyboard.press('KeyJ'); await pg.wait_for_timeout(120)
        await pg.locator('#game').screenshot(path='build/k1.png')
        await pg.wait_for_timeout(900)
        after=await pg.evaluate("()=>__dbg().en.filter(e=>e.hp>0).length")
        print('alive before/after',before,after)
        await pg.locator('#game').screenshot(path='build/k2.png')
        print(errs); await b.close()
asyncio.run(main())
