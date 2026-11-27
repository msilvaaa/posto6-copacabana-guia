(() => {
 'use strict';
 const pairs=[...document.querySelectorAll('.place-link-pair')];
 if (!pairs.length) return;
 let frame;
 const fit = () => {
  for (const pair of pairs) {
   if (!pair.getBoundingClientRect().width) continue;
   const labels=[...pair.querySelectorAll('.venue-name')];
   pair.removeAttribute('data-stack-names');
   labels.forEach(label=>label.style.removeProperty('--venue-label-size'));
   const sizes=labels.map(label=>{
    const width=label.clientWidth;
    return width && label.scrollWidth>width ? Math.floor(16*(width-1)/label.scrollWidth*20)/20 : 16;
   });
   // Keep names readable on narrow screens instead of clipping or squeezing the text.
   if (sizes.some(size=>size<14)) {
    pair.setAttribute('data-stack-names','');
   } else {
    labels.forEach((label,i)=>{if(sizes[i]<16)label.style.setProperty('--venue-label-size',`${sizes[i]}px`);});
   }
  }
 };
 const schedule=()=>{cancelAnimationFrame(frame);frame=requestAnimationFrame(fit);};
 const widths=new WeakMap();
 const observer=new ResizeObserver(entries=>{
  if(entries.some(entry=>{const width=entry.contentRect.width,previous=widths.get(entry.target);widths.set(entry.target,width);return previous!==width;}))schedule();
 });
 pairs.forEach(pair=>observer.observe(pair));
 window.addEventListener('resize',schedule);
 document.fonts?.ready.then(schedule);
 fit();
})();
