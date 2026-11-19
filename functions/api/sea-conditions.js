import {REFRESH_MS, MARINE_URL, WIND_URL, conditions} from '../../marine-data.js';

export async function onRequestGet(context) {
  const params = new URL(context.request.url).searchParams;
  const force = params.get('refresh') === '1';
  const cache = globalThis.caches?.default;
  const key = new Request(new URL('/api/sea-conditions', context.request.url));
  const cached = await cache?.match(key);
  const previous = cached ? await cached.clone().json() : null;
  const saved = () => Response.json(previous, {headers:{'Cache-Control':'no-store'}});
  if (params.get('cached') === '1') {
    return previous?.available ? saved() : Response.json({available:false}, {status:202, headers:{'Cache-Control':'no-store'}});
  }
  if (!force && previous?.available && Date.parse(previous.expiresAt) > Date.now()) {
    return Response.json(previous, {headers:{'Cache-Control':`public, max-age=${Math.max(0, Math.floor((Date.parse(previous.expiresAt)-Date.now())/1000))}`}});
  }
  const results = await Promise.all([MARINE_URL, WIND_URL].map(async url => {
    try {
      const response = await fetch(url, {cache:'no-store', signal: AbortSignal.timeout(12000)});
      return response.ok ? await response.json() : null;
    } catch { return null; }
  }));
  const data = conditions(...results);
  // Failed/partial queries must not erase a previously complete forecast.
  if (previous?.available && (!data.available || ['waveHeight','windSpeed'].some(key => Number.isFinite(previous[key]) && !Number.isFinite(data[key])))) return saved();
  const response = Response.json(data, {status: data.available ? 200 : 503,
    headers: {'Cache-Control': data.available ? `public, max-age=${REFRESH_MS / 1000}` : 'no-store'}});
  if (data.available && cache) {
    try {
      const retained = Response.json(data, {headers:{'Cache-Control':'public, max-age=604800'}});
      context.waitUntil(cache.put(key, retained).catch(() => {}));
    } catch {}
  }
  if (force) {
    const fresh = new Response(response.body, response);
    fresh.headers.set('Cache-Control', 'no-store');
    return fresh;
  }
  return response;
}
