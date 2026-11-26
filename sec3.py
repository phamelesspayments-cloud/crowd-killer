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
        await pg.evaluate("()=>__sec(2)"); await pg.wait_for_timeout(1400)
        await pg.locator('#game').screenshot(path='build/t3a.png')
        await pg.wait_for_timeout(2200)
        print(await pg.evaluate("()=>{var d=__dbg();return [d.sec,d.ph,d.ft,d.world,d.props,d.A.map(a=>a.state),d.en.map(e=>e.type+'@'+Math.round(e.x)+','+Math.round(e.y))]}"))
        await pg.locator('#game').screenshot(path='build/t3b.png')
        await pg.wait_for_timeout(3500)
        print(await pg.evaluate("()=>{var d=__dbg();return [d.A.map(a=>a.state),d.en.map(e=>(e.skin||e.type)+':'+e.state+':'+e.face)]}"))
        await pg.locator('#game').screenshot(path='build/t3c.png')
        print(errs); await b.close()
        ims=[Image.open('build/t3%s.png'%c).resize((488,275)) for c in 'abc']
        o=Image.new('RGB',(976,550));[o.paste(im,((i%2)*488,(i//2)*275)) for i,im in enumerate(ims)];o.save('build/t3grid.png')
asyncio.run(main())
