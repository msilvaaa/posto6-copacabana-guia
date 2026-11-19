import test, {beforeEach, afterEach} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const source = await readFile(new URL('../weather-data.js', import.meta.url), 'utf8');
const moduleURL = `data:text/javascript;base64,${Buffer.from(source).toString('base64')}`;
const api = (await readFile(new URL('../functions/api/weather.js', import.meta.url), 'utf8')).replace("'../../weather-data.js'", JSON.stringify(moduleURL));
const {onRequestGet} = await import(`data:text/javascript;base64,${Buffer.from(api).toString('base64')}`);
const RealDate = Date, realFetch = fetch;
let now, calls, pending, store;
const sample = () => ({weather:[19,20,21].map(day => ({date:`2026-11-${day}`,mintempC:'23',maxtempC:'27',hourly:[{chanceofrain:'20',weatherCode:'113'}]}))});
beforeEach(() => {
  now = Date.parse('2026-11-19T14:00:00Z'); calls=0; pending=[]; store=new Map();
  globalThis.Date = class extends RealDate {constructor(...args){super(...(args.length ? args : [now]));}static now(){return now;}};
  globalThis.fetch = async () => {calls++; return Response.json(sample());};
  globalThis.caches = {default:{match:async key => store.get(key.url)?.clone(),put:async (key,data) => store.set(key.url,data.clone())}};
});
afterEach(() => {globalThis.Date=RealDate;globalThis.fetch=realFetch;delete globalThis.caches;});
const context = (query='') => ({request:new Request('https://example.pages.dev/api/weather'+query),waitUntil:p => pending.push(p)});
test('forecast stays cached for three hours but page entry checks source immediately', async () => {
  const first = await (await onRequestGet(context())).json(); await Promise.all(pending);
  now+=60000;
  await onRequestGet(context()); assert.equal(calls,1);
  const response = await onRequestGet(context('?refresh=1'));
  const fresh = await response.json(); await Promise.all(pending);
  assert.equal(calls,2); assert.equal(response.headers.get('Cache-Control'),'no-store');
  assert.equal(Date.parse(fresh.checkedAt),now);
  assert.equal(fresh.updated_at,first.updated_at); // Unchanged forecasts must not pretend to change.
  assert.equal(Date.parse(fresh.expiresAt)-now,10800000);
  now+=10800001;
  await onRequestGet(context()); assert.equal(calls,3);
});
test('invalid live forecast fails explicitly without replacing valid cache', async () => {
  await onRequestGet(context()); await Promise.all(pending);
  globalThis.fetch=async () => Response.json({weather:[]});
  const response = await onRequestGet(context('?refresh=1'));
  assert.equal(response.status,503);
  assert.equal((await (await onRequestGet(context())).json()).days.length,3);
});
test('changed source values advance updated time and preserve rain and temperature values', async () => {
  await onRequestGet(context()); await Promise.all(pending);now+=60000;
  globalThis.fetch=async () => {const data=sample();data.weather[0].maxtempC='30';return Response.json(data);};
  const data=await (await onRequestGet(context('?refresh=1'))).json();
  assert.equal(Date.parse(data.updated_at),now);assert.equal(data.days[0].max,30);
  assert.equal(data.days[0].rain_probability,20);
});
