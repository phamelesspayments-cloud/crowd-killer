import asyncio,base64,io
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        await pg.goto('http://127.0.0.1:8765/dbg.html'); await pg.wait_for_timeout(1500)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); await pg.keyboard.press('Digit2')
        await pg.click('#start'); await pg.wait_for_timeout(2600)
        await pg.evaluate("()=>{__hold();__setup();}")
        await pg.evaluate("()=>__step(20)")
        tiles=[]
        for i in range(16):
            url,px,py=await pg.evaluate("()=>__step(4)")
            im=Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB')
            tiles.append(im.crop((int(px)-120,int(py)-250,int(px)+120,int(py)+20)))
        await b.close()
        o=Image.new('RGB',(240*8,270*2))
        for i,t in enumerate(tiles):o.paste(t,((i%8)*240,(i//8)*270));ImageDraw.Draw(o).text(((i%8)*240+4,(i//8)*270+4),str(i),fill=(255,255,0))
        o.save('build/stride.png')
asyncio.run(main())
