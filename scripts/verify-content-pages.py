#!/usr/bin/env python3
"""Verify menu destinations, translated pages, photos and section language switches."""
import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / 'work/copacabana-verification'
OUT.mkdir(parents=True, exist_ok=True)
content = json.loads((ROOT / 'templates/cover-content.json').read_text())
labels = json.loads((ROOT / 'templates/apartment-content.json').read_text())


async def main():
    report = {'pages': 0, 'menu_clicks': 0, 'language_switches': 0, 'failures': []}
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = await browser.new_page()
        for width in [320, 390, 768, 1440]:
            await page.set_viewport_size({'width': width, 'height': 1000})
            for lang in content:
                for section, title in [(1, 'apartment_title'), (4, 'gallery_title')]:
                    route = content[lang]['nav'][section]['href']
                    response = await page.goto('http://127.0.0.1:8000' + route)
                    await page.locator('img').evaluate_all('imgs=>Promise.all(imgs.map(i=>{i.loading="eager";return i.decode()}))')
                    layout = await page.evaluate('''()=>({
                      overflow:document.documentElement.scrollWidth>innerWidth,
                      language:document.documentElement.lang,
                      active:location.pathname,
                      images:[...document.images].every(i=>i.complete&&i.naturalWidth>0)
                    })''')
                    if (response.status != 200 or layout['overflow'] or not layout['images']
                            or layout['language'] != lang or layout['active'] != route
                            or await page.locator('h1').inner_text() != labels[lang][title]):
                        report['failures'].append(f'{width} {route}: content/layout')
                    if section == 4 and await page.locator('.photo-grid img').count() != 8:
                        report['failures'].append(route + ': expected 8 apartment photos')
                    report['pages'] += 1
        await page.set_viewport_size({'width': 1440, 'height': 1000})
        for lang in content:
            for index, link in enumerate(content[lang]['cover_nav']):
                await page.goto(f'http://127.0.0.1:8000/{lang}/')
                async with page.expect_navigation() as navigation:
                    await page.locator('.home-cover-nav a').nth(index).click()
                response = await navigation.value
                if response.status != 200 or not page.url.endswith(link['href']):
                    report['failures'].append(f'{lang}: menu {link["label"]}')
                report['menu_clicks'] += 1
            for section in [1, 4]:
                for target in content:
                    await page.goto('http://127.0.0.1:8000' + content[lang]['nav'][section]['href'])
                    async with page.expect_navigation() as navigation:
                        await page.get_by_role('link', name={'pt':'Português','en':'English','es':'Español'}[target], exact=True).click()
                    response = await navigation.value
                    expected = content[target]['nav'][section]['href']
                    if response.status != 200 or not page.url.endswith(expected):
                        report['failures'].append(f'{lang} -> {target}: section {section}')
                    report['language_switches'] += 1
        await browser.close()
    (OUT / 'content-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False))
    return bool(report['failures'])


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
