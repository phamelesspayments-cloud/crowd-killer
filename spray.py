import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit1')
        await pg.click('#start'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>__sec(3)"); await pg.wait_for_timeout(2600)
        await pg.evaluate("()=>{__toBoss4();var d=__dbg();d.p.inv=999999;d.p.x=250;d.p.y=470;}")
        await pg.wait_for_timeout(500)
        await pg.evaluate("()=>{var d=__dbg(),b=d.boss;d.en.forEach(e=>{if(e!==b){e.hp=0;e.gone=true;}});b.hp=1;b.state='walk';b.x=d.p.x+130;b.y=d.p.y;d.p.face=1;b.d.block=0;b.rh=0;}")
        await pg.keyboard.press('KeyJ')
        shots=[]
        for k in range(8):
            await pg.wait_for_timeout(260);fn='build/sp%d.png'%k;await pg.locator('#game').screenshot(path=fn);shots.append(fn)
        await b.close()
        ims=[]
        for f in shots:
            im=Image.open(f);sx=im.width/960;ims.append(im.crop((int(150*sx),int(120*sx),int(600*sx),int(540*sx))).resize((300,280)))
        o=Image.new('RGB',(1200,560));[o.paste(im,((i%4)*300,(i//4)*280)) for i,im in enumerate(ims)];o.save('build/spgrid.png')
asyncio.run(main())
