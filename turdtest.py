import asyncio,base64,io
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://127.0.0.1:8765/dbg.html');await pg.wait_for_timeout(2500)
        print(await pg.evaluate("()=>{var v=document.createElement('video');return [v.canPlayType('video/mp4; codecs=\"avc1.4D401E\"'),v.canPlayType('video/mp4')]}"))
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(300);await pg.keyboard.press('Enter');await pg.wait_for_timeout(300)
        await pg.click('#start');await pg.wait_for_timeout(1500)
        shots=[]
        async def snap(n,tag):
            url=await pg.evaluate("(n)=>__step(n)",n);shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'))
            print(tag,await pg.evaluate("()=>__dst()"),await pg.evaluate("()=>__php()"),await pg.evaluate("()=>__ev('SEC.vid?[SEC.vid.readyState,SEC.vid.paused,+SEC.vid.currentTime.toFixed(2),SEC.vid.error&&SEC.vid.error.code]:null')"),flush=True)
        await pg.evaluate("()=>{window.__boss='ned';__hold();__sec(9);}");await snap(200,'start')
        await pg.wait_for_timeout(1500);await snap(1,'later')
        await pg.evaluate("()=>__ev('enemies.forEach(function(e){e.hp=0;e.gone=true;});queue.length=0;')")
        await pg.evaluate("()=>__ev(\"(function(){for(var i=0;i<900;i++){player.hp=125;enemies.forEach(function(e){if(e.skin!==\\'ned\\'&&e.hp>0){e.hp=0;e.gone=true;}});__step(1);if(__dn())break;}})()\")")
        await snap(60,'ned out');await pg.wait_for_timeout(1000);await snap(60,'ned walk')
        await pg.evaluate("()=>__ev(\"player.x=900;player.y=400;\")");await snap(2,'wall test')
        print(errs);await b.close()
        for i,im in enumerate(shots):im.save('turd/t%02d.png'%i)
asyncio.run(main())
