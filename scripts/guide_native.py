"""Render readable guide chapters with HTML copy and independent photographs."""
from html import escape
import json
from pathlib import Path
from urllib.parse import urlencode
from site_components import LABELS, toolbar, pagination, whatsapp, dialogs, page_title

ORIGINAL_ART = json.loads((Path(__file__).resolve().parents[1] / 'data/guide-original-art.json').read_text())


def artwork(source, rect, css=''):
    x,y,w,h=rect
    # The SVG viewport displays the original artwork without resampling or editing it.
    return (f'<svg class="original-art {e(css)}" viewBox="{x} {y} {w} {h}" aria-hidden="true">'
            f'<image href="{e(source)}" width="1537" height="{2592 if source.endswith("-12.jpg") else 1728 if source.endswith("-13.jpg") else 864}"/></svg>')


def title_word_art(source, word=None):
    x,y,w,h=word or ORIGINAL_ART[source]['word']
    height=2592 if source.endswith('-12.jpg') else 1728 if source.endswith('-13.jpg') else 864
    return (f'<svg class="compact-title-art" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}" aria-hidden="true">'
            f'<image href="{e(source)}" width="1537" height="{height}"/></svg>')


def illustration(name):
    if name == 'fast-clock':
        return ('<svg viewBox="0 0 80 80" fill="none" stroke="#173f45" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                '<circle cx="49" cy="45" r="24" fill="#edf5f3"/><path d="M43 12h12M49 12v9m17 3 4-4M49 30v15l10 6M6 33h17M2 45h18M7 57h16"/>'
                '<circle cx="49" cy="45" r="2" fill="#173f45" stroke="none"/></svg>')
    if name == 'plane-trail':
        # Reveal the original right wing beyond the old viewport, without nearby text or bullets.
        return ('<svg class="original-art plane-trail" viewBox="1137 473 90 188" style="overflow:visible" aria-hidden="true">'
                '<defs><mask id="airport-plane-art" maskUnits="userSpaceOnUse" x="1137" y="473" width="104" height="188">'
                '<rect x="1137" y="473" width="104" height="188" fill="white"/>'
                '<rect x="1223" y="495" width="13" height="13" fill="black"/>'
                '<rect x="1223" y="586" width="13" height="14" fill="black"/></mask></defs>'
                '<image href="/assets/pt-04.jpg" width="1537" height="864" mask="url(#airport-plane-art)"/></svg>')
    item=ORIGINAL_ART['_illustrations'].get(name)
    if name=='wifi-monitor':
        # Exclude the overlapping Wi-Fi badge from the original monitor's corner.
        return ('<svg class="original-art wifi-monitor" viewBox="1170 182 271 220" aria-hidden="true">'
                '<defs><clipPath id="wifi-monitor-clip"><path d="M1170 182H1441V402H1240V372H1170Z"/></clipPath></defs>'
                '<image href="/assets/pt-05.jpg" width="1537" height="864" clip-path="url(#wifi-monitor-clip)"/></svg>')
    return artwork(item['src'],item['rect'],name) if item else icon(name)


def e(value):
    return escape(str(value), quote=True)


