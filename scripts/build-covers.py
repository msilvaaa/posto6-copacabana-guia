#!/usr/bin/env python3
"""Build translated covers, apartment and gallery pages from shared templates."""
import json
from decimal import Decimal
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
content = json.loads((ROOT / 'templates/cover-content.json').read_text())
page_content = json.loads((ROOT / 'templates/apartment-content.json').read_text())
photos = json.loads((ROOT / 'data/apartment-photos.json').read_text())
rating = json.loads((ROOT / 'data/airbnb-rating.json').read_text())
score = Decimal(rating['rating'])
if not score.is_finite() or not 1 <= score <= 5 or type(rating['review_count']) is not int or rating['review_count'] < 1:
    raise ValueError('Invalid confirmed Airbnb rating.')
cover_template = Template((ROOT / 'templates/cover.html').read_text())
page_template = Template((ROOT / 'templates/content-page.html').read_text())


def navigation(lang, active):
    return ''.join(
        f'<a href="{escape(item["href"], quote=True)}"'
        + (' aria-current="page"' if index == active else '')
        + f'>{escape(item["label"])}</a>'
        for index, item in enumerate(content[lang]['nav'])
    )


def flags(lang, section=0):
    links = []
    for code, label in [('es', 'Español'), ('pt', 'Português'), ('en', 'English')]:
        active = ' active' if code == lang else ''
        current = ' aria-current="page"' if code == lang else ''
        href = content[code]['nav'][section]['href']
        links.append(
            f'<a class="detail-modern-flag{active}"{current} href="{href}" '
            f'aria-label="{label}" title="{label}">'
            f'<img src="/assets/flag-{code}.png" alt="{label}"/></a>'
        )
    return '\n        '.join(links)


def rating_label(lang):
    localized_score = format(score, '.2f')
    if lang in ('pt', 'es'):
        localized_score = localized_score.replace('.', ',')
    return content[lang]['rating_template'].format(rating=localized_score, review_count=rating['review_count'])


def photo(lang, index, lazy=True):
    label = escape(page_content[lang]['photo_label'].format(number=index + 1))
    src = photos[index]['src']
    loading = ' loading="lazy"' if lazy else ''
    return f'<figure><a href="{src}"><img src="{src}" alt="{label}"{loading}/></a><figcaption>{label}</figcaption></figure>'


for lang, values in content.items():
    buttons = []
    for index, button in enumerate(values['buttons']):
        key, label, href = (escape(button[k], quote=True) for k in ('key', 'label', 'href'))
        buttons.append(
            f'        <a class="cover-html-button" data-row="{index // 3 + 1}" '
            f'data-column="{index % 3 + 1}" aria-label="{label}" href="{href}">'
            f'<img src="/assets/cover-icons/{key}.png" width="70" height="70" alt=""/></a>'
        )
    text = {k: escape(v, quote=True) for k, v in values.items() if isinstance(v, str)}
    text['heading'] = values['heading']  # Retain approved line breaks.
    stats = values['stats'] + [rating_label(lang)]
    result = cover_template.substitute(
        lang=lang, **text, nav_links=navigation(lang, 0), flags=flags(lang),
        **{f'stat_{i}': value for i, value in enumerate(stats)},
        buttons='\n'.join(buttons), next_href=values['buttons'][0]['href'],
    )
    (ROOT / lang / 'index.html').write_text(result)

    labels = page_content[lang]
    for section, title_key in [(1, 'apartment_title'), (4, 'gallery_title')]:
        if section == 1:
            body = (
                f'<img class="apartment-hero" src="{photos[0]["src"]}" alt="{escape(labels["photo_label"].format(number=1))}"/>'
                f'<h2>{escape(labels["intro"])}</h2><p>{escape(labels["description"])}</p>'
                f'<p class="listing-rating">★ {rating_label(lang)}</p>'
                f'<p>{escape(labels["amenities_intro"])}</p><div class="content-links">'
                f'<a href="{values["nav"][2]["href"]}">{escape(values["nav"][2]["label"])}</a>'
                f'<a href="{values["nav"][4]["href"]}">{escape(labels["view_gallery"])}</a></div>'
            )
        else:
            body = f'<p>{escape(labels["gallery_intro"])}</p><div class="photo-grid">'
            body += ''.join(photo(lang, i, lazy=i > 1) for i in range(len(photos))) + '</div>'
        result = page_template.substitute(
            lang=lang, title=escape(labels[title_key]), description=escape(labels['description']),
            site_label=escape(labels['site_label']), nav_label=escape(values['nav_label']),
            home_label=escape(values['home_label']), flags=flags(lang, section),
            nav_links=navigation(lang, section), body=body,
            listing_url=escape(rating['source_url'], quote=True), view_listing=escape(labels['view_listing']),
        )
        destination = ROOT / values['nav'][section]['href'].lstrip('/') / 'index.html'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(result)
