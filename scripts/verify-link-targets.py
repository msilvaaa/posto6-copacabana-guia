#!/usr/bin/env python3
"""Check expanded external hit areas and actual clicks outside the original text."""
import asyncio,json,sys
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:8000'
async def main():
 report={'layouts':0,'targets':0,'expanded':0,'outside_text_clicks':0,'failures':[]}
 pages=json.loads((ROOT/'data/guide-pages.json').read_text())
 pages=[p for p in pages if any(l['href'].startswith(('http:','https:','tel:','mailto:')) for l in p['links'])]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  context=await browser.new_context();page=await context.new_page()
  for width in [390,1440]:
   await page.set_viewport_size({'width':width,'height':1000})
   for item in pages:
    path='/'+item['path'].removesuffix('index.html')
    await page.goto(BASE+path);await page.wait_for_function('document.querySelector("[data-expanded-hit]")')
    result=await page.evaluate('''()=>{
     const targets=[...document.querySelectorAll('[data-expanded-hit]')].map(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e),pad=n=>parseFloat(s.getPropertyValue('--hit-'+n))||0;return {href:e.href,base:{l:r.left,t:r.top,r:r.right,b:r.bottom},hit:{l:r.left-pad('left'),t:r.top-pad('top'),r:r.right+pad('right'),b:r.bottom+pad('bottom')}}});
     const overlap=(a,b)=>Math.min(a.r,b.r)-Math.max(a.l,b.l)>.1&&Math.min(a.b,b.b)-Math.max(a.t,b.t)>.1;
     let collisions=0;
     targets.forEach((a,i)=>targets.slice(i+1).forEach(b=>{if(a.href!==b.href&&!overlap(a.base,b.base)&&overlap(a.hit,b.hit))collisions++}));
     return {count:targets.length,expanded:targets.filter(x=>(x.hit.r-x.hit.l)*(x.hit.b-x.hit.t)>(x.base.r-x.base.l)*(x.base.b-x.base.t)+1).length,collisions,overflow:document.documentElement.scrollWidth>innerWidth};
    }''')
    if result['collisions'] or result['overflow']:report['failures'].append([path,width,result])
    report['layouts']+=1;report['targets']+=result['count'];report['expanded']+=result['expanded']
  for lang,sections in [('pt',['bares','restaurantes','transportes']),('en',['bars','restaurants','transportation']),('es',['verja','restaurantes','transporte'])]:
   for section in sections:
    await page.goto(f'{BASE}/{lang}/{section}/');await page.wait_for_function('document.querySelector("[data-expanded-hit]")')
    link=page.locator('.guide-link[data-expanded-hit][href^="http"]').first
    await link.scroll_into_view_if_needed()
    target=await link.evaluate('e=>{let r=e.getBoundingClientRect(),s=getComputedStyle(e),l=parseFloat(s.getPropertyValue("--hit-left")),b=parseFloat(s.getPropertyValue("--hit-bottom"));return {href:e.href,x:l>1?r.left-l/2:r.left+r.width/2,y:l>1?r.top+r.height/2:r.bottom+b/2}}')
    await context.route(target['href'],lambda route:route.fulfill(status=200,body='<title>External link test</title>'))
    before=page.url
    async with page.expect_popup() as popup_event:await page.mouse.click(target['x'],target['y'])
    popup=await popup_event.value
    if page.url!=before:report['failures'].append([lang,section,'guide replaced'])
    await popup.close();await context.unroute(target['href']);report['outside_text_clicks']+=1
  await browser.close()
 print(json.dumps(report,ensure_ascii=False));return bool(report['failures'])
if __name__=='__main__':sys.exit(asyncio.run(main()))
