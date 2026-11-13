import importlib.util,json,tempfile,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sync_weather',ROOT/'scripts/sync-weather.py')
weather=importlib.util.module_from_spec(spec);spec.loader.exec_module(weather)
def sample():return {'weather':[{'date':f'2026-11-{13+i}','mintempC':'22','maxtempC':'28','hourly':[{'chanceofrain':'30','weatherCode':'116'},{'chanceofrain':'80','weatherCode':'176'}]} for i in range(3)]}
class WeatherTests(unittest.TestCase):
 def test_valid_regional_forecast(self):
  days=weather.normalize(sample());self.assertEqual(len(days),3);self.assertEqual(days[0]['rain_probability'],80)
 def test_bad_temperature_is_rejected(self):
  data=sample();data['weather'][0]['mintempC']='70'
  with self.assertRaises(ValueError):weather.normalize(data)
 def test_incomplete_days_are_rejected(self):
  data=sample();data['weather'].pop()
  with self.assertRaises(ValueError):weather.normalize(data)
 def test_invalid_response_does_not_erase_forecast(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);(root/'data').mkdir();destination=root/'data/weather.json';destination.write_text('{"last":"valid"}')
   source=root/'invalid.json';source.write_text('{"error":"not available"}')
   with patch.object(weather,'ROOT',root),patch.object(sys,'argv',['sync','--json-file',str(source)]):
    with self.assertRaises(KeyError):weather.main()
   self.assertEqual(destination.read_text(),'{"last":"valid"}')
 def test_unchanged_forecast_does_not_create_commit(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);(root/'data').mkdir();destination=root/'data/weather.json';previous=json.dumps({'days':weather.normalize(sample()),'updated_at':'old'});destination.write_text(previous)
   source=root/'valid.json';source.write_text(json.dumps(sample()))
   with patch.object(weather,'ROOT',root),patch.object(sys,'argv',['sync','--json-file',str(source)]):weather.main()
   self.assertEqual(destination.read_text(),previous)
if __name__=='__main__':unittest.main()
