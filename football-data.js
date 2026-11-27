export const CLUBS = [['819','Flamengo'],['3445','Fluminense'],['3454','Vasco da Gama'],['6086','Botafogo']];
const LEAGUES = {'bra.1':'Brasileirão Série A','bra.2':'Brasileirão Série B','bra.copa_do_brasil':'Copa do Brasil','bra.copa_brazil':'Copa do Brasil','bra.camp.carioca':'Campeonato Carioca','conmebol.libertadores':'CONMEBOL Libertadores','conmebol.sudamericana':'CONMEBOL Sudamericana'};
export function rioDate(value) {
 const parts = new Intl.DateTimeFormat('en-US',{timeZone:'America/Sao_Paulo',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date(value));
 const part = name => parts.find(p=>p.type===name).value;
 return `${part('year')}-${part('month')}-${part('day')}`;
}
export function weekWindow(now) {
 const start = rioDate(now);
 const end = new Date(Date.parse(start+'T00:00:00Z')+6*86400000).toISOString().slice(0,10);
 return {start,end};
}
export function normalizeClub(payloads, id, now = Date.now()) {
 const {end} = weekWindow(now), games = new Map(), finished = new Set();
 for (const payload of payloads) {
  if (!Array.isArray(payload?.events) || String(payload.team?.id)!==id) throw new Error('Unexpected club schedule');
  for (const event of payload.events) {
   const date = Date.parse(event.date), comp = event.competitions?.[0], status = comp?.status?.type;
   if (!Number.isFinite(date) || !status) throw new Error('Missing fixture status');
   if (status.completed || status.state==='post' || ['STATUS_CANCELED','STATUS_CANCELLED','STATUS_POSTPONED'].includes(status.name)) {
    finished.add(String(event.id));games.delete(String(event.id));continue;
   }
   if (finished.has(String(event.id))) continue;
   // Keep the announced match through kick-off until the provider confirms completion.
   if (date<now-12*3600000 || rioDate(date)>end) continue;
   const teams = comp.competitors || [];
   if (!teams.some(t=>String(t.team?.id)===id) || !/^\d+$/.test(String(event.id))) throw new Error('Invalid fixture');
   const home = teams.find(t=>t.homeAway==='home')?.team?.displayName;
   const away = teams.find(t=>t.homeAway==='away')?.team?.displayName;
   if (!home || !away) throw new Error('Missing teams');
   const league = event.league?.slug || '';
   games.set(String(event.id), {id:String(event.id),date:new Date(date).toISOString(),time_confirmed:Boolean(comp.timeValid ?? event.timeValid),home,away,competition:LEAGUES[league] || event.league?.name || '',league,state:status.state,url:'https://www.espn.com.br/futebol/partida/_/jogoId/'+event.id});
  }
 }
 return [...games.values()].sort((a,b)=>Date.parse(a.date)-Date.parse(b.date));
}
