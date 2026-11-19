"""Exercise route links, unavailable states and the 30-minute browser refresh."""
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse, parse_qs
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    instant = datetime(2026, 11, 17, 12, tzinfo=timezone.utc)
    checks = 0
    for lang, route in [('pt', 'localizacao'), ('en', 'location'), ('es', 'ubicacion')]:
        for scenario in ('missing', 'valid', 'expired'):
            page = browser.new_page(viewport={'width': 390, 'height': 900})
            page.clock.install(time=instant)
            page.clock.pause_at(instant)
            page.route('**/world-clocks.js*', lambda route: route.fulfill(body='', content_type='text/javascript'))
            requests = []
            def respond(route):
                requests.append(route.request.url)
                age = timedelta(hours=-1) if scenario == 'expired' else timedelta(minutes=30)
                data = {'available': False, 'reason': 'not_configured'} if scenario == 'missing' else {
                    'available': True,
                    'updatedAt': instant.isoformat(), 'expiresAt': (instant + age).isoformat(),
                    'routes': [{'id': 'sdu', 'available': True, 'minutes': 20, 'distanceMeters': 8300}, {'id': 'gig', 'available': True, 'minutes': 50, 'distanceMeters': 20000}]
                }
                import json
                route.fulfill(body=json.dumps(data), content_type='application/json')
            page.route('**/api/airport-transfers*', respond)
            page.goto(f'http://127.0.0.1:8000/{lang}/{route}/')
            page.wait_for_function("document.querySelector('[data-transfer-status]').textContent.length>0")
            outputs = page.locator('[data-transfer-time]').all_text_contents()
            if scenario == 'valid':
                assert all(outputs) and '20 min' in outputs[0] and '50 min' in outputs[1]
                with page.expect_response('**/api/airport-transfers*'):
                    page.clock.run_for(30 * 60 * 1000 + 1000)
                assert len(requests) == 2, requests
            else:
                assert not any(outputs), (scenario, outputs)
            for index, link in enumerate(page.locator('.airport-route').all()):
                query = parse_qs(urlparse(link.get_attribute('href')).query)
                assert 'Raul Pompéia, 131' in query['destination'][0]
                assert ('Santos Dumont' if index == 0 else 'Galeão') in query['origin'][0]
                assert query['travelmode'] == ['driving']
                link.click(trial=True)
            assert page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth')
            page.close()
            checks += 1
    browser.close()
print(f'{checks} browser scenarios passed: correct airport-to-building links, no invented/stale times, 30-minute refresh.')
