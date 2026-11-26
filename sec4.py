import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit3')
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(3)"); await pg.wait_for_timeout(900)
        print('ranges',await pg.evaluate("()=>{var d=__dbg();return [370,420,470,528].map(y=>[y].concat(d.fr(y).map(Math.round)))}"))
        await pg.locator('#game').screenshot(path='build/f0.png')
        await pg.evaluate("()=>{var d=__dbg();d.p.inv=99999;}")
        # walk up-left into the corner
        await pg.keyboard.down('ArrowUp');await pg.keyboard.down('ArrowLeft');await pg.wait_for_timeout(1500);await pg.keyboard.up('ArrowUp');await pg.keyboard.up('ArrowLeft')
        print('back-left corner',await pg.evaluate("()=>{var d=__dbg();return [Math.round(d.p.x),Math.round(d.p.y)]}"))
        await pg.locator('#game').screenshot(path='build/f1.png')
        await pg.keyboard.down('ArrowDown');await pg.keyboard.down('ArrowRight');await pg.wait_for_timeout(2500);await pg.keyboard.up('ArrowDown');await pg.keyboard.up('ArrowRight')
        print('front-right corner',await pg.evaluate("()=>{var d=__dbg();return [Math.round(d.p.x),Math.round(d.p.y),d.en.map(e=>e.type+'@'+Math.round(e.x)+','+Math.round(e.y))]}"))
        await pg.locator('#game').screenshot(path='build/f2.png')
        await pg.wait_for_timeout(1500);await pg.locator('#game').screenshot(path='build/f3.png')
        await pg.evaluate("()=>__kill()");await pg.wait_for_timeout(600)
        print('after wave1',await pg.evaluate("()=>{var d=__dbg();return [d.ph,d.enc]}"))
        await pg.wait_for_timeout(2500)
        await pg.evaluate("()=>__kill()");await pg.wait_for_timeout(4200)
        print('end',await pg.evaluate("()=>__dbg().ph"),await pg.locator('#over').is_visible(),await pg.locator('#over h3').text_content())
        print(errs); await b.close()
        ims=[Image.open('build/f%d.png'%i).resize((488,275)) for i in range(4)]
        o=Image.new('RGB',(976,550));[o.paste(im,((i%2)*488,(i//2)*275)) for i,im in enumerate(ims)];o.save('build/fgrid.png')
asyncio.run(main())
