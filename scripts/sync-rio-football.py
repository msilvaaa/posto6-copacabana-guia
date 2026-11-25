#!/usr/bin/env python3
"""Save seven days of confirmed Rio club fixtures; never replace the cache on a failed query."""
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timedelta,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
CLUBS=[('819','Flamengo'),('3445','Fluminense'),('3454','Vasco da Gama'),('6086','Botafogo')]
RIO=ZoneInfo('America/Sao_Paulo')

def normalize(payload,club_id,now):
 if not isinstance(payload.get('events'),list) or str(payload.get('team',{}).get('id'))!=club_id:
  raise ValueError('Unexpected team schedule')
 end=now.astimezone(RIO).date()+timedelta(days=7)
 games={}
 for event in payload['events']:
  start=datetime.fromisoformat(event['date'].replace('Z','+00:00'))
  if start<now or start.astimezone(RIO).date()>=end:continue
  comp=event['competitions'][0];status=comp.get('status',{}).get('type',{})
  if status.get('completed') or status.get('name') in ('STATUS_CANCELED','STATUS_POSTPONED'):continue
  teams=comp['competitors']
  if club_id not in [str(t['team']['id']) for t in teams]:raise ValueError('Wrong club')
  home=next(t['team']['displayName'] for t in teams if t['homeAway']=='home')
  away=next(t['team']['displayName'] for t in teams if t['homeAway']=='away')
  ident=str(event['id'])
  if not ident.isdigit():raise ValueError('Invalid event ID')
  games[ident]={'id':ident,'date':start.isoformat(),'time_confirmed':bool(comp.get('timeValid',event.get('timeValid',False))),
   'home':home,'away':away,'competition':event.get('league',{}).get('name',''),
   'league':event.get('league',{}).get('slug',''),'venue':comp.get('venue',{}).get('fullName',''),
   'url':'https://www.espn.com.br/futebol/partida/_/jogoId/'+ident}
 return sorted(games.values(),key=lambda g:g['date'])

def fetch_club(pair,now):
 club_id,name=pair
 url=f'https://site.api.espn.com/apis/site/v2/sports/soccer/all/teams/{club_id}/schedule?fixture=true'
 req=Request(url,headers={'User-Agent':'Posto6GuestGuide/1.0','Accept':'application/json'})
 with urlopen(req,timeout=20) as response:payload=json.load(response)
 return {'id':club_id,'name':name,'games':normalize(payload,club_id,now)}

def main():
 now=datetime.now(timezone.utc)
 with ThreadPoolExecutor(max_workers=4) as pool:clubs=list(pool.map(lambda pair:fetch_club(pair,now),CLUBS))
 start=now.astimezone(RIO).date()
 data={'updated_at':now.isoformat(),'window_start':start.isoformat(),'window_end':(start+timedelta(days=6)).isoformat(),
       'timezone':'America/Sao_Paulo','source':'ESPN','source_url':'https://www.espn.com.br/futebol/calendario','clubs':clubs}
 target=ROOT/'data/rio-football.json';temp=target.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');temp.replace(target)
 print('Confirmed fixtures:',sum(len(c['games']) for c in clubs),'club entries, next seven calendar days.')
if __name__=='__main__':main()
