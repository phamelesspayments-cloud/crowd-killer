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
        shots={}
        async def snap(name,n=1):
            url=await pg.evaluate("(n)=>__step(n)",n);shots[name]=Image.open(io.BytesIO(base64.b64decode(url.split(',')[1])))
        # 1-4 end -> 2-1
        await pg.evaluate("()=>{__hold();__sec(3);}");await pg.evaluate("()=>__step(120)")
        await pg.evaluate("()=>{__end14();}");await snap('a_14end',140)
        print('after 1-4',await pg.evaluate("()=>__st()"))
        await snap('b_21start',150)
        print('2-1 start',await pg.evaluate("()=>__st()"))
        # clear opening fight, walk left to first stop
        await pg.evaluate("()=>{__clear();__pl(__st().px);}");await pg.evaluate("()=>__step(5)")
        await snap('c_go',12)
        print('after open fight',await pg.evaluate("()=>__st()"))
        await pg.evaluate("()=>__key('left',1)")
        for i in range(30):
            await pg.evaluate("()=>__step(10)")
            st=await pg.evaluate("()=>__st()")
            if st['ph']=='fight':break
        print('stop 1',st)
        await snap('d_stop1',30)
        # jump through to the exit
        await pg.evaluate("()=>__key('left',0)")
        for k in range(3):
            await pg.evaluate("()=>{__clear();}");await pg.evaluate("()=>__step(3)")
            await pg.evaluate("()=>__key('left',1)")
            for i in range(80):
                await pg.evaluate("()=>{__clear();}") if False else None
                await pg.evaluate("()=>__step(10)")
                st=await pg.evaluate("()=>__st()")
                if st['ph'] in ('fight','exit','fade'):break
            print('step',k,st)
        await pg.evaluate("()=>{__clear();}");
        for i in range(60):
            await pg.evaluate("()=>__step(10)");st=await pg.evaluate("()=>__st()")
            if st['ph']=='fade':break
        print('exit',st)
        await pg.evaluate("()=>{mode='play';}");await pg.wait_for_timeout(2500)
        print('over',await pg.locator('#over').is_visible(),await pg.locator('#over h3').text_content(),errs)
        await b.close()
        o=Image.new('RGB',(960*2,540*2))
        for i,k in enumerate(sorted(shots)):o.paste(shots[k].convert('RGB'),((i%2)*960,(i//2)*540))
        o.resize((1440,810)).save('build/sec21grid.png')
asyncio.run(main())
