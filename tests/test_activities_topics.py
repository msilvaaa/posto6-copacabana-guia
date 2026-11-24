"""Check translated deep links, fallback panels and guide navigation."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from activities_topics import LANGS, parse, url

class ActivitiesTopicsTests(unittest.TestCase):
 def test_each_topic_has_a_translated_no_script_fallback(self):
  for lang,labels in LANGS.items():
   for topic in [0,1]:
    with self.subTest(lang=lang,topic=topic):
     doc=parse((ROOT/url(lang,topic).lstrip('/')/'index.html').read_text())
     panels=doc.all(lambda n:n.has('activities-topic-panel'))
     self.assertEqual(len(panels),2)
     self.assertEqual(['hidden' in n.attrs for n in panels],[topic!=0,topic!=1])
     self.assertEqual([len(n.all(lambda c:c.has('native-card'))) for n in panels],[3,2])
     self.assertEqual(len(doc.all(lambda n:n.has('activity-weather-container'))),1)
     self.assertFalse(doc.all(lambda n:n.has('preview-note')))
     self.assertFalse(doc.all(lambda n:n.tag=='meta' and n.attrs.get('name')=='robots' and 'noindex' in n.attrs.get('content','')))
     for flag in doc.all(lambda n:n.has('guide-flag')):
      code=flag.attrs['href'].strip('/').split('/')[0]
      self.assertEqual(flag.attrs['href'],url(code,topic))
     for cls in ['guide-previous','guide-next']:
      href=doc.all(lambda n:n.has(cls))[0].attrs['href']
      self.assertNotIn('/preview-atividades/',href)
      self.assertNotIn('/esportes/',href)
      self.assertNotIn('/sport/',href)
      self.assertNotIn('/deporte/',href)

if __name__=='__main__':unittest.main()
