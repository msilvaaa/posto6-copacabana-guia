"""Walking badges require a verified pedestrian route strictly below one kilometre."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from activities_topics import parse
from content_layout import add_walking_symbols


class WalkingSymbolsTests(unittest.TestCase):
    def render(self, distance, status='walking', lang='pt'):
        doc=parse(f'<html lang="{lang}"><body><a class="native-link" href="https://maps.app.goo.gl/example"><span>Venue</span></a></body></html>')
        with patch('content_layout.walking_distances',return_value={'https://maps.app.goo.gl/example':{'walking_m':distance,'status':status}}):
            add_walking_symbols(doc)
            add_walking_symbols(doc)
        return doc.all(lambda node:node.has('walking-distance-symbol'))

    def test_threshold_uses_walking_route_not_straight_line(self):
        for distance in (0,1000,1047,None):
            self.assertEqual(self.render(distance),[])
        for status in ('unresolved','origin','outside-radius'):
            self.assertEqual(self.render(500,status),[])
        self.assertEqual(len(self.render(999)),1)

    def test_symbol_is_small_localized_and_idempotent(self):
        for lang,label in [('pt','A pé'),('en','On foot'),('es','A pie')]:
            symbols=self.render(714,lang=lang)
            self.assertEqual(len(symbols),1)
            self.assertEqual(symbols[0].attrs['alt'],label)
            self.assertEqual(symbols[0].attrs['width'],'16')
            self.assertIn('714 m',symbols[0].attrs['title'])
