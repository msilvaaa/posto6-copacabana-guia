import {AIRBNB_REFRESH_MS, AIRBNB_SOURCE, parseRating} from '../../airbnb-data.js';
export async function onRequestGet(context) {
  const force=new URL(context.request.url).searchParams.get('refresh')==='1';
  const cache=globalThis.caches?.default;
  const key=new Request(new URL('/api/airbnb-rating',context.request.url));
  const cached=force ? null : await cache?.match(key);
  if (cached) {
    const data=await cached.clone().json();
    if (data.available && data.listing_id==='48382177' && Date.parse(data.expiresAt)>Date.now()) return cached;
  }
  try {
    const source=await fetch(AIRBNB_SOURCE,{cache:'no-store',headers:{'User-Agent':'Posto6CopacabanaGuide/1.0','Accept':'text/html'},signal:AbortSignal.timeout(12000)});
    if (!source.ok || !source.headers.get('Content-Type')?.includes('text/html')) throw new Error('Unavailable');
    if (source.url && new URL(source.url).hostname!=='www.airbnb.com.br') throw new Error('Unexpected destination');
    const html=await source.text();if(html.length>5000000)throw new Error('Response too large');
    const data=parseRating(html);
    const response=Response.json(data,{headers:{'Cache-Control':`public, max-age=${AIRBNB_REFRESH_MS/1000}`}});
    if(cache){try{context.waitUntil(cache.put(key,response.clone()).catch(()=>{}));}catch{}}
    if(force){const fresh=new Response(response.body,response);fresh.headers.set('Cache-Control','no-store');return fresh;}
    return response;
  } catch {
    return Response.json({available:false,reason:'source_unavailable'},{status:503,headers:{'Cache-Control':'no-store'}});
  }
}
