#!/usr/bin/env python3
"""Render the approved topic tabs for Activities and its separate preview."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import json
from site_components import pagination,LABELS
ROOT=Path(__file__).resolve().parents[1]
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Raw(str):pass
class Node:
 def __init__(self,tag='',attrs=None,children=None):self.tag=tag;self.attrs=dict(attrs or []);self.children=children or [];self.parent=None
 def add(self,node):
  self.children.append(node)
  if isinstance(node,Node):node.parent=self
  return node
 def has(self,cls):return cls in self.attrs.get('class','').split()
 def all(self,test):
  result=[]
  for child in self.children:
   if isinstance(child,Node):
    if test(child):result.append(child)
    result.extend(child.all(test))
  return result
 def remove(self):self.parent.children.remove(self)
 def insert(self,index,node):self.children.insert(index,node);node.parent=self
 def clone(self):return parse(self.html()).children[0]
 def html(self):
  if not self.tag:return ''.join(c.html() if isinstance(c,Node) else str(c) for c in self.children)
  attrs=''.join(' '+k+('' if v is None else '="'+escape(str(v),quote=True)+'"') for k,v in self.attrs.items())
  if self.tag in VOID:return '<'+self.tag+attrs+'/>'
  contents=''.join(c.html() if isinstance(c,Node) else str(c) if isinstance(c,Raw) or self.tag in {'script','style'} else escape(c,quote=False) for c in self.children)
  return '<'+self.tag+attrs+'>'+contents+'</'+self.tag+'>'
class Tree(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root]
 def handle_decl(self,decl):self.stack[-1].add(Raw('<!'+decl+'>'))
 def handle_starttag(self,tag,attrs):
  node=self.stack[-1].add(Node(tag,attrs))
  if tag not in VOID:self.stack.append(node)
 def handle_startendtag(self,tag,attrs):self.stack[-1].add(Node(tag,attrs))
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==tag:self.stack=self.stack[:i];break
 def handle_data(self,text):self.stack[-1].add(text)
def parse(source):
 parser=Tree();parser.feed(source);return parser.root
def fragment(source):return parse(source).children[0]
LANGS={
 'pt':{'source':'pt/atividades/index.html','slugs':['passeios','esportes'],'topics':['Passeios','Esporte e bem-estar'],'preview':'Prévia de layout','back':'Voltar à página atual','counter':'{n} de 2'},
 'en':{'source':'en/activities/index.html','slugs':['sightseeing','sport'],'topics':['Sightseeing','Sport and well-being'],'preview':'Layout preview','back':'Back to the current page','counter':'{n} of 2'},
 'es':{'source':'es/actividades/index.html','slugs':['paseos','deporte'],'topics':['Paseos','Deporte y bienestar'],'preview':'Vista previa','back':'Volver a la página actual','counter':'{n} de 2'},
}
def url(lang,index,preview=False):
 labels=LANGS[lang]
 if preview:return f'/preview-atividades/{lang}/{labels["slugs"][index]}/'
 root='/'+labels['source'].removesuffix('index.html')
 return root if index==0 else root+labels['slugs'][1]+'/'
def render(source,lang,index=0,preview=False):
 labels=LANGS[lang]
 doc=parse(source);body=doc.all(lambda n:n.tag=='body')[0]
 cards=doc.all(lambda n:n.tag=='section' and n.has('native-card'));assert len(cards)==4
 original_weather=doc.all(lambda n:n.has('activity-weather-container'))[0];weather=original_weather.clone();original_weather.remove()
 panels=[]
 for topic in [0,1]:
  attrs={'class':'activities-topic-panel','id':f'activities-panel-{topic}','role':'tabpanel','aria-labelledby':f'activities-tab-{topic}','tabindex':'0'}
  if topic!=index:attrs['hidden']=None
  panel_topic=Node('section',attrs)
  for card in cards[topic*2:topic*2+2]:card.remove();panel_topic.add(card)
  panels.append(panel_topic)
 head=doc.all(lambda n:n.tag=='head')[0];head.add(Node('link',{'rel':'stylesheet','href':'/activities-tabs.css?v=20261124-1'}));head.add(Node('script',{'src':'/activities-tabs.js?v=20261124-1','defer':None}))
 activity_title=doc.all(lambda n:n.has('native-title-text'))[0].children[0]
 body.attrs['data-activities-title']='Posto 6 Copacabana — '+lang.upper()+' — '+activity_title
 doc.all(lambda n:n.tag=='title')[0].children=[body.attrs['data-activities-title']+' — '+labels['topics'][index]]
 panel=doc.all(lambda n:n.has('native-panel'))[0]
 if preview:
  head.add(Node('meta',{'name':'robots','content':'noindex,nofollow'}))
  head.add(Node('link',{'rel':'stylesheet','href':'/preview-atividades/preview.css?v=20261124-2'}))
  note=fragment(f'<div class="preview-note"><span>{labels["preview"]}</span><a href="/{labels["source"].removesuffix("index.html")}">{labels["back"]}</a></div>');panel.insert(0,note)
 heading=doc.all(lambda n:n.tag=='h1')[0];position=panel.children.index(heading)+1
 tabs=''.join(f'<a id="activities-tab-{i}" role="tab" data-activities-topic="{i}" aria-controls="activities-panel-{i}" aria-selected="{str(i==index).lower()}" tabindex="{0 if i==index else -1}" href="{url(lang,i,preview)}"'+(' aria-current="page"' if i==index else '')+f'>{escape(labels["topics"][i])}</a>' for i in [0,1])
 panel.insert(position,fragment('<nav class="activities-topic-tabs" role="tablist" aria-label="'+activity_title+'">'+tabs+'</nav>'))
 wrapper=Node('div',{'class':'activities-shared-weather'});wrapper.add(weather);panel.insert(position+1,wrapper)
 panel.insert(position+2,panels[0]);panel.insert(position+3,panels[1])
 for flag in doc.all(lambda n:n.tag=='a' and n.has('guide-flag')):
  code=flag.attrs['href'].strip('/').split('/')[0];flag.attrs['href']=url(code,index,preview)
  for topic in [0,1]:flag.attrs[f'data-activities-path-{topic}']=url(code,topic,preview)
 footer=doc.all(lambda n:n.has('native-actions'))[0];original=next(page for page in json.loads((ROOT/'data/guide-pages.json').read_text()) if page['path']==labels['source'])
 nav=fragment('<nav class="site-pagination guide-pagination" aria-label="'+LABELS[lang]['navigation']+'">'+pagination(lang,original['previous'],original['next'])+'</nav>')
 footer.children=[nav];nav.parent=footer
 return doc.html()
