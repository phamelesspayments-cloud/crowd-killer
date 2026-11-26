import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); 
        crops=[]
        for i,k in enumerate(['Digit1','Digit2','Digit3']):
            pg=await b.new_page(viewport={'width':1100,'height':900})
            await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
            await pg.keyboard.press('Enter'); await pg.wait_for_timeout(200); await pg.keyboard.press(k)
            await pg.click('#start'); await pg.wait_for_timeout(2500)
            await pg.evaluate("()=>{var d=__dbg();d.p.weapon={type:'knife',uses:1};d.p.x=300;d.p.y=440;d.L.armed=false;d.p.face=1;}")
            await pg.wait_for_timeout(300)
            box=await pg.locator('#game').bounding_box()
            await pg.locator('#game').screenshot(path='build/h%d.png'%i)
            await pg.close()
            im=Image.open('build/h%d.png'%i); sx=im.width/960
            crops.append(im.crop((int(150*sx),int(180*sx),int(450*sx),int(460*sx))))
        o=Image.new('RGB',(sum(c.width for c in crops),crops[0].height));x=0
        for c in crops:o.paste(c,(x,0));x+=c.width
        o.save('build/hold.png')
        await b.close()
asyncio.run(main())
