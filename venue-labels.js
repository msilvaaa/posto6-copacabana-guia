(() => {
 'use strict';
 const pairs=[...document.querySelectorAll('.place-link-pair')];
 const singles=[...document.querySelectorAll('.venue-name')].filter(label=>!label.closest('.place-link-pair'));
 const groupSelector='.bank-links,.pharmacy-links,.fort-links,.gym-links,.bakery-links';
 const groups=[...new Set(singles.map(label=>label.closest(groupSelector)).filter(Boolean))];
 if (!pairs.length && !singles.length) return;
 let frame;
 const sizeFor=label=>label.clientWidth && label.scrollWidth>label.clientWidth ? Math.floor(16*(label.clientWidth-1)/label.scrollWidth*20)/20 : 16;
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
  groups.forEach(group=>group.removeAttribute('data-stack-venue-names'));
  singles.forEach(label=>label.style.removeProperty('--venue-label-size'));
  for(const label of singles) {
   if(!label.getBoundingClientRect().width) continue;
   const size=sizeFor(label);
   if(size<14) label.closest(groupSelector)?.setAttribute('data-stack-venue-names','');
   else if(size<16) label.style.setProperty('--venue-label-size',`${size}px`);
  }
  for(const group of groups.filter(group=>group.hasAttribute('data-stack-venue-names'))) {
   for(const label of group.querySelectorAll('.venue-name')) {
    label.style.removeProperty('--venue-label-size');
    const size=sizeFor(label);
    if(size<16) label.style.setProperty('--venue-label-size',`${Math.max(14,size)}px`);
   }
  }
 };
 const schedule=()=>{cancelAnimationFrame(frame);frame=requestAnimationFrame(fit);};
 const widths=new WeakMap();
 const observer=new ResizeObserver(entries=>{
  let changed=false;
  for(const entry of entries) {const width=entry.contentRect.width; if(widths.get(entry.target)!==width)changed=true; widths.set(entry.target,width);}
  if(changed)schedule();
 });
 new Set([...pairs,...singles.map(label=>label.parentElement)]).forEach(target=>observer.observe(target));
 window.addEventListener('resize',schedule);
 document.fonts?.ready.then(schedule);
 fit();
})();
