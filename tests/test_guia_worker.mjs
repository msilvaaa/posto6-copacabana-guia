import {test} from 'node:test';
import assert from 'node:assert/strict';
import worker,{handle,rewriteText,UPSTREAM} from '../deployment/guia/worker.mjs';
test('prefixes HTML, JS, CSS and srcset without changing external URLs',()=>{
 const out=rewriteText(`<a href="/pt/">PT</a><script>fetch('/api/weather');let x='/guia/es/';let y='https://example.com/pt';</script><style>x{background:url(/assets/a.png)}</style><img srcset="/assets/a.png 1x, /assets/b.png 2x">`);
 assert.match(out,/href="\/guia\/pt\//);assert.match(out,/fetch\('\/guia\/api\/weather'\)/);
 assert.match(out,/let x='\/guia\/es\//);assert.match(out,/https:\/\/example.com\/pt/);
 assert.match(out,/url\(\/guia\/assets\/a.png\)/);assert.match(out,/\/guia\/assets\/b.png 2x/);
});
test('old routes bypass the new upstream entirely',async()=>{
 for(const path of ['/pt','/es','/eua','/','/_assets/old.js','/guiabc']) {
  const request=new Request('https://posto6copacabana.com.br'+path);let seen;
  const response=await handle(request,async input=>{seen=input;return new Response('old')});
  assert.equal(seen,request);assert.equal(await response.text(),'old');
 }
});
test('entry redirect retains query and APIs preserve their query',async()=>{
 const root=await handle(new Request('https://posto6copacabana.com.br/guia?x=1'));
 assert.equal(root.status,308);assert.equal(root.headers.get('location'),'https://posto6copacabana.com.br/guia/?x=1');
 let seen;await handle(new Request('https://posto6copacabana.com.br/guia/api/weather?refresh=1'),async request=>{seen=request.url;return new Response('{}',{headers:{'content-type':'application/json'}})});
 assert.equal(seen,UPSTREAM+'/api/weather?refresh=1');
});
test('rewrites upstream redirects and strips credentials/invalid body metadata',async()=>{
 let seen;const response=await handle(new Request('https://posto6copacabana.com.br/guia/pt/',{headers:{Cookie:'old=private',Authorization:'Bearer private'}}),async request=>{
  seen=request;return new Response('<a href="/es/">ES</a>',{headers:{'content-type':'text/html','set-cookie':'private=x','content-length':'1','etag':'old','location':'/es/'}});
 });
 assert.equal(seen.headers.get('cookie'),null);assert.equal(seen.headers.get('authorization'),null);
 assert.equal(response.headers.get('set-cookie'),null);assert.equal(response.headers.get('etag'),null);assert.equal(response.headers.get('content-length'),null);
 assert.equal(response.headers.get('location'),'https://posto6copacabana.com.br/guia/es/');
 assert.match(await response.text(),/\/guia\/es\//);
});
test('Cloudflare module fetch accepts env as its second argument',async()=>{
 const old=globalThis.fetch;
 try {globalThis.fetch=async()=>new Response('ok');assert.equal(await (await worker.fetch(new Request('https://posto6copacabana.com.br/guia/a.png'),{})).text(),'ok');}
 finally {globalThis.fetch=old;}
});
