import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(600)
        await pg.keyboard.press('Enter'); await pg.click('#start'); await pg.wait_for_timeout(300)
        await pg.evaluate("()=>{__cam(1908);var d=__dbg();d.p.weapon={type:'knife',uses:1};d.p.x=2000;d.p.y=420;d.p.face=1;}")
        await pg.wait_for_timeout(6000)
        st=await pg.evaluate("()=>{var d=__dbg();var e=d.en.filter(e=>e.hp>0&&e.inn).sort((a,b)=>Math.abs(a.x-d.p.x)-Math.abs(b.x-d.p.x))[0];if(e){d.p.y=e.y;d.p.face=e.x>d.p.x?1:-1;d.p.inv=200;}return [d.p.state,e&&e.type,e&&Math.round(e.x-d.p.x),d.kl()]}")
        print('pre',st)
        await pg.keyboard.press('KeyJ'); await pg.wait_for_timeout(100)
        print('proj',await pg.evaluate("()=>__dbg().pr.map(q=>[q.type,Math.round(q.x)])"),await pg.evaluate("()=>__dbg().p.weapon"))
        await pg.locator('#game').screenshot(path='build/k3.png')
        await pg.wait_for_timeout(800)
        print('kills after',await pg.evaluate("()=>__dbg().kl()"))
        print(errs); await b.close()
asyncio.run(main())
