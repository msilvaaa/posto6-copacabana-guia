import test, {beforeEach, afterEach} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const shared = await readFile(new URL('../marine-data.js', import.meta.url), 'utf8');
const sharedURL = `data:text/javascript;base64,${Buffer.from(shared).toString('base64')}`;
const {conditions} = await import(sharedURL);
const api = (await readFile(new URL('../functions/api/sea-conditions.js', import.meta.url), 'utf8'))
  .replace("'../../marine-data.js'", JSON.stringify(sharedURL));
const {onRequestGet} = await import(`data:text/javascript;base64,${Buffer.from(api).toString('base64')}`);
const RealDate = Date, realFetch = fetch;
let now, calls, store, pending;
const marine = () => ({hourly:{time:[Math.floor(now / 3600000) * 3600 - 3600, Math.floor(now / 3600000) * 3600, Math.floor(now / 3600000) * 3600 + 3600], wave_height:[1,1.7,2], wave_period:[8,9,10]}});
const wind = () => ({hourly:{time:marine().hourly.time, wind_speed_10m:[10,18,22], wind_direction_10m:[45,180,270], wind_gusts_10m:[20,29,40]}});
beforeEach(() => {
  now = Date.parse('2026-11-18T14:25:00Z'); calls = []; store = new Map(); pending = [];
  globalThis.Date = class extends RealDate {constructor(...args){super(...(args.length ? args : [now]));} static now(){return now;}};
  globalThis.caches = {default:{match:async key => store.get(key.url)?.clone(), put:async (key,response) => store.set(key.url,response.clone())}};
  globalThis.fetch = async url => {calls.push(url); return Response.json(url.includes('marine-api') ? marine() : wind());};
});
afterEach(() => {globalThis.Date = RealDate; globalThis.fetch = realFetch; delete globalThis.caches;});
const context = () => ({request:new Request('https://example.pages.dev/api/sea-conditions'), waitUntil:p => pending.push(p)});
test('selects the current forecast hour, preserves units, and expires after exactly one hour', () => {
  const data = conditions(marine(),wind());
  assert.equal(data.waveHeight,1.7); assert.equal(data.windSpeed,18); assert.equal(data.windDirection,180);
  assert.equal(data.waveForecastAt,'2026-11-18T14:00:00.000Z');
  assert.equal(Date.parse(data.expiresAt) - Date.parse(data.checkedAt),3600000);
});
test('cached requests avoid both providers and expired cache fetches again', async () => {
  await onRequestGet(context()); await Promise.all(pending);
  await onRequestGet(context()); assert.equal(calls.length,2);
  now += 3600001; await onRequestGet(context()); assert.equal(calls.length,4);
});
test('a failed wave provider still returns wind, never invented waves', async () => {
  globalThis.fetch = async url => url.includes('marine-api') ? new Response('',{status:503}) : Response.json(wind());
  const response = await onRequestGet(context()); const data = await response.json();
  assert.equal(response.status,200); assert.equal(data.waveHeight,null); assert.equal(data.windSpeed,18);
});
test('missing or stale forecasts are unavailable and not cached', async () => {
  globalThis.fetch = async () => Response.json({hourly:{time:[1],wave_height:[1],wind_speed_10m:[10]}});
  const response = await onRequestGet(context());
  assert.equal(response.status,503); assert.equal((await response.json()).available,false); assert.equal(store.size,0);
});
test('null wave values do not become zero; genuine calm values remain zero', () => {
  const data = marine(); data.hourly.wave_height[1] = null;
  assert.equal(conditions(data,null).waveHeight,null);
  data.hourly.wave_height[1] = 0;
  assert.equal(conditions(data,null).waveHeight,0);
});

test('page entry bypasses valid sea and wind cache and retains the hourly interval', async () => {
  await onRequestGet(context()); await Promise.all(pending);
  now += 60000;
  const ctx = context(); ctx.request = new Request(ctx.request.url + '?refresh=1');
  const response = await onRequestGet(ctx); const data = await response.json(); await Promise.all(pending);
  assert.equal(calls.length, 4);
  assert.equal(response.headers.get('Cache-Control'), 'no-store');
  assert.equal(Date.parse(data.checkedAt), now);
  assert.equal(Date.parse(data.expiresAt) - now, 3600000);
  await onRequestGet(context()); assert.equal(calls.length, 4);
});
