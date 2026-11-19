(() => {
  'use strict';
  const labels=[...document.querySelectorAll('[data-airbnb-rating]')];
  if (!labels.length) return;
  const lang=document.documentElement.lang;
  const locale={pt:'pt-BR',en:'en-US',es:'es-ES'}[lang] || 'pt-BR';
  const words={pt:{airbnb:'no Airbnb',reviews:'avaliações',checked:'Avaliação consultada em'},en:{airbnb:'on Airbnb',reviews:'reviews',checked:'Rating checked at'},es:{airbnb:'en Airbnb',reviews:'reseñas',checked:'Valoración consultada a las'}}[lang];
  const period=12*60*60*1000;
  let pending=false,expiry=0,timer;
  function schedule(){clearTimeout(timer);timer=setTimeout(()=>{if(!document.hidden)refresh();else schedule();},expiry>Date.now()?Math.max(1000,expiry-Date.now()):period);}
  async function refresh(force=false){
    if(pending)return;pending=true;
    try {
      const response=await fetch('/api/airbnb-rating'+(force?'?refresh=1':''),{cache:'no-store',signal:AbortSignal.timeout(15000)});
      if(!response.ok)throw Error('Unavailable');
      const data=await response.json();const rating=Number(data.rating),count=data.review_count;
      if(!data.available || data.listing_id!=='48382177' || !Number.isFinite(rating) || rating<1 || rating>5 || !Number.isSafeInteger(count) || count<1 || !Number.isFinite(Date.parse(data.expiresAt)) || Date.parse(data.expiresAt)<=Date.now() || !Number.isFinite(Date.parse(data.checkedAt)))throw Error('Invalid rating');
      const checked=new Intl.DateTimeFormat(locale,{timeZone:'America/Sao_Paulo',dateStyle:'short',timeStyle:'short'}).format(new Date(data.checkedAt));
      for(const label of labels){
        const prefix=label.dataset.ratingPrefix || '';
        const score=new Intl.NumberFormat(locale,{minimumFractionDigits:2,maximumFractionDigits:2}).format(rating);
        label.replaceChildren(document.createTextNode(`${prefix}${score} ${words.airbnb}`),document.createElement('br'),document.createTextNode(`${new Intl.NumberFormat(locale).format(count)} ${words.reviews}`));
        label.title=`${words.checked} ${checked} (Brasília)`;
      }
      expiry=Date.parse(data.expiresAt);
    } catch {expiry=Date.now()+period; /* Keep the last genuinely confirmed, server-rendered rating. */}
    finally {pending=false;schedule();}
  }
  refresh(true);
  window.addEventListener('pageshow',event=>{if(event.persisted)refresh(true);});
  document.addEventListener('visibilitychange',()=>{if(!document.hidden && expiry<=Date.now())refresh();});
})();
