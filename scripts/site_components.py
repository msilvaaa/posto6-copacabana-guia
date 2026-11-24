"""Shared navigation and utilities for all internal guide sections."""
from html import escape
from urllib.parse import quote
from pathlib import Path
import json
from guide_icons_3d import icon_3d

LABELS = {
 'pt': {'weather_close':'Fechar','home':'Início','back':'Voltar ao guia','previous':'Anterior','next':'Próximo','navigation':'Navegação do guia','zoom':'Ampliar página','close':'Voltar ao guia','native':'Ver tamanho original','fit':'Ajustar à tela','weather':'Previsão de Copacabana','weather_hint':'Ver previsão','whatsapp':'Contato pelo WhatsApp','about':'Sobre o guia','reading':'Conteúdo do guia'},
 'en': {'weather_close':'Close','home':'Home','back':'Back to the guide','previous':'Previous','next':'Next','navigation':'Guide navigation','zoom':'Enlarge page','close':'Back to the guide','native':'View original size','fit':'Fit to screen','weather':'Copacabana forecast','weather_hint':'View forecast','whatsapp':'Contact on WhatsApp','about':'About the guide','reading':'Guide content'},
 'es': {'weather_close':'Cerrar','home':'Inicio','back':'Volver a la guía','previous':'Anterior','next':'Siguiente','navigation':'Navegación de la guía','zoom':'Ampliar página','close':'Volver a la guía','native':'Ver tamaño original','fit':'Ajustar a la pantalla','weather':'Pronóstico de Copacabana','weather_hint':'Ver pronóstico','whatsapp':'Contacto por WhatsApp','about':'Sobre la guía','reading':'Contenido de la guía'},
}
HOME_ICON = '<img class="home-icon" src="/assets/icon-preview/home-flat.svg" width="36" height="36" alt="" aria-hidden="true"/>'
WHATSAPP = 'https://wa.me/5521981020150'
WHATSAPP_MESSAGES = {
 'pt': 'Olá, eu gostaria de saber a disponibilidade do apartamento em Copacabana, para aluguel por temporada.',
 'en': 'Hello, I would like to check the availability of the apartment in Copacabana for a vacation rental.',
 'es': 'Hola, me gustaría consultar la disponibilidad del apartamento en Copacabana para un alquiler vacacional.',
}
WHATSAPP_CONTEXT = json.loads((Path(__file__).resolve().parents[1]/'data/whatsapp-topics.json').read_text())
WHATSAPP_GUEST_MESSAGES = {
 'pt': 'Olá, estou hospedado(a) no apartamento de temporada em Copacabana e tenho dúvidas sobre {topic}.',
 'en': 'Hello, I am staying at the vacation apartment in Copacabana and have a question about {topic}.',
 'es': 'Hola, estoy alojado(a) en el apartamento vacacional de Copacabana y tengo dudas sobre {topic}.',
}


def whatsapp_topic_key(context):
 if not context:return None
 parts=str(context).strip('/').split('/')
 if len(parts)>1 and parts[1] in {'atividades','activities','actividades','restaurantes','restaurants','bares','bars','verja','estabelecimentos','establishments','establecimientos'}:
  return WHATSAPP_CONTEXT['aliases'].get(parts[1],parts[1])
 slug=str(context).strip('/').removesuffix('index.html').strip('/').split('/')[-1]
 if slug in LABELS:return None
 return WHATSAPP_CONTEXT['aliases'].get(slug,slug)


def whatsapp_message(lang,context=None):
 key=whatsapp_topic_key(context)
 if key is None:return WHATSAPP_MESSAGES[lang]
 topic=WHATSAPP_CONTEXT['topics'].get(key,WHATSAPP_CONTEXT['topics']['bem-vindos'])[lang]
 return WHATSAPP_GUEST_MESSAGES[lang].format(topic=topic)


def e(value):
 return escape(str(value), quote=True)


def telephone_icon():
 # T6: same blue receiver and yellow ringing marks selected in the preview.
 return ('<svg class="telephone-icon" viewBox="0 0 28 28" width="18" height="18" aria-hidden="true" fill="#238cc6">'
         '<g transform="translate(1 3) scale(.85)"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.2 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.7 2.79a2 2 0 0 1-.45 2.11L8.09 9.89a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.89.33 1.83.57 2.79.7A2 2 0 0 1 22 16.92z"/></g>'
         '<path d="M17 4a7 7 0 0 1 7 7M17 8a3 3 0 0 1 3 3" fill="none" stroke="#e5a02d" stroke-width="2" stroke-linecap="round"/></svg>')


