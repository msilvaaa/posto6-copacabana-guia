#!/usr/bin/env python3
"""Verify persistent navigation, common sections, forecast, photo return and WhatsApp."""
import asyncio,json,sys
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'work/site-experience';OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:8000'
async def main():
 report={'pages':0,'fixed_footer_checks':0,'gallery_returns':0,'forecast_checks':0,'external_tabs':0,'failures':[]}
 paths=sorted({str(p.parent.relative_to(ROOT))+'/' for lang in ['pt','en','es'] for p in (ROOT/lang).rglob('index.html')})
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  context=await browser.new_context(viewport={'width':390,'height':844},device_scale_factor=2)
  page=await context.new_page()
  for path in paths:
   await page.goto(BASE+'/'+path,wait_until='load')
   if await page.locator('[data-weather-open]').count()!=(1 if path.count('/')==1 else 0) or await page.locator('.site-whatsapp').count()!=1:
    report['failures'].append(path+': missing utilities');continue
   if await page.locator('.site-back,.site-enlarge').count():report['failures'].append(path+': removed page controls still present')
   wa=page.locator('.site-whatsapp')
   props=await wa.evaluate('e=>({circle:getComputedStyle(e).borderRadius,w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height,footer:!!e.closest("footer,nav,.site-header"),number:e.getAttribute("href")})')
   if props['w']!=props['h'] or props['circle']!='50%' or props['footer'] or props['number']!='https://wa.me/5521981020150':
    report['failures'].append(path+': WhatsApp location/shape')
   if await page.locator('.site-frame').count():
    await page.locator('.site-reading').evaluate('e=>e.scrollTop=e.scrollHeight')
    footer=await page.locator('.site-pagination').evaluate('e=>e.getBoundingClientRect().toJSON()')
    wa_rect=await wa.evaluate('e=>e.getBoundingClientRect().toJSON()')
    reading=await page.locator('.site-reading').evaluate('e=>e.getBoundingClientRect().toJSON()')
    if footer['bottom']>845 or footer['top']<reading['bottom']-.5 or wa_rect['bottom']>reading['bottom']+.5:
     report['failures'].append(path+': footer overlaps content/contact')
    before=footer['top'];await page.locator('.site-reading').evaluate('e=>e.scrollTop=0')
    after=await page.locator('.site-pagination').evaluate('e=>e.getBoundingClientRect().top')
    if abs(before-after)>.5:report['failures'].append(path+': footer moves on scroll')
    report['fixed_footer_checks']+=1
   if await page.evaluate('document.documentElement.scrollWidth>innerWidth'):report['failures'].append(path+': overflow')
   report['pages']+=1
  for lang,apartment,gallery,amenities in [('pt','apartamento','galeria','comodidades'),('en','apartment','gallery','amenities'),('es','apartamento','galeria','comodidades')]:
   for section in [apartment,gallery,amenities]:
    await page.goto(f'{BASE}/{lang}/{section}/')
    if await page.locator('.section-layout').count()!=1 or await page.locator('.guide-home').get_attribute('href')!=f'/{lang}/':report['failures'].append(lang+'/'+section+': inconsistent section')
   await page.goto(f'{BASE}/{lang}/{amenities}/')
   if await page.locator('.amenity-card').count()!=16:report['failures'].append(lang+': amenities missing')
   await page.goto(f'{BASE}/{lang}/{gallery}/')
   url=page.url
   await page.locator('.photo-grid a').first.click()
   await page.locator('[data-photo-dialog]').wait_for(state='visible')
   image=page.locator('[data-photo-stage] img');await image.evaluate('i=>i.decode()')
   if await image.evaluate('i=>i.naturalWidth')<2500:report['failures'].append(lang+': photo not high resolution')
   await page.locator('[data-photo-native]').click()
   await page.locator('[data-photo-close]').click()
   if page.url!=url or await page.locator('[data-photo-dialog]').is_visible():report['failures'].append(lang+': gallery return failed')
   report['gallery_returns']+=1
   await page.goto(f'{BASE}/{lang}/')
   await page.locator('[data-weather-open]').click()
   await page.wait_for_function("document.querySelectorAll('.weather-day').length===3")
   if not await page.locator('[data-weather-dialog]').is_visible():report['failures'].append(lang+': forecast dialog missing')
   await page.locator('[data-weather-close]').click();report['forecast_checks']+=1
   restaurants={'pt':'restaurantes','en':'restaurants','es':'restaurantes'}[lang]
   await page.goto(f'{BASE}/{lang}/{restaurants}/')
   # Do not contact the external site: verify the new-tab boundary using a local response.
   external=page.locator('.guide-link[href^="https://"]').first
   destination=await external.get_attribute('href')
   await context.route(destination,lambda request_route:request_route.fulfill(status=200,body='<title>External destination</title>'))
   original=page.url
   async with page.expect_popup() as popup_event:await external.click()
   popup=await popup_event.value
   if page.url!=original:report['failures'].append(lang+': guide replaced by external destination')
   await popup.close();await context.unroute(destination);report['external_tabs']+=1
  await browser.close()
 (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False))
 return bool(report['failures'])
if __name__=='__main__':sys.exit(asyncio.run(main()))
