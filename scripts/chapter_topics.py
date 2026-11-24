"""Apply the approved instant-tab navigation to dining and shopping chapters."""
import json
from activities_topics import ROOT, Node, parse, fragment
from html import escape

TOPICS={
 '-11.jpg':{
  'pt':(['Bares','Cafés'],['','cafes']),
  'en':(['Bars','Cafés'],['','coffee']),
  'es':(['Bares','Cafés'],['','cafes']),
 },
 '-12.jpg':{
  'pt':(['Recomendações','Mais sabores','Outras opções'],['','mais-sabores','outras-opcoes']),
  'en':(['Recommendations','More flavours','Other options'],['','more-flavours','other-options']),
  'es':(['Recomendaciones','Más sabores','Otras opciones'],['','mas-sabores','otras-opciones']),
 },
 '-13.jpg':{
  'pt':(['Shoppings','Supermercados'],['','supermercados']),
  'en':(['Shopping centres','Supermarkets'],['','supermarkets']),
  'es':(['Centros comerciales','Supermercados'],['','supermercados']),
 },
}

def topic_url(page,index):
 suffix=next(key for key in TOPICS if page['image']['src'].endswith(key))
 slug=TOPICS[suffix][page['lang']][1][index]
 return '/'+page['path'].removesuffix('index.html')+(slug+'/' if slug else '')

def render(source,page,index=0):
 suffix=next(key for key in TOPICS if page['image']['src'].endswith(key))
 labels,slugs=TOPICS[suffix][page['lang']]
 doc=parse(source)
 body=doc.all(lambda n:n.tag=='body')[0]
 chapters=doc.all(lambda n:n.has('native-chapter'))
 first=chapters[0];first.attrs['class']+=' guide-topic-chapter'
 topic_photos=json.loads((ROOT/'data/guide-photo-upgrades.json').read_text()).get(suffix,{}).get('topic_photos',{})
 if topic_photos:
  photo=first.all(lambda n:n.has('native-photo'))[0]
  original=photo.all(lambda n:n.tag=='img')[0];original.attrs['data-topic-photo']='0'
  selected=str(index) if str(index) in topic_photos else '0'
  if selected!='0':original.attrs['hidden']=None
  for key,variant in topic_photos.items():
   attrs={'src':variant['src'],'width':str(variant['width']),'height':str(variant['height']),'alt':variant['alt'][page['lang']],'style':'object-position:'+variant.get('position','50% 50%'),'data-topic-photo':key}
   if key!=selected:attrs['hidden']=None
   photo.add(Node('img',attrs))
 panel=first.all(lambda n:n.has('native-panel'))[0]
 footer=doc.all(lambda n:n.has('native-actions'))[0];footer.remove()
 groups=[]
 if suffix=='-11.jpg':
  cards=first.all(lambda n:n.tag=='section' and n.has('native-card'))
  groups=[[cards[0]],cards[1:]]
  subtitles=[None,None]
 else:
  groups=[chapter.all(lambda n:n.tag=='section' and n.has('native-card')) for chapter in chapters]
  subtitles=[next(iter(chapter.all(lambda n:n.has('native-chapter-title'))),None) for chapter in chapters]
 assert len(groups)==len(labels)
 panels=[]
 for i,cards in enumerate(groups):
  attrs={'class':'activities-topic-panel','id':f'activities-panel-{i}','role':'tabpanel','aria-labelledby':f'activities-tab-{i}','tabindex':'0'}
  if i!=index:attrs['hidden']=None
  topic=Node('section',attrs)
  if subtitles[i]:subtitles[i].remove();topic.add(subtitles[i])
  for card in cards:card.remove();topic.add(card)
  panels.append(topic)
 for chapter in chapters[1:]:chapter.remove()
 title=doc.all(lambda n:n.tag=='title')[0]
 body.attrs['data-activities-title']=''.join(str(x) for x in title.children)
 title.children=[body.attrs['data-activities-title']+' — '+labels[index]]
 heading=panel.all(lambda n:n.tag=='h1')[0];position=panel.children.index(heading)+1
 tabs=''.join(f'<a id="activities-tab-{i}" role="tab" data-activities-topic="{i}" aria-controls="activities-panel-{i}" aria-selected="{str(i==index).lower()}" tabindex="{0 if i==index else -1}" href="{topic_url(page,i)}"'+(' aria-current="page"' if i==index else '')+f'>{escape(label)}</a>' for i,label in enumerate(labels))
 nav=fragment(f'<nav class="activities-topic-tabs" style="--topic-count:{len(labels)}" role="tablist" aria-label="{escape(body.attrs["data-activities-title"],quote=True)}">{tabs}</nav>')
 panel.insert(position,nav)
 for i,topic in enumerate(panels):panel.insert(position+i+1,topic)
 panel.add(footer)
 pages=json.loads((ROOT/'data/guide-pages.json').read_text())
 translated={p['lang']:p for p in pages if p['image']['src'].endswith(suffix)}
 for flag in doc.all(lambda n:n.has('guide-flag')):
  lang=flag.attrs['href'].strip('/').split('/')[0]
  flag.attrs['href']=topic_url(translated[lang],index)
  for i in range(len(labels)):flag.attrs[f'data-activities-path-{i}']=topic_url(translated[lang],i)
 head=doc.all(lambda n:n.tag=='head')[0]
 head.add(Node('link',{'rel':'stylesheet','href':'/activities-tabs.css?v=20261124-9'}))
 head.add(Node('script',{'src':'/activities-tabs.js?v=20261124-9','defer':None}))
 return doc.html()
