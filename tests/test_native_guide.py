import json
import unittest
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.destinations = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href')
            if href:
                self.destinations.add(href)


class NativeGuideTests(unittest.TestCase):
    def test_migration_preserves_original_destinations_in_each_language(self):
        content = json.loads((ROOT / 'data/guide-native-content.json').read_text())
        pages = json.loads((ROOT / 'data/guide-pages.json').read_text())
        for page in pages:
            if not any(page['image']['src'].endswith(key) for key in content):
                continue
            parser = Links()
            parser.feed((ROOT / page['path']).read_text())
            expected = {item['href'] for item in page['links']}
            if page['image']['src'].endswith(('-09.jpg','-13.jpg')):
                # The owner moved Colombo, breakfast venues and fairs into Bars > Cafés.
                cafes={'pt':'pt/bares/cafes/index.html','en':'en/bars/coffee/index.html','es':'es/verja/cafes/index.html'}
                moved=Links();moved.feed((ROOT/cafes[page['lang']]).read_text())
                parser.destinations.update(moved.destinations)
            if page['image']['src'].endswith(('-11.jpg','-13.jpg')):
                # The owner removed the generic Belmonte location, retaining its two branches.
                expected.discard('https://maps.app.goo.gl/w6MaQtLco1SCjhwC7')
                # The owner removed the repeated Apetite entry at the end of Breakfast.
                expected.discard('https://maps.app.goo.gl/hLs5ywFp32u4TgAu8')
            if page['image']['src'].endswith('-04.jpg'):
                # The original Santos Dumont shortcut incorrectly led to the apartment.
                expected.discard('https://maps.app.goo.gl/RT7GMYay3J4vLoMr9')
                expected.add('https://maps.app.goo.gl/iq6CcoLazX9RHe7dA')
            if page['image']['src'].endswith('-09.jpg'):
                # Keep only the first Sugarloaf destination, as requested by the owner.
                expected.discard('https://maps.app.goo.gl/imZYbmEEZMEBJauH9')
                # The owner provided the exact Forte destination, separate from Colombo.
                expected.difference_update({'https://maps.app.goo.gl/qCLcaRsKFsPj7ujY6', 'https://maps.app.goo.gl/usPwAX4m68TupqMs6'})
                expected.add('https://maps.app.goo.gl/kgNHcDh1MSWXHFaE6')
                # EN/ES reused a Bodytech marker for both Smart Fit branches.
                expected.discard('https://maps.app.goo.gl/V8Pnoz79Ebj6DoRB8')
                expected.update({'https://maps.app.goo.gl/infS3pCMii5sRV3M6', 'https://maps.app.goo.gl/5vWSPofpSnwqATEY6'})
            if page['image']['src'].endswith('-10.jpg'):
                # The owner supplied the updated Santander branch destination.
                expected.discard('https://maps.app.goo.gl/4mU4g6BEkhpWK7eL9')
                expected.add('https://maps.app.goo.gl/CCuLTKmBoQ9qnmY48')
                expected.discard('https://maps.app.goo.gl/NcpfUoFF1y3YV8wv7')
                expected.add('https://maps.app.goo.gl/6voiU2QM6yEgBB7SA')
                # The owner removed both travel agencies and their contact links.
                expected.difference_update({
                    'https://city.rio.br/', 'https://www.instagram.com/cityrioturismo/',
                    'tel:+55213066-0269', 'https://maps.app.goo.gl/zK2PxtaeeHgbK5Wu7',
                    'tel:(21)7847-4197',
                })
            with self.subTest(page=page['path']):
                self.assertTrue(expected <= parser.destinations)

    def test_content_and_photographs_are_available_in_all_languages(self):
        content = json.loads((ROOT / 'data/guide-native-content.json').read_text())
        upgrades = json.loads((ROOT / 'data/guide-photo-upgrades.json').read_text())
        for guide in content.values():
            self.assertEqual(set(guide['title']), {'pt', 'en', 'es'})
            for chapter in guide['chapters']:
                for section in chapter['sections']:
                    for node in [section['title']] + [item['text'] for item in section['items']]:
                        self.assertTrue(all(node.get(lang, '').strip() for lang in ['pt', 'en', 'es']))
        for upgrade in upgrades.values():
            images=([upgrade] if upgrade.get('src') else [])+list(upgrade.get('topic_photos',{}).values())
            self.assertTrue(images)
            for image in images:
                self.assertTrue((ROOT / image['src'].lstrip('/')).is_file())
                self.assertEqual(set(image['alt']),{'pt','en','es'})


if __name__ == '__main__':
    unittest.main()
