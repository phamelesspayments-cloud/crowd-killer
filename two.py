import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.click('#start'); await pg.wait_for_timeout(2400)
        await pg.locator('#game').screenshot(path='build/t0.png')
        await pg.keyboard.down('ArrowRight'); await pg.wait_for_timeout(500); await pg.keyboard.up('ArrowRight')
        for i,t in enumerate([5000,900,900]):
            await pg.wait_for_timeout(t); await pg.locator('#game').screenshot(path='build/t%d.png'%(i+1))
            print(await pg.evaluate("()=>{var d=__dbg();return [d.A.map(a=>a.state),d.en.map(e=>e.skin+':'+e.state),d.B.map(q=>[Math.round(q.x),Math.round(q.z),q.landed])]}"))
        await pg.wait_for_timeout(2500); await pg.locator('#game').screenshot(path='build/t4.png')
        print(errs); await b.close()
        ims=[Image.open('build/t%d.png'%i).resize((488,275)) for i in [0,1,2,4]]
        o=Image.new('RGB',(976,550));[o.paste(im,((i%2)*488,(i//2)*275)) for i,im in enumerate(ims)];o.save('build/tgrid.png')
asyncio.run(main())
