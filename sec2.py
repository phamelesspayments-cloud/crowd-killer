import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit1')
        await pg.click('#start'); await pg.wait_for_timeout(2600)
        print('1-1',await pg.evaluate("()=>{var d=__dbg();return [d.sec,d.ph,d.props,d.world,d.A.length]}"))
        await pg.locator('#game').screenshot(path='build/s0.png')
        await pg.evaluate("()=>__toExit()")
        await pg.keyboard.down('ArrowRight'); await pg.wait_for_timeout(700); await pg.keyboard.up('ArrowRight')
        print('after walk off',await pg.evaluate("()=>{var d=__dbg();return [d.sec,d.ph]}"))
        await pg.wait_for_timeout(900); await pg.locator('#game').screenshot(path='build/s1.png')
        await pg.wait_for_timeout(1300)
        print('loaded',await pg.evaluate("()=>{var d=__dbg();return [d.sec,d.ph,d.props,d.world,d.en.map(e=>e.type+'@'+Math.round(e.x)+','+Math.round(e.y)+':'+e.state)]}"))
        await pg.locator('#game').screenshot(path='build/s2.png')
        await pg.wait_for_timeout(1300); await pg.locator('#game').screenshot(path='build/s3.png')
        await pg.wait_for_timeout(1500); await pg.locator('#game').screenshot(path='build/s4.png')
        print('fight',await pg.evaluate("()=>{var d=__dbg();return [d.ph,d.en.map(e=>e.state)]}"))
        print(errs); await b.close()
        ims=[Image.open('build/s%d.png'%i).resize((488,275)) for i in [1,2,3,4]]
        o=Image.new('RGB',(976,550));[o.paste(im,((i%2)*488,(i//2)*275)) for i,im in enumerate(ims)];o.save('build/sgrid.png')
asyncio.run(main())
