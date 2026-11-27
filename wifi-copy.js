(() => {
 'use strict';
 const messages={pt:{copied:'Senha copiada!',failed:'Copie manualmente'},en:{copied:'Password copied!',failed:'Copy manually'},es:{copied:'¡Contraseña copiada!',failed:'Copia manual'}}[document.documentElement.lang] || {copied:'Senha copiada!',failed:'Copie manualmente'};
 for(const button of document.querySelectorAll('[data-copy-wifi]')) {
  const value=button.querySelector('[data-wifi-password]');
  const status=button.parentElement.querySelector('[data-wifi-copy-status]');
  const originalTitle=button.title;
  let reset;
  const legacyCopy=text=>{
   const field=document.createElement('textarea');
   field.value=text;field.readOnly=true;field.tabIndex=-1;
   field.style.cssText='position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;pointer-events:none';
   document.body.append(field);
   try {field.focus({preventScroll:true});field.select();field.setSelectionRange(0,text.length);return document.execCommand('copy');}
   finally {field.remove();}
  };
  button.addEventListener('click',async()=>{
   clearTimeout(reset);button.disabled=true;
   let copied=false;
   try {
    if(navigator.clipboard?.writeText) {
     try {await navigator.clipboard.writeText(value.textContent);copied=true;} catch {}
    }
    if(!copied)copied=legacyCopy(value.textContent);
   } catch {}
   finally {button.disabled=false;button.focus({preventScroll:true});}
   status.toggleAttribute('data-error',!copied);
   button.dataset.state=copied?'copied':'error';
   status.textContent=copied?messages.copied:messages.failed;
   button.title=status.textContent;
   if(!copied) {
    const selection=window.getSelection(),range=document.createRange();
    range.selectNodeContents(value);selection.removeAllRanges();selection.addRange(range);
   }
   reset=setTimeout(()=>{delete button.dataset.state;status.textContent='';status.removeAttribute('data-error');button.title=originalTitle;},3000);
  });
 }
})();