def app_icon(spaced=False):
 # A2: colored mobile phone selected from the app/site preview.
 gap = 'margin-right:8px;' if spaced else ''
 size = 20 if spaced else 18
 return (f'<svg class="app-link-icon" viewBox="0 0 32 32" width="{size}" height="{size}" style="width:{size}px;height:{size}px;flex:0 0 {size}px;{gap}" aria-hidden="true">'
         '<rect x="7" y="1" width="18" height="30" rx="4" fill="#238cc6"/><rect x="9" y="5" width="14" height="21" rx="1" fill="#d5f5f6"/>'
         '<path d="M13 3h6" stroke="#113e5c" stroke-linecap="round"/><rect x="11" y="8" width="4" height="5" rx="1" fill="#f5ac37"/>'
         '<rect x="17" y="8" width="4" height="5" rx="1" fill="#21a877"/><path d="M14 28h4" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/></svg>')


def page_title(lang,name):
 return f'Posto 6 Copacabana — {lang.upper()} — {name}'


def flag_src(code):
 return '/assets/flags/en-round.svg' if code=='en' else f'/assets/flags/{code}.svg'


def toolbar(lang, destinations, home_href=None, home_label=None):
 labels=LABELS[lang]
 home_href=home_href or f'/{lang}/'
 home_label=home_label or labels['home']
 out=f'<nav class="site-toolbar guide-toolbar" aria-label="{labels["navigation"]}"><a class="site-round guide-home" href="{e(home_href)}" aria-label="{e(home_label)}" title="{e(home_label)}">{HOME_ICON}</a>'
 for code,name in [('es','Español'),('pt','Português'),('en','English')]:
  current=' aria-current="page"' if code==lang else ''
  out+=f'<a class="site-round guide-flag" href="{e(destinations[code])}" aria-label="{name}" title="{name}"{current}><img src="{flag_src(code)}" width="48" height="48" alt="{name}"/></a>'
 return out+'</nav>'


def arrow(previous=False):
 path='m14.5 5-7 7 7 7' if previous else 'm9.5 5 7 7-7 7'
 return f'<svg aria-hidden="true" viewBox="0 0 24 24"><path d="{path}" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/></svg>'


def pagination(lang, previous=None, following=None):
 labels=LABELS[lang]
 links=[]
 if previous: links.append(f'<a class="site-step guide-previous" rel="prev" href="{e(previous)}">{arrow(True)}<span>{labels["previous"]}</span></a>')
 if following: links.append(f'<a class="site-step guide-next" rel="next" href="{e(following)}"><span>{labels["next"]}</span>{arrow()}</a>')
 if not links: links.append(f'<a class="site-step" href="/{lang}/">{arrow(True)}<span>{labels["back"]}</span></a>')
 return ''.join(links)


def theme_toggle(lang):
 label={'pt':'Ativar modo escuro','en':'Switch to dark mode','es':'Activar modo oscuro'}[lang]
 return f'<button class="theme-toggle" type="button" data-theme-toggle aria-pressed="false" aria-label="{label}" title="{label}"><span data-theme-symbol aria-hidden="true">☾</span></button>'


def sun_times(lang):
 from datetime import datetime
 from zoneinfo import ZoneInfo
 path=Path(__file__).resolve().parents[1]/'data/sun-times.json'
 data=json.loads(path.read_text()) if path.exists() else {'days':[]}
 today=datetime.now(ZoneInfo('America/Sao_Paulo')).date().isoformat()
 day=next((row for row in data['days'] if row['date']==today),{})
 labels={'pt':('Nascer do sol','Pôr do sol','Horários de hoje em Copacabana, no fuso do Rio de Janeiro'),
         'en':('Sunrise','Sunset',"Today's times in Copacabana, Rio de Janeiro time"),
         'es':('Amanecer','Atardecer','Horarios de hoy en Copacabana, hora de Río de Janeiro')}[lang]
 def entry(key,label):
  stamp=day.get(key,'');time=stamp[11:16] if stamp else '—'
  arrow='m9 10 3-3 3 3M12 7v8' if key=='sunrise' else 'm9 12 3 3 3-3M12 7v8'
  symbol=('<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
          '<path d="M3 19h18M5 16a7 7 0 0 1 14 0M2 13h2m16 0h2M5 5l2 2m12-2-2 2"/>'
          f'<path d="{arrow}"/></svg>')
  return f'<span class="cover-sun-event" title="" data-sun-tooltip="{e(label)}" tabindex="0" aria-label="{e(label)}">{symbol}<span class="cover-sun-label">{e(label)}</span><time data-sun-value="{key}" datetime="{e(stamp)}">{e(time)}</time></span>'
 markup=f'<div class="cover-sun-times" data-sun-times aria-label="{e(labels[2])}" title="{e(labels[2])}">{entry("sunrise",labels[0])}{entry("sunset",labels[1])}</div>'
 saved=json.dumps(data,ensure_ascii=False).replace('<',chr(92)+'u003c')
 return '<link rel="stylesheet" href="/sun-times.css?v=20261124-2"/>'+markup+f'<script type="application/json" data-sun-saved>{saved}</script>'


