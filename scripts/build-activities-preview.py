#!/usr/bin/env python3
"""Build a separate, navigable two-page Activities proposal from the current guide."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from site_components import pagination
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
def url(lang,index):return f'/preview-atividades/{lang}/{LANGS[lang]["slugs"][index]}/'
for lang,labels in LANGS.items():
 for index in [0,1]:
  doc=parse((ROOT/labels['source']).read_text());body=doc.all(lambda n:n.tag=='body')[0];body.attrs['class']+=' activities-preview'
  cards=doc.all(lambda n:n.tag=='section' and n.has('native-card'));assert len(cards)==4
  weather=doc.all(lambda n:n.has('activity-weather-container'))[0].clone()
  for position,card in enumerate(cards):
   if (position<2)!=(index==0):card.remove()
  head=doc.all(lambda n:n.tag=='head')[0];head.add(Node('meta',{'name':'robots','content':'noindex,nofollow'}));head.add(Node('link',{'rel':'stylesheet','href':'/preview-atividades/preview.css?v=20261124-1'}))
  doc.all(lambda n:n.tag=='title')[0].children=[labels['preview']+' — Atividades — '+labels['topics'][index]]
  panel=doc.all(lambda n:n.has('native-panel'))[0]
  note=fragment(f'<div class="preview-note"><span>{labels["preview"]}</span><a href="/{labels["source"].removesuffix("index.html")}">{labels["back"]}</a></div>');panel.insert(0,note)
  heading=doc.all(lambda n:n.tag=='h1')[0];position=panel.children.index(heading)+1
  tabs=''.join(f'<a href="{url(lang,i)}"'+(' aria-current="page"' if i==index else '')+f'>{i+1}. {escape(labels["topics"][i])}</a>' for i in [0,1])
  panel.insert(position,fragment('<nav class="preview-pages" aria-label="'+labels['preview']+'">'+tabs+'</nav>'))
  if index==1:
   wrapper=Node('div',{'class':'preview-weather'});wrapper.add(weather);panel.insert(position+1,wrapper)
  for flag in doc.all(lambda n:n.tag=='a' and n.has('guide-flag')):
   code=flag.attrs['href'].strip('/').split('/')[0];flag.attrs['href']=url(code,index)
  footer=doc.all(lambda n:n.has('native-actions'))[0]
  nav=fragment('<nav class="site-pagination guide-pagination" aria-label="'+labels['preview']+'">'+pagination(lang,url(lang,0) if index else None,url(lang,1) if index==0 else None)+'</nav>')
  counter=Node('span',{'class':'preview-page-count'},[labels['counter'].format(n=index+1)]);counter.parent=nav
  if index==0:nav.children.insert(0,counter)
  else:nav.children.append(counter)
  footer.children=[nav];nav.parent=footer
  destination=ROOT/url(lang,index).lstrip('/')/'index.html';destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(doc.html())
folder=ROOT/'preview-atividades';(folder/'index.html').write_text('<!doctype html><html lang="pt"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url='+url('pt',0)+'"><title>Prévia de Atividades</title></head><body><a href="'+url('pt',0)+'">Ver a prévia das duas páginas de Atividades</a></body></html>')
print('Built separate Activities preview: two pages in three languages; live Activities split unchanged.')
