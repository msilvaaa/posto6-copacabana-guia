(() => {
 const schedule = document.querySelector('[data-football-schedule]');
 if (!schedule) return;
 const lang = document.documentElement.lang;
 const locale = {pt:'pt-BR',en:'en-GB',es:'es-ES'}[lang] || 'pt-BR';
 const days = {pt:['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'],en:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],es:['Dom','Lun','Mar','Mié','Jue','Vie','Sáb']}[lang] || [];
 const tbd = {pt:'Horário a confirmar',en:'Time to be confirmed',es:'Horario por confirmar'}[lang];
 const dateParts = date => new Intl.DateTimeFormat('en-US',{timeZone:'America/Sao_Paulo',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23',weekday:'short'}).formatToParts(new Date(date));
 const stamp = game => {
  const parts=dateParts(game.date), part=name=>parts.find(p=>p.type===name).value;
  const weekday=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(part('weekday'));
  return `${days[weekday]} · ${part('day')}/${part('month')} · ${game.time_confirmed?part('hour')+':'+part('minute'):tbd}`;
 };
 // Static fixtures remain visible throughout a failed or pending request.
 const renderClub = data => {
  const club = [...schedule.querySelectorAll('.football-club')].find(el=>el.dataset.club===data.id);
  if (!club || !data.available || !Array.isArray(data.games)) return;
  const game = data.games[0], list=club.querySelector('ul');
  if (game) {
   if (!/^\d+$/.test(game.id) || !Number.isFinite(Date.parse(game.date))) return;
   const item=document.createElement('li');item.className='football-fixture';item.dataset.matchStart=game.date;
   const time=document.createElement('time');time.dateTime=game.date;time.textContent=stamp(game);
   const link=document.createElement('a');link.href='https://www.espn.com.br/futebol/partida/_/jogoId/'+game.id;link.target='_blank';link.rel='noopener noreferrer';link.textContent=game.home+' × '+game.away;
   const competition=document.createElement('small');competition.textContent=game.competition;
   item.append(time,link,competition);list.replaceChildren(item);
  } else list.replaceChildren();
  club.querySelector('.football-empty').hidden=Boolean(game);
 };
 let inFlight=false;
 const refresh = async () => {
  if (inFlight || document.visibilityState==='hidden' || schedule.closest('[hidden]')) return;
  inFlight=true;
  try {
   const response=await fetch('/api/rio-football',{cache:'no-store',signal:AbortSignal.timeout(15000)});
   if (!response.ok) throw new Error('Unavailable');
   const data=await response.json();
   if (!data.available || !Array.isArray(data.clubs)) throw new Error('Unavailable');
   data.clubs.forEach(renderClub);
   const checked=schedule.querySelector('[data-football-checked]');
   if (checked && Number.isFinite(Date.parse(data.checkedAt))) checked.textContent=new Intl.DateTimeFormat(locale,{timeZone:'America/Sao_Paulo',day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).format(new Date(data.checkedAt));
   const period=schedule.querySelector('[data-football-window]');
   if (period && /^\d{4}-\d{2}-\d{2}$/.test(data.window?.start) && /^\d{4}-\d{2}-\d{2}$/.test(data.window?.end)) {
    const short=value=>value.slice(8,10)+'/'+value.slice(5,7);
    period.textContent=short(data.window.start)+'–'+short(data.window.end);
   }
  } catch {} finally {inFlight=false;}
 };
 refresh();
 window.addEventListener('pageshow',event=>{if(event.persisted)refresh();});
 document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')refresh();});
 const panel=schedule.closest('.activities-topic-panel');
 if (panel) new MutationObserver(()=>{if(!panel.hidden)refresh();}).observe(panel,{attributes:true,attributeFilter:['hidden']});
 setInterval(refresh,60000);
})();
