#!/usr/bin/env python3
"""Cache the public three-day forecast; retain the last valid forecast on failures."""
import argparse,json
from datetime import date,datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[1]
SOURCE='https://wttr.in/-22.9842,-43.1918?format=j1'


def normalize(payload):
 days=[]
 for day in payload['weather'][:3]:
  day_date=date.fromisoformat(day['date']).isoformat()
  minimum,maximum=int(day['mintempC']),int(day['maxtempC'])
  hourly=day['hourly']
  rain=max(int(hour.get('chanceofrain','0')) for hour in hourly)
  if not (-15<=minimum<=maximum<=60 and 0<=rain<=100):raise ValueError('Invalid forecast values')
  code=str(hourly[len(hourly)//2]['weatherCode'])
  if not code.isdigit():raise ValueError('Invalid forecast code')
  days.append({'date':day_date,'min':minimum,'max':maximum,'rain_probability':rain,'code':code})
 if len(days)!=3 or len({day['date'] for day in days})!=3:raise ValueError('Three forecast days are required')
 if [d['date'] for d in days]!=sorted(d['date'] for d in days):raise ValueError('Invalid forecast order')
 return days


def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--json-file',type=Path);args=parser.parse_args()
 if args.json_file:payload=json.loads(args.json_file.read_text())
 else:
  with urlopen(Request(SOURCE,headers={'User-Agent':'Posto6CopacabanaGuide/1.0'}),timeout=25) as response:
   content=response.read(2_000_001)
   if len(content)>2_000_000:raise ValueError('Forecast response too large')
   payload=json.loads(content)
 days=normalize(payload)
 destination=ROOT/'data/weather.json'
 previous=json.loads(destination.read_text()) if destination.exists() else {}
 if previous.get('days')==days:print('Copacabana forecast confirmed; no changes.');return
 result={'location':'Copacabana, Rio de Janeiro','latitude':-22.9842,'longitude':-43.1918,'provider':'wttr.in','source':SOURCE,'updated_at':datetime.now(timezone.utc).isoformat(),'days':days}
 temporary=destination.with_suffix('.tmp');temporary.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');temporary.replace(destination)
 print('Updated Copacabana three-day forecast.')
if __name__=='__main__':main()
