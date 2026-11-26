import asyncio,base64,io
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://127.0.0.1:8765/dbg.html');await pg.wait_for_timeout(2500)
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(300);await pg.keyboard.press('Enter');await pg.wait_for_timeout(300)
        await pg.click('#start');await pg.wait_for_timeout(1500)
        shots=[]
        async def snap(n,tag):
            url=await pg.evaluate("(n)=>__step(n)",n);shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'))
            print(tag,await pg.evaluate("()=>__dst()"),await pg.evaluate("()=>__php()"),flush=True)
        await pg.evaluate("()=>{window.__boss='ned';__hold();__sec(9);}");await snap(200,'start')
        await pg.evaluate("()=>__ev('enemies.forEach(function(e){e.hp=0;e.gone=true;});queue.length=0;')")
        await pg.evaluate("()=>__ev(\"(function(){for(var i=0;i<1500;i++){player.x=Math.min(player.x+4,1250);player.hp=125;enemies.forEach(function(e){if(e.skin!==\'ned\'&&e.hp>0){e.hp=0;e.gone=true;}});__step(1);if(__dn())break;}})()\")");await snap(140,'ned arrives')
        await pg.evaluate("()=>__ev(\"__only();var d=__dn();player.x=camX+250;player.y=440;d.x=camX+700;d.y=440;d.cd=0;d.sumCd=0;d.state='walk';\")")
        await pg.evaluate("()=>__ev(\"var d=__dn();player.hp=125;player.inv=0;player.state='free';player.x=camX+150;player.y=440;d.x=camX+760;d.y=440;d.state='shoot';d.t=0;d.face=-1;\")")
        await snap(51,'far fire');await snap(3,'far fire+3');await snap(30,'after')
        print(errs);await b.close()
        for i,im in enumerate(shots):im.save('ned/f%02d.png'%i)
asyncio.run(main())
