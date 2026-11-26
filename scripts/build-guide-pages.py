#!/usr/bin/env python3
"""Build every guide route with readable native content; never fall back to a page image."""
import json
from page_navigation import with_toolbar_navigation
from pathlib import Path
from guide_native import build_native
from amenity_native import build_detail
from activities_topics import render as render_activities, url as activities_url
from chapter_topics import TOPICS, render as render_topics, topic_url
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
  if page['image']['src'].endswith('-09.jpg'):
   lang=page['lang']
   secondary=ROOT/activities_url(lang,1).lstrip('/')/'index.html'
   secondary.parent.mkdir(parents=True,exist_ok=True)
   secondary.write_text(with_toolbar_navigation(render_activities(output,lang,1)));count+=1
   output=render_activities(output,lang)
  topic_key=next((key for key in TOPICS if page['image']['src'].endswith(key)),None)
  if topic_key:
   for topic in range(1,len(TOPICS[topic_key][page['lang']][0])):
    destination=ROOT/topic_url(page,topic).lstrip('/')/'index.html'
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(with_toolbar_navigation(render_topics(output,page,topic)));count+=1
   output=render_topics(output,page)
  (ROOT/page['path']).write_text(with_toolbar_navigation(output));count+=1
 print(f'Generated {count} native guide routes.')
if __name__=='__main__':build()
