"""Check the 2x2 bank layout, quote precision and daily refresh."""
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
            quotes = [dict(id=key, base=base, target=target, bid=bid, quotedAt=now.isoformat()) for key, base, target, bid in [('usd-tourism','USD','BRL',5.7),('ars','USD','ARS',1552.23),('eur','USD','EUR',0.90911),('brl','USD','BRL',5.7792)]]
            route.fulfill(content_type='application/json', body=json.dumps({'available': True, 'side': 'buy', 'basis': 'USD', 'quotes': quotes, 'checkedAt': now.isoformat(), 'expiresAt': (now + timedelta(hours=24)).isoformat()}))
        page.route('**/economia.awesomeapi.com.br/**', lambda route: route.fulfill(status=429, body='', headers={'Access-Control-Allow-Origin':'*'}))
        page.route('**/api/exchange-rates', reply)
        page.goto(f'http://127.0.0.1:8000/{lang}/{route}/')
        page.wait_for_function("document.querySelector('[data-exchange-unit]').textContent.length>0")
        assert page.locator('.exchange-rate').count() == 4
        assert page.locator('.exchange-rate h4 img').count() == 4
        cards = page.locator('.native-card.illustrated-card')
        assert cards.nth(0).locator('[data-exchange-rates]').count() == 0
        assert cards.nth(1).locator('[data-exchange-rates]').count() == 1
        assert all(text != '—' for text in page.locator('.exchange-rate output').all_text_contents())
        assert '155223' in page.locator('[data-exchange-id="ars"] .exchange-value').inner_text().replace('.', '').replace(',', '')
        assert 'R$' in page.locator('[data-exchange-id="brl"] .exchange-value').inner_text()
        assert all('US$ 1 = ' in text for text in page.locator('.exchange-rate output').all_text_contents())
        caption = 'buy rate · tourism' if lang == 'en' else 'compra · turismo'
        assert page.locator('[data-exchange-unit]').all_text_contents() == [caption] * 4
        for width in (390, 1440):
            page.set_viewport_size({'width': width, 'height': 1000})
            rects = [a.bounding_box() for a in page.locator('.bank-links a').all()]
            assert len(rects) == 4
            assert abs(rects[0]['x']-rects[1]['x'])<1 and abs(rects[2]['x']-rects[3]['x'])<1
            assert rects[2]['x'] > rects[0]['x'] and rects[1]['y'] > rects[0]['y']
            assert page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth')
            for link in page.locator('.bank-links a').all():link.click(trial=True)
        with page.expect_response('**/api/exchange-rates'):
            page.clock.run_for(24*3600000+1000)
        assert len(calls) == 2
        page.close()
    page = browser.new_page()
    page.route('**/economia.awesomeapi.com.br/**', lambda route: route.fulfill(status=429, body='', headers={'Access-Control-Allow-Origin':'*'}))
    page.route('**/api/exchange-rates', lambda route: route.fulfill(content_type='application/json', body='{"available":false}'))
    page.goto('http://127.0.0.1:8000/pt/informacoes/')
    page.wait_for_function("document.querySelector('[data-exchange-status]').textContent.includes('indisponíveis')")
    assert all(text == '—' for text in page.locator('.exchange-rate output').all_text_contents())
    page = browser.new_page()
    page.clock.install(time=now)
    page.clock.pause_at(now)
    direct_calls = []
    def direct_reply(route):
        direct_calls.append(route.request.url)
        raw = {key: {'bid': str(bid), 'ask': str(bid+1), 'timestamp': str(int(now.timestamp()))} for key, bid in [('USDBRLT',5.7),('USDARS',1552.23),('USDEUR',0.90911),('USDBRL',5.7792)]}
        route.fulfill(content_type='application/json', body=json.dumps(raw), headers={'Access-Control-Allow-Origin':'*'})
    page.route('**/economia.awesomeapi.com.br/**', direct_reply)
    page.goto('http://127.0.0.1:8000/pt/informacoes/')
    page.wait_for_function("document.querySelector('[data-exchange-unit]').textContent.length>0")
    assert '5,70' in page.locator('[data-exchange-id="usd-tourism"] .exchange-value').inner_text()
    page.reload()
    page.wait_for_function("document.querySelector('[data-exchange-unit]').textContent.length>0")
    assert len(direct_calls) == 1, direct_calls
    with page.expect_response('**/economia.awesomeapi.com.br/**'):
        page.clock.run_for(24*3600000+1000)
    assert len(direct_calls) == 2
    page.locator('[data-exchange-rates]').screenshot(path='/workspace/work/daily-exchange-flags.png')
    browser.close()
print('3 languages: bank links in 2x2, quote precision, daily refresh; unavailable rates never fabricated.')
