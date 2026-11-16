"""Render readable guide chapters with HTML copy and independent photographs."""
from html import escape
from site_components import LABELS, toolbar, pagination, whatsapp, dialogs


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
        variants = upgrade.get('variants', [])
        srcset = ' srcset="' + e(', '.join(f'{v["src"]} {v["width"]}w' for v in variants)) + '" sizes="(max-width:760px) 100vw, max(70vw,150vh)"' if variants else ''
        position=e(upgrade.get('position','50% 50%'))
        return f'<img src="{e(upgrade["src"])}" width="{upgrade["width"]}" height="{upgrade["height"]}" alt="{e(label)}" style="object-position:{position}"{srcset}/>'
    # Crop only the photograph. The old text, icons and page seams are excluded.
    y = chapter.get('tile', 0) * 864 + 2
    return (f'<svg viewBox="2 {y} 1063 860" preserveAspectRatio="xMidYMid slice" '
            f'role="img" aria-label="{e(image["alt"])}">'
            f'<image href="{e(image["src"])}" width="{image["width"]}" height="{image["height"]}"/></svg>')


def build_native(page, content, upgrades, photos):
    lang = page['lang']
    title = content['title'][lang]
    chapters = []
    for index, chapter in enumerate(content['chapters']):
        parts = []
        for section in chapter['sections']:
            nodes = []
            for item in section['items']:
                text = e(item['text'][lang])
                if item.get('href'):
                    href = item.get('href_by_lang', {}).get(lang, item['href'])
                    external = ' target="_blank" rel="noopener noreferrer"' if href.startswith(('https://', 'http://')) else ''
                    nodes.append(f'<a class="native-link" href="{e(href)}"{external}>{icon("pin") if href.startswith("https://maps") else ""}<span>{text}</span></a>')
                else:
                    nodes.append(f'<p>{text}</p>')
            parts.append(f'<section class="native-card"><div class="native-card-heading"><span class="native-icon">{icon(section["icon"])}</span><h2>{e(section["title"][lang])}</h2></div><div class="native-card-copy">{"".join(nodes)}</div></section>')
        navigation = ''
        if index == len(content['chapters']) - 1:
            navigation = f'<div class="native-actions"><nav class="site-pagination guide-pagination" aria-label="{LABELS[lang]["navigation"]}">{pagination(lang, page["previous"], page["next"])}</nav></div>'
        top = f'<div class="native-toolbar">{toolbar(lang, page["languages"])}</div><h1 class="native-title">{e(title)}</h1>' if index == 0 else ''
        subtitle = f'<h2 class="native-chapter-title">{e(chapter["title"][lang])}</h2>' if chapter.get('title') else ''
        chapters.append(f'<section class="native-chapter"><div class="native-visual"><div class="native-photo">{photograph(page, chapter, upgrades, photos)}</div></div><div class="native-panel">{top}{subtitle}{"".join(parts)}{navigation}</div></section>')
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
  <title>Posto 6 Copacabana — {e(title)}</title>
  <meta name="description" content="{e(page['description'])}"/>
  <link rel="stylesheet" href="/site-shell.css?v=20261116-34"/>
  <link rel="stylesheet" href="/native-guide.css?v=20261116-34"/>
  <script src="/site.js?v=20261116-34" defer></script>
</head>
<body class="site-page native-guide">
  <div class="site-frame"><main class="site-reading" aria-label="{LABELS[lang]['reading']}">{''.join(chapters)}</main></div>
  {whatsapp(lang)}
  {dialogs(lang)}
</body>
</html>
'''
