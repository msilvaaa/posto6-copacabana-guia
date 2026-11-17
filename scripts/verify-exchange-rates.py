"""Check the 2x2 bank layout, quote precision and three-hour refresh."""
from datetime import datetime, timedelta, timezone
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    now = datetime(2026, 11, 17, 12, tzinfo=timezone.utc)
    for lang, route in [('pt', 'informacoes'), ('en', 'information'), ('es', 'informacion')]:
        page = browser.new_page()
        page.clock.install(time=now)
        page.clock.pause_at(now)
        calls = []
        def reply(route):
            calls.append(route.request.url)
            quotes = [dict(id=key, base=base, target=target, ask=ask, quotedAt=now.isoformat()) for key, base, target, ask in [('usd-tourism','USD','BRL',6.2),('ars','ARS','BRL',0.003725),('eur','EUR','BRL',6.36),('brl','BRL','USD',0.173)]]
            route.fulfill(content_type='application/json', body=json.dumps({'available': True, 'quotes': quotes, 'checkedAt': now.isoformat(), 'expiresAt': (now + timedelta(hours=3)).isoformat()}))
        page.route('**/api/exchange-rates', reply)
        page.goto(f'http://127.0.0.1:8000/{lang}/{route}/')
        page.wait_for_function("document.querySelector('[data-exchange-unit]').textContent.length>0")
        assert page.locator('.exchange-rate').count() == 4
        assert all(text != '—' for text in page.locator('.exchange-rate output').all_text_contents())
        assert '003725' in page.locator('[data-exchange-id="ars"] output').inner_text()
        assert 'US$' in page.locator('[data-exchange-id="brl"] output').inner_text()
        for width in (390, 1440):
            page.set_viewport_size({'width': width, 'height': 1000})
            rects = [a.bounding_box() for a in page.locator('.bank-links a').all()]
            assert len(rects) == 4
            assert abs(rects[0]['x']-rects[1]['x'])<1 and abs(rects[2]['x']-rects[3]['x'])<1
            assert rects[2]['x'] > rects[0]['x'] and rects[1]['y'] > rects[0]['y']
            assert page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth')
            for link in page.locator('.bank-links a').all():link.click(trial=True)
        with page.expect_response('**/api/exchange-rates'):
            page.clock.run_for(3*3600000+1000)
        assert len(calls) == 2
        page.close()
    page = browser.new_page()
    page.route('**/api/exchange-rates', lambda route: route.fulfill(content_type='application/json', body='{"available":false}'))
    page.goto('http://127.0.0.1:8000/pt/informacoes/')
    page.wait_for_function("document.querySelector('[data-exchange-status]').textContent.includes('indisponíveis')")
    assert all(text == '—' for text in page.locator('.exchange-rate output').all_text_contents())
    page = browser.new_page()
    page.route('**/api/exchange-rates', reply)
    page.goto('http://127.0.0.1:8000/pt/informacoes/')
    page.locator('.bank-links').locator('..').screenshot(path='/workspace/work/banks-and-exchange.png')
    browser.close()
print('3 languages: bank links in 2x2, quote precision, 3-hour refresh; unavailable rates never fabricated.')
