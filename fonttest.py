import asyncio,base64,io
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://127.0.0.1:8765/dbg.html');await pg.wait_for_timeout(2500)
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(500);await pg.screenshot(path='font2/s_opts.png')
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(500);await pg.screenshot(path='font2/s_select.png')
        await pg.click('#start');await pg.wait_for_timeout(1500)
        shots=[]
        async def snap(n):
            url=await pg.evaluate("(n)=>__step(n)",n);shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'))
        await pg.evaluate("()=>{__hold();__sec(0);}");await snap(60)
        await pg.evaluate("()=>{window.__boss='ned';__sec(10);}");await snap(60)
        await pg.evaluate("()=>__ev(\"(function(){for(var i=0;i<1500;i++){player.hp=125;enemies.forEach(function(e){if(e.skin!==\\'ned\\'&&e.hp>0){e.hp=0;e.gone=true;}});__step(1);if(__dn())break;}})()\")");await snap(40)
        await pg.evaluate("()=>__sec(8)");await snap(150)
        print(errs);await b.close()
        o=Image.new('RGB',(1920,1080))
        for i,im in enumerate(shots):o.paste(im,((i%2)*960,(i//2)*540))
        o.save('font2/game.png')
asyncio.run(main())
