"""Keep the reading column centered without moving page titles or navigation."""
from activities_topics import Node, parse
from urllib.parse import urlparse
import re
import json
from pathlib import Path
from functools import lru_cache


def is_map_link(node):
    if node.tag != 'a' or not node.has('native-link'):
        return False
    url = urlparse(node.attrs.get('href', ''))
    return url.hostname in ('maps.app.goo.gl', 'maps.google.com') or (url.hostname in ('www.google.com', 'google.com', 'goo.gl') and '/maps' in url.path)


def pair_place_links(doc):
    for parent in doc.all(lambda node: any(isinstance(child, Node) and child.has('native-link') for child in node.children)):
        children = [child for child in parent.children if isinstance(child, Node)]
        for i, website in enumerate(children):
            if website not in parent.children or website.tag != 'a' or not website.has('native-link') or is_map_link(website):
                continue
            if urlparse(website.attrs.get('href', '')).scheme not in ('http', 'https'):
                continue
            count = int(website.attrs.get('data-location-count', '1'))
            locations, found = [], 0
            for sibling in children[i + 1:]:
                maps = [sibling] if is_map_link(sibling) else sibling.all(is_map_link) if sibling.has('belmonte-branches') else []
                if not maps:
                    break
                locations.append(sibling)
                found += len(maps)
                if found >= count:
                    break
            if found < count:
                continue
            position = parent.children.index(website)
            pair = Node('div', {'class': 'place-link-pair'})
            site_column = pair.add(Node('div', {'class': 'place-website'}))
            map_column = pair.add(Node('div', {'class': 'place-locations'}))
            website.remove(); site_column.add(website)
            for location in locations:
                location.remove(); map_column.add(location)
            parent.insert(position, pair)
            for link in pair.all(lambda node: node.tag == 'a' and node.has('native-link')):
                for label in link.all(lambda node: node.tag == 'span'):
                    text = ''.join(str(child) for child in label.children if not isinstance(child, Node))
                    # Address details may wrap; venue names remain a single readable label.
                    if is_map_link(link) and (re.search(r'\d', text) or re.match(r'^(Rua|R\.|Av\.|Avenida|Praça|Praia|Rodovia|Estação)\b', text, re.I)):
                        continue
                    label.attrs['class'] = (label.attrs.get('class', '') + ' venue-name').strip()


@lru_cache(maxsize=1)
def walking_distances():
    path = Path(__file__).resolve().parents[1] / 'data/walking-distances.json'
    return json.loads(path.read_text())['destinations'] if path.exists() else {}


def add_walking_symbols(doc):
    html = doc.all(lambda node: node.tag == 'html')[0]
    lang = html.attrs.get('lang', 'pt').split('-')[0]
    label = {'pt': 'A pé', 'en': 'On foot', 'es': 'A pie'}.get(lang, 'On foot')
    for link in doc.all(is_map_link):
        entry = walking_distances().get(link.attrs.get('href'), {})
        distance = entry.get('walking_m')
        if entry.get('status') != 'walking' or not isinstance(distance, (int, float)) or not 0 < distance < 1000:
            continue
        if link.all(lambda node: node.has('walking-distance-symbol')):
            continue
        title = f'{label} · ≈ {distance} m · © OpenStreetMap contributors'
        link.add(Node('img', {'class': 'walking-distance-symbol',
                             'src': '/assets/icons-3d/footprints.svg',
                             'width': '16', 'height': '16', 'alt': label,
                             'title': title, 'data-walking-m': str(distance)}))


def with_centered_content(source):
    if 'class="native-panel"' not in source and 'class="section-panel"' not in source:
        return source
    doc = parse(source)
    pair_place_links(doc)
    add_walking_symbols(doc)
    for link in doc.all(is_map_link):
        for label in link.all(lambda node: node.tag == 'span'):
            text = ''.join(str(child) for child in label.children if not isinstance(child, Node))
            if re.search(r'\d| — ', text) or re.match(r'^(Rua|R\.|Av\.|Avenida|Praça|Praia|Rodovia|Estação|Aeroporto|Estacionamento|Estacionamiento|Parking|Aparcamiento)\b', text, re.I):
                continue
            if not label.has('venue-name'):
                label.attrs['class'] = (label.attrs.get('class', '') + ' venue-name').strip()
    for panel in doc.all(lambda node: node.has('native-panel') or node.has('section-panel')):
        content = Node('div', {'class': 'guide-content'})
        for child in list(panel.children):
            if isinstance(child, Node) and (child.tag == 'h1' or any(child.has(name) for name in ('native-toolbar', 'native-actions', 'section-actions'))):
                continue
            panel.children.remove(child)
            content.add(child)
        panel.add(content)
    head = doc.all(lambda node: node.tag == 'head')[0]
    version = '20261127-wifi-copy-walking' if 'class="wifi-connection"' in source else '20261127-walking-symbols-sport'
    if 'class="information-services"' in source:
        version = '20261127-bank-walking-symbols'
    head.add(Node('link', {'rel': 'stylesheet', 'href': '/reading-layout.css?v=' + version}))
    if doc.all(lambda node: node.has('venue-name')):
        head.add(Node('script', {'src': '/venue-labels.js?v=20261127-walking-symbols', 'defer': None}))
    return doc.html()
