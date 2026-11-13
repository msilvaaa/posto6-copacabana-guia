#!/usr/bin/env python3
"""Build covers and the shared Apartment, Amenities and Gallery sections."""
import json,re
from decimal import Decimal
from html import escape
from pathlib import Path
from string import Template
from site_components import LABELS,toolbar,pagination,utilities,dialogs,whatsapp
ROOT=Path(__file__).resolve().parents[1]
content=json.loads((ROOT/'templates/cover-content.json').read_text())
page_content=json.loads((ROOT/'templates/apartment-content.json').read_text())
photos=json.loads((ROOT/'data/apartment-photos.json').read_text())
cover_art=json.loads((ROOT/'data/cover-art.json').read_text())
guide=json.loads((ROOT/'data/guide-pages.json').read_text())
rating=json.loads((ROOT/'data/airbnb-rating.json').read_text())
score=Decimal(rating['rating'])
if not score.is_finite() or not 1<=score<=5 or type(rating['review_count']) is not int or rating['review_count']<1:raise ValueError('Invalid confirmed Airbnb rating')
cover_template=Template((ROOT/'templates/cover.html').read_text())
page_template=Template((ROOT/'templates/content-page.html').read_text())
AMENITY_NAMES={
 'pt':['Lixeira','TV da sala','Ar-condicionado','Geladeira','Luz do quarto','TV do quarto','Tábua de passar','Lava-louças','Máquina de lavar','Sofá-cama','Cofre','Banheiro','Luminária','Uber no aeroporto','Fechadura','Portão'],
 'en':['Trash bin','Living room TV','Air conditioning','Refrigerator','Bedroom light','Bedroom TV','Ironing board','Dishwasher','Washing machine','Sofa bed','Safe','Bathroom','Lamp','Airport Uber','Door lock','Building gate'],
 'es':['Papelera','TV de la sala','Aire acondicionado','Nevera','Luz del dormitorio','TV del dormitorio','Tabla de planchar','Lavavajillas','Lavadora','Sofá cama','Caja fuerte','Baño','Lámpara','Uber del aeropuerto','Cerradura','Portón'],
}


def e(value):return escape(str(value),quote=True)


def navigation(lang):
 return ''.join(f'<a href="{e(n["href"])}"'+(' aria-current="page"' if i==0 else '')+f'>{e(n["label"])}</a>' for i,n in enumerate(content[lang]['cover_nav']))


def cover_flags(lang):
 return ''.join(f'<a class="detail-modern-flag'+(' active' if code==lang else '')+f'" href="/{code}/" aria-label="{name}" title="{name}"'+(' aria-current="page"' if code==lang else '')+f'><img src="/assets/flag-{code}.png" alt="{name}"/></a>' for code,name in [('es','Español'),('pt','Português'),('en','English')])


def rating_label(lang):
 value=format(score,'.2f')
 if lang in ('pt','es'):value=value.replace('.',',')
 return content[lang]['rating_template'].format(rating=value,review_count=rating['review_count'])


def photo_attrs(index,sizes):
 photo=photos[index]
 variants=photo.get('variants',[{'src':photo['src'],'width':photo.get('width',1200)}])
 srcset=', '.join(f'{e(p["src"])} {p["width"]}w' for p in variants)
 return f'src="{e(photo["src"])}" srcset="{srcset}" sizes="{sizes}" width="{photo.get("width",1200)}" height="{photo.get("height",800)}"'


def photo_card(lang,index):
 label=e(page_content[lang]['photo_label'].format(number=index+1));photo=photos[index]
 loading=' loading="lazy"' if index>1 else ''
 return f'<figure><a href="{e(photo.get("full_src",photo["src"]))}" data-photo-open><img {photo_attrs(index,"(max-width:760px) 48vw, 32vw")} alt="{label}"{loading}/></a><figcaption>{label}</figcaption></figure>'


def amenity_cards(lang):
 source=next(p for p in guide if p['path']==content[lang]['nav'][2]['href'].lstrip('/')+'index.html')
 links=[p for p in source['links'] if '/comodidades/' in p['href']][:16]
 result=[]
 for i,link in enumerate(links):
  rect={k:float(v) for k,v in re.findall(r'(left|top|width|height):([\d.]+)%',link['style'])}
  x=(rect['left']+rect['width']*.1)*1537/100;y=(rect['top']+rect['height']*.07)*864/100
  w=rect['width']*.8*1537/100;h=rect['height']*.65*864/100
  style=f"background-image:url('/assets/pt-08.jpg');background-size:{1537/w*100:.4f}% {864/h*100:.4f}%;background-position:{x/(1537-w)*100:.4f}% {y/(864-h)*100:.4f}%"
  result.append(f'<a class="amenity-card" href="{e(link["href"])}"><span class="amenity-icon" aria-hidden="true" style="{style}"></span><span>{e(AMENITY_NAMES[lang][i])}</span></a>')
 return '<div class="amenities-grid">'+''.join(result)+'</div>'


