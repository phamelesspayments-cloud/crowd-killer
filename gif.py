import asyncio,sys,base64
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit2')
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(3)"); await pg.wait_for_timeout(2600)
        await pg.evaluate("()=>{__toBoss4();var d=__dbg();d.p.x=330;d.p.y=470;}")
        await pg.wait_for_timeout(700)
        await pg.evaluate("""()=>{__hold();var d=__dbg(),b=d.boss;d.q.length=0;d.en.forEach(e=>{if(e!==b){e.hp=0;e.gone=true;}});
          b.hp=1;b.state='walk';b.cd=999;b.x=d.p.x+150;b.y=d.p.y;b.face=-1;b.vx=0;b.vy=0;b.d.block=0;b.rh=0;b.bar=0;
          d.p.face=1;d.p.inv=0;d.p.state='free';}""")
        n=0
        async def grab(ticks):
            nonlocal n
            url=await pg.evaluate("(k)=>__step(k)",ticks)
            open('gif/%04d.png'%n,'wb').write(base64.b64decode(url.split(',')[1]));n+=1
        for i in range(8):await grab(3)          # a beat of him squaring up
        await pg.evaluate("()=>{var d=__dbg(),b=d.boss;b.x=d.p.x+150;b.y=d.p.y;}")
        # Cody's heavy (Sledgehammer) for the finishing blow
        await pg.evaluate("()=>{document.dispatchEvent(new KeyboardEvent('keydown',{code:'KeyL'}));}")
        for i in range(150):await grab(3)
        await pg.evaluate("()=>{document.dispatchEvent(new KeyboardEvent('keyup',{code:'KeyL'}));}")
        print('frames',n,'boss',await pg.evaluate("()=>{var b=__dbg().boss;return [b.state,b.t,!!b.corpse]}"),errs)
        await b.close()
asyncio.run(main())
