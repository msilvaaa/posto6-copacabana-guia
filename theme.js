(() => {
  'use strict';
  const root = document.documentElement;
  const key = 'posto6-theme';
  const words = {
    pt: {dark:'Ativar modo escuro', light:'Ativar modo claro'},
    en: {dark:'Switch to dark mode', light:'Switch to light mode'},
    es: {dark:'Activar modo oscuro', light:'Activar modo claro'}
  }[root.lang] || {dark:'Ativar modo escuro', light:'Ativar modo claro'};
  function stored() {
    try {return localStorage.getItem(key) === 'dark' ? 'dark' : 'light';}
    catch {return 'light';}
  }
  function apply(mode) {
    root.dataset.theme = mode === 'dark' ? 'dark' : 'light';
    const dark = root.dataset.theme === 'dark';
    for (const button of document.querySelectorAll('[data-theme-toggle]')) {
      button.setAttribute('aria-pressed', String(dark));
      button.setAttribute('aria-label', dark ? words.light : words.dark);
      button.title = dark ? words.light : words.dark;
    }
  }
  apply(stored());
  function setup() {
    apply(root.dataset.theme);
    for (const button of document.querySelectorAll('[data-theme-toggle]')) {
      button.addEventListener('click', () => {
        const mode = root.dataset.theme === 'dark' ? 'light' : 'dark';
        try {localStorage.setItem(key, mode);} catch { /* The button also works without persistent storage. */ }
        apply(mode);
      });
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup, {once:true});
  else setup();
  window.addEventListener('storage', event => {if (event.key === key || event.key === null) apply(stored());});
  window.addEventListener('pageshow', event => {if (event.persisted) apply(stored());});
})();
