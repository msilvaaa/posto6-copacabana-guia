(() => {
  'use strict';
  const box = document.querySelector('[data-exchange-rates]');
  if (!box) return;
  const lang = document.documentElement.lang;
  const locale = {pt: 'pt-BR', en: 'en-US', es: 'es-ES'}[lang] || 'pt-BR';
  const words = {
    pt: {unavailable: 'Cotações indisponíveis no momento.', unit: 'venda', checked: 'Consulta em', refresh: 'Consulta automática diária.'},
    en: {unavailable: 'Exchange rates currently unavailable.', unit: 'sell rate', checked: 'Checked at', refresh: 'Automatically checked daily.'},
    es: {unavailable: 'Cotizaciones no disponibles por el momento.', unit: 'venta', checked: 'Consulta a las', refresh: 'Consulta automáticdiária.'}
  }[lang];
  const dateFormat = new Intl.DateTimeFormat(locale, {timeZone: 'America/Sao_Paulo', day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'});
  const status = box.querySelector('[data-exchange-status]');
  let expiresAt = 0;
  let pending = false;
  function unavailable() {
    for (const card of box.querySelectorAll('[data-exchange-id]')) {
      card.querySelector('output').textContent = '—';
      card.querySelector('[data-exchange-unit]').textContent = '';
      card.querySelector('time').textContent = '';
      card.querySelector('time').removeAttribute('datetime');
    }
    status.textContent = words.unavailable;
    expiresAt = 0;
  }
  async function refresh() {
    if (pending) return;
    pending = true;
    try {
      const response = await fetch('/api/exchange-rates', {cache: 'no-store'});
      if (!response.ok) throw new Error('Unavailable');
      const data = await response.json();
      if (!data.available || Date.parse(data.expiresAt) <= Date.now()) throw new Error('Unavailable');
      for (const card of box.querySelectorAll('[data-exchange-id]')) {
        const quote = data.quotes.find(q => q.id === card.dataset.exchangeId);
        if (!quote || !Number.isFinite(quote.ask) || quote.ask <= 0) throw new Error('Invalid quote');
        const currency = quote.target === 'BRL' ? 'R$' : 'US$';
        const digits = quote.base === 'ARS' ? 6 : quote.base === 'BRL' ? 4 : 2;
        card.querySelector('output').textContent = `${currency} ${new Intl.NumberFormat(locale, {minimumFractionDigits: digits, maximumFractionDigits: digits}).format(quote.ask)}`;
        card.querySelector('[data-exchange-unit]').textContent = `1 ${quote.base} · ${words.unit}`;
        const time = card.querySelector('time');
        time.dateTime = quote.quotedAt;
        time.textContent = `${dateFormat.format(new Date(quote.quotedAt))} (Brasília)`;
      }
      expiresAt = Date.parse(data.expiresAt);
      status.textContent = `${words.checked} ${dateFormat.format(new Date(data.checkedAt))} (Brasília). ${words.refresh}`;
    } catch {
      unavailable();
    } finally {
      pending = false;
    }
  }
  refresh();
  setInterval(() => {if (!document.hidden) refresh();}, 86400000);
  document.addEventListener('visibilitychange', () => {if (!document.hidden && expiresAt <= Date.now()) refresh();});
})();
