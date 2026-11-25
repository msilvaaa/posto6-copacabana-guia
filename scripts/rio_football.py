"""Render the saved Rio football schedule without delaying the page with an API call."""
import json
from datetime import datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
LEAGUES={'bra.1':'Brasileirão Série A','bra.2':'Brasileirão Série B','bra.copa_do_brasil':'Copa do Brasil','bra.copa_brazil':'Copa do Brasil','bra.camp.carioca':'Campeonato Carioca','conmebol.libertadores':'CONMEBOL Libertadores','conmebol.sudamericana':'CONMEBOL Sudamericana'}
def render(lang):
 data=json.loads((ROOT/'data/rio-football.json').read_text());zone=ZoneInfo(data['timezone'])
 title,period,none,tbd,updated,note={
  'pt':('Confrontos cariocas','Próximos 7 dias','Nenhum jogo confirmado nesta agenda.','Horário a confirmar','Consulta','Horários de Brasília. Atualização às segundas e quintas, às 9h. A programação pode mudar.'),
  'en':('Rio club matchups','Next 7 days','No confirmed match in this schedule.','Time to be confirmed','Checked','Brasília time. Updated Mondays and Thursdays at 9 am. Fixtures may change.'),
  'es':('Encuentros cariocas','Próximos 7 días','Ningún partido confirmado en esta agenda.','Horario por confirmar','Consulta','Hora de Brasilia. Actualización los lunes y jueves a las 9 h. La programación puede cambiar.')
 }[lang]
 weekdays={'pt':['Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],'en':['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],'es':['Lun','Mar','Mié','Jue','Vie','Sáb','Dom']}[lang]
 cards=[]
 for club in data['clubs']:
  fixtures=[]
  for game in club['games']:
   when=datetime.fromisoformat(game['date']).astimezone(zone)
   stamp=when.strftime('%d/%m · %H:%M') if game['time_confirmed'] else when.strftime('%d/%m')+' · '+tbd
   stamp=weekdays[when.weekday()]+' · '+stamp
   league=LEAGUES.get(game['league'],game['competition'])
   fixtures.append(f'<li class="football-fixture" data-match-start="{escape(game["date"])}"><time datetime="{escape(game["date"])}">{escape(stamp)}</time><a href="{escape(game["url"])}" target="_blank" rel="noopener noreferrer">{escape(game["home"])} × {escape(game["away"])}</a><small>{escape(league)}</small></li>')
  cards.append(f'<article class="football-club" data-club="{club["id"]}"><h3><img class="football-crest" src="/assets/football/{club["id"]}.svg" alt="{escape(club["name"])}" title="{escape(club["name"])}" width="40" height="40" loading="lazy" decoding="async"/></h3><ul>{"".join(fixtures)}</ul><p class="football-empty"'+(' hidden' if fixtures else '')+f'>{escape(none)}</p></article>')
 checked=datetime.fromisoformat(data['updated_at']).astimezone(zone).strftime('%d/%m, %H:%M')
 start=datetime.fromisoformat(data['window_start']).strftime('%d/%m');end=datetime.fromisoformat(data['window_end']).strftime('%d/%m')
 return (f'<section class="native-card rio-football" data-football-schedule><h2>{escape(title)}</h2><p class="football-period">{escape(period)} · {start}–{end}</p>'
         f'<div class="football-clubs">{"".join(cards)}</div><p class="football-note">{escape(note)}<br>{escape(updated)}: {checked} · <a href="{escape(data["source_url"])}" target="_blank" rel="noopener noreferrer">ESPN</a></p></section>')
