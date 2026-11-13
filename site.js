(() => {
 'use strict';
 const lang = document.documentElement.lang || 'pt';
 const locale = {pt:'pt-BR',en:'en-US',es:'es-ES'}[lang] || 'pt-BR';
 const strings = {
  pt:{external:'Abre em outra aba',unavailable:'Previsão indisponível no momento',rain:'Chance de chuva',updated:'Dados da previsão atualizados em',refresh:'Consulta automática a cada 30 minutos. O horário acima muda quando a previsão muda.',region:'Previsão regional para Copacabana, Rio de Janeiro.',stale:'Esta é a última previsão disponível; os dados podem estar desatualizados.'},
  en:{external:'Opens in a new tab',unavailable:'Forecast currently unavailable',rain:'Chance of rain',updated:'Forecast data updated on',refresh:'Automatically checked every 30 minutes. The time above changes when the forecast changes.',region:'Regional forecast for Copacabana, Rio de Janeiro.',stale:'This is the last available forecast; the data may be outdated.'},
  es:{external:'Abre en otra pestaña',unavailable:'Pronóstico no disponible por el momento',rain:'Probabilidad de lluvia',updated:'Datos del pronóstico actualizados el',refresh:'Consulta automática cada 30 minutos. La hora anterior cambia cuando cambia el pronóstico.',region:'Pronóstico regional para Copacabana, Río de Janeiro.',stale:'Este es el último pronóstico disponible; los datos pueden estar desactualizados.'}
 }[lang] || {};
 for (const anchor of document.querySelectorAll('a[href]')) {
  const url = new URL(anchor.href, location.href);
  if (/^https?:$/.test(url.protocol) && url.origin !== location.origin) {
   anchor.target = '_blank'; anchor.rel = 'noopener noreferrer';
   anchor.title = anchor.title ? `${anchor.title} — ${strings.external}` : strings.external;
  }
 }
 const viewer = document.querySelector('[data-photo-dialog]');
 const stage = document.querySelector('[data-photo-stage]');
 let trigger = null;
 document.addEventListener('click', event => {
  const source = event.target.closest('[data-photo-open]');
  if (!source || !viewer || !viewer.showModal) return;
  event.preventDefault(); trigger = source;
  stage.classList.toggle('has-guide', source.hasAttribute('data-photo-guide'));
  const canvas = source.hasAttribute('data-photo-guide') ? source.closest('.site-frame').querySelector('.guide-canvas').cloneNode(true) : null;
  const image = new Image();
  image.alt = source.dataset.photoAlt || source.querySelector('img')?.alt || '';
  image.src = source.dataset.photoSrc || source.href;
  if (canvas) {
   canvas.style.maxWidth = '';
   canvas.style.setProperty('--source-width', canvas.querySelector('.guide-image').getAttribute('width')+'px');
   stage.replaceChildren(canvas);
  } else stage.replaceChildren(image);
  stage.classList.remove('is-native');
  const button = viewer.querySelector('[data-photo-native]'); button.textContent = button.dataset.nativeLabel;
  viewer.showModal();
 });
 document.querySelector('[data-photo-close]')?.addEventListener('click', () => viewer.close());
 document.querySelector('[data-photo-native]')?.addEventListener('click', event => {
  const native = stage.classList.toggle('is-native');
  event.currentTarget.textContent = native ? event.currentTarget.dataset.fitLabel : event.currentTarget.dataset.nativeLabel;
 });
 viewer?.addEventListener('close', () => { stage.replaceChildren(); trigger?.focus(); });
 const weatherDialog = document.querySelector('[data-weather-dialog]');
 let weatherRequest;
 let weatherReadAt = 0;
 const weatherRefreshMs = 30 * 60 * 1000;
 async function loadWeather() {
  if (weatherRequest && Date.now() - weatherReadAt < weatherRefreshMs) return weatherRequest;
  weatherReadAt = Date.now();
  weatherRequest = fetch('/data/weather.json', {cache:'no-cache'}).then(response => {
   if (!response.ok) throw new Error('Forecast unavailable'); return response.json();
  }).then(data => {
   const content = document.querySelector('[data-weather-content]');
   content.replaceChildren();
   const grid = document.createElement('div'); grid.className = 'weather-days';
   const today = new Intl.DateTimeFormat('sv-SE',{timeZone:'America/Sao_Paulo',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
   const upcoming = data.days.filter(day => day.date >= today);
   if (!upcoming.length) throw new Error('Expired forecast');
   for (const day of upcoming.slice(0,3)) {
    const card = document.createElement('div'); card.className = 'weather-day';
    const date = new Date(day.date+'T12:00:00-03:00');
    const title = document.createElement('b'); title.textContent = new Intl.DateTimeFormat(locale,{weekday:'short',day:'2-digit',month:'2-digit',timeZone:'America/Sao_Paulo'}).format(date);
    const icon = document.createElement('span'); icon.textContent = day.rain_probability>=50 ? '🌧' : day.code==='113' ? '☀' : '⛅'; icon.setAttribute('aria-hidden','true');
    const temperature = document.createElement('span'); temperature.textContent = `${day.min}° – ${day.max}°C`;
    const rain = document.createElement('span'); rain.textContent = `${strings.rain}: ${day.rain_probability}%`;
    card.append(title,icon,temperature,rain); grid.append(card);
   }
   const note = document.createElement('p'); note.textContent = strings.region;
   const updated = document.createElement('p'); updated.textContent = `${strings.updated} ${new Intl.DateTimeFormat(locale,{dateStyle:'short',timeStyle:'short',timeZone:'America/Sao_Paulo'}).format(new Date(data.updated_at))}`;
   const refresh = document.createElement('p'); refresh.textContent = strings.refresh;
   content.append(grid,note,updated,refresh);
   const old = Date.now()-Date.parse(data.updated_at)>24*60*60*1000;
   if (old) { const warning=document.createElement('p'); warning.textContent=strings.stale; content.append(warning); }
   for (const summary of document.querySelectorAll('[data-weather-summary]')) summary.textContent = old ? strings.stale : `${upcoming[0].min}° – ${upcoming[0].max}°C`;
   return data;
  }).catch(() => {
   weatherRequest = null;
   const content=document.querySelector('[data-weather-content]');
   if (content) content.textContent = strings.unavailable;
   for (const summary of document.querySelectorAll('[data-weather-summary]')) summary.textContent = strings.unavailable;
  });
  return weatherRequest;
 }
 document.querySelector('[data-weather-open]')?.addEventListener('click', () => { weatherDialog?.showModal(); loadWeather(); });
 document.querySelector('[data-weather-close]')?.addEventListener('click', () => weatherDialog.close());
 if (document.querySelector('[data-weather-summary]')) {
  loadWeather();
  setInterval(() => { if (document.visibilityState === 'visible') loadWeather(); }, weatherRefreshMs);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') loadWeather(); });
 }
})();
