(() => {
  'use strict';
  const box = document.querySelector('[data-exchange-rates]');
  if (!box) return;
  const lang = document.documentElement.lang;
  const locale = {pt: 'pt-BR', en: 'en-US', es: 'es-ES'}[lang] || 'pt-BR';
  const words = {
    pt: {unavailable: 'Cotações indisponíveis no momento.', unit: 'venda', checked: 'Consulta em', refresh: 'Consulta automática diária.'},
    en: {unavailable: 'Exchange rates currently unavailable.', unit: 'sell rate', checked: 'Checked at', refresh: 'Automatically checked daily.'},
    es: {unavailable: 'Cotizaciones no disponibles por el momento.', unit: 'venta', checked: 'Consulta a las', refresh: 'Consulta automática diaria.'}
  }[lang];
  const dateFormat = new Intl.DateTimeFormat(locale, {timeZone: 'America/Sao_Paulo', day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'});
  const status = box.querySelector('[data-exchange-status]');
  let expiresAt = 0;
  let pending = false;
  let timer;
  function schedule() {
    clearTimeout(timer);
    const delay = expiresAt > Date.now() ? Math.max(1000, expiresAt - Date.now()) : 86400000;
    timer = setTimeout(() => {if (!document.hidden) refresh(); else schedule();}, delay);
  }
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
  const cacheKey = 'posto6-exchange-rates-v1';
  const pairs = [
    {id: 'usd-tourism', key: 'USDBRLT', base: 'USD', target: 'BRL'},
    {id: 'ars', key: 'ARSBRL', base: 'ARS', target: 'BRL'},
    {id: 'eur', key: 'EURBRL', base: 'EUR', target: 'BRL'},
    {id: 'brl', key: 'BRLUSD', base: 'BRL', target: 'USD'}
  ];
  function valid(data) {
    return data?.available && Date.parse(data.expiresAt) > Date.now() && Number.isFinite(Date.parse(data.checkedAt)) &&
      pairs.every(pair => data.quotes?.some(quote => quote.id === pair.id && quote.base === pair.base && quote.target === pair.target && Number.isFinite(quote.ask) && quote.ask > 0 && Number.isFinite(Date.parse(quote.quotedAt))));
  }
  function readCache() {
    try { const data = JSON.parse(localStorage.getItem(cacheKey)); return valid(data) ? data : null; }
    catch { return null; }
  }
  async function loadQuotes() {
    const cached = readCache();
    if (cached) return cached;
    let data;
    // The public source allows CORS; a direct request avoids shared-server rate limits.
    try {
      const response = await fetch('https://economia.awesomeapi.com.br/json/last/USD-BRLT,ARS-BRL,EUR-BRL,BRL-USD', {cache: 'no-store', signal: AbortSignal.timeout(10000)});
      if (!response.ok) throw new Error('Unavailable');
      const raw = await response.json();
      const now = Date.now();
      data = {available: true, checkedAt: new Date(now).toISOString(), expiresAt: new Date(now + 86400000).toISOString(),
        quotes: pairs.map(pair => ({id: pair.id, base: pair.base, target: pair.target, ask: Number(raw[pair.key]?.ask), quotedAt: new Date(Number(raw[pair.key]?.timestamp) * 1000).toISOString()}))};
      if (!valid(data)) throw new Error('Invalid quote');
    } catch {
      const response = await fetch('/api/exchange-rates', {cache: 'no-store', signal: AbortSignal.timeout(10000)});
      if (!response.ok) throw new Error('Unavailable');
      data = await response.json();
      if (!valid(data)) throw new Error('Unavailable');
    }
    try {localStorage.setItem(cacheKey, JSON.stringify(data));} catch { /* Storage may be unavailable in private browsing. */ }
    return data;
  }
  async function refresh() {
    if (pending) return;
    pending = true;
    try {
      const data = await loadQuotes();
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
      schedule();
    }
  }
  refresh();
  document.addEventListener('visibilitychange', () => {if (!document.hidden && expiresAt <= Date.now()) refresh();});
})();
