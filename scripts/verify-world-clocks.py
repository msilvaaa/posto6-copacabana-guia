"""Check real clock rendering against IANA rules, including seasonal offsets."""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from playwright.sync_api import sync_playwright

ROUTES = {'pt': 'localizacao', 'en': 'location', 'es': 'ubicacion'}
DATES = ['2026-01-15T12:00:00+00:00', '2026-07-15T12:00:00+00:00', '2026-12-31T23:30:00+00:00']

def check(page, instant):
    for clock in page.locator('[data-time-zone]').all():
        zone = clock.get_attribute('data-time-zone')
        local = instant.astimezone(ZoneInfo(zone))
        assert clock.locator('time').inner_text() == local.strftime('%H:%M'), (zone, instant)
        assert clock.locator('time').get_attribute('datetime') == instant.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        offset = int(local.utcoffset().total_seconds() / 3600)
        assert clock.locator('[data-clock-offset]').inner_text() in ({'UTC', 'UTC+0'} if offset == 0 else {f'UTC{offset:+d}'})

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(timezone_id='Asia/Tokyo')
    count = 0
    for lang, route in ROUTES.items():
        for date in DATES:
            page = context.new_page()
            instant = datetime.fromisoformat(date)
            page.clock.install(time=instant)
            page.clock.pause_at(instant)
            page.goto(f'http://127.0.0.1:8000/{lang}/{route}/')
            assert page.locator('[data-time-zone]').count() == 6
            check(page, instant)
            page.close()
            count += 6
    page = context.new_page()
    instant = datetime.fromisoformat('2026-03-08T06:59:59+00:00')
    page.clock.install(time=instant)
    page.clock.pause_at(instant)
    page.goto('http://127.0.0.1:8000/en/location/')
    check(page, instant)
    page.clock.run_for(1000)
    check(page, instant + timedelta(seconds=1))
    assert page.locator('[data-time-zone="America/New_York"] time').inner_text() == '03:00'
    for width in (390, 1440):
        page.set_viewport_size({'width': width, 'height': 1000})
        assert page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth')
    browser.close()
print(f'{count} seasonal/midnight clock checks passed in 3 languages, independent of browser zone; DST transition and live ticking passed.')
