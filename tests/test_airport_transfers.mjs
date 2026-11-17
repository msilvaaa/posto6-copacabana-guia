import test, {beforeEach, afterEach} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

const source = await readFile(new URL('../functions/api/airport-transfers.js', import.meta.url), 'utf8');
const {onRequestGet} = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const realFetch = globalThis.fetch;
const RealDate = Date;
let now, calls, pending, cached;
beforeEach(() => {
  now = Date.parse('2026-11-17T12:00:00Z');
  globalThis.Date = class extends RealDate {constructor(...args) {super(...(args.length ? args : [now]));} static now() {return now;}};
  calls = [];
  pending = [];
  cached = new Map();
  globalThis.caches = {default: {
    match: async key => cached.get(key.url)?.clone(),
    put: async (key, response) => {cached.set(key.url, response.clone());}
  }};
  globalThis.fetch = async (url, options) => {
    calls.push({url, options, body: JSON.parse(options.body)});
    const sdu = JSON.parse(options.body).origin.address.includes('Santos Dumont');
    return Response.json({routes: [{duration: sdu ? '1200s' : '3000s', distanceMeters: sdu ? 8300 : 20000}]});
  };
});
afterEach(() => {globalThis.Date = RealDate; globalThis.fetch = realFetch; delete globalThis.caches;});
const context = (key = 'private-test-key', query = '') => ({
  request: new Request(`https://example.pages.dev/api/airport-transfers${query}`),
  env: key ? {GOOGLE_MAPS_ROUTES_API_KEY: key} : {},
  waitUntil: promise => pending.push(promise)
});

test('missing key makes no provider request and invents no durations', async () => {
  const data = await (await onRequestGet(context(''))).json();
  assert.equal(data.available, false);
  assert.equal(data.reason, 'not_configured');
  assert.equal(calls.length, 0);
});
test('both traffic-aware driving routes end at Rua Raul Pompéia 131; secret stays private', async () => {
  const data = await (await onRequestGet(context())).json();
  assert.equal(calls.length, 2);
  for (const call of calls) {
    assert.equal(call.body.travelMode, 'DRIVE');
    assert.equal(call.body.routingPreference, 'TRAFFIC_AWARE');
    assert.match(call.body.destination.address, /Rua Raul Pompéia, 131/);
  }
  assert.deepEqual(data.routes.map(route => route.minutes), [20, 50]);
  assert.equal(Date.parse(data.expiresAt) - Date.parse(data.updatedAt), 1800000);
  assert.ok(!JSON.stringify(data).includes('private-test-key'));
});
test('query strings cannot bypass the 30-minute cache; expiry triggers fresh traffic', async () => {
  await onRequestGet(context());
  await Promise.all(pending);
  now += 29 * 60 * 1000;
  await onRequestGet(context('private-test-key', '?fresh=1'));
  assert.equal(calls.length, 2);
  now += 60 * 1000 + 1;
  await onRequestGet(context());
  assert.equal(calls.length, 4);
});
test('provider failures do not reuse old or fabricated travel times', async () => {
  globalThis.fetch = async () => Response.json({error: 'unavailable'}, {status: 503});
  const data = await (await onRequestGet(context())).json();
  assert.equal(data.available, false);
  assert.ok(data.routes.every(route => !route.available && !('minutes' in route)));
  assert.equal(cached.size, 0);
});
