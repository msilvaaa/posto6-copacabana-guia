(() => {
 const bar=document.querySelector('.activities-topic-tabs');
 if (!bar) return;
 const visualTabs=[...bar.querySelectorAll('[data-activities-topic]')];
 const tabs=[...visualTabs].sort((a,b)=>Number(a.dataset.activitiesTopic)-Number(b.dataset.activitiesTopic));
 const panels=[...document.querySelectorAll('.activities-topic-panel')];
 function select(index,remember=false,focus=false) {
  if (!tabs[index] || !panels[index]) return;
  tabs.forEach((tab,i)=>{
   const active=i===index;
   tab.setAttribute('aria-selected',String(active));
   tab.tabIndex=active?0:-1;
   if (active) tab.setAttribute('aria-current','page'); else tab.removeAttribute('aria-current');
   panels[i].hidden=!active;
  });
  for (const photo of document.querySelectorAll('[data-topic-photo]')) photo.hidden=Number(photo.dataset.topicPhoto)!==index;
  for (const flag of document.querySelectorAll('.guide-flag')) {
   const destination=flag.getAttribute('data-activities-path-'+index);
   if (destination) flag.href=destination;
  }
  document.title=document.body.dataset.activitiesTitle+' — '+tabs[index].textContent.trim();
  if (remember && new URL(tabs[index].href).pathname!==location.pathname) history.pushState({topic:index},'',tabs[index].href);
  if (focus) tabs[index].focus();
 }
 function current() {return Math.max(0,tabs.findIndex(tab=>new URL(tab.href).pathname===location.pathname));}
 bar.addEventListener('click',event=>{
  const tab=event.target.closest('[data-activities-topic]');
  if (!tab || event.button!==0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  event.preventDefault();select(Number(tab.dataset.activitiesTopic),true);
 });
 bar.addEventListener('keydown',event=>{
  const tab=event.target.closest('[data-activities-topic]');
  if (!tab) return;
  let index=visualTabs.indexOf(tab);
  if (event.key==='ArrowRight') index=(index+1)%tabs.length;
  else if (event.key==='ArrowLeft') index=(index+tabs.length-1)%tabs.length;
  else if (event.key==='Home') index=0;
  else if (event.key==='End') index=tabs.length-1;
  else return;
  event.preventDefault();select(Number(visualTabs[index].dataset.activitiesTopic),true,true);
 });
 window.addEventListener('popstate',()=>select(current()));
 select(current());
})();
