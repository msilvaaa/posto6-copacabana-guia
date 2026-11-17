import test, {beforeEach, afterEach} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const source = await readFile(new URL('../functions/api/exchange-rates.js', import.meta.url), 'utf8');
const {onRequestGet} = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const RealDate = Date, realFetch = fetch;
let now, calls, pending, stored;
const sample = {
  USDBRLT: {bid: '5.7', ask: '6.2', timestamp: '1794916500'},
  USDARS: {bid: '1552.23', ask: '1553.00', timestamp: '1794916500'},
  USDEUR: {bid: '0.90911', ask: '0.91911', timestamp: '1794916500'},
  USDBRL: {bid: '5.7792', ask: '5.7892', timestamp: '1794916500'}
};
beforeEach(() => {
  now = Date.parse('2026-11-17T12:00:00Z'); calls = []; pending = []; stored = new Map();
  globalThis.Date = class extends RealDate {constructor(...args) {super(...(args.length ? args : [now]));} static now() {return now;}};
  globalThis.caches = {default: {match: async key => stored.get(key.url)?.clone(), put: async (key, response) => {stored.set(key.url, response.clone());}}};
  globalThis.fetch = async url => {calls.push(url); return Response.json(sample);};
});
afterEach(() => {globalThis.Date = RealDate; globalThis.fetch = realFetch; delete globalThis.caches;});
const context = (query = '') => ({request: new Request(`https://example.pages.dev/api/exchange-rates${query}`), waitUntil: promise => pending.push(promise)});
test('tourist dollar comes from USD-BRLT buy quote; each currency has an explicit target', async () => {
  const data = await (await onRequestGet(context())).json();
  assert.match(calls[0], /USD-BRLT/);
  assert.equal(data.available, true);
  assert.equal(data.quotes[0].bid, 5.7);
  assert.deepEqual(data.quotes.map(q => [q.base, q.target]), [['USD','BRL'],['USD','ARS'],['USD','EUR'],['USD','BRL']]);
  assert.equal(data.quotes[1].bid, 1552.23);
  assert.equal(Date.parse(data.expiresAt) - Date.parse(data.checkedAt), 86400000);
});
test('rates stay cached for 24 hours and URL queries do not bypass cache', async () => {
  await onRequestGet(context()); await Promise.all(pending);
  now += 24 * 3600000 - 1;
  await onRequestGet(context('?refresh=1')); assert.equal(calls.length, 1);
  now += 2;
  await onRequestGet(context()); assert.equal(calls.length, 2);
});
test('incomplete data is never presented as a current complete quote set', async () => {
  globalThis.fetch = async () => Response.json({USDBRLT: sample.USDBRLT});
  const data = await (await onRequestGet(context())).json();
  assert.equal(data.available, false); assert.equal(stored.size, 0);
});

test('Cloudflare waitUntil retains its execution context', async () => {
  const ctx = context();
  ctx.waitUntil = function(promise) {assert.equal(this, ctx); pending.push(promise);};
  const data = await (await onRequestGet(ctx)).json();
  assert.equal(data.available, true);
});

test('cache scheduling failure does not hide valid source quotes', async () => {
  const ctx = context();
  ctx.waitUntil = () => {throw new Error('cache context unavailable');};
  const data = await (await onRequestGet(ctx)).json();
  assert.equal(data.available, true);
});

test('old sale-rate cache is rejected after switching to buy rates and USD basis', async () => {
  const key = 'https://example.pages.dev/api/exchange-rates?basis=usd-buy-v2';
  stored.set(key, Response.json({available: true, side: 'sell', basis: 'BRL', expiresAt: new Date(now+86400000).toISOString()}));
  const data = await (await onRequestGet(context())).json();
  assert.equal(calls.length, 1);
  assert.equal(data.side, 'buy');
  assert.equal(data.basis, 'USD');
});
