import base64
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sync_rating', ROOT / 'scripts/sync-airbnb-rating.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


def public_page(score=4.98, count='120', listing='48382177', identifier=None):
    value = {
        '@type': 'VacationRental',
        'identifier': identifier or base64.b64encode(f'DemandStayListing:{listing}'.encode()).decode(),
        'aggregateRating': {'ratingValue': score, 'ratingCount': count},
    }
    return (f'<link rel="canonical" href="https://www.airbnb.com.br/rooms/{listing}"/>'
            '<script type="application/ld+json">' + json.dumps(value) + '</script>')


class AirbnbRatingTests(unittest.TestCase):
    def test_public_listing_data(self):
        self.assertEqual(sync.parse_rating(public_page()), ('4.98', 120))

    def test_rejects_other_listing(self):
        with self.assertRaises(ValueError):
            sync.parse_rating(public_page(listing='123'))

    def test_rejects_different_identifier_on_expected_url(self):
        with self.assertRaises(ValueError):
            sync.parse_rating(public_page(identifier='other-listing'))

    def test_missing_or_blocked_response_is_not_a_rating(self):
        for html in ['<title>Access denied</title>', '<html></html>', public_page().replace('aggregateRating', 'unavailable')]:
            with self.subTest(html=html), self.assertRaises(ValueError):
                sync.parse_rating(html)

    def test_invalid_numbers_are_not_published(self):
        for score, count in [('NaN', '120'), (5.1, '120'), (0, '120'), (4.98, '120.5'), (4.98, '-1'), (4.98, 'unknown')]:
            with self.subTest(score=score, count=count), self.assertRaises(ValueError):
                sync.parse_rating(public_page(score, count))

    def test_conflicting_readings_are_rejected(self):
        with self.assertRaises(ValueError):
            sync.parse_rating(public_page() + public_page(4.99, '121'))

    def test_failed_read_leaves_last_confirmed_file_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'data').mkdir()
            destination = root / 'data/airbnb-rating.json'
            destination.write_text('{"rating":"4.98","review_count":120}')
            previous = destination.read_bytes()
            html = root / 'blocked.html'
            html.write_text('<title>Access denied</title>')
            with patch.object(sync, 'ROOT', root), patch.object(sys, 'argv', ['sync', '--html-file', str(html)]):
                with self.assertRaises(ValueError):
                    sync.main()
            self.assertEqual(destination.read_bytes(), previous)

    def test_unchanged_data_does_not_create_commits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'data').mkdir()
            destination = root / 'data/airbnb-rating.json'
            destination.write_text('{"rating":"4.98","review_count":120,"verified_at":"previous"}')
            previous = destination.read_bytes()
            html = root / 'public.html'
            html.write_text(public_page())
            with patch.object(sync, 'ROOT', root), patch.object(sys, 'argv', ['sync', '--html-file', str(html)]):
                sync.main()
            self.assertEqual(destination.read_bytes(), previous)

    def test_changed_rating_rebuilds_all_languages(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder in ['templates', 'data']:
                shutil.copytree(ROOT / folder, root / folder)
            (root / 'scripts').mkdir()
            shutil.copy(ROOT / 'scripts/build-covers.py', root / 'scripts/build-covers.py')
            shutil.copy(ROOT / 'scripts/site_components.py', root / 'scripts/site_components.py')
            for lang in ['pt', 'en', 'es']:
                (root / lang).mkdir()
            html = root / 'changed.html'
            html.write_text(public_page(4.99, '121'))
            with patch.object(sync, 'ROOT', root), patch.object(sys, 'argv', ['sync', '--html-file', str(html)]):
                sync.main()
            subprocess.run([sys.executable, str(root / 'scripts/build-covers.py')], check=True)
            for lang, apartment, score in [('pt', 'apartamento', '4,99'), ('en', 'apartment', '4.99'), ('es', 'apartamento', '4,99')]:
                for page in [root / lang / 'index.html', root / lang / apartment / 'index.html']:
                    rendered = page.read_text()
                    self.assertIn(score, rendered)
                    self.assertIn('121', rendered)
                    self.assertNotIn('4,98', rendered)
                    self.assertNotIn('4.98', rendered)


if __name__ == '__main__':
    unittest.main()
