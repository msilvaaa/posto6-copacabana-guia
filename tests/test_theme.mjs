import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';
const source = await readFile(new URL('../theme.js', import.meta.url), 'utf8');
function browser({lang='pt', saved=null, blocked=false}={}) {
  const events={}, attributes={}, clicks={};
  const root={lang, dataset:{}};
  const icon={src:''};
  const button={title:'', setAttribute:(key,value)=>attributes[key]=value, querySelector:()=>icon, addEventListener:(key,handler)=>clicks[key]=handler};
  const storage={value:saved,getItem(){if(blocked)throw Error('Blocked');return this.value;},setItem(key,value){if(blocked)throw Error('Blocked');this.value=value;}};
  const document={documentElement:root,readyState:'loading',querySelectorAll:()=>[button],addEventListener:(key,handler)=>events[key]=handler};
  const window={addEventListener:(key,handler)=>events[key]=handler};
  vm.runInNewContext(source,{document,window,localStorage:storage});
  return {root,icon,button,attributes,storage,events,setup:()=>events.DOMContentLoaded(),click:()=>clicks.click()};
}
test('saved theme is applied before controls mount, then the button changes and persists it',()=>{
  const page=browser({saved:'dark'});assert.equal(page.root.dataset.theme,'dark');page.setup();
  assert.equal(page.attributes['aria-pressed'],'true');
  page.click();assert.equal(page.root.dataset.theme,'light');assert.equal(page.storage.value,'light');
  assert.equal(page.attributes['aria-pressed'],'false');
});
test('default is light and the action label follows both the current mode and language',()=>{
  for(const [lang,dark,light] of [['pt','Ativar modo escuro','Ativar modo claro'],['en','Switch to dark mode','Switch to light mode'],['es','Activar modo oscuro','Activar modo claro']]){
    const page=browser({lang});page.setup();assert.equal(page.root.dataset.theme,'light');assert.equal(page.attributes['aria-label'],dark);
    page.click();assert.equal(page.attributes['aria-label'],light);assert.equal(page.button.title,light);
  }
});
test('unavailable local storage does not stop the control from switching themes',()=>{
  const page=browser({blocked:true});page.setup();page.click();assert.equal(page.root.dataset.theme,'dark');
  page.click();assert.equal(page.root.dataset.theme,'light');
});
test('cross-tab preference changes and back/forward restoration update the displayed theme',()=>{
  const page=browser();page.setup();page.storage.value='dark';page.events.storage({key:'posto6-theme'});assert.equal(page.root.dataset.theme,'dark');
  page.storage.value='light';page.events.pageshow({persisted:true});assert.equal(page.root.dataset.theme,'light');
});
