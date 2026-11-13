#!/usr/bin/env python3
"""Verify stable pagination, unique toolbars and preserved navigation on every guide page."""
import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://127.0.0.1:8000'
PAGES = json.loads((ROOT / 'data/guide-pages.json').read_text())
OUT = ROOT.parent / 'work/guide-navigation'
OUT.mkdir(parents=True, exist_ok=True)


def route(page):
    return '/' + page['path'].removesuffix('index.html')


async def main():
    report = {'pages': len(PAGES), 'layouts': 0, 'pagination_clicks': 0, 'slow_image_checks': 0, 'failures': []}
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = await browser.new_page()
        for width in [320, 768, 1440]:
            await page.set_viewport_size({'width': width, 'height': 1000})
            for item in PAGES:
                path = route(item)
                response = await page.goto(BASE + path, wait_until='load')
                geometry = await page.evaluate('''()=>{
                  const image=document.querySelector('.guide-image').getBoundingClientRect();
                  const footer=document.querySelector('.guide-pagination').getBoundingClientRect();
                  const buttons=[...document.querySelectorAll('.guide-pagination a')].map(e=>e.getBoundingClientRect());
                  const controlBounds=buttons.length?[Math.min(...buttons.map(r=>r.left)),Math.max(...buttons.map(r=>r.right))]:null;
                  return {
                    below:footer.top>=image.bottom-.5 && buttons.every(r=>r.top>=image.bottom),
                    centered:!controlBounds||Math.abs((controlBounds[0]+controlBounds[1])/2-(image.left+image.width/2))<1,
                    readable:buttons.every(r=>r.height>=44),
                    overflow:document.documentElement.scrollWidth>innerWidth,
                    loaded:[...document.images].every(i=>i.complete&&i.naturalWidth>0),
                    legacy:!!document.querySelector('.modern-prev,.modern-next,.modern-home,.detail-modern-prev,.detail-modern-next,.main-html-topbar,.pdf-toolbar'),
                    home:document.querySelectorAll('.guide-home').length,
                    flags:document.querySelectorAll('.guide-flag').length
                  };
                }''')
                if (response.status != 200 or not all(geometry[k] for k in ['below', 'centered', 'readable', 'loaded'])
                        or geometry['overflow'] or geometry['legacy'] or geometry['home'] != 1 or geometry['flags'] != 3):
                    report['failures'].append({'path': path, 'width': width, 'geometry': geometry, 'http': response.status})
                for selector, href in [('.guide-previous', item['previous']), ('.guide-next', item['next'])]:
                    if href and await page.locator(selector).get_attribute('href') != href:
                        report['failures'].append({'path': path, 'reason': 'incorrect destination', 'selector': selector})
                report['layouts'] += 1
        # Click every previous/next control once; do not infer working links from HTML alone.
        for item in PAGES:
            for selector, expected in [('.guide-previous', item['previous']), ('.guide-next', item['next'])]:
                if not expected:
                    continue
                await page.goto(BASE + route(item))
                async with page.expect_navigation() as navigation:
                    await page.locator(selector).click()
                response = await navigation.value
                if response.status != 200 or not page.url.endswith(expected):
                    report['failures'].append({'path': route(item), 'reason': 'click failed', 'target': expected})
                report['pagination_clicks'] += 1
        # Hold the main JPEG response until after the initial footer position is measured.
        slow_items = [item for item in PAGES if item['image']['src'].endswith('-12.jpg') or item['path'].endswith('/tvsala/index.html')]
        for width in [320, 1440]:
            await page.set_viewport_size({'width': width, 'height': 1000})
            for item in slow_items:
                gate = asyncio.Event()
                async def delay_image(request_route):
                    await gate.wait()
                    await request_route.continue_()
                pattern = '**' + item['image']['src']
                await page.route(pattern, delay_image)
                await page.goto(BASE + route(item), wait_until='domcontentloaded')
                await page.wait_for_function("getComputedStyle(document.querySelector('.guide-pagination')).display==='flex'")
                before = await page.locator('.guide-pagination').evaluate('e=>e.getBoundingClientRect().top+scrollY')
                gate.set()
                await page.locator('.guide-image').evaluate('i=>i.decode()')
                after = await page.locator('.guide-pagination').evaluate('e=>e.getBoundingClientRect().top+scrollY')
                if abs(before - after) > .5:
                    report['failures'].append({'path': route(item), 'width': width, 'reason': 'footer moved on image load', 'before': before, 'after': after})
                await page.unroute(pattern, delay_image)
                report['slow_image_checks'] += 1
        await browser.close()
    (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False))
    return bool(report['failures'])


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
