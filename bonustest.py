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
            print(tag,await pg.evaluate("()=>__ev('[phase,SEC.name,car&&car.hp,car&&car.stage,bonusT,score,Math.round(player.x)]')"),flush=True)
        await pg.evaluate("()=>{__hold();__sec(8);}");await snap(60,'intro');await snap(80,'ready')
        hit="(function(n,zone){for(var i=0;i<n;i++){var tx=zone?car.l+car.w-75+60:car.l-10;player.x+=clamp(tx-player.x,-4,4);player.y=car.y;player.face=zone?-1:1;if(i%14===0)pressed.attack=1;if(i%60===30)pressed.heavy=1;__step(1);}})"
        await pg.evaluate("()=>__ev(%r)"%(hit+"(300,0)"));await snap(1,'front hits')
        await pg.evaluate("()=>__ev(%r)"%(hit+"(400,1)"));await snap(1,'rear hits')
        await pg.evaluate("()=>__ev(%r)"%(hit+"(600,0)"));await snap(1,'more')
        await snap(40,'clear');await snap(240,'fade');await snap(200,'next')
        print(errs);await b.close()
        for i,im in enumerate(shots):im.save('dyehard/t%02d.png'%i)
asyncio.run(main())
