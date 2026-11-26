#!/usr/bin/env python3
"""Trace original lettering without changing its font or frame (requires Pillow, potracer, fonttools).

Run manually after changing the original artwork: pip install Pillow potracer fonttools,
then python scripts/build-title-vectors.py. Normal page builds use the saved SVGs.
"""
from pathlib import Path
import json
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'assets/title-vectors'
BOUNDS=json.loads((ROOT/'data/title-ink-bounds.json').read_text())

def asset_name(source):return source.lstrip('/').rsplit('.',1)[0].replace('/','--')+'.svg'

def crop(source,box):
 x,y,w,h=box
 with Image.open(ROOT/source.lstrip('/')) as image:return image.convert('L').crop((x,y,x+w,y+h))

def lettering(source,box):
 if source.startswith('/assets/') and source.endswith('-03.jpg'):
  # Match the existing composite Check-in lettering, including its uppercase C.
  image=Image.new('L',(133,32),255)
  image.paste(crop('/assets/pt-15.jpg',(1246,132,102,32)),(0,0))
  image.paste(crop('/assets/pt-03.jpg',(1353,108,31,32)),(102,0))
  return image
 return crop(source,box)

def point(p):return f'{p.x:.3f},{p.y:.3f}'

def trace(image):
 import potrace
 curves=potrace.Bitmap(image,blacklevel=.5).trace(turdsize=1,alphamax=1.0,opttolerance=.15)
 commands=[]
 for curve in curves:
  commands.append('M'+point(curve.start_point))
  for segment in curve:
   if segment.is_corner:commands.append('L'+point(segment.c)+' '+point(segment.end_point))
   else:commands.append('C'+point(segment.c1)+' '+point(segment.c2)+' '+point(segment.end_point))
  commands.append('Z')
 return ' '.join(commands)

def font_word_svg(text):
 # New titles use the guide's existing Courgette font, kept as scalable outlines.
 from fontTools.ttLib import TTFont
 from fontTools.pens.svgPathPen import SVGPathPen
 from fontTools.pens.boundsPen import BoundsPen
 from fontTools.pens.transformPen import TransformPen
 font=TTFont(ROOT/'assets/fonts/courgette.ttf')
 glyphs=font.getGlyphSet();cmap=font.getBestCmap();pen=SVGPathPen(glyphs);bounds=BoundsPen(glyphs)
 kerning={}
 if 'kern' in font:
  for table in font['kern'].kernTables:kerning.update(table.kernTable)
 cursor=0;previous=None
 for char in text:
  name=cmap[ord(char)]
  if previous:cursor+=kerning.get((previous,name),0)
  matrix=(1,0,0,-1,cursor,0)
  glyphs[name].draw(TransformPen(pen,matrix));glyphs[name].draw(TransformPen(bounds,matrix))
  cursor+=font['hmtx'][name][0];previous=name
 left,top,right,bottom=bounds.bounds;width=right-left;height=bottom-top
 return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{left:g} {top:g} {width:g} {height:g}" '
         f'width="{width:g}" height="{height:g}" style="--title-ratio:{width/height:.6f}">'
         f'<path fill="#000" fill-rule="nonzero" d="{pen.getCommands()}"/></svg>')

def build():
 DEST.mkdir(parents=True,exist_ok=True)
 for source,box in BOUNDS.items():
  if source.endswith('-10.jpg'):
   lang=Path(source).name[:2]
   title=json.loads((ROOT/'data/guide-native-content.json').read_text())['-10.jpg']['title'][lang]
   (DEST/asset_name(source)).write_text(font_word_svg(title))
   continue
  image=lettering(source,box);w,h=image.size;path=trace(image)
  assert path,source
  svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="--title-ratio:{w/h:.6f}">'
       f'<path fill="#000" fill-rule="evenodd" d="{path}"/></svg>')
  (DEST/asset_name(source)).write_text(svg)
 print(f'Generated {len(BOUNDS)} vector titles from the original lettering.')
if __name__=='__main__':build()
