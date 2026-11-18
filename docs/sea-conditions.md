# Copacabana sea and wind forecast

The Emergency page shows regional wave height and period, wind speed/direction, and gusts in Portuguese, English and Spanish. Values are forecasts, not lifeguard beach flags or real-time surf observations.

`functions/api/sea-conditions.js` queries Open-Meteo Marine near the Copacabana coast (-23.01, -43.17) and the weather forecast at Copacabana (-22.98, -43.19). The selected forecast is the current UTC hour; stale forecast hours older than 90 minutes are rejected. Wind units are km/h, waves metres, period seconds.

Cloudflare and browser storage cache a successful response for one hour. The page refreshes at expiry while open, and checks expiry when returning to the tab. Reloading or switching languages reuses the unexpired browser cache. If the site endpoint is unavailable, the browser can query the same public sources directly. Partial provider failures leave the unavailable fields blank rather than inventing values. Complete failures retry after one hour.

The forecast time and consultation time are shown separately in Brasília time. The original emergency telephone links remain available regardless of provider status. No private API credential is needed.

Validation: `node --test tests/test_sea_conditions.mjs` checks hourly selection, one-hour cache expiry, partial and complete failures, stale data rejection, and real zero values.
