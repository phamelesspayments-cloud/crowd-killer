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
        await pg.evaluate("()=>{__hold();__sec(5);}");await pg.evaluate("()=>__step(120)")
        await pg.evaluate("()=>__toLast()")
        shots=[];log=[]
        async def snap(n,tag):
            url=await pg.evaluate("(n)=>__step(n)",n);shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'));log.append((tag,await pg.evaluate("()=>__gst()")))
        await snap(45,'banner')
        seen=set()
        for i in range(400):
            await pg.evaluate("()=>__step(2)");st=await pg.evaluate("()=>__gst()")
            s0=st[0][0] if st[0] else None
            if s0 in ('gcrouch','gjump','gslide') and s0 not in seen:
                seen.add(s0);await snap(6 if s0!='gjump' else 12,s0)
            if 'gslide' in seen and len(shots)>=4:break
        await snap(30,'after slide')
        await pg.evaluate("()=>{__pinv();__killG();}");await snap(60,'death');
        for l in log:print(l)
        print(errs);await b.close()
        o=Image.new('RGB',(960*3,540*2))
        for i,im in enumerate(shots[:6]):o.paste(im,((i%3)*960,(i//3)*540))
        o.resize((1920,720)).save('build/gerrygrid.png')
asyncio.run(main())
