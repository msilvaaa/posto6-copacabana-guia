import {CLUBS,normalizeClub,weekWindow} from '../../football-data.js';

export async function onRequestGet() {
 const now = Date.now();
 const clubs = await Promise.all(CLUBS.map(async ([id,name]) => {
  try {
   // Upcoming and recent schedules together retain a match while it is in progress.
   const payloads = await Promise.all(['true','false'].map(async fixture => {
    const response = await fetch(`https://site.api.espn.com/apis/site/v2/sports/soccer/all/teams/${id}/schedule?fixture=${fixture}`, {cache:'no-store',signal:AbortSignal.timeout(12000),headers:{Accept:'application/json','User-Agent':'Posto6GuestGuide/1.0'}});
    if (!response.ok) throw new Error('Unavailable');
    return response.json();
   }));
   return {id,name,available:true,games:normalizeClub(payloads,id,now)};
  } catch {return {id,name,available:false};}
 }));
 const available = clubs.some(club=>club.available);
 return Response.json({available,checkedAt:new Date(now).toISOString(),window:weekWindow(now),clubs}, {status:available?200:503,headers:{'Cache-Control':'no-store'}});
}
