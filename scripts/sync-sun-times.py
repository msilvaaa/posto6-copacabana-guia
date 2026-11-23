#!/usr/bin/env python3
"""Prepare Copacabana sunrise/sunset for the next days; preserve saved data on failure."""
import argparse,json
from datetime import date,datetime,timedelta,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
ZONE='America/Sao_Paulo'
SOURCE='https://wttr.in/-22.9842,-43.1918?format=j1'

def normalize(payload,today=None):
 days=[]
 for row in payload['weather'][:3]:
  target=date.fromisoformat(row['date']);astro=row['astronomy'][0]
  start=datetime.combine(target,datetime.strptime(astro['sunrise'],'%I:%M %p').time(),ZoneInfo(ZONE))
  end=datetime.combine(target,datetime.strptime(astro['sunset'],'%I:%M %p').time(),ZoneInfo(ZONE))
  if not timedelta(hours=9)<end-start<timedelta(hours=15):raise ValueError('Invalid sun times')
  days.append({'date':target.isoformat(),'sunrise':start.isoformat(timespec='minutes'),'sunset':end.isoformat(timespec='minutes')})
 dates=[d['date'] for d in days]
 if len(days)!=3 or dates!=sorted(set(dates)):raise ValueError('Three ordered days required')
 today=today or datetime.now(ZoneInfo(ZONE)).date()
 if not {today.isoformat(),(today+timedelta(days=1)).isoformat()}<=set(dates):raise ValueError('Today and tomorrow required')
 return days

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--json-file',type=Path);args=parser.parse_args()
 if args.json_file:payload=json.loads(args.json_file.read_text())
 else:
  with urlopen(Request(SOURCE,headers={'User-Agent':'Posto6CopacabanaGuide/1.0'}),timeout=25) as response:
   raw=response.read(2000001)
   if len(raw)>2000000:raise ValueError('Response too large')
   payload=json.loads(raw)
 days=normalize(payload)
 dest=ROOT/'data/sun-times.json'
 previous=json.loads(dest.read_text()) if dest.exists() else {}
 if previous.get('days')==days:print('Sun times confirmed; no changes.');return
 result={'location':'Copacabana, Rio de Janeiro','latitude':-22.9842,'longitude':-43.1918,'timezone':ZONE,'provider':'wttr.in','source':SOURCE,'updated_at':datetime.now(timezone.utc).isoformat(),'days':days}
 temp=dest.with_suffix('.tmp');temp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');temp.replace(dest)
 print('Prepared Copacabana sunrise and sunset, including tomorrow.')
if __name__=='__main__':main()
