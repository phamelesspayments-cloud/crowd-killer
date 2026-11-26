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
        shots=[];log=[]
        async def snap(n,tag):
            url=await pg.evaluate("(n)=>__step(n)",n);shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'));log.append((tag,await pg.evaluate("()=>__dst()")));print(log[-1],flush=True)
        await pg.evaluate("()=>{__hold();__sec(7);}");await snap(230,'arrive')
        await pg.evaluate("()=>{__only();__farD();}")
        print('summon after',flush=True);print(await pg.evaluate("()=>__until('summon',900)"));await snap(46,'summon point')
        await pg.evaluate("()=>__step(40)");await pg.evaluate("()=>__nearD()")
        print('punch after',flush=True);print(await pg.evaluate("()=>__until('attack',900)"));await snap(3,'punch')
        await snap(30,'after')
        await pg.evaluate("()=>{__pinv();__killD();}");await snap(60,'death a');await snap(70,'death b')
        for l in log:print(l)
        print(errs);await b.close()
        o=Image.new('RGB',(960*3,540*2))
        for i,im in enumerate(shots[:6]):o.paste(im,((i%3)*960,(i//3)*540))
        o.resize((1920,720)).save('build/dangrid.png')
asyncio.run(main())