def utilities(lang):
 labels=LABELS[lang]
 from datetime import datetime
 from zoneinfo import ZoneInfo
 symbol='cloud'
 try:
  saved=json.loads((Path(__file__).resolve().parents[1]/'data/weather.json').read_text())
  today=datetime.now(ZoneInfo('America/Sao_Paulo')).date().isoformat()
  day=next(day for day in saved['days'] if day['date']>=today)
  symbol='rain' if day['rain_probability']>=50 else 'sun' if str(day['code'])=='113' else 'cloud'
 except (OSError,ValueError,KeyError,TypeError,StopIteration):pass
 return f'<div class="site-utilities"><button class="site-weather" type="button" data-weather-open aria-label="{labels["weather"]}"><span aria-hidden="true" data-weather-icon>{icon_3d(symbol)}</span><span><b>Copacabana</b><small data-weather-summary>{labels["weather_hint"]}</small></span></button></div>'


def whatsapp(lang,context=None):
 label=LABELS[lang]['whatsapp']
 return (f'<div class="site-contact-corner"><a class="site-whatsapp" aria-label="{label}" title="{label}" href="{WHATSAPP}?text={quote(whatsapp_message(lang,context), safe="")}" target="_blank" rel="noopener noreferrer">'
 '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M20.5 3.5A11.2 11.2 0 0 0 3 17L1.5 22.5 7 21a11.2 11.2 0 0 0 13.5-17.5Z" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M8 6.5c-.5 0-1.5 1-1.5 2.5 0 3 4 7 7 7 1.5 0 2.5-1 2.5-1.5l-2.5-1.5-1 1c-1.5-.5-3.5-2.5-4-4l1-1Z" fill="currentColor"/></svg></a></div>')


def cover_photo_credits(lang):
 names={'pt':['Cristo Redentor','Calçadão de Copacabana','Atividades','Emergência','Check-in','Shopping','Transporte','Check-out'],'en':['Christ the Redeemer','Copacabana promenade','Activities','Emergency','Check-in','Shopping','Transport','Check-out'],'es':['Cristo Redentor','Paseo de Copacabana','Actividades','Emergencia','Check-in','Shopping','Transporte','Check-out']}[lang]
 credits=json.loads((Path(__file__).resolve().parents[1]/'data/cover-photo-credits.json').read_text())
 notice={'pt':'Fotos exibidas em recorte circular nos botões.','en':'Photos displayed with a circular crop in the buttons.','es':'Fotos mostradas con recorte circular en los botones.'}[lang]
 result=[f'<p>{notice}</p>']
 for name,item in zip(names,credits):
  license_link=f' · <a href="{e(item["license_url"])}" target="_blank" rel="noopener noreferrer">{e(item["license"])}</a>' if item.get('license_url') else ''
  result.append(f'<p>{e(name)}: {e(item["author"])} · <a href="{e(item["source"])}" target="_blank" rel="noopener noreferrer">{e(item.get("source_label","Wikimedia Commons"))}</a>{license_link}.</p>')
 return ''.join(result)



def dialogs(lang, cover=False):
 labels=LABELS[lang]
 photo_credits=cover_photo_credits(lang) if cover else ''
 return (f'<dialog class="site-dialog photo-viewer" data-photo-dialog aria-label="{labels["zoom"]}"><header class="dialog-bar"><button type="button" data-photo-close>← {labels["close"]}</button><button type="button" data-photo-native data-native-label="{labels["native"]}" data-fit-label="{labels["fit"]}">{labels["native"]}</button></header><div class="photo-stage" data-photo-stage></div></dialog>'
 f'<dialog class="site-dialog weather-dialog" data-weather-dialog aria-label="{labels["weather"]}"><header class="dialog-bar"><h2>{labels["weather"]}</h2><button type="button" data-weather-close aria-label="{labels["weather_close"]}">× {labels["weather_close"]}</button></header><div class="weather-content" data-weather-content></div><details class="site-about"><summary>{labels["about"]}</summary><p>Copacabana: Donatas Dabravolskas · <a href="https://commons.wikimedia.org/wiki/File:Carlos_DA_2.jpg" target="_blank" rel="noopener noreferrer">Wikimedia Commons</a> · <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener noreferrer">CC BY-SA 4.0</a>.</p><p>Weather: <a href="https://wttr.in/-22.9842,-43.1918" target="_blank" rel="noopener noreferrer">wttr.in</a>.</p>{photo_credits}<p>3D: <a href="https://github.com/microsoft/fluentui-emoji" target="_blank" rel="noopener noreferrer">Microsoft Fluent Emoji</a> · <a href="/assets/icons-3d/LICENSES.txt">MIT</a>.</p></details></dialog>')


def external_attrs(link):
 values=dict(link)
 if values.get('href','').startswith(('https://','http://')):
  values['target']='_blank'
  values['rel']='noopener noreferrer'
 return values
