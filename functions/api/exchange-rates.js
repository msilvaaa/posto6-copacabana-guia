const SOURCE = 'https://economia.awesomeapi.com.br/json/last/USD-BRLT,USD-ARS,USD-EUR,USD-BRL';
const PAIRS = [
  {id: 'usd-tourism', key: 'USDBRLT', base: 'USD', target: 'BRL'},
  {id: 'ars', key: 'USDARS', base: 'USD', target: 'ARS'},
  {id: 'eur', key: 'USDEUR', base: 'USD', target: 'EUR'},
  {id: 'brl', key: 'USDBRL', base: 'USD', target: 'BRL'}
];
const json = (data, cacheControl = 'no-store') => new Response(JSON.stringify(data), {
  headers: {'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': cacheControl}
});
export async function onRequestGet(context) {
  const force = new URL(context.request.url).searchParams.get('refresh') === '1';
  const {request} = context;
  const cache = globalThis.caches?.default;
  const cacheKey = new Request(new URL('/api/exchange-rates?basis=usd-buy-v2', request.url));
  const cached = force ? null : await cache?.match(cacheKey);
  if (cached) {
    const data = await cached.clone().json();
    if (data.side === 'buy' && data.basis === 'USD' && Date.parse(data.expiresAt) > Date.now()) return cached;
  }
  try {
    const response = await fetch(SOURCE, {cache:'no-store', headers: {'Accept': 'application/json'}, signal: AbortSignal.timeout(10000)});
    if (!response.ok) return json({available: false, reason: `source_http_${response.status}`});
    const raw = await response.json();
    const quotes = PAIRS.map(pair => {
      const quote = raw[pair.key];
      const bid = Number(quote?.bid);
      const quotedAt = Number(quote?.timestamp) * 1000;
      if (!Number.isFinite(bid) || bid <= 0 || !Number.isFinite(quotedAt) || quotedAt <= 0) throw new Error('Invalid quote');
      return {id: pair.id, base: pair.base, target: pair.target, bid, quotedAt: new Date(quotedAt).toISOString()};
    });
    const now = Date.now();
    const data = {available: true, source: 'AwesomeAPI', side: 'buy', basis: 'USD', quotes, checkedAt: new Date(now).toISOString(), expiresAt: new Date(now + 86400000).toISOString()};
    const result = json(data, 'public, max-age=86400');
    if (cache) {
      try { context.waitUntil(cache.put(cacheKey, result.clone())); }
      catch { console.warn('Response cache unavailable'); }
    }
    if (force) {
      const fresh = new Response(result.body, result);
      fresh.headers.set('Cache-Control', 'no-store');
      return fresh;
    }
    return result;
  } catch {
    return json({available: false, reason: 'source_unavailable'});
  }
}
