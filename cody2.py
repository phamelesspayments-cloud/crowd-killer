import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':1000})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300)
        await pg.keyboard.press('Digit2'); await pg.click('#start'); await pg.wait_for_timeout(2300)
        await pg.evaluate("()=>{var d=__dbg();d.A.forEach(a=>a.armed=false);d.p.x=400;d.p.y=450;}")
        await pg.wait_for_timeout(200)
        await pg.evaluate("()=>{var d=__dbg();d.p.state='down';d.p.air=true;d.p.z=1;d.p.vz=7*Math.SQRT2;d.p.vx=-3;d.p.lt=0;}")
        for i in range(4):
            await pg.wait_for_timeout(260);await pg.locator('#game').screenshot(path='build/dn%d.png'%i)
            print(await pg.evaluate("()=>{var d=__dbg();return [d.p.state,d.p.air,Math.round(d.p.z),d.p.lt,d.p._rot&&+d.p._rot.toFixed(2),Math.round(d.p.x)]}"))
        print(errs); await b.close()
        ims=[Image.open('build/dn%d.png'%i) for i in range(4)];sx=ims[0].width/960
        o=Image.new('RGB',(400*4,300))
        for k,im in enumerate(ims):o.paste(im.crop((int(150*sx),int(220*sx),int(650*sx),int(540*sx))).resize((400,300)),(k*400,0))
        o.save('build/dgrid2.png')
asyncio.run(main())
