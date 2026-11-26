import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':1000})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(600)
        await pg.screenshot(path='build/sel.png')
        await pg.keyboard.press('Digit2'); await pg.click('#start'); await pg.wait_for_timeout(2300)
        await pg.evaluate("()=>{var d=__dbg();d.A.forEach(a=>a.armed=false);d.p.x=300;d.p.y=450;}")
        shots=[]
        async def snap(n):
            await pg.locator('#game').screenshot(path='build/cd_%s.png'%n);shots.append(n)
        await pg.wait_for_timeout(300);await snap('idle')
        await pg.keyboard.down('ArrowRight');await pg.wait_for_timeout(350);await snap('walk');await pg.keyboard.up('ArrowRight')
        await pg.wait_for_timeout(300)
        await pg.keyboard.press('KeyJ');await pg.wait_for_timeout(160);await snap('jab')
        await pg.wait_for_timeout(500)
        await pg.keyboard.press('KeyL');await pg.wait_for_timeout(420);await snap('heavy')
        await pg.wait_for_timeout(700)
        await pg.keyboard.press('KeyK');await pg.wait_for_timeout(250);await pg.keyboard.press('KeyJ');await pg.wait_for_timeout(120);await snap('airkick')
        await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>{var d=__dbg();d.p.state='down';d.p.air=false;d.p.z=0;d.p.lt=8;}");await pg.wait_for_timeout(60);await snap('down')
        await pg.evaluate("()=>{var d=__dbg();d.p.state='free';d.p.weapon={type:'knife',uses:1};}");await pg.wait_for_timeout(300);await snap('knife')
        print(errs); await b.close()
        ims=[Image.open('build/cd_%s.png'%n) for n in shots]
        sx=ims[0].width/960
        crops=[im.crop((int(150*sx),int(180*sx),int(520*sx),int(500*sx))).resize((300,260)) for im in ims]
        o=Image.new('RGB',(300*4,260*2))
        for k,c in enumerate(crops):o.paste(c,((k%4)*300,(k//4)*260))
        o.save('build/cgrid2.png')
asyncio.run(main())