PATHS = {
    'pin': '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    'bank': '<path d="m2 8 10-6 10 6ZM3 21h18M5 9v9m7-9v9m7-9v9M3 18h18"/>',
    'money': '<rect x="2" y="5" width="20" height="14" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M5 9v6m14-6v6"/>',
    'pencil': '<path d="m4 16 12-12 4 4L8 20l-5 1ZM14 6l4 4M4 16l4 4"/>',
    'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m3 6 9 7 9-7"/>',
    'case': '<rect x="3" y="6" width="18" height="15" rx="3"/><path d="M8 6V3h8v3M8 10v7m8-7v7"/>',
    'key': '<circle cx="8" cy="8" r="5"/><path d="m12 12 9 9m-5-5 3-3m0 6 3-3"/>',
    'wifi': '<path d="M2 7a17 17 0 0 1 20 0M5 11a12 12 0 0 1 14 0m-11 4a7 7 0 0 1 8 0"/><circle cx="12" cy="20" r="1"/>',
    'home': '<path d="m2 11 10-9 10 9M5 9v12h14V9M9 21v-8h6v8"/>',
    'bed': '<path d="M2 8v13m20-13v13M2 17h20M4 8V4h16v4M2 11h20v6H2Z"/>',
    'sofa': '<path d="M5 12V5h14v7M2 11h4v7h12v-7h4v10H2ZM5 21v2m14-2v2"/>',
    'water': '<path d="M12 2S4 11 4 16a8 8 0 0 0 16 0c0-5-8-14-8-14ZM8 16a4 4 0 0 0 4 4"/>',
    'kitchen': '<path d="M5 2v7m4-7v7M2 2v7c0 3 10 3 10 0V2M7 12v10m13 0V2c-7 2-7 13 0 13"/>',
    'car': '<path d="m3 10 2-6h14l2 6M2 10h20v9H2ZM5 19v3m14-3v3M5 14h2m10 0h2"/>',
    'bus': '<rect x="4" y="2" width="16" height="18" rx="3"/><path d="M4 11h16M8 2v9m8 4h1M7 15h1M7 20v2m10-2v2"/>',
    'transport': '<rect x="5" y="2" width="14" height="17" rx="4"/><path d="M5 11h14M9 2v9M8 15h1m6 0h1M8 19l-3 4m11-4 3 4M7 21h10"/>',
    'plane': '<path d="m2 15 8-5V3c0-2 4-2 4 0v7l8 5v3l-8-3v5l3 2H7l3-2v-5l-8 3Z"/>',
    'shield': '<path d="m12 2 9 4v6c0 6-9 10-9 10S3 18 3 12V6ZM8 12l3 3 5-6"/>',
    'people': '<circle cx="9" cy="7" r="4"/><path d="M2 22v-5a7 7 0 0 1 14 0v5M17 3a4 4 0 0 1 0 8m2 3c3 1 3 4 3 8"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 5v7l5 3"/>',
    'check': '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="m7 12 4 4 7-8"/>',
    'info': '<circle cx="12" cy="12" r="10"/><path d="M12 10v7m0-11v1"/>',
    'medical': '<path d="M8 2h8v6h6v8h-6v6H8v-6H2V8h6Z"/>',
    'fire': '<path d="M12 2c1 6 7 7 7 13a7 7 0 0 1-14 0c0-3 2-5 4-7-1 5 2 6 2 6s3-5 1-12Z"/>',
    'food': '<path d="M5 2v7m4-7v7M2 2v7c0 3 10 3 10 0V2M7 12v10m13 0V2c-7 2-7 13 0 13"/>',
    'coffee': '<path d="M3 7h14v8a6 6 0 0 1-6 6H9a6 6 0 0 1-6-6ZM17 8h2a3 3 0 0 1 0 6h-2M6 2v2m5-2v2m5-2v2"/>',
    'glass': '<path d="M5 2h14v6a7 7 0 0 1-14 0ZM12 15v7M6 22h12M5 7h14"/>',
    'leaf': '<path d="M20 3C3 1-1 17 8 21c8 4 13-6 12-18ZM4 22l12-14"/>',
    'cart': '<path d="M1 2h3l4 15h12l3-11H5M9 21h1m8 0h1"/>',
    'bag': '<path d="M4 7h16l2 15H2ZM8 8V6a4 4 0 0 1 8 0v2"/>',
    'bread': '<path d="M5 10a5 5 0 0 1 1-9 6 6 0 0 1 12 0 5 5 0 0 1 1 9v12H5Z"/>',
    'gift': '<path d="M2 8h20v5H2ZM4 13v9h16v-9M12 8v14m0-14S1 8 4 3s8 5 8 5 5-10 8-5-8 5-8 5Z"/>',
    'bike': '<circle cx="5" cy="17" r="4"/><circle cx="19" cy="17" r="4"/><path d="m5 17 5-10 6 10H5m10-14h3l1 14M8 7h5"/>',
    'fitness': '<path d="m3 8 13 13M8 3l13 13M2 10l8-8m4 20 8-8M6 6l12 12"/>',
    'landmark': '<path d="M3 22V8h4V4h3v4h4V4h3v4h4v14ZM9 22v-6h6v6"/>',
    'mountain': '<path d="m1 22 8-16 5 8 3-6 6 14ZM6 12l3 3 3-3"/>',
    'bin': '<path d="M3 5h18M9 5V2h6v3M5 5l1 17h12l1-17M10 9v9m4-9v9"/>',
    'tv': '<rect x="2" y="3" width="20" height="15" rx="2"/><path d="M8 22h8m-4-4v4"/>',
    'snow': '<path d="M12 1v22M2 6l20 12M2 18 22 6M8 3l4 4 4-4M8 21l4-4 4 4M3 10l5-1-1-5m10 16-1-5 5-1M3 14l5 1-1 5m10-16-1 5 5 1"/>',
    'fridge': '<rect x="5" y="1" width="14" height="22" rx="2"/><path d="M5 9h14M8 4v2m0 7v4"/>',
    'bulb': '<path d="M8 18c0-4-4-5-4-10a8 8 0 0 1 16 0c0 5-4 6-4 10ZM8 21h8M10 24h4"/>',
    'wash': '<rect x="3" y="1" width="18" height="22" rx="2"/><path d="M3 6h18M6 3h1m3 0h1"/><circle cx="12" cy="14" r="5"/>',
    'door': '<path d="M4 23V2h16v21M4 2l12 3v18H4ZM12 13h1"/>',
    'iron': '<path d="M2 19h20l-3-9H8c-4 0-6 5-6 9ZM10 6h6l3 4M5 22h14"/>',
    'lamp': '<path d="M8 2h8l5 12H3ZM12 14v8M7 22h10"/>',
    'safe': '<rect x="2" y="2" width="20" height="20" rx="2"/><rect x="5" y="5" width="14" height="14" rx="1"/><circle cx="13" cy="12" r="3"/><path d="M7 9v6"/>',
}


