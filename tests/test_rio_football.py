import importlib.util,json,sys,unittest
from datetime import datetime,timezone
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sync_rio_football',ROOT/'scripts/sync-rio-football.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
sys.path.insert(0,str(ROOT/'scripts'))
from rio_football import render

class RioFootballTests(unittest.TestCase):
 def event(self,date,ident='123',status='STATUS_SCHEDULED',time=True):
  return {'id':ident,'date':date,'timeValid':time,'league':{'slug':'bra.1','name':'Brazilian Serie A'},'competitions':[{'status':{'type':{'name':status}},'competitors':[{'homeAway':'home','team':{'id':'819','displayName':'Flamengo'}},{'homeAway':'away','team':{'id':'6086','displayName':'Botafogo'}}]}]}
 def payload(self,events):return {'team':{'id':'819'},'events':events}
 def test_seven_calendar_days_use_rio_date_not_utc_date(self):
  now=datetime(2026,11,25,15,tzinfo=timezone.utc)
  data=self.payload([self.event('2026-12-02T01:30Z','1'),self.event('2026-12-02T03:30Z','2')])
  # Dec 2 01:30 UTC is still Dec 1 in Rio: inside Nov 25–Dec 1 window.
  self.assertEqual([g['id'] for g in sync.normalize(data,'819',now)],['1'])
 def test_exclude_started_and_postponed_matches_and_deduplicate(self):
  now=datetime(2026,11,25,15,tzinfo=timezone.utc)
  event=self.event('2026-11-27T20:00Z')
  data=self.payload([self.event('2026-11-25T14:00Z','1'),self.event('2026-11-28T20:00Z','2','STATUS_POSTPONED'),event,event])
  self.assertEqual([g['id'] for g in sync.normalize(data,'819',now)],['123'])
 def test_wrong_team_payload_is_not_accepted_as_empty_schedule(self):
  with self.assertRaises(ValueError):sync.normalize({'team':{'id':'99'},'events':[]},'819',datetime.now(timezone.utc))
 def test_failed_query_leaves_previous_cache_untouched(self):
  target=ROOT/'data/rio-football.json';before=target.read_bytes()
  with patch.object(sync,'fetch_club',side_effect=OSError('Provider unavailable')):
   with self.assertRaises(OSError):sync.main()
  self.assertEqual(target.read_bytes(),before)
 def test_saved_schedule_contains_four_clubs_and_brasilia_times_in_all_languages(self):
  data=json.loads((ROOT/'data/rio-football.json').read_text());self.assertEqual({c['id'] for c in data['clubs']},{'819','3445','3454','6086'})
  for lang in ['pt','en','es']:
   html=render(lang)
   for c in data['clubs']:self.assertIn(c['name'],html)
   self.assertIn('ESPN',html)
   for c in data['clubs']:
    for game in c['games']:
     local=datetime.fromisoformat(game['date']).astimezone(sync.RIO)
     if game['time_confirmed']:self.assertIn(local.strftime('%d/%m · %H:%M'),html)
if __name__=='__main__':unittest.main()
