import {WEATHER_REFRESH_MS, WEATHER_SOURCE, forecast} from '../../weather-data.js';

export async function onRequestGet(context) {
  const force = new URL(context.request.url).searchParams.get('refresh') === '1';
  const cache = globalThis.caches?.default;
  const key = new Request(new URL('/api/weather', context.request.url));
  const cached = await cache?.match(key);
  const previous = cached ? await cached.clone().json() : null;
  if (!force && Date.parse(previous?.expiresAt) > Date.now()) return cached;
  try {
    const source = await fetch(WEATHER_SOURCE, {cache:'no-store', signal:AbortSignal.timeout(12000)});
    if (!source.ok) throw new Error('Unavailable');
    const data = forecast(await source.json(), previous);
    const response = Response.json(data, {headers:{'Cache-Control':`public, max-age=${WEATHER_REFRESH_MS / 1000}`}});
    if (cache) {
      try {context.waitUntil(cache.put(key, response.clone()).catch(() => {}));} catch {}
    }
    if (force) {
      const fresh = new Response(response.body, response);
      fresh.headers.set('Cache-Control', 'no-store');
      return fresh;
    }
    return response;
  } catch {
    return Response.json({available:false}, {status:503, headers:{'Cache-Control':'no-store'}});
  }
}
