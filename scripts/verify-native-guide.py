import asyncio,json,re
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT.parent/'work'/'native-guide';OUT.mkdir(parents=True,exist_ok=True);allpaths=sorted(p.relative_to(ROOT) for lang in ['pt','en','es'] for p in (ROOT/lang).rglob('index.html'))
async def main():
 report={'pages':0,'layouts':0,'errors':[],'whatsapp':{},'requests':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await b.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)))
  for width in [390,1440,1920]:
   await page.set_viewport_size({'width':width,'height':1000})
   for path in allpaths:
    r=await page.goto('http://127.0.0.1:8000/'+str(path),wait_until='load');await page.evaluate('document.fonts.ready')
    result=await page.evaluate('''()=>{const r=e=>{const a=e.getBoundingClientRect();return {x:a.x,y:a.y,w:a.width,h:a.height}};const wa=document.querySelector('.site-whatsapp');const toolbar=document.querySelector('.site-toolbar');const native=document.body.classList.contains('native-guide');return {overflow:document.documentElement.scrollWidth>innerWidth+1,wa:wa?r(wa):null,toolbar:toolbar?[...toolbar.children].map(r):[],broken:[...document.images].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.src),native,panels:[...document.querySelectorAll('.native-panel')].map(r),photos:[...document.querySelectorAll('.native-photo')].map(r),vector:document.querySelectorAll('.native-card h2').length};}''')
    assert r.status==200,(path,r.status)
    assert not result['overflow'],('overflow',width,path)
    assert not result['broken'],('broken',path,result['broken'])
    wa=result['wa'];assert wa and abs(width-wa['x']-wa['w']-(16 if width<761 else 18))<1 and abs(1000-wa['y']-wa['h']-(16 if width<761 else 18))<1,('whatsapp',width,path,wa)
    if result['native']:
     assert result['vector']>0
     if width>760:
      panel=result['panels'][0];buttons=result['toolbar'];mid=(buttons[0]['x']+buttons[-1]['x']+buttons[-1]['w'])/2
      assert abs(mid-(panel['x']+panel['w']/2))<1,('menu centre',path)
      gaps=[buttons[i+1]['x']-buttons[i]['x']-buttons[i]['w'] for i in range(len(buttons)-1)]
      assert max(gaps)-min(gaps)<.1,('menu gaps',path,gaps)
      assert all(abs(x['x'])<.1 for x in result['photos']),('photo left gutter',path)
    if width in [390,1440] and str(path) in ['pt/informacoes/index.html','pt/localizacao/index.html','pt/comodidades/index.html','pt/checkin/index.html','pt/restaurantes/index.html','pt/estabelecimentos/index.html']:
     await page.screenshot(path=str(OUT/(str(path).split('/')[1]+f'-{width}.png')),full_page=True)
    report['layouts']+=1
   print('Verified',width,len(allpaths),'pages',flush=True)
  report['pages']=len(allpaths)
  # Verify links through their visible text, including entire click targets.
  for path in ['pt/informacoes/','pt/estabelecimentos/','pt/restaurantes/','en/transportation/','es/actividades/']:
   await page.goto('http://127.0.0.1:8000/'+path)
   for a in await page.locator('.native-link').all():await a.click(trial=True,timeout=3000)
  # Amenity navigation is centred in the description column.
  await page.goto('http://127.0.0.1:8000/pt/comodidades/')
  assert await page.evaluate('''()=>{const a=document.querySelector('.section-panel').getBoundingClientRect(),n=document.querySelector('.site-pagination').getBoundingClientRect();return Math.abs(a.x+a.width/2-n.x-n.width/2)<1}''')
  await b.close()
 OUT.joinpath('report.json').write_text(json.dumps(report,indent=2));print(report)
asyncio.run(main())
