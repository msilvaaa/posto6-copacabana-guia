#!/usr/bin/env python3
"""Build the separate Activities preview from the same production tab renderer."""
import json
from activities_topics import ROOT, LANGS, render, url
from guide_native import build_native
pages=json.loads((ROOT/'data/guide-pages.json').read_text())
content=json.loads((ROOT/'data/guide-native-content.json').read_text())
upgrades=json.loads((ROOT/'data/guide-photo-upgrades.json').read_text())
photos=json.loads((ROOT/'data/apartment-photos.json').read_text())
for lang,labels in LANGS.items():
 page=next(p for p in pages if p['path']==labels['source'])
 native=next(v for key,v in content.items() if page['image']['src'].endswith(key))
 source=build_native(page,native,upgrades,photos)
 for index in [0,1]:
  target=ROOT/url(lang,index,True).lstrip('/')/'index.html'
  target.parent.mkdir(parents=True,exist_ok=True)
  target.write_text(render(source,lang,index,True))
print('Built translated Activities previews.')
