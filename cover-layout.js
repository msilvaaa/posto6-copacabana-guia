(() => {
  'use strict';
  const hero = document.querySelector('.home-cover-hero');
  if (!hero) return;
  const title = hero.querySelector('.home-cover-copy h1');
  const place = title?.querySelector('.cover-place-name');
  const index = hero.querySelector('.home-cover-nav');
  const photo = hero.querySelector('.home-cover-photo');
  const toggle = hero.querySelector('[data-theme-toggle]');
  if (!title || !place || !index || !photo || !toggle) return;
  let frame;
  function align() {
    const area = hero.getBoundingClientRect();
    const word = place.getBoundingClientRect();
    const image = photo.getBoundingClientRect();
    const button = toggle.getBoundingClientRect();
    hero.style.setProperty('--cover-theme-top', `${word.y + word.height / 2 - area.y - button.height / 2}px`);
    hero.style.setProperty('--cover-theme-right', `calc(${area.right - image.right}px + 2cm)`);
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
  for (const element of [hero, title, place, toggle]) observer.observe(element);
  window.addEventListener('resize', schedule);
  document.fonts?.ready.then(schedule);
  align();
})();
