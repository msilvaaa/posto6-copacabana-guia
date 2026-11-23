import importlib.util,json,tempfile,sys,unittest
from datetime import date,datetime,timedelta
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sync_sun',ROOT/'scripts/sync-sun-times.py');sun=importlib.util.module_from_spec(spec);spec.loader.exec_module(sun)
def sample():
 return {'weather':[{'date':f'2026-11-{23+i}','astronomy':[{'sunrise':'04:59 AM','sunset':'06:20 PM'}]} for i in range(3)]}
class SunTimesTests(unittest.TestCase):
 def test_local_dates_and_24hour_times_include_tomorrow(self):
  days=sun.normalize(sample(),date(2026,11,23));self.assertEqual(days[0]['sunrise'],'2026-11-23T04:59-03:00');self.assertEqual(days[1]['sunset'],'2026-11-24T18:20-03:00')
 def test_different_seasons_keep_rio_timezone_and_sensible_day_lengths(self):
  p=sample()
  for i,row in enumerate(p['weather']):row.update(date=f'2027-06-{20+i}',astronomy=[{'sunrise':'06:32 AM','sunset':'05:16 PM'}])
  days=sun.normalize(p,date(2027,6,20));self.assertTrue(days[0]['sunrise'].endswith('-03:00'))
 def test_stale_dates_and_inverted_or_missing_sun_times_are_rejected(self):
  with self.assertRaises(ValueError):sun.normalize(sample(),date(2026,11,26))
  p=sample();p['weather'][0]['astronomy'][0]['sunset']='03:00 AM'
  with self.assertRaises(ValueError):sun.normalize(p,date(2026,11,23))
  p=sample();p['weather'].pop()
  with self.assertRaises(ValueError):sun.normalize(p,date(2026,11,23))
 def test_source_failure_preserves_last_saved_file(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'data').mkdir();dest=root/'data/sun-times.json';dest.write_text('{"last":"valid"}');source=root/'bad.json';source.write_text('{}')
   with patch.object(sun,'ROOT',root),patch.object(sys,'argv',['sync','--json-file',str(source)]):
    with self.assertRaises(KeyError):sun.main()
   self.assertEqual(dest.read_text(),'{"last":"valid"}')
 def test_unchanged_rows_do_not_create_new_commit(self):
  p=sample();days=sun.normalize(p,date(2026,11,23))
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'data').mkdir();dest=root/'data/sun-times.json';content=json.dumps({'days':days,'updated_at':'old'});dest.write_text(content);source=root/'ok.json';source.write_text(json.dumps(p))
   with patch.object(sun,'ROOT',root),patch.object(sun,'normalize',return_value=days),patch.object(sys,'argv',['sync','--json-file',str(source)]):sun.main()
   self.assertEqual(dest.read_text(),content)
