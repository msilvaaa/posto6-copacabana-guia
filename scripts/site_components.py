"""Shared navigation and utilities for all internal guide sections."""
from html import escape
from urllib.parse import quote

LABELS = {
 'pt': {'home':'Início','back':'Voltar ao guia','previous':'Anterior','next':'Próximo','navigation':'Navegação do guia','zoom':'Ampliar página','close':'Voltar ao guia','native':'Ver tamanho original','fit':'Ajustar à tela','weather':'Previsão de Copacabana','weather_hint':'Ver previsão','whatsapp':'Contato pelo WhatsApp','about':'Sobre o guia','reading':'Conteúdo do guia'},
 'en': {'home':'Home','back':'Back to the guide','previous':'Previous','next':'Next','navigation':'Guide navigation','zoom':'Enlarge page','close':'Back to the guide','native':'View original size','fit':'Fit to screen','weather':'Copacabana forecast','weather_hint':'View forecast','whatsapp':'Contact on WhatsApp','about':'About the guide','reading':'Guide content'},
 'es': {'home':'Inicio','back':'Volver a la guía','previous':'Anterior','next':'Siguiente','navigation':'Navegación de la guía','zoom':'Ampliar página','close':'Volver a la guía','native':'Ver tamaño original','fit':'Ajustar a la pantalla','weather':'Pronóstico de Copacabana','weather_hint':'Ver pronóstico','whatsapp':'Contacto por WhatsApp','about':'Sobre la guía','reading':'Contenido de la guía'},
}
HOME_ICON = '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M3 10.8 12 3l9 7.8v8.3a1.9 1.9 0 0 1-1.9 1.9H4.9A1.9 1.9 0 0 1 3 19.1z" fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="1.8"/><path d="M8 20.9v-6.1h8v6.1" fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="1.8"/></svg>'
WHATSAPP = 'https://wa.me/5521981020150'
WHATSAPP_MESSAGES = {
 'pt': 'Olá, eu gostaria de saber a disponibilidade do apartamento em Copacabana, para aluguel por temporada.',
 'en': 'Hello, I would like to check the availability of the apartment in Copacabana for a vacation rental.',
 'es': 'Hola, me gustaría consultar la disponibilidad del apartamento en Copacabana para un alquiler vacacional.',
}


def e(value):
 return escape(str(value), quote=True)


def toolbar(lang, destinations):
 labels=LABELS[lang]
 out=f'<nav class="site-toolbar guide-toolbar" aria-label="{labels["navigation"]}"><a class="site-round guide-home" href="/{lang}/" aria-label="{labels["home"]}" title="{labels["home"]}">{HOME_ICON}</a>'
 for code,name in [('es','Español'),('pt','Português'),('en','English')]:
  current=' aria-current="page"' if code==lang else ''
  out+=f'<a class="site-round guide-flag" href="{e(destinations[code])}" aria-label="{name}" title="{name}"{current}><img src="/assets/flag-{code}.png" width="48" height="48" alt="{name}"/></a>'
 return out+'</nav>'


def arrow(previous=False):
 path='m14.5 5-7 7 7 7' if previous else 'm9.5 5 7 7-7 7'
 return f'<svg aria-hidden="true" viewBox="0 0 24 24"><path d="{path}" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/></svg>'


def pagination(lang, previous=None, following=None):
 labels=LABELS[lang]
 links=[]
 if previous: links.append(f'<a class="guide-previous" rel="prev" href="{e(previous)}">{arrow(True)}<span>{labels["previous"]}</span></a>')
 if following: links.append(f'<a class="guide-next" rel="next" href="{e(following)}"><span>{labels["next"]}</span>{arrow()}</a>')
 if not links: links.append(f'<a href="/{lang}/">{arrow(True)}<span>{labels["back"]}</span></a>')
 return ''.join(links)


def utilities(lang):
 labels=LABELS[lang]
 return f'<div class="site-utilities"><button class="site-weather" type="button" data-weather-open aria-label="{labels["weather"]}"><span aria-hidden="true">☀</span><span><b>Copacabana</b><small data-weather-summary>{labels["weather_hint"]}</small></span></button></div>'


def whatsapp(lang):
 label=LABELS[lang]['whatsapp']
 return (f'<div class="site-contact-corner"><a class="site-whatsapp" aria-label="{label}" title="{label}" href="{WHATSAPP}?text={quote(WHATSAPP_MESSAGES[lang], safe="")}" target="_blank" rel="noopener noreferrer">'
 '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M20.5 3.5A11.2 11.2 0 0 0 3 17L1.5 22.5 7 21a11.2 11.2 0 0 0 13.5-17.5Z" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M8 6.5c-.5 0-1.5 1-1.5 2.5 0 3 4 7 7 7 1.5 0 2.5-1 2.5-1.5l-2.5-1.5-1 1c-1.5-.5-3.5-2.5-4-4l1-1Z" fill="currentColor"/></svg></a></div>')


def dialogs(lang):
 labels=LABELS[lang]
 return (f'<dialog class="site-dialog photo-viewer" data-photo-dialog aria-label="{labels["zoom"]}"><header class="dialog-bar"><button type="button" data-photo-close>← {labels["close"]}</button><button type="button" data-photo-native data-native-label="{labels["native"]}" data-fit-label="{labels["fit"]}">{labels["native"]}</button></header><div class="photo-stage" data-photo-stage></div></dialog>'
 f'<dialog class="site-dialog weather-dialog" data-weather-dialog aria-label="{labels["weather"]}"><header class="dialog-bar"><h2>{labels["weather"]}</h2><button type="button" data-weather-close aria-label="{labels["close"]}">← {labels["close"]}</button></header><div class="weather-content" data-weather-content></div><details class="site-about"><summary>{labels["about"]}</summary><p>Copacabana: Donatas Dabravolskas · <a href="https://commons.wikimedia.org/wiki/File:Carlos_DA_2.jpg" target="_blank" rel="noopener noreferrer">Wikimedia Commons</a> · <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener noreferrer">CC BY-SA 4.0</a>.</p><p>Weather: <a href="https://wttr.in/-22.9842,-43.1918" target="_blank" rel="noopener noreferrer">wttr.in</a>.</p></details></dialog>')


def external_attrs(link):
 values=dict(link)
 if values.get('href','').startswith(('https://','http://')):
  values['target']='_blank'
  values['rel']='noopener noreferrer'
 return values
