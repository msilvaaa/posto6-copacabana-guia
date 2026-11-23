(() => {
 const panel=document.querySelector('[data-sun-times]');
 if (!panel) return;
 const zone='America/Sao_Paulo';
 const date=new Intl.DateTimeFormat('sv-SE',{timeZone:zone,year:'numeric',month:'2-digit',day:'2-digit'});
 const time=new Intl.DateTimeFormat('en-GB',{timeZone:zone,hour:'2-digit',minute:'2-digit',hourCycle:'h23'});
 let saved={},lastDate='';
 try {saved=JSON.parse(document.querySelector('[data-sun-saved]').textContent);} catch {}
 function render(data) {
  const today=date.format(new Date());
  const row=data?.timezone===zone && data.days?.find(day=>day.date===today);
  const valid=row && ['sunrise','sunset'].every(key=>typeof row[key]==='string' && row[key].startsWith(today+'T') && Number.isFinite(Date.parse(row[key])));
  for (const key of ['sunrise','sunset']) {
   const output=panel.querySelector(`[data-sun-value="${key}"]`);
   output.textContent=valid?time.format(new Date(row[key])):'—';
   if (valid) output.dateTime=row[key]; else output.removeAttribute('datetime');
  }
  lastDate=today;
  return Boolean(valid);
 }
 async function check() {
  render(saved);
  try {
   const response=await fetch('/data/sun-times.json',{cache:'no-cache',signal:AbortSignal.timeout(6000)});
   if (!response.ok) return;
   const data=await response.json();
   if (data?.timezone===zone && Array.isArray(data.days) && data.days.some(day=>day.date===lastDate)) {
    if (render(data)) saved=data; else render(saved);
   }
  } catch {} // Saved days remain visible when offline or during a slow fetch.
 }
 check();
 window.addEventListener('pageshow',event=>{if(event.persisted)check();});
 document.addEventListener('visibilitychange',()=>{if(!document.hidden && date.format(new Date())!==lastDate)check();});
 setInterval(()=>{if(date.format(new Date())!==lastDate)check();},30000);
})();
