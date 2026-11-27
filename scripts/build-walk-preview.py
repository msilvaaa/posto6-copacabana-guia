"""Build the requested walking-symbol example from the current Activities page."""
from pathlib import Path
from activities_topics import parse,Node
ROOT=Path(__file__).resolve().parents[1]
doc=parse((ROOT/'pt/atividades/index.html').read_text())
head=doc.all(lambda node:node.tag=='head')[0]
head.add(Node('meta',{'name':'robots','content':'noindex,nofollow'}))
doc.all(lambda node:node.tag=='title')[0].children=['Exemplo · símbolo A pé · Posto 6']
doc.all(lambda node:node.tag=='body')[0].attrs['data-activities-title']='Exemplo · símbolo A pé · Posto 6'
destination=ROOT/'mostruario-a-pe/index.html'
destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(doc.html())
print('Built walking-symbol example for Forte de Copacabana.')
