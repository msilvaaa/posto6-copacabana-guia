(() => {
 const bar=document.querySelector('.preview-pages');
 if (!bar) return;
 const tabs=[...bar.querySelectorAll('[data-preview-topic]')];
 const panels=[...document.querySelectorAll('.preview-topic-panel')];
 function select(index,remember=false,focus=false) {
  if (!tabs[index] || !panels[index]) return;
  tabs.forEach((tab,i)=>{
   const active=i===index;
   tab.setAttribute('aria-selected',String(active));
   tab.tabIndex=active?0:-1;
   if (active) tab.setAttribute('aria-current','page'); else tab.removeAttribute('aria-current');
   panels[i].hidden=!active;
  });
  for (const flag of document.querySelectorAll('.guide-flag')) {
   const destination=flag.getAttribute('data-preview-path-'+index);
   if (destination) flag.href=destination;
  }
  document.title=document.body.dataset.previewTitle+' — '+tabs[index].textContent.trim();
  if (remember && new URL(tabs[index].href).pathname!==location.pathname) history.pushState({topic:index},'',tabs[index].href);
  if (focus) tabs[index].focus();
 }
 function current() {return Math.max(0,tabs.findIndex(tab=>new URL(tab.href).pathname===location.pathname));}
 bar.addEventListener('click',event=>{
  const tab=event.target.closest('[data-preview-topic]');
  if (!tab || event.button!==0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  event.preventDefault();select(Number(tab.dataset.previewTopic),true);
 });
 bar.addEventListener('keydown',event=>{
  const tab=event.target.closest('[data-preview-topic]');
  if (!tab) return;
  let index=Number(tab.dataset.previewTopic);
  if (event.key==='ArrowRight') index=(index+1)%tabs.length;
  else if (event.key==='ArrowLeft') index=(index+tabs.length-1)%tabs.length;
  else if (event.key==='Home') index=0;
  else if (event.key==='End') index=tabs.length-1;
  else return;
  event.preventDefault();select(index,true,true);
 });
 window.addEventListener('popstate',()=>select(current()));
 select(current());
})();
