import {REFRESH_MS, MARINE_URL, WIND_URL, conditions} from './marine-data.js';

const panel = document.querySelector('[data-sea-conditions]');
if (panel) {
  const lang = document.documentElement.lang;
  const locale = {pt:'pt-BR', en:'en-US', es:'es-ES'}[lang] || 'pt-BR';
  const words = {
    pt: {loading:'Consultando previsão…', missing:'Previsão temporariamente indisponível.', forecast:'Previsão para', checked:'Consultado em', refresh:'Consulta automática a cada hora.', directions:['N','NE','L','SE','S','SO','O','NO']},
    en: {loading:'Checking forecast…', missing:'Forecast temporarily unavailable.', forecast:'Forecast for', checked:'Checked at', refresh:'Automatically checked every hour.', directions:['N','NE','E','SE','S','SW','W','NW']},
    es: {loading:'Consultando previsión…', missing:'Previsión temporalmente no disponible.', forecast:'Previsión para', checked:'Consultado a las', refresh:'Consulta automática cada hora.', directions:['N','NE','E','SE','S','SO','O','NO']}
  }[lang] || {};
  const status = panel.querySelector('[data-sea-status]');
  const storageKey = 'posto6-sea-conditions-v1';
  const number = new Intl.NumberFormat(locale, {maximumFractionDigits:1});
  const date = new Intl.DateTimeFormat(locale, {timeZone:'America/Sao_Paulo', day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit', hourCycle:'h23'});
  let expiry = 0, pending = false, timer;
  function render(data) {
    if (!data?.available || !Number.isFinite(Date.parse(data.expiresAt)) || Date.parse(data.expiresAt) <= Date.now()) return false;
    for (const key of ['waveHeight','windSpeed','windGusts']) {
      const output = panel.querySelector(`[data-sea-value="${key}"]`);
      const unit = key === 'waveHeight' ? 'm' : 'km/h';
      output.textContent = Number.isFinite(data[key]) ? `${number.format(data[key])} ${unit}` : '—';
    }
    panel.querySelector('[data-sea-period]').textContent = Number.isFinite(data.wavePeriod) ? `${number.format(data.wavePeriod)} s` : '';
    panel.querySelector('[data-sea-direction]').textContent = Number.isFinite(data.windDirection) ? words.directions[Math.round(data.windDirection / 45) % 8] : '';
    const forecast = data.waveForecastAt || data.windForecastAt;
    status.textContent = `${words.forecast} ${date.format(new Date(forecast))} · ${words.checked} ${date.format(new Date(data.checkedAt))} (Brasília). ${words.refresh}`;
    expiry = Date.parse(data.expiresAt);
    return true;
  }
  async function refresh() {
    if (pending || expiry > Date.now()) return;
    pending = true;
    for (const field of panel.querySelectorAll('[data-sea-value]')) field.textContent = '—';
    panel.querySelector('[data-sea-period]').textContent = '';
    panel.querySelector('[data-sea-direction]').textContent = '';
    status.textContent = words.loading;
    try {
      let data;
      try {
        const response = await fetch('/api/sea-conditions', {cache:'no-store', signal:AbortSignal.timeout(15000)});
        if (!response.ok) throw new Error('Unavailable');
        data = await response.json();
        if (!data.available) throw new Error('Unavailable');
      } catch {
        const results = await Promise.all([MARINE_URL, WIND_URL].map(async url => {
          try { const response = await fetch(url, {signal:AbortSignal.timeout(12000)}); return response.ok ? await response.json() : null; }
          catch { return null; }
        }));
        data = conditions(...results);
      }
      if (!render(data)) throw new Error('Unavailable');
      try { localStorage.setItem(storageKey, JSON.stringify(data)); } catch {}
    } catch { status.textContent = `${words.missing} ${words.refresh}`; expiry = Date.now() + REFRESH_MS; }
    finally { pending = false; schedule(); }
  }
  function schedule() {
    clearTimeout(timer);
    timer = setTimeout(refresh, Math.max(1000, expiry - Date.now()));
  }
  try { render(JSON.parse(localStorage.getItem(storageKey))); } catch {}
  if (expiry > Date.now()) schedule(); else refresh();
  document.addEventListener('visibilitychange', () => {if (!document.hidden) refresh();});
}
