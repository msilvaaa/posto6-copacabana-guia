"""Refresh verified walking distances from public map markers and OSRM's foot network.

Run after adding destinations. Unresolved destinations receive no walking badge.
No visitor location or runtime routing request is required.
"""
import concurrent.futures
import datetime
import json
import math
from html import unescape
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = [-43.1919094, -22.9841532]  # longitude, latitude: apartment
DESTINATION = ROOT / 'data/walking-distances.json'
AGENT = 'Posto6GuestGuide/1.0 (walking-distance-maintenance)'


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': AGENT}), timeout=40)


def air_distance(point):
    lng1, lat1, lng2, lat2 = map(math.radians, [*ORIGIN, *point])
    a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lng2-lng1)/2)**2
    return 6371000 * 2 * math.asin(math.sqrt(a))


def resolve(pair):
    href, label = pair
    result = {'label': label, 'status': 'unresolved'}
    try:
        with fetch(href) as response:
            final = urllib.parse.unquote(response.geturl())
        markers = re.findall(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', final)
        if not markers:
            return href, result
        lat, lng = map(float, markers[-1])
        result.update(coordinates=[lng, lat], straight_line_m=round(air_distance([lng,lat])), status='outside-radius')
    except Exception as error:
        result['error'] = type(error).__name__
    return href, result


def main():
    # Generated routes include all language-specific destinations.
    import sys
    sys.path.insert(0, str(ROOT / 'scripts'))
    from activities_topics import parse
    from content_layout import is_map_link
    urls = {}
    for lang in ('pt','en','es'):
        for path in (ROOT/lang).rglob('index.html'):
            for link in parse(path.read_text()).all(is_map_link):
                urls[link.attrs['href']] = unescape(re.sub('<[^>]+>', '', link.html())).strip()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        entries = dict(pool.map(resolve, urls.items()))
    if 'https://maps.app.goo.gl/oHfNoJEv7JXWGAo18' in entries:
        entries['https://maps.app.goo.gl/oHfNoJEv7JXWGAo18']['status'] = 'origin'
    candidates = [(href, entry) for href, entry in entries.items()
                  if entry.get('coordinates') and air_distance(entry['coordinates']) < 1000
                  and href != 'https://maps.app.goo.gl/oHfNoJEv7JXWGAo18']
    coordinates = [ORIGIN] + [entry['coordinates'] for _,entry in candidates]
    encoded = ';'.join(','.join(map(str,point)) for point in coordinates)
    endpoint = 'https://routing.openstreetmap.de/routed-foot/table/v1/foot/'
    with fetch(endpoint + encoded + '?sources=0&annotations=distance') as response:
        routes = json.load(response)
    if routes.get('code') != 'Ok':
        raise RuntimeError('Walking router did not return a valid distance table')
    origin_snap = routes['sources'][0]['distance']
    for i,(href,entry) in enumerate(candidates,1):
        distance = routes['distances'][0][i]
        snap = routes['destinations'][i]['distance']
        if distance is None or max(origin_snap, snap) > 100:
            entry['status'] = 'unresolved-route'
            continue
        # Include snapping offsets, conservatively rounding upwards at the threshold.
        entry['walking_m'] = math.ceil(distance + origin_snap + snap)
        entry['status'] = 'walking' if entry['walking_m'] < 1000 else 'outside-walking-radius'
    result = {'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'origin':ORIGIN, 'threshold_m':1000, 'mode':'foot',
              'source':'https://routing.openstreetmap.de/',
              'attribution':'© OpenStreetMap contributors', 'destinations':entries}
    DESTINATION.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print('Destinations:',len(entries), 'walking under 1 km:',sum(e['status']=='walking' for e in entries.values()))
    print('Unresolved:',sum(e['status']=='unresolved' for e in entries.values()))


if __name__ == '__main__':
    main()
