import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit2')
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(3)"); await pg.wait_for_timeout(2600)
        await pg.evaluate("()=>{__toBoss4();var d=__dbg();d.p.inv=999999;d.p.x=300;d.p.y=450;}")
        await pg.wait_for_timeout(600)
        print('spawned',await pg.evaluate("()=>{var d=__dbg();return [d.boss&&d.boss.type,d.boss&&Math.round(d.boss.hp),d.en.map(e=>e.type+':'+e.state)]}"))
        await pg.locator('#game').screenshot(path='build/n0.png')
        # get the boss next to the player and punch repeatedly
        states=set();blocks=0
        for i in range(60):
            await pg.evaluate("()=>{var d=__dbg(),b=d.boss;d.en.forEach(e=>{if(e!==b){e.hp=0;e.gone=true;}});if(b&&b.hp>0&&b.state==='walk'){b.x=d.p.x+110;b.y=d.p.y;}d.p.face=1;d.p.hp=d.p.c.hp;}")
            await pg.keyboard.press('KeyJ'); await pg.wait_for_timeout(110)
            st=await pg.evaluate("()=>{var b=__dbg().boss;return b?b.state+(b.move?':'+b.move.kind:''):''}");states.add(st)
            if st=='block' and blocks<1:
                await pg.locator('#game').screenshot(path='build/n1.png');blocks+=1
        print('states seen',sorted(states))
        print('boss hp',await pg.evaluate("()=>Math.round(__dbg().boss.hp)"))
        await pg.locator('#game').screenshot(path='build/n2.png')
        # finish him with a punch
        await pg.evaluate("()=>{var d=__dbg(),b=d.boss;b.hp=1;b.state='walk';b.x=d.p.x+110;b.y=d.p.y;d.p.face=1;b.d.block=0;b.rh=0;}")
        await pg.keyboard.press('KeyJ')
        shots=[]
        for k,t in enumerate([450,350,300,250,300,500,900]):
            await pg.wait_for_timeout(t);fn='build/nd%d.png'%k;await pg.locator('#game').screenshot(path=fn);shots.append(fn)
            print(k,await pg.evaluate("()=>{var d=__dbg(),b=d.boss;return [b.state,b.t,d.heads.length,d.sprays.length,!!b.corpse]}"))
        await pg.wait_for_timeout(4500)
        print('end',await pg.locator('#over').is_visible(),await pg.locator('#over h3').text_content())
        print(errs); await b.close()
        ims=[Image.open(f).resize((488,275)) for f in shots]+[Image.open('build/n1.png').resize((488,275)) if blocks else Image.new('RGB',(488,275))]
        o=Image.new('RGB',(976,275*4));[o.paste(im,((i%2)*488,(i//2)*275)) for i,im in enumerate(ims)];o.save('build/ngrid.png')
asyncio.run(main())
