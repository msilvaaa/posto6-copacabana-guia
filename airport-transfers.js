(() => {
  'use strict';
  const container = document.querySelector('[data-airport-transfers]');
  if (!container) return;
  const lang = document.documentElement.lang;
  const locale = {pt: 'pt-BR', en: 'en-US', es: 'es-ES'}[lang] || 'pt-BR';
  const words = {
    pt: {consult: 'Consulte o tempo atual no Google Maps.', car: 'de carro', updated: 'Trânsito consultado em', refresh: 'Atualização automática a cada 30 minutos. O tempo é uma estimativa e varia com o trânsito.'},
    en: {consult: 'Check the current travel time on Google Maps.', car: 'by car', updated: 'Traffic checked at', refresh: 'Automatically refreshed every 30 minutes. Travel time is an estimate and varies with traffic.'},
    es: {consult: 'Consulta el tiempo actual en Google Maps.', car: 'en coche', updated: 'Tráfico consultado a las', refresh: 'Actualización automática cada 30 minutos. El tiempo es una estimación y varía con el tráfico.'}
  }[lang];
  const status = container.querySelector('[data-transfer-status]');
  const note = container.querySelector('[data-transfer-note]');
  let expiresAt = 0;
  let pending = false;
  function unavailable() {
    for (const output of container.querySelectorAll('[data-transfer-time]')) output.textContent = '';
    status.textContent = words.consult;
    note.textContent = '';
    expiresAt = 0;
  }
  async function refresh(force = false) {
    if (pending) return;
    pending = true;
    if (expiresAt <= Date.now()) unavailable();
    try {
      const response = await fetch('/api/airport-transfers' + (force ? '?refresh=1' : ''), {cache: 'no-store', signal:AbortSignal.timeout(15000)});
      if (!response.ok) throw new Error('Unavailable');
      const data = await response.json();
      const expiry = Date.parse(data.expiresAt);
      if (!data.available || !Number.isFinite(expiry) || expiry <= Date.now()) throw new Error('Unavailable');
      for (const output of container.querySelectorAll('[data-transfer-time]')) {
        const route = data.routes.find(route => route.id === output.dataset.transferTime && route.available);
        output.textContent = route ? `≈ ${route.minutes} min ${words.car} · ${new Intl.NumberFormat(locale, {maximumFractionDigits: 1}).format(route.distanceMeters / 1000)} km` : '';
      }
      expiresAt = expiry;
      status.textContent = `${words.updated} ${new Intl.DateTimeFormat(locale, {timeZone: 'America/Sao_Paulo', day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'}).format(new Date(data.updatedAt))} (Brasília).`;
      note.textContent = words.refresh;
    } catch {
      unavailable();
    } finally {
      pending = false;
    }
  }
  refresh(true);
  window.addEventListener('pageshow', event => {if (event.persisted) refresh(true);});
  setInterval(() => { if (!document.hidden) refresh(); }, 30 * 60 * 1000);
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden && expiresAt <= Date.now()) refresh();
  });
})();
