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
            if page['image']['src'].endswith('-04.jpg'):
                # The original Santos Dumont shortcut incorrectly led to the apartment.
                expected.discard('https://maps.app.goo.gl/RT7GMYay3J4vLoMr9')
                expected.add('https://maps.app.goo.gl/iq6CcoLazX9RHe7dA')
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
        for image in upgrades.values():
            self.assertTrue((ROOT / image['src'].lstrip('/')).is_file())


if __name__ == '__main__':
    unittest.main()
