import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={'width':360,'height':740},device_scale_factor=2,is_mobile=True,has_touch=True)
        pg=await ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]);await pg.wait_for_timeout(1500)
        await pg.touchscreen.tap(180,700);await pg.wait_for_timeout(400)     # empty area below the title picture
        print('after tap on page:',await pg.evaluate("()=>__dbg().mode"))
        cur=await pg.evaluate('()=>__dbg().sel');idx=0 if cur!='tim' else 2;card=pg.locator('.card').nth(idx);await card.tap();await pg.wait_for_timeout(300)
        print('after first card tap:',await pg.evaluate("()=>__dbg()"))
        await pg.screenshot(path='build/tap_select.png')
        await card.tap();await pg.wait_for_timeout(600)
        print('after second card tap:',await pg.evaluate("()=>__dbg()"),errs)
        await b.close()
asyncio.run(main())
