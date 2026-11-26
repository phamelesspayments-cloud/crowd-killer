import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,vw,vh in (('portrait',360,740),('landscape',844,390)):
            ctx=await b.new_context(viewport={'width':vw,'height':vh},device_scale_factor=2,is_mobile=True,has_touch=True)
            pg=await ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('file://'+sys.argv[1]);await pg.wait_for_timeout(1500)
            await pg.tap('#title');await pg.wait_for_timeout(300)
            await pg.tap('#start');await pg.wait_for_timeout(2600)
            cdp=await ctx.new_cdp_session(pg)
            d=await pg.locator('#dpad').bounding_box();a=await pg.locator('.ab.attack').bounding_box()
            cx,cy=d['x']+d['width']/2,d['y']+d['height']/2
            x0=await pg.evaluate("()=>__dbg().p.x")
            async def touch(typ,pts):await cdp.send('Input.dispatchTouchEvent',{'type':typ,'touchPoints':pts})
            await touch('touchStart',[{'x':cx+d['width']*.4,'y':cy,'id':1}])
            await pg.wait_for_timeout(500)
            x1=await pg.evaluate("()=>__dbg().p.x");k1=await pg.evaluate("()=>{var k=__dbg().keys;return [k.left,k.right,k.up,k.down]}")
            await touch('touchMove',[{'x':cx+d['width']*.35,'y':cy+d['height']*.35,'id':1}])
            await pg.wait_for_timeout(150)
            k2=await pg.evaluate("()=>{var k=__dbg().keys;return [k.left,k.right,k.up,k.down]}")
            await pg.screenshot(path='build/touch_%s.png'%name)
            await touch('touchStart',[{'x':cx+d['width']*.35,'y':cy+d['height']*.35,'id':1},{'x':a['x']+a['width']/2,'y':a['y']+a['height']/2,'id':2}])
            await pg.wait_for_timeout(60)
            st=await pg.evaluate("()=>[__dbg().p.state,__dbg().keys.attack]")
            await touch('touchEnd',[])
            await pg.wait_for_timeout(200)
            k3=await pg.evaluate("()=>{var k=__dbg().keys;return [k.left,k.right,k.up,k.down,k.attack]}")
            print(name,'moved',round(x1-x0),'right-hold keys',k1,'diag keys',k2,'attack while holding',st,'after release',k3,errs)
            await ctx.close()
        await b.close()
asyncio.run(main())