def icon(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">' + PATHS.get(name, PATHS['info']) + '</svg>')


def photograph(page, chapter, upgrades, photos):
    image = page['image']
    upgrade = next((p for suffix, p in upgrades.items() if image['src'].endswith(suffix)), None)
    if image['src'].endswith('-02.jpg'):
        upgrade = photos[0]
    if upgrade:
        label = upgrade.get('alt', {})
        label = label.get(page['lang'], '') if isinstance(label, dict) else label
        if upgrade.get('crop'):
            viewport = ' '.join(str(value) for value in upgrade['crop'])
            return (f'<svg class="native-cropped-photo" viewBox="{viewport}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{e(label)}">'
                    f'<image href="{e(upgrade["src"])}" width="{upgrade["width"]}" height="{upgrade["height"]}"/></svg>')
        variants = upgrade.get('variants', [])
        srcset = ' srcset="' + e(', '.join(f'{v["src"]} {v["width"]}w' for v in variants)) + '" sizes="(max-width:760px) 100vw, max(70vw,150vh)"' if variants else ''
        position=e(upgrade.get('position','50% 50%'))
        preserve_ratio=' data-preserve-ratio' if upgrade.get('preserve_ratio') else ''
        return f'<img src="{e(upgrade["src"])}" width="{upgrade["width"]}" height="{upgrade["height"]}" alt="{e(label)}" style="object-position:{position}"{srcset}{preserve_ratio}/>'
    # Crop only the photograph. The old text, icons and page seams are excluded.
    y = chapter.get('tile', 0) * 864 + 2
    return (f'<svg viewBox="2 {y} 1063 860" preserveAspectRatio="xMidYMid slice" '
            f'role="img" aria-label="{e(image["alt"])}">'
            f'<image href="{e(image["src"])}" width="{image["width"]}" height="{image["height"]}"/></svg>')


def wifi_access(lang, source):
    scan = {'pt': 'ESCANEIE', 'en': 'SCAN ME', 'es': 'ESCANEA'}[lang]
    return (f'<svg class="original-art wifi-access-art" viewBox="1135 180 310 463" role="img" aria-label="{e(LABELS[lang].get("wifi", "Wi-Fi"))}">'
            '<defs><clipPath id="wifi-upper-art"><rect x="1135" y="180" width="310" height="368"/></clipPath>'
            '<clipPath id="wifi-original-qr"><rect x="1258" y="548" width="98" height="95"/></clipPath></defs>'
            f'<image href="{e(source)}" width="1537" height="864" clip-path="url(#wifi-upper-art)"/>'
            '<g class="wifi-screen-signal" aria-hidden="true"><circle cx="1404" cy="219" r="17" fill="#173f45" fill-opacity=".75"/>'
            '<g fill="none" stroke="white" stroke-width="2" stroke-linecap="round">'
            '<path class="wifi-signal-outer" d="M1393 216q11-10 22 0"/><path class="wifi-signal-inner" d="M1397 221q7-6 14 0"/>'
            '<path d="M1401 225q3-2 6 0"/></g><circle cx="1404" cy="229" r="1.5" fill="white"/></g>'
            '<g class="wifi-scan-group">'
            f'<image href="{e(source)}" width="1537" height="864" clip-path="url(#wifi-original-qr)"/>'
            '<path d="M1162 582h59v-7l18 16-18 16v-7h-59Z" fill="#f0273e"/>'
            f'<text x="1191" y="594" text-anchor="middle" fill="white" font-family="Arial,Helvetica,sans-serif" font-size="9" font-weight="700">{scan}</text>'
            '</g></svg>')


def sea_conditions(lang):
    title, waves, wind, gusts, loading, note = {
        'pt': ('Mar e ventos · Copacabana', 'Ondas', 'Vento', 'Rajadas', 'Consultando previsão…', 'Previsão regional para a orla. Siga a sinalização dos guarda-vidas.'),
        'en': ('Sea and wind · Copacabana', 'Waves', 'Wind', 'Gusts', 'Checking forecast…', 'Regional coastal forecast. Follow the lifeguards’ beach flags and instructions.'),
        'es': ('Mar y viento · Copacabana', 'Olas', 'Viento', 'Ráfagas', 'Consultando previsión…', 'Previsión regional para la costa. Sigue las banderas e indicaciones de los socorristas.'),
    }[lang]
    return (f'<section class="sea-conditions native-card" data-sea-conditions aria-labelledby="sea-title"><h2 id="sea-title">{e(title)}</h2>'
            f'<dl class="sea-values"><div><dt>{e(waves)}</dt><dd><strong data-sea-value="waveHeight">—</strong> <small data-sea-period></small></dd></div>'
            f'<div><dt>{e(wind)}</dt><dd><strong data-sea-value="windSpeed">—</strong> <small data-sea-direction></small></dd></div>'
            f'<div><dt>{e(gusts)}</dt><dd><strong data-sea-value="windGusts">—</strong></dd></div></dl>'
            f'<p class="sea-status" data-sea-status role="status">{e(loading)}</p><p class="sea-note">{e(note)} '
            '<a href="https://open-meteo.com/" target="_blank" rel="noopener noreferrer">Open-Meteo</a></p></section>')


def local_clocks(lang):
    labels = {
        'pt': ('Horários locais', ['Brasil — Brasília', 'EUA — Washington, D.C.', 'Itália — Roma', 'Argentina — Buenos Aires', 'Singapura — Singapura', 'Reino Unido — Londres'], 'Fusos e horário de verão ajustados automaticamente para as cidades indicadas.'),
        'en': ('Local times', ['Brazil — Brasília', 'USA — Washington, D.C.', 'Italy — Rome', 'Argentina — Buenos Aires', 'Singapore — Singapore', 'United Kingdom — London'], 'Time zones and daylight saving time adjust automatically for the cities shown.'),
        'es': ('Horas locales', ['Brasil — Brasilia', 'EE. UU. — Washington, D. C.', 'Italia — Roma', 'Argentina — Buenos Aires', 'Singapur — Singapur', 'Reino Unido — Londres'], 'Las zonas horarias y el horario de verano se ajustan automáticamente para las ciudades indicadas.'),
    }
    heading, cities, note = labels[lang]
    zones = ['America/Sao_Paulo', 'America/New_York', 'Europe/Rome', 'America/Argentina/Buenos_Aires', 'Asia/Singapore', 'Europe/London']
    flags = ['/assets/flag-pt.png', '/assets/flag-en.png', '/assets/flags/it.svg', '/assets/flags/ar.svg', '/assets/flags/sg.svg', '/assets/flags/gb.svg']
    clocks = ''.join(f'<div class="local-clock" data-time-zone="{zone}"><h3><img class="local-clock-flag" src="{flag}" alt="{e(city.split(" — ")[0])}" width="32" height="32"/><span>{e(city.split(" — ")[1])}</span></h3><time data-clock-time>--:--:--</time><span data-clock-date></span><small data-clock-offset></small></div>' for city, zone, flag in zip(cities, zones, flags))
    return f'<section class="native-card local-clocks" aria-labelledby="local-clocks-title"><h2 id="local-clocks-title">{e(heading)}</h2><div class="local-clocks-grid">{clocks}</div><p>{e(note)}</p></section>'


def airport_transfers(lang):
    labels = {
        'pt': ('Até Rua Raul Pompéia, 131 — Copacabana', 'Ver trajeto até o prédio', 'Consulte o tempo atual no Google Maps.', 'Aeroporto Santos Dumont — SDU', 'Aeroporto Internacional do Galeão — GIG'),
        'en': ('To Rua Raul Pompéia, 131 — Copacabana', 'View route to the building', 'Check the current travel time on Google Maps.', 'Santos Dumont Airport — SDU', 'Galeão International Airport — GIG'),
        'es': ('Hasta Rua Raul Pompéia, 131 — Copacabana', 'Ver trayecto hasta el edificio', 'Consulta el tiempo actual en Google Maps.', 'Aeropuerto Santos Dumont — SDU', 'Aeropuerto Internacional de Galeão — GIG'),
    }
    _destination, action, fallback, sdu, gig = labels[lang]
    airports = [('sdu', sdu, 'Aeroporto Santos Dumont (SDU), Rio de Janeiro, RJ, Brasil', 'https://maps.app.goo.gl/iq6CcoLazX9RHe7dA'), ('gig', gig, 'Aeroporto Internacional do Galeão (GIG), Terminal 2, Rio de Janeiro, RJ, Brasil', 'https://maps.app.goo.gl/fYKyHM98FECg4Rh37')]
    rows = []
    for airport_id, name, origin, place in airports:
        route = 'https://www.google.com/maps/dir/?' + urlencode({'api': '1', 'origin': origin, 'destination': 'Rua Raul Pompéia, 131, Copacabana, Rio de Janeiro, RJ, Brasil', 'travelmode': 'driving'})
        rows.append(f'<div class="airport-transfer"><a class="native-link" href="{place}" target="_blank" rel="noopener noreferrer">{icon("pin")}<span>{e(name)}</span></a><output data-transfer-time="{airport_id}"></output><a class="airport-route" href="{e(route)}" target="_blank" rel="noopener noreferrer">{e(action)}</a></div>')
    return f'<div class="airport-transfers" data-airport-transfers>{"".join(rows)}<p class="transfer-status" data-transfer-status>{e(fallback)}</p><p class="transfer-status" data-transfer-note></p></div>'


def exchange_rates(lang):
    labels = {
        'pt': ('Cotações', ['Dólar turismo', 'Peso argentino', 'Euro', 'Real'], 'Referências para turismo: dólar turismo; demais moedas, compra comercial. Base: US$ 1. IOF e tarifas podem variar.', 'Carregando cotações…', 'Fonte'),
        'en': ('Exchange rates', ['Tourist US dollar', 'Argentine peso', 'Euro', 'Brazilian real'], 'Travel references: tourist dollar; other currencies use market buy rates. Base: US$ 1. Taxes and fees may vary.', 'Loading exchange rates…', 'Source'),
        'es': ('Cotizaciones', ['Dólar turismo', 'Peso argentino', 'Euro', 'Real brasileño'], 'Referencias para turismo: dólar turismo; demás monedas, compra comercial. Base: US$ 1. Los impuestos y las comisiones pueden variar.', 'Cargando cotizaciones…', 'Fuente'),
    }
    heading, names, note, loading, source = labels[lang]
    ids = ['usd-tourism', 'ars', 'eur', 'brl']
    flags = ['/assets/flag-en.png', '/assets/flags/ar.svg', '/assets/flags/eu.svg', '/assets/flag-pt.png']
    cards = ''.join(f'<div class="exchange-rate" data-exchange-id="{key}"><h4><img class="exchange-flag" src="{flag}" alt="{e(name)}" title="{e(name)}" width="28" height="28"/></h4><output>—</output><small data-exchange-unit></small><time></time></div>' for key, name, flag in zip(ids, names, flags))
    return f'<section class="exchange-rates" data-exchange-rates aria-labelledby="exchange-title"><h3 id="exchange-title">{e(heading)}</h3><div class="exchange-grid">{cards}</div><p data-exchange-status>{e(loading)}</p><p>{e(note)} <a href="https://docs.awesomeapi.com.br/api-de-moedas" target="_blank" rel="noopener noreferrer">{e(source)}: AwesomeAPI</a></p></section>'


def build_native(page, content, upgrades, photos):
    lang = page['lang']
    title = content['title'][lang]
    chapters = []
    for index, chapter in enumerate(content['chapters']):
        parts = []
        for section_index, section in enumerate(chapter['sections']):
            if page['image']['src'].endswith('-05.jpg') and section_index<2:
                accessible=' '.join(e(item['text'][lang]) for item in section['items'])
                parts.append(f'<section class="native-card native-wifi-accessible"><h2>{e(section["title"][lang])}</h2><p>{accessible}</p></section>')
                continue
            if page['image']['src'].endswith('-06.jpg') and section_index==0:
                accessible=' '.join(e(item['text'][lang]) for item in section['items'])
                parts.append(f'<section class="native-card native-art-accessible"><h2>{e(section["title"][lang])}</h2><p>{accessible}</p></section>')
                continue
            nodes = []
            descriptions=[]
            for item in section['items']:
                text = e(item['text'][lang])
                if item.get('href'):
                    href = item.get('href_by_lang', {}).get(lang, item['href'])
                    external = ' target="_blank" rel="noopener noreferrer"' if href.startswith(('https://', 'http://')) else ''
                    nodes.append(f'<a class="native-link" href="{e(href)}"{external}>{icon("pin") if href.startswith("https://maps") else ""}<span>{text}</span></a>')
                else:
                    nodes.append(f'<p>{text}</p>')
                    descriptions.append(f'<p>{text}</p>')
            if page['image']['src'].endswith('-10.jpg') and section_index == 0:
                nodes = ['<div class="bank-links">' + ''.join(nodes) + '</div>']
            if page['image']['src'].endswith('-10.jpg') and section_index == 4:
                nodes = ['<div class="agency-links"><div>' + ''.join(nodes[:3]) + '</div><div>' + ''.join(nodes[3:]) + '</div></div>']
            if page['image']['src'].endswith('-10.jpg') and section_index == 1:
                nodes.append(exchange_rates(lang))
            if page['image']['src'].endswith('-04.jpg') and section_index == 2:
                nodes = [airport_transfers(lang)]
            if page['image']['src'].endswith('-12.jpg') and section_index<len(ORIGINAL_ART['_restaurants'][index]):
                links=''.join(node for node in nodes if node.startswith('<a '))
                parts.append(f'<section class="native-card native-restaurant-card"><h2 class="native-title-text">{e(section["title"][lang])}</h2>{links}{"".join(descriptions)}</section>')
                continue
            name=section['icon']
            if page['image']['src'].endswith('-04.jpg'):
                name=['phone-map','plane-trail','fast-clock'][section_index]
            elif page['image']['src'].endswith('-05.jpg'):
                name=['wifi','wifi-qr','info'][section_index]
            elif page['image']['src'].endswith('-07.jpg') and section_index==3:
                name='uber'
            elif page['image']['src'].endswith('-09.jpg'):
                name=['landmark','mountain','bike','fitness'][section_index]
            elif page['image']['src'].endswith('-13.jpg'):
                name=(['bag','cart','market'] if index==0 else ['bread','coffee','craft'])[section_index]
            elif page['image']['src'].endswith('-14.jpg'):
                name=['samu','shield','hospital','pharmacy','fire'][section_index]
            elif page['image']['src'].endswith('-11.jpg'):
                name=['glass','coffee-bars'][section_index]
            elif page['image']['src'].endswith('-06.jpg'):
                name=['rule','people'][section_index]
            elif page['image']['src'].endswith('-03.jpg') and section_index==1:
                name='parking'
            room_index=None
            if page['image']['src'].endswith('-02.jpg'):
                room_index=[0,0,2,4,3][section_index]
            if room_index is not None:
                room=photos[room_index]
                image_src=next((v['src'] for v in room.get('variants',[]) if v['width']==720),room['src'])
                art=f'<img class="native-room-thumb" src="{e(image_src)}" alt="{e(section["title"][lang])}" width="100" height="100"/>'
            else:
                art=illustration(name)
                if page['image']['src'].endswith('-05.jpg') and section_index==2:
                    art=''
                if page['image']['src'].endswith('-03.jpg') and section_index==0:
                    art='<img class="native-room-thumb" src="/assets/cover-photos/checkin-porta-apartamento.jpg" width="76" height="76" alt=""/>'
                elif page['image']['src'].endswith('-13.jpg') and index==0 and section_index==0:
                    art='<img class="original-brand" src="/assets/brands/americanas.svg" alt="" width="76" height="24"/>'
            if page['image']['src'].endswith('-02.jpg') and section_index==0:
                art=''
            if page['image']['src'].endswith('-04.jpg') and section_index==1:
                art=''
            extra=''
            if page['image']['src'].endswith('-06.jpg') and section_index==0:
                extra=f'<div class="native-art-strip">{illustration("rules-strip")}</div>'
            elif page['image']['src'].endswith('-11.jpg') and section_index==0:
                extra='<div class="native-bar-photos">'+''.join(artwork('/assets/pt-11.jpg',rect) for rect in ORIGINAL_ART['_bar_photos'])+'</div>'
            heading = f'<h2>{e(section["title"][lang])}</h2>'
            if page['image']['src'].endswith('-09.jpg') and section_index == 0:
                weather = f'<button type="button" class="activity-weather" data-weather-open aria-label="{e(LABELS[lang]["weather"])}"><span aria-hidden="true">☀</span><span>Copacabana</span><small data-weather-summary>{e(LABELS[lang]["weather_hint"])}</small></button>'
                heading = f'<div class="native-heading-text">{heading}{weather}</div>'
            airport = page['image']['src'].endswith('-04.jpg') and section_index==2
            card_class = ' airport-card' if airport else ''
            plane = f'<div class="airport-plane" aria-hidden="true">{illustration("plane-trail")}</div>' if airport else ''
            icon_markup = f'<span class="native-icon original-illustration {e(name)}">{art}</span>'
            if page['image']['src'].endswith('-04.jpg') and section_index==0:
                address = section['items'][0]
                icon_markup = (f'<a class="native-icon original-illustration {e(name)}" href="{e(address["href"])}" '
                               f'target="_blank" rel="noopener noreferrer" aria-label="{e(address["text"][lang])}">{art}</a>')
            parts.append(f'<section class="native-card illustrated-card{card_class}">{extra}<div class="native-card-heading">{icon_markup}{heading}</div><div class="native-card-copy">{"".join(nodes)}</div>{plane}</section>')
        if page['image']['src'].endswith('-14.jpg'):
            parts = [parts[0], '<div class="emergency-services">' + parts[1] + parts[4] + '</div>', *parts[2:4]]
        if page['image']['src'].endswith('-04.jpg'):
            parts.append(local_clocks(lang))
        navigation = ''
        if index == len(content['chapters']) - 1:
            navigation = f'<div class="native-actions"><nav class="site-pagination guide-pagination" aria-label="{LABELS[lang]["navigation"]}">{pagination(lang, page["previous"], page["next"])}</nav></div>'
            if page['image']['src'].endswith('-15.jpg') and lang=='pt':
                navigation=f'<div class="native-art-hero native-thanks">{illustration("thanks")}</div>'+navigation
        title_art=title_word_art(page['image']['src'])
        if page['image']['src'].endswith('-03.jpg'):
            # Reuse the original handwritten Check- and in glyphs, with an uppercase C.
            title_art = ('<svg class="compact-title-art" viewBox="0 0 133 32" width="133" height="32" aria-hidden="true">'
                         '<svg x="0" y="0" width="102" height="32" viewBox="1246 132 102 32"><image href="/assets/pt-15.jpg" width="1537" height="864"/></svg>'
                         '<svg x="102" y="0" width="31" height="32" viewBox="1353 108 31 32"><image href="/assets/pt-03.jpg" width="1537" height="864"/></svg></svg>')
        heading = f'<span class="native-title-text">{e(title)}</span>{title_art}'
        top = f'<div class="native-toolbar">{toolbar(lang, page["languages"])}</div><h1 class="native-title original-heading">{heading}</h1>' if index == 0 else ''
        if index==0 and page['image']['src'].endswith('-14.jpg'):
            top+=sea_conditions(lang)
        if index==0 and page['image']['src'].endswith('-05.jpg'):
            top+=f'<div class="native-wifi-access">{wifi_access(lang,page["image"]["src"])}</div>'
        if index==0 and page['image']['src'].endswith('-06.jpg'):
            top+=f'<div class="native-rules-grid">{artwork(page["image"]["src"],[1104,210,411,435])}</div>'
        subtitle = f'<h2 class="native-chapter-title">{e(chapter["title"][lang])}</h2>' if chapter.get('title') else ''
        chapters.append(f'<section class="native-chapter"><div class="native-visual"><div class="native-photo">{photograph(page, chapter, upgrades, photos)}</div></div><div class="native-panel">{top}{subtitle}{"".join(parts)}{navigation}</div></section>')
    clocks_script = '\n  <script src="/world-clocks.js?v=20261117-1" defer></script>\n  <script src="/airport-transfers.js?v=20261117-1" defer></script>' if page['image']['src'].endswith('-04.jpg') else ''
    exchange_script = '\n  <script src="/exchange-rates.js?v=20261117-4" defer></script>' if page['image']['src'].endswith('-10.jpg') else ''
    sea_script = '\n  <script type="module" src="/sea-conditions.js?v=20261118-1"></script>' if page['image']['src'].endswith('-14.jpg') else ''
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
  <title>{e(page_title(lang,title))}</title>
  <meta name="description" content="{e(page['description'])}"/>
  <link rel="stylesheet" href="/site-shell.css?v=20261116-34"/>
  <link rel="stylesheet" href="/native-guide.css?v={"20261118-6" if page["image"]["src"].endswith("-04.jpg") else "20261118-1" if page["image"]["src"].endswith("-03.jpg") else "20261118-7" if page["image"]["src"].endswith("-10.jpg") else "20261118-8" if page["image"]["src"].endswith("-05.jpg") else "20261118-10" if page["image"]["src"].endswith("-14.jpg") else "20261116-34"}"/>
  <script src="/site.js?v=20261116-34" defer></script>{clocks_script}{exchange_script}{sea_script}
</head>
<body class="site-page native-guide">
  <div class="site-frame"><main class="site-reading" aria-label="{LABELS[lang]['reading']}">{''.join(chapters)}</main></div>
  {whatsapp(lang,page['path'])}
  {dialogs(lang)}
</body>
</html>
'''
