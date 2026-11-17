import test, {beforeEach, afterEach} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const source = await readFile(new URL('../functions/api/exchange-rates.js', import.meta.url), 'utf8');
const {onRequestGet} = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const RealDate = Date, realFetch = fetch;
let now, calls, pending, stored;
const sample = {
  USDBRLT: {bid: '5.7', ask: '6.2', timestamp: '1794916500'},
  ARSBRL: {bid: '0.0036', ask: '0.003725', timestamp: '1794916500'},
  EURBRL: {bid: '6.3', ask: '6.36', timestamp: '1794916500'},
  BRLUSD: {bid: '0.172', ask: '0.173', timestamp: '1794916500'}
};
beforeEach(() => {
  now = Date.parse('2026-11-17T12:00:00Z'); calls = []; pending = []; stored = new Map();
  globalThis.Date = class extends RealDate {constructor(...args) {super(...(args.length ? args : [now]));} static now() {return now;}};
  globalThis.caches = {default: {match: async key => stored.get(key.url)?.clone(), put: async (key, response) => {stored.set(key.url, response.clone());}}};
  globalThis.fetch = async url => {calls.push(url); return Response.json(sample);};
});
afterEach(() => {globalThis.Date = RealDate; globalThis.fetch = realFetch; delete globalThis.caches;});
const context = (query = '') => ({request: new Request(`https://example.pages.dev/api/exchange-rates${query}`), waitUntil: promise => pending.push(promise)});
test('tourist dollar comes from USD-BRLT sell quote; each currency has an explicit target', async () => {
  const data = await (await onRequestGet(context())).json();
  assert.match(calls[0], /USD-BRLT/);
  assert.equal(data.available, true);
  assert.equal(data.quotes[0].ask, 6.2);
  assert.deepEqual(data.quotes.map(q => [q.base, q.target]), [['USD','BRL'],['ARS','BRL'],['EUR','BRL'],['BRL','USD']]);
  assert.equal(data.quotes[1].ask, 0.003725);
  assert.equal(Date.parse(data.expiresAt) - Date.parse(data.checkedAt), 10800000);
});
test('rates stay cached for three hours and URL queries do not bypass cache', async () => {
  await onRequestGet(context()); await Promise.all(pending);
  now += 3 * 3600000 - 1;
  await onRequestGet(context('?refresh=1')); assert.equal(calls.length, 1);
  now += 2;
  await onRequestGet(context()); assert.equal(calls.length, 2);
});
test('incomplete data is never presented as a current complete quote set', async () => {
  globalThis.fetch = async () => Response.json({USDBRLT: sample.USDBRLT});
  const data = await (await onRequestGet(context())).json();
  assert.equal(data.available, false); assert.equal(stored.size, 0);
});
