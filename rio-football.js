(() => {
 const refresh = () => {
  for (const club of document.querySelectorAll('[data-football-schedule] .football-club')) {
   const fixtures = [...club.querySelectorAll('[data-match-start]')];
   for (const fixture of fixtures) fixture.hidden = Date.parse(fixture.dataset.matchStart) < Date.now();
   club.querySelector('.football-empty').hidden = fixtures.some(fixture => !fixture.hidden);
  }
 };
 refresh();
 window.addEventListener('pageshow', refresh);
})();
