"""Deep links must retain every recommendation and the global guide navigation."""
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from activities_topics import parse
from chapter_topics import TOPICS,topic_url

class ChapterTopicsTests(unittest.TestCase):
 def test_topic_routes_keep_content_and_navigation_without_javascript(self):
  pages=json.loads((ROOT/'data/guide-pages.json').read_text())
  for suffix in TOPICS:
   translated={p['lang']:p for p in pages if p['image']['src'].endswith(suffix)}
   for lang,page in translated.items():
    primary=parse((ROOT/page['path']).read_text())
    recommendations=[n.attrs['href'] for n in primary.all(lambda n:n.has('native-link'))]
    for index in range(len(TOPICS[suffix][lang][0])):
     with self.subTest(lang=lang,page=page['path'],topic=index):
      doc=parse((ROOT/topic_url(page,index).lstrip('/')/'index.html').read_text())
      self.assertEqual(len(doc.all(lambda n:n.has('native-chapter'))),1)
      self.assertEqual([n.attrs['href'] for n in doc.all(lambda n:n.has('native-link'))],recommendations)
      panels=doc.all(lambda n:n.has('activities-topic-panel'))
      self.assertEqual([i for i,n in enumerate(panels) if 'hidden' not in n.attrs],[index])
      self.assertEqual(doc.all(lambda n:n.has('guide-previous'))[0].attrs['href'],page['previous'])
      self.assertEqual(doc.all(lambda n:n.has('guide-next'))[0].attrs['href'],page['next'])
      for flag in doc.all(lambda n:n.has('guide-flag')):
       code=flag.attrs['href'].strip('/').split('/')[0]
       self.assertEqual(flag.attrs['href'],topic_url(translated[code],index))

if __name__=='__main__':unittest.main()
