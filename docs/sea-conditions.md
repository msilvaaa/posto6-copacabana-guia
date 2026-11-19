# Copacabana sea and wind forecast

The Emergency page shows regional wave height and period, wind speed/direction, and gusts in Portuguese, English and Spanish. Values are forecasts, not lifeguard beach flags or real-time surf observations.

`functions/api/sea-conditions.js` queries Open-Meteo Marine near the Copacabana coast (-23.01, -43.17) and the weather forecast at Copacabana (-22.98, -43.19). The selected forecast is the current UTC hour; stale forecast hours older than 90 minutes are rejected. Wind units are km/h, waves metres, period seconds.

The page displays the last saved snapshot immediately, including expired snapshots with their original timestamps and an explicit last-saved label. A cache-only API read (`cached=1`) can supply a saved snapshot to a new browser without calling forecast providers. Entry then forces a background source query (`refresh=1`), saving the result for the next visit without replacing or clearing the current display. With no saved data, the first successful result is displayed once. Hourly refresh and expiry checks on tab return remain active.

Cloudflare retains last-good snapshots for seven days; payload freshness remains exactly one hour. Ordinary requests refresh after that hour; cached-only requests never wait for providers. Failed or degraded partial queries preserve a previously complete snapshot and its timestamps. The browser can query the public sources directly if the endpoint is unavailable. Failed requests retry after one hour without removing visible data.

The forecast time and consultation time are shown separately in Brasília time. The original emergency telephone links remain available regardless of provider status. No private API credential is needed.

Validation: `node --test tests/test_sea_conditions.mjs` checks hourly selection, one-hour cache expiry, partial and complete failures, stale data rejection, and real zero values.
