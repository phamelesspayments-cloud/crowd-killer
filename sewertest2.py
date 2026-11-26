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
            print(tag,await pg.evaluate("()=>__ev('[phase,encIdx,Math.round(camX),enemies.filter(function(e){return e.hp>0}).map(function(e){return e.skin||e.type}).join(),Math.round(player.x),Math.round(player.y)]')"),flush=True)
        await pg.evaluate("()=>{__hold();__sec(8);__pinv();}");await snap(200,'start')
        await snap(120,'wave0')
        for w in range(7):
            await pg.evaluate("()=>__ev('enemies.forEach(function(e){if(!e.d||!e.d.boss){e.hp=0;e.gone=true;}});queue.length=0;')")
            await pg.evaluate("()=>__ev(\"(function(){for(var i=0;i<900;i++){player.x+=4;player.y=390;__step(1);if(phase===\\'fight\\'&&enemies.some(function(e){return e.hp>0&&e.x>camX&&e.x<camX+W;}))break;if(phase===\\'door\\')break;}})()\")")
            await snap(90,'w%d'%w)
        await pg.evaluate("()=>__ev('player.x=2900;player.y=400;frames=frames|16;')");await snap(0,'sign')
        await pg.evaluate("()=>__ev(\"(function(){for(var i=0;i<400;i++){player.x+=Math.sign(3074-player.x)*Math.min(4,Math.abs(3074-player.x));player.y=Math.max(330,player.y-3);__step(1);if(phase!==\\'door\\')break;}})()\")")
        await snap(1,'at door');await snap(150,'after')
        print(errs);await b.close()
        for i,im in enumerate(shots):im.save('wolf/sew%02d.png'%i)
asyncio.run(main())
