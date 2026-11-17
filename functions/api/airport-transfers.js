const REFRESH_MS = 30 * 60 * 1000;
const DESTINATION = 'Rua Raul Pompéia, 131, Copacabana, Rio de Janeiro, RJ, 22080-001, Brasil';
const AIRPORTS = [
  {id: 'sdu', address: 'Aeroporto Santos Dumont (SDU), Rio de Janeiro, RJ, Brasil'},
  {id: 'gig', address: 'Aeroporto Internacional do Galeão (GIG), Terminal 2, Rio de Janeiro, RJ, Brasil'}
];
const json = (data, cacheControl = 'no-store') => new Response(JSON.stringify(data), {
  headers: {'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': cacheControl}
});

export async function onRequestGet({request, env, waitUntil}) {
  const key = env.GOOGLE_MAPS_ROUTES_API_KEY;
  if (!key) return json({available: false, reason: 'not_configured'});
  const cache = globalThis.caches?.default;
  const cacheKey = new Request(new URL('/api/airport-transfers', request.url));
  const cached = await cache?.match(cacheKey);
  if (cached) {
    const data = await cached.clone().json();
    if (Date.parse(data.expiresAt) > Date.now()) return cached;
  }
  const updatedAt = new Date();
  const routes = await Promise.all(AIRPORTS.map(async airport => {
    try {
      const response = await fetch('https://routes.googleapis.com/directions/v2:computeRoutes', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-Goog-Api-Key': key, 'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters'},
        body: JSON.stringify({
          origin: {address: airport.address}, destination: {address: DESTINATION},
          travelMode: 'DRIVE', routingPreference: 'TRAFFIC_AWARE',
          computeAlternativeRoutes: false,
          languageCode: 'pt-BR', units: 'METRIC'
        }),
        signal: AbortSignal.timeout(10000)
      });
      if (!response.ok) return {id: airport.id, available: false};
      const route = (await response.json()).routes?.[0];
      const seconds = Number(String(route?.duration || '').replace(/s$/, ''));
      if (!Number.isFinite(seconds) || seconds <= 0 || !Number.isFinite(route?.distanceMeters) || route.distanceMeters <= 0) {
        return {id: airport.id, available: false};
      }
      return {id: airport.id, available: true, minutes: Math.ceil(seconds / 60), distanceMeters: route.distanceMeters};
    } catch {
      return {id: airport.id, available: false};
    }
  }));
  const available = routes.some(route => route.available);
  const data = {available, routes, updatedAt: updatedAt.toISOString(), expiresAt: new Date(updatedAt.getTime() + REFRESH_MS).toISOString()};
  if (!available) return json(data);
  const response = json(data, 'public, max-age=1800');
  if (cache) waitUntil(cache.put(cacheKey, response.clone()));
  return response;
}
