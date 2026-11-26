import asyncio,sys,base64,io
from playwright.async_api import async_playwright
from PIL import Image
async def run(pg,side):
    await pg.goto('http://127.0.0.1:8765/dbg.html'); await pg.wait_for_timeout(1500)
    await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit1')
    await pg.click('#start'); await pg.wait_for_timeout(1200)
    await pg.evaluate("()=>__sec(3)"); await pg.wait_for_timeout(2600)
    await pg.evaluate("()=>{__toBoss4();var d=__dbg();d.p.x=480;d.p.y=470;}")
    await pg.wait_for_timeout(600)
    await pg.evaluate("""(side)=>{__hold();var d=__dbg(),b=d.boss;d.q.length=0;d.en.forEach(e=>{if(e!==b){e.hp=0;e.gone=true;}});
      b.hp=1;b.state='walk';b.cd=999;b.x=d.p.x+side*140;b.y=d.p.y;b.vx=0;b.vy=0;b.d.block=0;b.rh=0;d.p.face=side;d.p.inv=0;d.p.state='free';}""",side)
    await pg.evaluate("()=>document.dispatchEvent(new KeyboardEvent('keydown',{code:'KeyJ'}))")
    tiles=[]
    for i in range(70):
        url=await pg.evaluate("(k)=>__step(k)",3)
        st=await pg.evaluate("()=>{var b=__dbg().boss;return [b.state,b.t,Math.round(b.x),Math.round(b.y)]}")
        if st[0]=='decap' and st[1] in range(24,140) and (st[1]//3)%4==0 and len(tiles)<8:
            im=Image.open(io.BytesIO(base64.b64decode(url.split(',')[1])));x,y=st[2],st[3]
            tiles.append(im.crop((x-150,y-260,x+150,y+20)))
    await pg.evaluate("()=>document.dispatchEvent(new KeyboardEvent('keyup',{code:'KeyJ'}))")
    return tiles
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();rows=[]
        for side in (1,-1):
            pg=await b.new_page(viewport={'width':1100,'height':900});rows.append(await run(pg,side));await pg.close()
        await b.close()
        o=Image.new('RGB',(300*8,280*2))
        for r,row in enumerate(rows):
            for i,t in enumerate(row):o.paste(t,(i*300,r*280))
        o.save('build/neckgame.png');print([len(r) for r in rows])
asyncio.run(main())
