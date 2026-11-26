import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit1')
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(1)"); await pg.wait_for_timeout(2800)
        print('1-2 start',await pg.evaluate("()=>{var d=__dbg();return [d.sec,d.ph,d.cans.map(c=>[c.x,c.loot])]}"))
        await pg.evaluate("()=>{__toBoss();var d=__dbg();d.p.inv=9999;}")
        shots=[]
        for i,t in enumerate([700,700,900,1100]):
            await pg.wait_for_timeout(t);await pg.locator('#game').screenshot(path='build/b%d.png'%i);shots.append('build/b%d.png'%i)
            print(await pg.evaluate("()=>{var d=__dbg();return [d.ph,Math.round(d.cam),d.en.map(e=>e.type+':'+e.state+'@'+Math.round(e.x)+','+Math.round(e.y))]}"))
        # beat everyone
        await pg.evaluate("()=>__kill()")
        await pg.wait_for_timeout(500)
        print('after boss',await pg.evaluate("()=>__dbg().ph"))
        await pg.locator('#game').screenshot(path='build/b4.png');shots.append('build/b4.png')
        # walk to the door: line up x then go up
        await pg.evaluate("()=>{var d=__dbg();d.p.x=2356;d.p.y=400;}")
        await pg.keyboard.down('ArrowUp'); await pg.wait_for_timeout(800); await pg.keyboard.up('ArrowUp')
        print('entering',await pg.evaluate("()=>{var d=__dbg();return [d.ph,Math.round(d.p.y),d.p.enterA]}"))
        await pg.wait_for_timeout(500);await pg.locator('#game').screenshot(path='build/b5.png');shots.append('build/b5.png')
        await pg.wait_for_timeout(3000)
        print('result',await pg.locator('#over').is_visible(),await pg.locator('#over h3').text_content())
        print(errs); await b.close()
        ims=[Image.open(f).resize((488,275)) for f in shots]
        o=Image.new('RGB',(976,275*3));[o.paste(im,((i%2)*488,(i//2)*275)) for i,im in enumerate(ims)];o.save('build/bgrid.png')
asyncio.run(main())
