(() => {
 'use strict';
 if (location.pathname.startsWith('/preview-')) return;
 const root=document.documentElement;
 const desktop=matchMedia('(min-width:1101px)');
 function fit() {
  root.setAttribute('data-guide-layout','');
  root.toggleAttribute('data-desktop-frame',desktop.matches);
  root.toggleAttribute('data-fluid-frame',!desktop.matches);
  if (!desktop.matches) {
   root.style.removeProperty('zoom');
   for (const name of ['--desktop-frame-width','--desktop-frame-height','--desktop-frame-side']) root.style.removeProperty(name);
   delete root.dataset.guideScale;
   return;
  }
  // Grow the approved 1440 × 900 composition uniformly to use the available screen.
  const scale=Math.max(1,Math.min(innerWidth/1440,innerHeight/900));
  root.style.zoom=String(scale);
  root.dataset.guideScale=String(scale);
  root.style.setProperty('--desktop-frame-width',`${innerWidth/scale}px`);
  root.style.setProperty('--desktop-frame-height',`${innerHeight/scale}px`);
  root.style.setProperty('--desktop-frame-side','0px');
 }
 window.addEventListener('resize',fit);
 window.addEventListener('pageshow',fit);
 desktop.addEventListener('change',fit);
 fit();
})();
