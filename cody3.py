import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':1000})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300)
        await pg.keyboard.press('Digit2'); await pg.click('#start'); await pg.wait_for_timeout(2300)
        await pg.evaluate("()=>{var d=__dbg();d.A.forEach(a=>a.armed=false);d.p.x=420;d.p.y=450;}")
        await pg.wait_for_timeout(200)
        await pg.evaluate("()=>{var d=__dbg();d.p.state='hurt';d.p.t=16;}")
        await pg.wait_for_timeout(120);await pg.locator('#game').screenshot(path='build/q0.png')
        await pg.wait_for_timeout(300)
        await pg.evaluate("()=>{var d=__dbg();d.p.state='down';d.p.air=true;d.p.z=1;d.p.vz=7*Math.SQRT2;d.p.vx=-3;d.p.lt=0;}")
        ts=[200,250,350,300,350,350,400]
        for i,t in enumerate(ts):
            await pg.wait_for_timeout(t);await pg.locator('#game').screenshot(path='build/q%d.png'%(i+1))
        print(errs); await b.close()
        ims=[Image.open('build/q%d.png'%i) for i in range(len(ts)+1)];sx=ims[0].width/960
        o=Image.new('RGB',(300*4,240*2))
        for k,im in enumerate(ims):o.paste(im.crop((int(170*sx),int(220*sx),int(600*sx),int(560*sx))).resize((300,240)),((k%4)*300,(k//4)*240))
        o.save('build/qgrid.png')
asyncio.run(main())
