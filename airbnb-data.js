export const AIRBNB_REFRESH_MS = 12 * 60 * 60 * 1000;
export const AIRBNB_SOURCE = 'https://www.airbnb.com.br/h/posto6copa';
const LISTING_ID = '48382177';
const IDENTIFIER = 'RGVtYW5kU3RheUxpc3Rpbmc6NDgzODIxNzc=';
function attribute(tag, name) {
  const match = tag.match(new RegExp('\\b' + name + '\\s*=\\s*(["\\\'])(.*?)\\1', 'i'));
  return match?.[2];
}
function* objects(value) {
  if (value && typeof value === 'object') {
    yield value;
    for (const child of Object.values(value)) yield* objects(child);
  }
}
export function parseRating(html, now = Date.now()) {
  const canonical = [...html.matchAll(/<link\b[^>]*>/gi)].map(match=>match[0]).find(tag=>attribute(tag,'rel')?.toLowerCase()==='canonical');
  const url = new URL(attribute(canonical || '', 'href') || 'about:blank');
  if (url.protocol!=='https:' || url.hostname!=='www.airbnb.com.br' || url.pathname.replace(/\/$/,'')!==`/rooms/${LISTING_ID}`) throw new Error('Unexpected listing');
  const readings = new Map();
  for (const match of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi)) {
    if (attribute(match[1],'type')?.toLowerCase()!=='application/ld+json') continue;
    let data;try {data=JSON.parse(match[2]);} catch {continue;}
    for (const item of objects(data)) {
      const types=Array.isArray(item['@type']) ? item['@type'] : [item['@type']];
      if (!types.includes('VacationRental') || item.identifier!==IDENTIFIER) continue;
      const rating=Number(item.aggregateRating?.ratingValue);
      const rawCount=String(item.aggregateRating?.reviewCount ?? item.aggregateRating?.ratingCount ?? '');
      const count=Number(rawCount);
      if (!Number.isFinite(rating) || rating<1 || rating>5 || !/^[1-9][0-9]*$/.test(rawCount) || !Number.isSafeInteger(count)) continue;
      const score=rating.toFixed(2);readings.set(`${score}:${count}`,{rating:score,review_count:count});
    }
  }
  if (readings.size!==1) throw new Error('No unique confirmed rating');
  return {available:true,listing_id:LISTING_ID,source_url:AIRBNB_SOURCE,...readings.values().next().value,checkedAt:new Date(now).toISOString(),expiresAt:new Date(now+AIRBNB_REFRESH_MS).toISOString()};
}
