(() => {
  'use strict';
  const hero = document.querySelector('.home-cover-hero');
  if (!hero) return;
  const title = hero.querySelector('.home-cover-copy h1');
  const place = title?.querySelector('.cover-place-name');
  const index = hero.querySelector('.home-cover-nav');
  const photo = hero.querySelector('.home-cover-photo');
  const toggle = hero.querySelector('[data-theme-toggle]');
  const sun = hero.querySelector('[data-sun-times]');
  const emergency = index?.querySelector('a:last-child');
  if (!title || !place || !index || !photo || !toggle) return;
  let frame;
  function align() {
    const area = hero.getBoundingClientRect();
    const word = place.getBoundingClientRect();
    const image = photo.getBoundingClientRect();
    const button = toggle.getBoundingClientRect();
    if (sun && emergency) {
      const text = document.createRange(); text.selectNodeContents(emergency);
      const label = text.getBoundingClientRect();
      const current = sun.getBoundingClientRect();
      const shift = parseFloat(hero.style.getPropertyValue('--cover-sun-shift')) || 0;
      hero.style.setProperty('--cover-sun-shift', `${shift + label.y + label.height / 2 - current.y - current.height / 2}px`);
    }
    hero.style.setProperty('--cover-theme-top', `${word.y + word.height / 2 - area.y - button.height / 2}px`);
    const sunset = sun?.querySelector('[data-sun-value="sunset"]')?.closest('.cover-sun-event');
    const sunsetBox = sunset?.getBoundingClientRect();
    const center = sunsetBox ? sunsetBox.x + sunsetBox.width / 2 : image.right - 2 * 96 / 2.54 - button.width / 2;
    const safeCenter = Math.max(image.left + button.width / 2 + 8, Math.min(center, image.right - button.width / 2 - 8));
    hero.style.setProperty('--cover-theme-right', `${area.right - safeCenter - button.width / 2}px`);
    if (window.matchMedia('(min-width:1101px)').matches) {
      const range = document.createRange(); range.selectNodeContents(place);
      const end = range.getBoundingClientRect().right;
      const start = index.getBoundingClientRect().left;
      const width = Math.max(0, end - start);
      hero.style.setProperty('--cover-index-width', `${width}px`);
      hero.style.setProperty('--cover-index-font-size', '14px');
      const links = [...index.querySelectorAll('a')];
      const naturalWidth = links.reduce((sum, link) => sum + link.getBoundingClientRect().width, 0);
      const textSpace = Math.max(0, width - Math.max(0, links.length - 1) * 8);
      hero.style.setProperty('--cover-index-font-size', `${Math.min(14, Math.max(11, 14 * textSpace / naturalWidth))}px`);
    } else {
      hero.style.removeProperty('--cover-index-width');
      hero.style.removeProperty('--cover-index-font-size');
    }
  }
  function schedule() { cancelAnimationFrame(frame); frame = requestAnimationFrame(align); }
  const observer = new ResizeObserver(schedule);
  for (const element of [hero, title, place, toggle, index, sun].filter(Boolean)) observer.observe(element);
  window.addEventListener('resize', schedule);
  document.fonts?.ready.then(schedule);
  align();
})();
