#!/usr/bin/env python3
"""Read the listing's public JSON-LD; keep confirmed data on any fetch/parse failure."""
import argparse
import base64
import json
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://www.airbnb.com.br/h/posto6copa'
LISTING_ID = '48382177'


class ListingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.documents = []
        self.canonical = None
        self.collect = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.collect = True
            self.parts = []

    def handle_data(self, data):
        if self.collect:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.collect:
            try:
                self.documents.append(json.loads(''.join(self.parts)))
            except json.JSONDecodeError:
                pass
            self.collect = False


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def parse_rating(html):
    parser = ListingParser()
    parser.feed(html)
    canonical = urlparse(parser.canonical or '')
    if (canonical.scheme != 'https' or canonical.hostname != 'www.airbnb.com.br'
            or canonical.path.rstrip('/') != f'/rooms/{LISTING_ID}'):
        raise ValueError('The public page does not identify the expected listing.')
    readings = set()
    expected_identifier = base64.b64encode(f'DemandStayListing:{LISTING_ID}'.encode()).decode()
    for document in parser.documents:
        for item in objects(document):
            types = item.get('@type', [])
            if isinstance(types, str):
                types = [types]
            if 'VacationRental' not in types:
                continue
            if item.get('identifier') != expected_identifier:
                continue
            rating = item.get('aggregateRating', {})
            try:
                score = Decimal(str(rating['ratingValue']))
                count = str(rating.get('reviewCount', rating.get('ratingCount', '')))
                if not score.is_finite() or not Decimal('1') <= score <= Decimal('5'):
                    continue
                if not re.fullmatch(r'[1-9][0-9]*', count):
                    continue
                readings.add((format(score.quantize(Decimal('.01')), 'f'), int(count)))
            except (KeyError, InvalidOperation, TypeError):
                continue
    if len(readings) != 1:
        raise ValueError('A unique valid rating was not found for this listing.')
    return readings.pop()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html-file', type=Path, help='Read a saved public response for verification.')
    args = parser.parse_args()
    if args.html_file:
        html = args.html_file.read_text()
    else:
        request = Request(SOURCE, headers={'User-Agent': 'Posto6CopacabanaGuide/1.0', 'Accept': 'text/html'})
        with urlopen(request, timeout=30) as response:
            final = urlparse(response.geturl())
            if final.scheme != 'https' or final.hostname != 'www.airbnb.com.br':
                raise ValueError('Unexpected redirect destination.')
            if response.headers.get_content_type() != 'text/html':
                raise ValueError('The listing did not return HTML.')
            content = response.read(5_000_001)
            if len(content) > 5_000_000:
                raise ValueError('The public response exceeded the size limit.')
            html = content.decode('utf-8')
    score, count = parse_rating(html)
    destination = ROOT / 'data/airbnb-rating.json'
    previous = json.loads(destination.read_text()) if destination.exists() else {}
    if previous.get('rating') == score and previous.get('review_count') == count:
        print(f'Confirmed Airbnb rating: {score}, {count} reviews; no changes.')
        return
    data = {
        'listing_id': LISTING_ID, 'source_url': SOURCE, 'rating': score,
        'review_count': count, 'verified_at': datetime.now(timezone.utc).isoformat(),
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(destination)
    print(f'Updated Airbnb rating: {score}, {count} reviews.')


if __name__ == '__main__':
    main()
