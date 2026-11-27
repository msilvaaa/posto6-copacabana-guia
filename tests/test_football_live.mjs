import test,{afterEach} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const moduleURL=source=>`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`;
const sharedURL=moduleURL(await readFile(new URL('../football-data.js',import.meta.url),'utf8'));
const {normalizeClub,weekWindow}=await import(sharedURL);
const source=(await readFile(new URL('../functions/api/rio-football.js',import.meta.url),'utf8')).replace("'../../football-data.js'",JSON.stringify(sharedURL));
const {onRequestGet}=await import(moduleURL(source));
const realFetch=globalThis.fetch;
afterEach(()=>{globalThis.fetch=realFetch;});
const now=Date.parse('2026-11-27T23:30:00Z');
const event=(id,date,state='pre')=>({id,date,timeValid:true,league:{slug:'bra.1'},competitions:[{status:{type:{state,completed:state==='post',name:state==='post'?'STATUS_FULL_TIME':'STATUS_SCHEDULED'}},competitors:[{homeAway:'home',team:{id:'819',displayName:'Flamengo'}},{homeAway:'away',team:{id:'6086',displayName:'Botafogo'}}]}]});
const payload=events=>({team:{id:'819'},events});
test('keeps the announced match after kick-off and advances only when completion is confirmed',()=>{
 const live=event('1','2026-11-27T23:00:00Z','in'),next=event('2','2026-11-29T20:00:00Z');
 assert.deepEqual(normalizeClub([payload([next]),payload([live])],'819',now).map(g=>g.id),['1','2']);
 const ended=event('1',live.date,'post');
 for(const feeds of [[payload([live,next]),payload([ended])],[payload([ended]),payload([live,next])]]) {
  assert.deepEqual(normalizeClub(feeds,'819',now).map(g=>g.id),['2']);
 }
});
test('does not assume completion from the scheduled start alone',()=>{
 const delayed=event('1','2026-11-27T23:00:00Z');
 assert.equal(normalizeClub([payload([delayed])],'819',now)[0].id,'1');
});
test('uses Rio calendar dates and excludes matches outside the current seven-day window',()=>{
 assert.deepEqual(weekWindow(Date.parse('2026-11-28T01:00Z')),{start:'2026-11-27',end:'2026-12-03'});
 const data=payload([event('1','2026-12-04T01:00Z'),event('2','2026-12-04T04:00Z')]);
 assert.deepEqual(normalizeClub([data],'819',now).map(g=>g.id),['1']);
});
test('rejects unrelated teams instead of publishing a false empty state',()=>{
 assert.throws(()=>normalizeClub([{team:{id:'99'},events:[]}],'819',now));
});
test('entry queries always fetch fresh upcoming and recent schedules, isolating failed clubs',async()=>{
 const calls=[];
 globalThis.fetch=async (url,options)=>{
  calls.push({url,options});
  const id=url.match(/teams\/(\d+)/)[1];
  if(id==='3445')return new Response('',{status:503});
  return Response.json({team:{id},events:[]});
 };
 const response=await onRequestGet();const data=await response.json();
 assert.equal(response.status,200);assert.equal(response.headers.get('Cache-Control'),'no-store');
 assert.equal(calls.length,8);assert.ok(calls.every(c=>c.options.cache==='no-store'));
 assert.equal(data.clubs.find(c=>c.id==='3445').available,false);
 assert.equal(data.clubs.find(c=>c.id==='819').available,true);
 await onRequestGet();assert.equal(calls.length,16);
});
test('provider failure returns unavailable rather than an empty replacement schedule',async()=>{
 globalThis.fetch=async()=>{throw new Error('Offline');};
 const response=await onRequestGet();assert.equal(response.status,503);
 const data=await response.json();assert.equal(data.available,false);
 assert.ok(data.clubs.every(c=>!c.available&&!('games' in c)));
});
