import asyncio,base64,io
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1100,'height':900})
        await pg.goto('http://127.0.0.1:8765/dbg.html');await pg.wait_for_timeout(2500)
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(300);await pg.keyboard.press('Enter');await pg.wait_for_timeout(300)
        await pg.click('#start');await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>{__hold();__sec(4);}");await pg.evaluate("()=>__step(130)")
        await pg.evaluate("()=>{__clear();}")
        for i in range(12):
            url=await pg.evaluate("()=>__step(4)")
            st=await pg.evaluate("()=>__st().ph")
            if st=='walk':
                im=Image.open(io.BytesIO(base64.b64decode(url.split(',')[1])))
                if sum(im.convert('L').crop((40,150,300,330)).getdata())!=sum(im.convert('L').crop((40,150,300,330)).getdata())*0+0:pass
        shots=[]
        for i in range(8):
            url=await pg.evaluate("()=>__step(8)");shots.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB'))
        best=max(shots,key=lambda im:sum(1 for px in im.crop((40,150,300,330)).getdata() if px[0]>220 and px[1]>190 and px[2]<90))
        best.save('build/goleft.png');await b.close()
asyncio.run(main())
