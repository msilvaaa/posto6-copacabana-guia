"""Render amenity instructions as actual text beside authentic photographs."""
import json,re
from pathlib import Path
from html import escape,unescape
from guide_native import title_word_art
from site_components import LABELS,toolbar,pagination,whatsapp,dialogs,page_title,arrow,app_icon
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/amenity-native.json').read_text())
TITLES=json.loads((ROOT/'data/detail-title-art.json').read_text())

def e(v):return escape(str(v),quote=True)

def build_detail(page,photos):
 key=page['path'].split('/')[-2];detail=DATA[key];lang=page['lang'];title=detail['title'][lang]
 title_art=title_word_art(page['image']['src'],TITLES[page['image']['src']]['word'],page['image']['width'],page['image']['height'])
 labels={'pt':('Como usar','Fotos de referência','Assista ao vídeo','Foto de referência'), 'en':('How to use','Reference photos','Watch the video','Reference photo'), 'es':('Cómo usar','Fotos de referencia','Ver el vídeo','Foto de referencia')}[lang]
 photo=detail['photo']
 if isinstance(photo,int):
  p=photos[photo];src=p['src'];width=p['width'];height=p['height']
 elif photo=='lock':src='/assets/checkin/entrada-fechadura-original.jpg';width=2088;height=1418
 else:src='/assets/rules/edificio-copacabana.webp';width=1001;height=1570
 source='/comod-assets/pt-'+('lavabo' if key=='banheiro' else key)+'-1.jpg'
 figures=[]
 for i,(x,y,w,h) in enumerate(detail['references']):
  caption=f'{labels[3]} {i+1}'
  figures.append(f'<figure class="technical-reference" style="max-width:{w}px"><svg viewBox="{x} {y} {w} {h}" width="{w}" height="{h}" role="img" aria-label="{e(caption)}"><defs><clipPath id="reference-{i}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath></defs><image href="{source}" width="900" height="1350" clip-path="url(#reference-{i})"/></svg><figcaption>{e(caption)}</figcaption></figure>')
 items=''.join(f'<li>{e(t)}</li>' for t in detail['copy'][lang])
 copy=f'<section class="detail-instructions"><h2>{labels[0]}</h2><'+('ol' if detail['ordered'] else 'ul')+f' class="instruction-list">{items}</'+('ol' if detail['ordered'] else 'ul')+'></section>'
 urls=list(dict.fromkeys(unescape(u) for u in re.findall(r'href="([^"]+)"',page['source_text']) if u.startswith('http')))
 videos=''.join(f'<a class="native-link detail-video" href="{e(u)}" target="_blank" rel="noopener noreferrer">{app_icon()}<span>{labels[2]}</span></a>' for u in urls)
 refs=f'<section class="detail-references"><h2>{labels[1]}</h2><div class="reference-grid">{"".join(figures)}</div></section>' if figures else ''
 navigation=pagination(lang,page['previous'],page['next']) if page['previous'] or page['next'] else f'<a class="site-step" href="{e(page["back"]["href"])}">{arrow(True)}<span>{e(page["back"]["label"].removeprefix("← "))}</span></a>'
 nav=toolbar(lang,page['languages'],home_href=page['back']['href'],home_label=page['back']['label'].removeprefix('← '))
 return f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<title>{e(page_title(lang,title))}</title><meta name="description" content="{e(page['description'])}"/>
<link rel="stylesheet" href="/site-shell.css?v=20261124-larger-home"/><link rel="stylesheet" href="/native-guide.css?v=20261119-theme"/>
<link rel="stylesheet" href="/guide-titles.css?v=20261119-colorful"/>
<script src="/site.js?v=20261124-weather-symbol" defer></script><link rel="stylesheet" href="/theme.css?v=20261119-dashboard-toggle"/>
<script src="/theme.js?v=20261119-dashboard-toggle"></script>
<script src="/airbnb-rating.js?v=20261119-entry-refresh" defer></script>
<link rel="stylesheet" href="/icon-frames.css?v=20261119-1"/>
</head>
<body class="site-page native-guide amenity-detail"><div class="site-frame"><main class="site-reading" aria-label="{LABELS[lang]['reading']}">
<section class="native-chapter"><div class="native-visual"><div class="native-photo"><img src="{e(src)}" width="{width}" height="{height}" alt="{e(title)}" style="object-position:50% 50%"/></div></div>
<div class="native-panel"><div class="native-toolbar">{nav}</div><h1 class="native-title original-heading"><span class="native-title-text">{e(title)}</span>{title_art}</h1>{copy}{videos}{refs}
<div class="native-actions"><nav class="site-pagination guide-pagination" aria-label="{LABELS[lang]['navigation']}">{navigation}</nav></div>
</div></section></main></div>{whatsapp(lang,page['path'])}{dialogs(lang)}</body></html>'''
