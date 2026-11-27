import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from activities_topics import parse
from content_layout import with_centered_content

def link(href,label,extra=''):
 return f'<a class="native-link" href="{href}"{extra}><span>{label}</span></a>'
def document(content):
 return '<html><head></head><body><div class="native-panel"><h1>Places</h1><div class="native-card-copy">'+content+'</div></div></body></html>'
class PlaceLinkLayoutTests(unittest.TestCase):
 def test_bank_names_load_the_single_line_fitter_without_a_website_pair(self):
  doc=parse(with_centered_content(document(link('https://maps.app.goo.gl/bank','Caixa Econômica Federal'))))
  self.assertEqual(len(doc.all(lambda n:n.has('venue-name'))),1)
  self.assertTrue(doc.all(lambda n:n.tag=='script' and n.attrs.get('src','').startswith('/venue-labels.js')))
 def test_street_addresses_remain_wrappable(self):
  doc=parse(with_centered_content(document(link('https://maps.app.goo.gl/address','Rua Francisco Sá, 35'))))
  self.assertFalse(doc.all(lambda n:n.has('venue-name')))
 def test_does_not_attach_the_next_unrelated_map_to_a_website(self):
  source=document(link('https://apetite.example','Apetite')+link('https://maps.app.goo.gl/apetite','Apetite')+link('https://maps.app.goo.gl/colombo','Colombo'))
  doc=parse(with_centered_content(source));pairs=doc.all(lambda n:n.has('place-link-pair'))
  self.assertEqual(len(pairs),1)
  self.assertEqual([n.attrs['href'] for n in pairs[0].all(lambda n:n.tag=='a')],['https://apetite.example','https://maps.app.goo.gl/apetite'])
  colombo=doc.all(lambda n:n.tag=='a' and n.attrs.get('href','').endswith('/colombo'))[0]
  self.assertTrue(colombo.parent.has('native-card-copy'))
 def test_explicit_multiple_locations_stay_in_the_same_right_column(self):
  source=document(link('https://shop.example','Shop',' data-location-count="3"')+''.join(link('https://maps.app.goo.gl/'+str(i),'Branch') for i in range(3)))
  doc=parse(with_centered_content(source));maps=doc.all(lambda n:n.has('place-locations'))
  self.assertEqual(len(maps),1);self.assertEqual(len(maps[0].all(lambda n:n.tag=='a')),3)
 def test_unrelated_website_after_map_is_not_paired(self):
  doc=parse(with_centered_content(document(link('https://maps.app.goo.gl/station','Station')+link('https://buser.example','Buser'))))
  self.assertFalse(doc.all(lambda n:n.has('place-link-pair')))
 def test_grouping_preserves_existing_destinations_and_order(self):
  source=document(link('https://bar.example','Bar')+'<div class="belmonte-branches">'+link('https://maps.app.goo.gl/a','A')+link('https://maps.app.goo.gl/b','B')+'</div>')
  before=[n.attrs['href'] for n in parse(source).all(lambda n:n.tag=='a')]
  after=[n.attrs['href'] for n in parse(with_centered_content(source)).all(lambda n:n.tag=='a')]
  self.assertEqual(before,after)
if __name__=='__main__':unittest.main()
