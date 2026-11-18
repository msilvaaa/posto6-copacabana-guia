export const REFRESH_MS = 60 * 60 * 1000;
export const MARINE_URL = 'https://marine-api.open-meteo.com/v1/marine?latitude=-23.01&longitude=-43.17&hourly=wave_height,wave_period&timezone=GMT&timeformat=unixtime&forecast_days=2';
export const WIND_URL = 'https://api.open-meteo.com/v1/forecast?latitude=-22.98&longitude=-43.19&hourly=wind_speed_10m,wind_direction_10m,wind_gusts_10m&wind_speed_unit=kmh&timezone=GMT&timeformat=unixtime&forecast_days=2';

function hour(data, now) {
  const times = data?.hourly?.time;
  if (!Array.isArray(times)) return null;
  let index = -1;
  for (let i = 0; i < times.length; i++) {
    if (Number.isFinite(times[i]) && times[i] * 1000 <= now) index = i;
  }
  if (index < 0 || now - times[index] * 1000 > 90 * 60 * 1000) return null;
  return {values: data.hourly, index, time: new Date(times[index] * 1000).toISOString()};
}
const value = (row, key, max) => {
  const number = row?.values[key]?.[row.index];
  return Number.isFinite(number) && number >= 0 && number <= max ? number : null;
};
export function conditions(marine, wind, now = Date.now()) {
  const sea = hour(marine, now), air = hour(wind, now);
  const waveHeight = value(sea, 'wave_height', 30);
  const wavePeriod = value(sea, 'wave_period', 60);
  const windSpeed = value(air, 'wind_speed_10m', 500);
  const windDirection = value(air, 'wind_direction_10m', 360);
  const windGusts = value(air, 'wind_gusts_10m', 500);
  return {available: waveHeight !== null || windSpeed !== null, waveHeight, wavePeriod,
    windSpeed, windDirection, windGusts, waveForecastAt: sea?.time || null,
    windForecastAt: air?.time || null, checkedAt: new Date(now).toISOString(),
    expiresAt: new Date(now + REFRESH_MS).toISOString(), source: 'Open-Meteo'};
}
