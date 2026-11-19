import {REFRESH_MS, MARINE_URL, WIND_URL, conditions} from '../../marine-data.js';

export async function onRequestGet(context) {
  const force = new URL(context.request.url).searchParams.get('refresh') === '1';
  const cache = globalThis.caches?.default;
  const key = new Request(new URL('/api/sea-conditions', context.request.url));
  const cached = force ? null : await cache?.match(key);
  if (cached) {
    const data = await cached.clone().json();
    if (Date.parse(data.expiresAt) > Date.now()) return cached;
  }
  const results = await Promise.all([MARINE_URL, WIND_URL].map(async url => {
    try {
      const response = await fetch(url, {cache:'no-store', signal: AbortSignal.timeout(12000)});
      return response.ok ? await response.json() : null;
    } catch { return null; }
  }));
  const data = conditions(...results);
  const response = Response.json(data, {status: data.available ? 200 : 503,
    headers: {'Cache-Control': data.available ? `public, max-age=${REFRESH_MS / 1000}` : 'no-store'}});
  if (data.available && cache) {
    try { context.waitUntil(cache.put(key, response.clone()).catch(() => {})); } catch {}
  }
  if (force) {
    const fresh = new Response(response.body, response);
    fresh.headers.set('Cache-Control', 'no-store');
    return fresh;
  }
  return response;
}
