import json
import unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Headings(HTMLParser):
    def __init__(self):
        super().__init__();self.inside=False;self.text='';self.images=0;self.paths=0
    def handle_starttag(self,tag,attrs):
        if tag=='h1':self.inside=True
        elif self.inside and tag in ('img','image'):self.images+=1
        elif self.inside and tag=='path':self.paths+=1
    def handle_endtag(self,tag):
        if tag=='h1':self.inside=False
    def handle_data(self,data):
        if self.inside:self.text+=data
class NativeInstructionTests(unittest.TestCase):
    def test_every_detail_has_readable_localized_title_and_instructions(self):
        content=json.loads((ROOT/'data/amenity-native.json').read_text())
        pages=json.loads((ROOT/'data/guide-pages.json').read_text())
        for page in pages:
            if page['kind']!='detail':continue
            with self.subTest(page=page['path']):
                html=(ROOT/page['path']).read_text();data=content[page['path'].split('/')[-2]];heading=Headings();heading.feed(html)
                self.assertEqual(heading.text,data['title'][page['lang']]);self.assertEqual(heading.images,0);self.assertGreater(heading.paths,0)
                self.assertNotIn('class="guide-image"',html)
                self.assertIn(data['copy'][page['lang']][0],html)
                self.assertIn('href="'+page['back']['href']+'"',html)
    def test_all_original_guide_titles_use_vector_outlines(self):
        pages=json.loads((ROOT/'data/guide-pages.json').read_text())
        for page in pages:
            with self.subTest(page=page['path']):
                heading=Headings();heading.feed((ROOT/page['path']).read_text())
                self.assertTrue(heading.text.strip())
                self.assertEqual(heading.images,0)
                self.assertGreater(heading.paths,0)
    def test_reference_photos_stay_within_original_pixel_bounds(self):
        for key,data in json.loads((ROOT/'data/amenity-native.json').read_text()).items():
            self.assertEqual(set(data['copy']),{'pt','en','es'})
            for x,y,w,h in data['references']:
                with self.subTest(topic=key):
                    self.assertGreater(w,0);self.assertGreater(h,0);self.assertGreaterEqual(x,0);self.assertGreaterEqual(y,0)
                    self.assertLessEqual(x+w,900);self.assertLessEqual(y+h,1350)
