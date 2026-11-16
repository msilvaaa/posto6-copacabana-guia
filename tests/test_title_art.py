import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


class TitleArtTests(unittest.TestCase):
    def test_all_technical_titles_keep_their_source_and_fit_the_frame(self):
        pages=json.loads((ROOT/'data/guide-pages.json').read_text())
        titles=json.loads((ROOT/'data/detail-title-art.json').read_text())
        for page in pages:
            if page['kind']!='detail':
                continue
            with self.subTest(page=page['path']):
                title=titles[page['image']['src']]
                x,y,w,h=title['rect']
                self.assertGreaterEqual(x,0)
                self.assertGreaterEqual(y,0)
                self.assertLessEqual(x+w,title['width'])
                self.assertLessEqual(y+h,title['height'])
                self.assertGreater(title['scale'],0.5)
                self.assertLessEqual(title['scale'],0.85)
                self.assertIn('class="guide-title-art"',(ROOT/page['path']).read_text())

    def test_previously_oversized_labels_match_the_other_titles(self):
        titles=json.loads((ROOT/'data/detail-title-art.json').read_text())
        for source,title in titles.items():
            if any(label in source for label in ['-lixeira-','-luminaria-']):
                with self.subTest(source=source):
                    self.assertLessEqual(title['glyph_height']*title['scale'],38.01)


if __name__=='__main__':
    unittest.main()
