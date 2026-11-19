import test,{beforeEach,afterEach} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const moduleURL=source=>`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`;
const sharedURL=moduleURL(await readFile(new URL('../airbnb-data.js',import.meta.url),'utf8'));
const {parseRating}=await import(sharedURL);
const airbnbSource=(await readFile(new URL('../functions/api/airbnb-rating.js',import.meta.url),'utf8')).replace("'../../airbnb-data.js'",JSON.stringify(sharedURL));
const {onRequestGet:airbnb}=await import(moduleURL(airbnbSource));
const {onRequestGet:airports}=await import(moduleURL(await readFile(new URL('../functions/api/airport-transfers.js',import.meta.url),'utf8')));
const RealDate=Date,realFetch=fetch;
let now,calls,store,pending;
const sample=(score=4.98,count=120,id='48382177')=>`<link rel="canonical" href="https://www.airbnb.com.br/rooms/${id}"/><script type="application/ld+json">${JSON.stringify({'@type':'VacationRental',identifier:btoa('DemandStayListing:'+id),aggregateRating:{ratingValue:score,ratingCount:count}})}</script>`;
beforeEach(()=>{
 now=Date.parse('2026-11-19T15:00:00Z');calls=[];store=new Map();pending=[];
 globalThis.Date=class extends RealDate{constructor(...a){super(...(a.length?a:[now]));}static now(){return now;}};
 globalThis.caches={default:{match:async key=>store.get(key.url)?.clone(),put:async(key,data)=>store.set(key.url,data.clone())}};
 globalThis.fetch=async(url,options)=>{calls.push({url,options});return String(url).includes('airbnb')?new Response(sample(),{headers:{'Content-Type':'text/html'}}):Response.json({routes:[{duration:'1200s',distanceMeters:8300}]});};
});
afterEach(()=>{globalThis.Date=RealDate;globalThis.fetch=realFetch;delete globalThis.caches;});
const context=(path,force=false,configured=true)=>({request:new Request('https://example.pages.dev/api/'+path+(force?'?refresh=1':'')),env:configured?{GOOGLE_MAPS_ROUTES_API_KEY:'test-only'}:{},waitUntil:p=>pending.push(p)});
test('Airbnb validates listing identity, count and score before accepting live data',()=>{
 assert.equal(parseRating(sample()).rating,'4.98');
 assert.throws(()=>parseRating(sample(4.98,120,'123')));
 assert.throws(()=>parseRating(sample(6)));
 assert.throws(()=>parseRating(sample(4.98,0)));
 assert.throws(()=>parseRating(sample()+sample(4.99)));
 assert.throws(()=>parseRating('<html>temporarily unavailable</html>'));
});
test('Airbnb uses twelve hours normally and bypasses valid cache on each forced entry',async()=>{
 const first=await (await airbnb(context('airbnb-rating'))).json();await Promise.all(pending);
 assert.equal(Date.parse(first.expiresAt)-now,43200000);
 await airbnb(context('airbnb-rating'));assert.equal(calls.length,1);
 now+=1000;const response=await airbnb(context('airbnb-rating',true));const fresh=await response.json();await Promise.all(pending);
 assert.equal(calls.length,2);assert.equal(Date.parse(fresh.checkedAt),now);assert.equal(response.headers.get('Cache-Control'),'no-store');
 assert.equal(Date.parse(fresh.expiresAt)-now,43200000);
});
test('Airbnb blocked or unrelated source never overwrites a valid cached rating',async()=>{
 await airbnb(context('airbnb-rating'));await Promise.all(pending);
 globalThis.fetch=async()=>new Response('Blocked',{status:403});
 assert.equal((await airbnb(context('airbnb-rating',true))).status,503);
 assert.equal((await (await airbnb(context('airbnb-rating'))).json()).rating,'4.98');
});
test('airport traffic is cached for thirty minutes and queried immediately on forced entry',async()=>{
 const first=await (await airports(context('airport-transfers'))).json();await Promise.all(pending);
 assert.equal(Date.parse(first.expiresAt)-now,1800000);assert.equal(calls.length,2);
 await airports(context('airport-transfers'));assert.equal(calls.length,2);
 now+=1000;const response=await airports(context('airport-transfers',true));const fresh=await response.json();await Promise.all(pending);
 assert.equal(calls.length,4);assert.equal(response.headers.get('Cache-Control'),'no-store');assert.equal(Date.parse(fresh.updatedAt),now);
 assert.equal(Date.parse(fresh.expiresAt)-now,1800000);
});
test('unconfigured airport traffic remains unavailable without invented journey times',async()=>{
 const data=await (await airports(context('airport-transfers',true,false))).json();assert.equal(data.available,false);assert.equal(data.reason,'not_configured');assert.equal(calls.length,0);
});
