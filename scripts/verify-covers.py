import asyncio,json,hashlib,sys
from datetime import datetime, timezone
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent / "work" / "copacabana-verification"
OUT.mkdir(parents=True, exist_ok=True)
async def main():
 report={'verified_at':datetime.now(timezone.utc).isoformat(),'viewports':[],'links':{},'failures':[]}
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await browser.new_page(device_scale_factor=1)
  for width in [320,390,768,1100,1280,1440,1664,1920]:
   reference=None
   for lang in ['pt','en','es']:
    await page.set_viewport_size({'width':width,'height':1000})
    errors=[]
    def failed(request): errors.append(request.url)
    page.on('requestfailed',failed)
    response=await page.goto(f'http://127.0.0.1:8000/{lang}/',wait_until='networkidle')
    await page.evaluate('document.fonts.ready')
    result=await page.evaluate('''()=>{
      const rect=e=>{const r=e.getBoundingClientRect(); return [r.x,r.y,r.width,r.height].map(n=>Math.round(n*100)/100)};
      const buttons=[...document.querySelectorAll('.cover-html-button')];
      const toolbar=[...document.querySelectorAll('.main-html-topbar a')];
      const overflow=[...document.querySelectorAll('a')].filter(e=>{const r=e.getBoundingClientRect(); return r.left<0||r.right>innerWidth+.5});
      return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
        images:[...document.images].every(i=>i.complete&&i.naturalWidth>0),
        buttons:buttons.map(rect),toolbar:toolbar.map(rect),
        sources:buttons.map(e=>e.querySelector('img').getAttribute('src')),
        overflow:overflow.map(e=>e.outerHTML),
        links:[...document.querySelectorAll('a[href^="/"]')].map(e=>e.getAttribute('href'))};
    }''')
    photo_ok=await page.locator('.home-cover-photo').evaluate("""async e=>{
      const background=getComputedStyle(e).backgroundImage;
      const image=new Image(); image.src='/assets/copacabana-drummond.jpg';
      try { await image.decode(); return image.naturalWidth>0 && background.includes('/assets/copacabana-drummond.jpg'); }
      catch { return false; }
    }""")
    checks={
      'http':response.status==200,'images':result['images'], '15_buttons':len(result['buttons'])==15,
      'no_horizontal_scroll':result['scrollWidth']==width,'controls_in_viewport':not result['overflow'],
      'requests':not errors, 'background_photo':photo_ok,
    }
    if reference:
     checks['same_button_geometry']=result['buttons']==reference['buttons']
     checks['same_toolbar_geometry']=result['toolbar']==reference['toolbar']
     checks['same_images']=result['sources']==reference['sources']
    else: reference=result
    for i,a in enumerate(result['toolbar']):
     for b in result['toolbar'][i+1:]:
      if a[0]<b[0]+b[2] and a[0]+a[2]>b[0] and a[1]<b[1]+b[3] and a[1]+a[3]>b[1]:
       checks['toolbar_no_overlap']=False
    for name,ok in checks.items():
     if not ok: report['failures'].append(f'{lang} {width}: {name}')
    report['viewports'].append({'language':lang,'width':width,'checks':checks})
    for href in result['links']:
     if href not in report['links']:
      r=await page.request.get('http://127.0.0.1:8000'+href)
      report['links'][href]=r.status
      if r.status!=200: report['failures'].append(f'link {href}: {r.status}')
    if width in [390,1440]:
     await page.screenshot(path=str(OUT/f'{lang}-{width}.png'),full_page=True)
    # Verify the image can actually receive a click through its navigation link.
    await page.locator('.cover-html-button').first.click(trial=True)
    home=page.locator('.main-html-topbar a').first
    await home.hover()
    await page.wait_for_timeout(220)
    transform=await home.evaluate('e=>getComputedStyle(e).transform')
    if not transform.endswith('-3)'): report['failures'].append(f'{lang} {width}: hover {transform}')
    await page.mouse.move(0,999)
    page.remove_listener('requestfailed',failed)
  # Language controls must open the selected language in the same browser.
  for lang in ['pt','en','es']:
   for target in ['es','pt','en']:
    await page.goto('http://127.0.0.1:8000/'+lang+'/')
    async with page.expect_navigation() as navigation:
     await page.locator(f'.main-html-topbar .detail-modern-flag[href="/{target}/"]').click()
    response=await navigation.value
    if response.status!=200 or not page.url.endswith('/'+target+'/'):
     report['failures'].append(f'language {lang} -> {target}')
  # Every menu destination must be reached by an actual browser click once.
  for lang in ['pt','en','es']:
   for index in range(15):
    await page.goto('http://127.0.0.1:8000/'+lang+'/')
    link=page.locator('.cover-html-button').nth(index)
    expected=await link.get_attribute('href')
    async with page.expect_navigation() as nav:
     await link.click()
    r=await nav.value
    if r.status!=200 or not page.url.endswith(expected):
     report['failures'].append('click '+expected)
  await browser.close()
 report['unique_icons']=len({v['src'] for v in json.loads((ROOT/'data/cover-art.json').read_text()).values()})
 if report['unique_icons'] != 15: report['failures'].append('expected 15 distinct icons')
 (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps({'pages':len(report['viewports']),'links':len(report['links']),'unique_icons':report['unique_icons'],'failures':report['failures']},ensure_ascii=False,indent=2))
 return 1 if report['failures'] else 0
sys.exit(asyncio.run(main()))
