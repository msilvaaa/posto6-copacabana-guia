# Refresh on page entry

Opening a relevant page triggers a new provider query, regardless of the last successful browser or endpoint cache entry. This includes reloads, language navigation and restored back/forward pages. Existing intervals remain unchanged: weather 3 hours, buy exchange rates daily, sea and wind hourly. Successful source consultations renew the existing timer. The source may return identical values or an earlier quote/forecast timestamp; those timestamps are preserved.

Weather now has `/api/weather?refresh=1`, with wttr.in source validation and a three-hour cache for ordinary requests. When the live source is unavailable, the frontend uses the saved forecast and labels it as the last available forecast. This does not change the scheduled repository weather sync. Sea and exchange endpoints accept `refresh=1` to bypass their own caches, return `no-store` for that consultation, and update their normal TTL caches. Browser exchange requests retain the direct provider path to avoid shared-server rate limits. Existing missing-data behavior and partial sea forecasts remain intact.

The Wi-Fi monitor displays the exact original Pão de Açúcar photo from `pt-05.jpg`, clipped to the original screen rectangle with a mild SVG sharpening filter. No generative replacement or geometry change is applied. Crisp native credentials, QR and signal animation remain.

Validation: Python suite; Node provider/cache tests including forced rechecks, unchanged/changed forecast timestamps and failure behavior; Playwright tests with unexpired browser storage, reloads and back/forward entry, plus Wi-Fi proportions in all three languages at 390/1440px.
