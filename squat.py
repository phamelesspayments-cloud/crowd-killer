import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit1')
        await pg.click('#start'); await pg.wait_for_timeout(2600)
        shots=[]
        for sec,x in ((0,1320),(1,1900)):
            if sec==1:
                await pg.evaluate("()=>__sec(1)");await pg.wait_for_timeout(2600)
            await pg.evaluate("(x)=>{var d=__dbg();d.p.inv=99999;d.en.forEach(e=>{e.hp=0;e.gone=true;});__at(x-420,440,Math.max(0,x-560),x>1500?2:null);}",x)
            await pg.wait_for_timeout(300)
            fn='build/sq%d_a.png'%sec;await pg.locator('#game').screenshot(path=fn);shots.append(fn)
            st=await pg.evaluate("(x)=>{var a=__dbg().A.filter(a=>a.c.key==='squat'+x)[0];return a&&a.state}",x);print(sec,'before',st)
            await pg.evaluate("(x)=>{__at(x-180,360,Math.max(0,x-560));}",x)
            for k,t in enumerate([700,1200,2200]):
                await pg.wait_for_timeout(t)
                fn='build/sq%d_%d.png'%(sec,k);await pg.locator('#game').screenshot(path=fn);shots.append(fn)
                print(sec,k,await pg.evaluate("(x)=>{var d=__dbg();var a=d.A.filter(a=>a.c.key==='squat'+x)[0];return [a&&a.state,d.en.map(e=>(e.skin||e.type)+':'+e.state+'@'+Math.round(e.x)+','+Math.round(e.y))]}",x))
        print(errs);await b.close()
        ims=[Image.open(f).crop((0,90,976,550)).resize((488,230)) for f in shots]
        o=Image.new('RGB',(976*2,230*4))
        for i,im in enumerate(ims):o.paste(im,((i//4)*976+((i%4)%2)*488,((i%4)//2)*230))
        o=Image.new('RGB',(488*4,230*2))
        for i,im in enumerate(ims):o.paste(im,((i%4)*488,(i//4)*230))
        o.save('build/sqgrid.png')
asyncio.run(main())
