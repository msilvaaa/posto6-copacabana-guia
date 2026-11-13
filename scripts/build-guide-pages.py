#!/usr/bin/env python3
"""Generate the original image-based guide with stable, shared HTML navigation."""
import json
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    'pt': {'home': 'Início', 'toolbar': 'Início e idiomas', 'pagination': 'Navegação entre páginas', 'previous': 'Anterior', 'next': 'Próximo'},
    'en': {'home': 'Home', 'toolbar': 'Home and languages', 'pagination': 'Page navigation', 'previous': 'Previous', 'next': 'Next'},
    'es': {'home': 'Inicio', 'toolbar': 'Inicio e idiomas', 'pagination': 'Navegación entre páginas', 'previous': 'Anterior', 'next': 'Siguiente'},
}


def e(value):
    return escape(str(value), quote=True)


def attrs(values):
    return ' '.join(f'{name}="{e(value)}"' for name, value in values.items())


def percentage_rect(rect, width, height):
    x, y, w, h = rect
    return f'left:{100*x/width:.6f}%;top:{100*y/height:.6f}%;width:{100*w/width:.6f}%;height:{100*h/height:.6f}%'


def arrow(direction):
    path = 'm14.5 5-7 7 7 7' if direction == 'previous' else 'm9.5 5 7 7-7 7'
    return f'<svg aria-hidden="true" viewBox="0 0 24 24"><path d="{path}" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/></svg>'


def build():
    template = Template((ROOT / 'templates/guide-page.html').read_text())
    pages = json.loads((ROOT / 'data/guide-pages.json').read_text())
    for page in pages:
        lang = page['lang']
        labels = LABELS[lang]
        image = page['image']
        flags = []
        for code, label in [('es', 'Español'), ('pt', 'Português'), ('en', 'English')]:
            current = ' aria-current="page"' if lang == code else ''
            flags.append(
                f'<a class="guide-round guide-flag" href="{e(page["languages"][code])}" aria-label="{label}" title="{label}"{current}>'
                f'<img src="/assets/flag-{code}.png" width="58" height="58" alt="{label}"/></a>'
            )
        pagination = []
        for key in ['previous', 'next']:
            if page[key]:
                pagination.append(
                    f'<a class="guide-{key}" rel="{"prev" if key == "previous" else "next"}" href="{e(page[key])}">'
                    + (arrow(key) if key == 'previous' else '') + f'<span>{labels[key]}</span>'
                    + (arrow(key) if key == 'next' else '') + '</a>'
                )
        back = page['back']
        back_html = f'<a class="guide-back" href="{e(back["href"])}">{e(back["label"])}</a>' if back else ''
        if not pagination and back:
            pagination.append(f'<a href="{e(back["href"])}">{e(back["label"])}</a>')
        links = ''.join(
            f'<a class="guide-link" {attrs(link)}></a>'
            for link in page['links']
            if not (page.get('americanas') and link['href'] == page['americanas']['href'])
        )
        masks = ''.join(
            f'<span class="guide-mask" aria-hidden="true" style="{percentage_rect(rect,image["width"],image["height"])}"></span>'
            for rect in page['masks']
        )
        americanas = ''
        if page.get('americanas'):
            item = page['americanas']
            americanas = f'<a class="guide-americanas" href="{e(item["href"])}" aria-label="{e(item["label"])}"><img src="/assets/brands/americanas.svg" alt="" width="163" height="32"/><span>LOJAS AMERICANAS</span></a>'
        result = template.substitute(
            lang=lang, title=e(page['title']), description=e(page['description']),
            kind='guide-'+page['kind'], home=e(page['home']), back=back_html,
            heading=f'<h1 class="guide-heading">{e(page["heading"])}</h1>' if page['heading'] else '',
            flags='\n        '.join(flags), home_label=labels['home'], toolbar_label=labels['toolbar'],
            pagination_label=labels['pagination'], pagination=''.join(pagination),
            width=image['width'], height=image['height'], src=e(image['src']), alt=e(image['alt']),
            masks=masks, links=links, americanas=americanas, source_text=page['source_text'],
        )
        (ROOT / page['path']).write_text('\n'.join(line.rstrip() for line in result.splitlines()) + '\n')
    print(f'Generated {len(pages)} guide pages with shared navigation.')


if __name__ == '__main__':
    build()
