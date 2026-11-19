import {REFRESH_MS, MARINE_URL, WIND_URL, conditions} from './marine-data.js';

const panel = document.querySelector('[data-sea-conditions]');
if (panel) {
  const lang = document.documentElement.lang;
  const locale = {pt:'pt-BR', en:'en-US', es:'es-ES'}[lang] || 'pt-BR';
  const words = {
    pt: {loading:'Consultando previsão…', missing:'Previsão temporariamente indisponível.', forecast:'Previsão para', checked:'Consultado em', refresh:'Atualização em segundo plano a cada hora e ao abrir a página.', directions:['N','NE','L','SE','S','SO','O','NO']},
    en: {loading:'Checking forecast…', missing:'Forecast temporarily unavailable.', forecast:'Forecast for', checked:'Checked at', refresh:'Updated in the background hourly and on page entry.', directions:['N','NE','E','SE','S','SW','W','NW']},
    es: {loading:'Consultando previsión…', missing:'Previsión temporalmente no disponible.', forecast:'Previsión para', checked:'Consultado a las', refresh:'Actualización en segundo plano cada hora y al abrir la página.', directions:['N','NE','E','SE','S','SO','O','NO']}
  }[lang] || {};
  const status = panel.querySelector('[data-sea-status]');
  const storageKey = 'posto6-sea-conditions-v1';
  const number = new Intl.NumberFormat(locale, {maximumFractionDigits:1});
  const date = new Intl.DateTimeFormat(locale, {timeZone:'America/Sao_Paulo', day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit', hourCycle:'h23'});
  let expiry = 0, pending = false, timer, displayed = null;
  const savedLabel = {pt:'Última previsão salva', en:'Last saved forecast', es:'Última previsión guardada'}[lang];
  function valid(data) {
    return data?.available && Number.isFinite(Date.parse(data.expiresAt)) &&
      Number.isFinite(Date.parse(data.checkedAt)) &&
      Number.isFinite(Date.parse(data.waveForecastAt || data.windForecastAt)) &&
      (Number.isFinite(data.waveHeight) || Number.isFinite(data.windSpeed));
  }
  function degrades(data, previous) {
    return previous && ['waveHeight','windSpeed'].some(key => Number.isFinite(previous[key]) && !Number.isFinite(data[key]));
  }
  function render(data) {
    if (!valid(data)) return false;
    for (const key of ['waveHeight','windSpeed','windGusts']) {
      const output = panel.querySelector(`[data-sea-value="${key}"]`);
      const unit = key === 'waveHeight' ? 'm' : 'km/h';
      output.textContent = Number.isFinite(data[key]) ? `${number.format(data[key])} ${unit}` : '—';
    }
    panel.querySelector('[data-sea-period]').textContent = Number.isFinite(data.wavePeriod) ? `${number.format(data.wavePeriod)} s` : '';
    panel.querySelector('[data-sea-direction]').textContent = Number.isFinite(data.windDirection) ? words.directions[Math.round(data.windDirection / 45) % 8] : '';
    const forecast = data.waveForecastAt || data.windForecastAt;
    status.textContent = `${Date.parse(data.expiresAt) <= Date.now() ? savedLabel : words.forecast} ${date.format(new Date(forecast))} · ${words.checked} ${date.format(new Date(data.checkedAt))} (Brasília). ${words.refresh}`;
    displayed = data;
    return true;
  }
  async function refresh(force = false) {
    if (pending || (!force && expiry > Date.now())) return;
    pending = true;
    if (!displayed) status.textContent = words.loading;
    try {
      let data;
      try {
        const response = await fetch('/api/sea-conditions' + (force ? '?refresh=1' : ''), {cache:'no-store', signal:AbortSignal.timeout(15000)});
        if (!response.ok) throw new Error('Unavailable');
        data = await response.json();
        if (!data.available) throw new Error('Unavailable');
      } catch {
        const results = await Promise.all([MARINE_URL, WIND_URL].map(async url => {
          try { const response = await fetch(url, {cache:'no-store', signal:AbortSignal.timeout(12000)}); return response.ok ? await response.json() : null; }
          catch { return null; }
        }));
        data = conditions(...results);
      }
      if (!valid(data)) throw new Error('Unavailable');
      let previous = displayed;
      try { previous = JSON.parse(localStorage.getItem(storageKey)) || previous; } catch {}
      if (!degrades(data, previous) && (!valid(previous) || Date.parse(data.checkedAt) >= Date.parse(previous.checkedAt))) {
        try { localStorage.setItem(storageKey, JSON.stringify(data)); } catch {}
        // Existing visitors keep their visible snapshot; the new one is ready for the next visit.
        if (!displayed) render(data);
      }
      expiry = Math.max(Date.now() + REFRESH_MS, Date.parse(data.expiresAt));
    } catch { if (!displayed) status.textContent = `${words.missing} ${words.refresh}`; expiry = Date.now() + REFRESH_MS; }
    finally { pending = false; schedule(); }
  }
  function schedule() {
    clearTimeout(timer);
    timer = setTimeout(refresh, Math.max(1000, expiry - Date.now()));
  }
  async function enter() {
    try { render(JSON.parse(localStorage.getItem(storageKey))); } catch {}
    // This cache-only read never contacts forecast providers.
    try {
      const response = await fetch('/api/sea-conditions?cached=1', {cache:'no-store', signal:AbortSignal.timeout(2500)});
      const data = await response.json();
      if (valid(data) && !degrades(data, displayed) && (!displayed || Date.parse(data.checkedAt) > Date.parse(displayed.checkedAt))) render(data);
    } catch {}
    refresh(true);
  }
  enter();
  window.addEventListener('pageshow', event => {if (event.persisted) enter();});
  document.addEventListener('visibilitychange', () => {if (!document.hidden) refresh();});
}
