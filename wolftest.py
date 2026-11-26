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
            print(tag,await pg.evaluate("()=>__dst()"),await pg.evaluate("()=>__wolves()"),await pg.evaluate("()=>__php()"),flush=True)
        await pg.evaluate("()=>{__hold();__sec(7);}");await snap(200,'room start')
        # walk to the far right
        await pg.evaluate("()=>__ev(\"(function(){for(var i=0;i<400;i++){player.x=Math.min(player.x+4,1300);__step(1);if(phase===\'fight\')break;}})()\")");await snap(1,'first fight')
        await pg.evaluate("()=>__ev(\"enemies.forEach(function(e){e.hp=0;e.gone=true;});queue.length=0;\")")
        await pg.evaluate("()=>__ev(\"(function(){for(var i=0;i<500;i++){player.x=Math.min(player.x+4,1250);__step(1);if(__dn())break;}})()\")");await snap(120,'dan arrives')
        await pg.evaluate("()=>__ev(\"__only();var d=__dn();player.x=camX+200;player.y=470;d.x=camX+760;d.y=470;d.cd=0;d.sumCd=0;d.state='walk';\")")
        print('summon',await pg.evaluate("()=>__until('summon',900)"))
        await snap(44,'point');await snap(18,'wolf in');await snap(16,'wolf leap')
        for k in range(8):
            await snap(5,'w%d'%k)
        await snap(60,'after')
        print(errs);await b.close()
        o=Image.new('RGB',(960*3,540*3))
        sel=[shots[i] for i in (0,2,3,4,5,7,8,10,13)]
        for i,im in enumerate(sel):o.paste(im,((i%3)*960,(i//3)*540))
        o.resize((1920,1080)).save('wolf/grid.png')
asyncio.run(main())
