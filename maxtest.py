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
        await pg.evaluate("()=>{__hold();__sec(4);}");await pg.evaluate("()=>__step(130)")
        await pg.evaluate("()=>__setupM()")
        shots=[];log=[]
        async def snap(n,tag):
            url=await pg.evaluate("(n)=>__step(n)",n);shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'));log.append((tag,await pg.evaluate("()=>__mst()")))
        await snap(40,'walk');await snap(60,'walk2')
        # wait for his windup and punch
        hit=False
        for i in range(120):
            await pg.evaluate("()=>__step(2)");st=await pg.evaluate("()=>__mst()")
            if st[0]=='windup' and len(shots)==2:await snap(16,'windup')
            if st[0]=='attack' and len(shots)==3:await snap(1,'punch');break
        await snap(40,'after punch')
        await pg.evaluate("()=>{__pinv();__knockM();}");await snap(18,'knocked')
        await pg.evaluate("()=>{__setupM();__pinv();__killM(false);}");await snap(30,'light death a');await snap(40,'light death b')
        await pg.evaluate("()=>{__setupM();__pinv();__killM(true);}");await snap(20,'heavy death')
        for l in log:print(l)
        print(errs);await b.close()
        o=Image.new('RGB',(960*3,540*3))
        for i,im in enumerate(shots[:9]):o.paste(im,((i%3)*960,(i//3)*540))
        o.resize((1920,1080)).save('build/maxgrid.png')
asyncio.run(main())
