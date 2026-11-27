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
  if (!title || !place || !index || !photo || !toggle) return;
  let frame;
  function align() {
    const scale=Number(document.documentElement.dataset.guideScale)||1;
    const box=element=>{const r=element.getBoundingClientRect();return {x:r.x/scale,y:r.y/scale,left:r.left/scale,right:r.right/scale,width:r.width/scale,height:r.height/scale};};
    const area = box(hero);
    const word = box(place);
    const image = box(photo);
    const button = box(toggle);
    hero.style.setProperty('--cover-sun-shift', '0px');
    hero.style.setProperty('--cover-theme-top', `${word.y + word.height / 2 - area.y - button.height / 2}px`);
    const sunset = sun?.querySelector('[data-sun-value="sunset"]')?.closest('.cover-sun-event');
    const sunsetBox = sunset ? box(sunset) : null;
    const center = sunsetBox ? sunsetBox.x + sunsetBox.width / 2 : image.right - 2 * 96 / 2.54 - button.width / 2;
    const safeCenter = Math.max(image.left + button.width / 2 + 8, Math.min(center, image.right - button.width / 2 - 8));
    hero.style.setProperty('--cover-theme-right', `${area.right - safeCenter - button.width / 2}px`);
    if (window.matchMedia('(min-width:1101px)').matches) {
      const start = box(index).left;
      const available = Math.max(0, image.right - start - 20);
      hero.style.setProperty('--cover-index-font-size', '14px');
      hero.style.setProperty('--cover-index-width', `${Math.min(493.375,available)}px`);
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
