#!/usr/bin/env python3
"""Build every guide route with readable native content; never fall back to a page image."""
import json
from pathlib import Path
from guide_native import build_native
from amenity_native import build_detail
ROOT=Path(__file__).resolve().parents[1]
def build():
 pages=json.loads((ROOT/'data/guide-pages.json').read_text())
 photos=json.loads((ROOT/'data/apartment-photos.json').read_text())
 upgrades=json.loads((ROOT/'data/guide-photo-upgrades.json').read_text())
 content=json.loads((ROOT/'data/guide-native-content.json').read_text())
 count=0
 for page in pages:
  if page['image']['src'].endswith('-08.jpg'):continue
  if page['kind']=='detail':
   output=build_detail(page,photos)
  else:
   native=next((v for key,v in content.items() if page['image']['src'].endswith(key)),None)
   if native is None:raise ValueError('Missing native content: '+page['path'])
   output=build_native(page,native,upgrades,photos)
  (ROOT/page['path']).write_text(output);count+=1
 print(f'Generated {count} native guide routes.')
if __name__=='__main__':build()
