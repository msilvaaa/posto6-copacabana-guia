#!/usr/bin/env python3
"""Audit all generated routes for rasterized text, distortion, and broken images."""
import argparse,json,re
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://127.0.0.1:8000');parser.add_argument('--fixtures');parser.add_argument('--output',default=str(ROOT.parent/'work/visual-quality-report.json'));args=parser.parse_args()
paths=sorted(str(p.relative_to(ROOT)).replace('index.html','') for lang in ['pt','en','es'] for p in (ROOT/lang).rglob('index.html'))
fixtures={}
if args.fixtures:
 for item in json.loads(Path(args.fixtures).read_text()):
  if 'error' not in item:fixtures[item['source']]=Path(item['path']).read_bytes()
photo_pixels={}
for photo in json.loads((ROOT/'data/apartment-photos.json').read_text()):
 for variant in photo['variants']:
  photo_pixels[variant['src']]=(variant['width'],variant['height'])
 photo_pixels[photo['src']]=(photo['width'],photo['height'])
report={'routes':len(paths),'layouts':0,'errors':[],'hero_upscale':[],'technical_references':0,'raster_text_panels':0,'original_photo_sources':len(fixtures)}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);context=browser.new_context(device_scale_factor=2)
 if fixtures:
  context.route('https://a0.muscache.com/**',lambda route:route.fulfill(body=fixtures[route.request.url],content_type='image/jpeg') if route.request.url in fixtures else route.continue_())
 page=context.new_page();page.on('pageerror',lambda error:report['errors'].append(str(error)))
 for width in [390,1440,1920]:
  page.set_viewport_size({'width':width,'height':1000})
  for path in paths:
   response=page.goto(args.base+'/'+path,wait_until='load',timeout=45000);page.evaluate('document.fonts.ready')
   data=page.evaluate('''()=>{
    const box=e=>e.getBoundingClientRect();
    const images=[...document.images].filter(e=>e.complete&&e.naturalWidth);
    const distorted=images.filter(e=>{const r=box(e),s=getComputedStyle(e);return !e.src.endsWith('.svg')&&r.width>30&&r.height>30&&s.objectFit==='fill'&&Math.abs(r.width/r.height-e.naturalWidth/e.naturalHeight)>.03;}).map(e=>e.src);
    const heroes=[...document.querySelectorAll('.native-photo>img,.section-photo')].map(e=>{const r=box(e);return {src:e.currentSrc,width:r.width,height:r.height,pixelWidth:e.naturalWidth,pixelHeight:e.naturalHeight}});
    const references=[...document.querySelectorAll('.technical-reference>svg')].map(e=>{const r=box(e);const v=e.viewBox.baseVal;return {scale:Math.max(r.width/v.width,r.height/v.height),ratio:r.width/r.height-v.width/v.height};});
    return {overflow:document.documentElement.scrollWidth>innerWidth+1,broken:[...document.images].filter(e=>e.complete&&!e.naturalWidth).map(e=>e.src),distorted,heroes,references,rasterText:document.querySelectorAll('.guide-image,.native-rules-grid image,.guide-title-word image').length,headings:[...document.querySelectorAll('h1')].map(e=>e.textContent.trim()),wa:document.querySelectorAll('.site-whatsapp').length};
   }''')
   issues=[]
   if response.status!=200:issues.append('HTTP '+str(response.status))
   if data['overflow']:issues.append('horizontal overflow')
   if data['broken']:issues.append('broken images '+str(data['broken']))
   if data['distorted']:issues.append('distorted images '+str(data['distorted']))
   if data['rasterText']:issues.append('rasterized text panel')
   if data['wa']!=1:issues.append('WhatsApp button count')
   if not data['headings'] or not all(data['headings']):issues.append('empty heading')
   if any(r['scale']>1.01 or abs(r['ratio'])>.01 for r in data['references']):issues.append('enlarged/distorted technical photograph')
   for hero in data['heroes']:
    key=hero['src'].replace(args.base,'')
    pw,ph=photo_pixels.get(key,(hero['pixelWidth'],hero['pixelHeight']))
    hero['scale']=max(hero['width']/pw,hero['height']/ph)
    if hero['scale']>1.25:report['hero_upscale'].append({'path':path,'width':width,**hero})
   report['technical_references']+=len(data['references']);report['raster_text_panels']+=data['rasterText']
   if issues:report['errors'].append({'path':path,'width':width,'issues':issues})
   report['layouts']+=1
  print(f'Checked {len(paths)} pages at {width}px / DPR 2',flush=True)
 # A reference photograph must remain stationary while reading long instructions.
 page.set_viewport_size({'width':1440,'height':900});page.goto(args.base+'/pt/bancos/');page.evaluate("document.querySelector('.site-reading').scrollTop=100");page.wait_for_timeout(100)
 report['sticky_photo_top']=page.locator('.native-photo').bounding_box()['y']
 if abs(report['sticky_photo_top'])>1:report['errors'].append('Main photo failed sticky positioning')
 # All technical Home controls return to the amenities section in their language.
 for lang in ['pt','en','es']:
  page.goto(args.base+f'/{lang}/comodidades/fechadura/');report.setdefault('detail_home',{})[lang]=page.locator('.guide-home').get_attribute('href')
 # Verify the credential QR image remains decodable after replacement with vector paths.
 page.goto(args.base+'/pt/wifi/');page.emulate_media(reduced_motion='reduce');page.locator('.wifi-scan-group').screenshot(path=str(Path(args.output).with_suffix('.qr.png')))
 browser.close()
Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))
if report['errors'] or report['hero_upscale']:raise SystemExit(1)
