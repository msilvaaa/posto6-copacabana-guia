export const WEATHER_REFRESH_MS = 3 * 60 * 60 * 1000;
export const WEATHER_SOURCE = 'https://wttr.in/-22.9842,-43.1918?format=j1';

export function forecast(payload, previous, now = Date.now()) {
  const days = payload.weather?.slice(0, 3).map(day => {
    const min = Number(day.mintempC), max = Number(day.maxtempC);
    const rain = Math.max(...day.hourly.map(hour => Number(hour.chanceofrain || 0)));
    const code = String(day.hourly[Math.floor(day.hourly.length / 2)]?.weatherCode);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(day.date) || !Number.isFinite(Date.parse(day.date)) || !Number.isFinite(min) || !Number.isFinite(max) || min < -15 || min > max || max > 60 || !Number.isFinite(rain) || rain < 0 || rain > 100 || !/^\d+$/.test(code)) throw new Error('Invalid forecast');
    return {date:day.date, min, max, rain_probability:rain, code};
  });
  if (days?.length !== 3 || new Set(days.map(day => day.date)).size !== 3 || days.some((day, i) => i && day.date <= days[i-1].date)) throw new Error('Incomplete forecast');
  const today = new Intl.DateTimeFormat('sv-SE', {timeZone:'America/Sao_Paulo'}).format(new Date(now));
  if (!days.some(day => day.date >= today)) throw new Error('Expired forecast');
  const unchanged = JSON.stringify(previous?.days) === JSON.stringify(days);
  return {location:'Copacabana, Rio de Janeiro', latitude:-22.9842, longitude:-43.1918, provider:'wttr.in', source:WEATHER_SOURCE,
    updated_at:unchanged && Number.isFinite(Date.parse(previous.updated_at)) ? previous.updated_at : new Date(now).toISOString(),
    checkedAt:new Date(now).toISOString(), expiresAt:new Date(now + WEATHER_REFRESH_MS).toISOString(), days};
}
