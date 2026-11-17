(() => {
  'use strict';
  const locale = {pt: 'pt-BR', en: 'en-US', es: 'es-ES'}[document.documentElement.lang] || 'pt-BR';
  const clocks = [...document.querySelectorAll('[data-time-zone]')].map(element => {
    const timeZone = element.dataset.timeZone;
    return {
      time: element.querySelector('[data-clock-time]'),
      date: element.querySelector('[data-clock-date]'),
      offset: element.querySelector('[data-clock-offset]'),
      timeFormat: new Intl.DateTimeFormat(locale, {timeZone, hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23'}),
      dateFormat: new Intl.DateTimeFormat(locale, {timeZone, day: '2-digit', month: 'short', year: 'numeric'}),
      offsetFormat: new Intl.DateTimeFormat('en', {timeZone, timeZoneName: 'shortOffset'})
    };
  });
  if (!clocks.length) return;
  function update() {
    const now = new Date();
    for (const clock of clocks) {
      clock.time.textContent = clock.timeFormat.format(now);
      clock.time.dateTime = now.toISOString();
      clock.date.textContent = clock.dateFormat.format(now);
      const offset = clock.offsetFormat.formatToParts(now).find(part => part.type === 'timeZoneName');
      clock.offset.textContent = offset.value.replace('GMT', 'UTC');
    }
  }
  let timer;
  function resume() {
    clearInterval(timer);
    update();
    if (!document.hidden) timer = setInterval(update, 1000);
  }
  document.addEventListener('visibilitychange', resume);
  resume();
})();