for lang,values in content.items():
 labels=page_content[lang];common=LABELS[lang]
 buttons=[]
 for index,button in enumerate(values['buttons']):
  key,label,href=(e(button[k]) for k in ['key','label','href'])
  art=cover_art[button['key']]
  position=e(art.get('position','50% 50%'))
  buttons.append(f'<a class="cover-html-button" data-row="{index//3+1}" data-column="{index%3+1}" aria-label="{label}" href="{href}"><span class="cover-button-art art-{e(art["kind"])}"><img src="{e(art["src"])}" style="object-position:{position}" width="70" height="70" alt=""/></span></a>')
 text={k:e(v) for k,v in values.items() if isinstance(v,str)};text['heading']=values['heading']
 stats=values['stats']+[rating_label(lang)]
 output=cover_template.substitute(lang=lang,**text,nav_links=navigation(lang),flags=cover_flags(lang),**{f'stat_{i}':v for i,v in enumerate(stats)},buttons='\n'.join(buttons),next_href=values['buttons'][0]['href'],utilities=utilities(lang),whatsapp=whatsapp(lang),dialogs=dialogs(lang))
 (ROOT/lang/'index.html').write_text(output)
 for section,title_key in [(1,'apartment_title'),(2,'amenities_title'),(4,'gallery_title')]:
  title=labels.get(title_key,values['nav'][section]['label'])
  if section==4:
   visual='<div class="photo-grid">'+''.join(photo_card(lang,i) for i in range(len(photos)))+'</div>'
   copy=f'<p>{e(labels["gallery_intro"])}</p><p>{e(labels["open_photo"])}</p>'
  else:
   photo_index=2 if section==2 else 0
   visual=f'<a href="{e(photos[photo_index].get("full_src",photos[photo_index]["src"]))}" data-photo-open><img class="section-photo" {photo_attrs(photo_index,"(max-width:760px) 100vw, 66vw")} alt="{e(labels["photo_label"].format(number=photo_index+1))}"/></a>'
   if section==2:copy=amenity_cards(lang)
   else:copy=(f'<h2>{e(labels["intro"])}</h2><p>{e(labels["description"])}</p><p class="listing-rating">★ {rating_label(lang)}</p><p>{e(labels["amenities_intro"])}</p><div class="content-links"><a href="{values["nav"][2]["href"]}">{e(values["nav"][2]["label"])}</a><a href="{values["nav"][4]["href"]}">{e(labels["view_gallery"])}</a></div>')
  copy+=f'<div class="content-links"><a href="{e(rating["source_url"])}" target="_blank" rel="noopener noreferrer">{e(labels["view_listing"])}</a></div>'
  previous,following=('/'+lang+'/',values['nav'][2]['href']) if section==1 else (values['nav'][2]['href'],'/'+lang+'/') if section==4 else (next(p for p in guide if p['path']==values['nav'][2]['href'].lstrip('/')+'index.html')['previous'],next(p for p in guide if p['path']==values['nav'][2]['href'].lstrip('/')+'index.html')['next'])
  body=f'<section class="section-layout"><div class="section-visual">{visual}</div><div class="section-panel"><h1 class="section-title">{e(title)}</h1>{copy}<nav class="site-pagination guide-pagination" aria-label="{common["navigation"]}">{pagination(lang,previous,following)}</nav></div></section>'
  destinations={code:content[code]['nav'][section]['href'] for code in content}
  output=page_template.substitute(lang=lang,title=e(title),description=e(labels['description']),back_label=common['back'],toolbar=toolbar(lang,destinations),utilities=utilities(lang),whatsapp=whatsapp(lang),reading_label=common['reading'],body=body,nav_label=common['navigation'],pagination=pagination(lang,previous,following),dialogs=dialogs(lang))
  destination=ROOT/values['nav'][section]['href'].lstrip('/')/'index.html';destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(output)
  if lang=='en' and section==2:
   alias=ROOT/'en/comodidades/index.html';alias.parent.mkdir(parents=True,exist_ok=True);alias.write_text(output)
