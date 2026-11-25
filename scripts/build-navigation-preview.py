#!/usr/bin/env python3
"""Build a single review page; production pagination remains fixed at the bottom."""
from pathlib import Path
from activities_topics import parse,Node,fragment
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'pt/restaurantes/outras-opcoes/index.html'
doc=parse(source.read_text());head=doc.all(lambda n:n.tag=='head')[0];body=doc.all(lambda n:n.tag=='body')[0]
body.attrs['class']+=' navigation-preview'
head.add(Node('meta',{'name':'robots','content':'noindex,nofollow'}))
head.add(Node('link',{'rel':'canonical','href':'https://posto6-copacabana-guia.pages.dev/pt/restaurantes/outras-opcoes/'}))
head.add(Node('style',children=['''
body.navigation-preview .site-pagination { position:static; inset:auto; transform:none; margin:0 auto 16px; }
body.navigation-preview .native-panel { padding-bottom:24px; }
body.navigation-preview::after { display:none; }
.navigation-preview .preview-note { margin:16px 0; text-align:center; font:400 12px/1.5 Arial,Helvetica,sans-serif; }
''']))
# Keep this single preview on the selected panel; tab links open the normal site.
for script in doc.all(lambda n:n.tag=='script' and '/activities-tabs.js' in n.attrs.get('src','')):script.remove()
panel=doc.all(lambda n:n.has('native-panel'))[0];heading=panel.all(lambda n:n.tag=='h1')[0]
nav=doc.all(lambda n:n.has('site-pagination'))[0];nav.remove();panel.insert(panel.children.index(heading)+1,nav)
for footer in doc.all(lambda n:n.has('native-actions')):footer.remove()
panel.add(fragment('<p class="preview-note">Prévia: navegação abaixo do título. <a href="/pt/restaurantes/outras-opcoes/">Ver página atual</a></p>'))
target=ROOT/'preview-navegacao/pt/restaurantes/outras-opcoes/index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(doc.html())
print('Built one navigation preview; production routes unchanged.')
