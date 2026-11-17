const SOURCE = 'https://economia.awesomeapi.com.br/json/last/USD-BRLT,ARS-BRL,EUR-BRL,BRL-USD';
const PAIRS = [
  {id: 'usd-tourism', key: 'USDBRLT', base: 'USD', target: 'BRL'},
  {id: 'ars', key: 'ARSBRL', base: 'ARS', target: 'BRL'},
  {id: 'eur', key: 'EURBRL', base: 'EUR', target: 'BRL'},
  {id: 'brl', key: 'BRLUSD', base: 'BRL', target: 'USD'}
];
const json = (data, cacheControl = 'no-store') => new Response(JSON.stringify(data), {
  headers: {'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': cacheControl}
});
export async function onRequestGet({request, waitUntil}) {
  const cache = globalThis.caches?.default;
  const cacheKey = new Request(new URL('/api/exchange-rates', request.url));
  const cached = await cache?.match(cacheKey);
  if (cached) {
    const data = await cached.clone().json();
    if (Date.parse(data.expiresAt) > Date.now()) return cached;
  }
  try {
    const response = await fetch(SOURCE, {headers: {'Accept': 'application/json'}, signal: AbortSignal.timeout(10000)});
    if (!response.ok) throw new Error('Unavailable');
    const raw = await response.json();
    const quotes = PAIRS.map(pair => {
      const quote = raw[pair.key];
      const ask = Number(quote?.ask);
      const quotedAt = Number(quote?.timestamp) * 1000;
      if (!Number.isFinite(ask) || ask <= 0 || !Number.isFinite(quotedAt) || quotedAt <= 0) throw new Error('Invalid quote');
      return {id: pair.id, base: pair.base, target: pair.target, ask, quotedAt: new Date(quotedAt).toISOString()};
    });
    const now = Date.now();
    const data = {available: true, source: 'AwesomeAPI', quotes, checkedAt: new Date(now).toISOString(), expiresAt: new Date(now + 10800000).toISOString()};
    const result = json(data, 'public, max-age=10800');
    if (cache) waitUntil(cache.put(cacheKey, result.clone()));
    return result;
  } catch {
    return json({available: false});
  }
}
