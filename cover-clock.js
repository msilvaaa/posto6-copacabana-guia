(() => {
  'use strict';
  const clock = document.querySelector('[data-cover-clock]');
  const output = clock?.querySelector('time');
  if (!output) return;
  const lang = document.documentElement.lang;
  const label = {pt: 'Hora local de Copacabana', en: 'Copacabana local time', es: 'Hora local de Copacabana'}[lang] || 'Copacabana local time';
  const format = new Intl.DateTimeFormat('pt-BR', {
    timeZone: 'America/Sao_Paulo', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
  });
  function update() {
    const now = new Date();
    output.textContent = format.format(now);
    output.dateTime = now.toISOString();
    clock.setAttribute('aria-label', `${label}: ${output.textContent}`);
    clock.title = label;
  }
  let timer;
  function resume() {
    clearInterval(timer);
    update();
    if (!document.hidden) timer = setInterval(update, 1000);
  }
  document.addEventListener('visibilitychange', resume);
  window.addEventListener('pageshow', resume);
  resume();
})();
