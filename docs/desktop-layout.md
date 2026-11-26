# Desktop layout reference

The guest guide uses a centered content area capped at **1440 × 900 CSS pixels**. Wider TV and desktop viewports add outer margins instead of spreading the content or increasing font sizes. Smaller desktop windows use the available width and height; short cover windows scroll inside the content area.

`desktop-layout.css` contains the reference dimensions, toolbar anchors, fixed cover type sizes, menu button diameter and arrow gaps. Do not use a CSS transform or browser zoom to scale the page: normal CSS layout preserves text rendering, dialogs and pointer coordinates.

The initial head script applies `data-desktop-frame` before the first paint. `site.js` maintains it on resize. Activation requires a viewport wider than 1100px and `navigator.maxTouchPoints === 0`; it does not require a fine mouse pointer, so a TV remote is supported. Phone and touch-tablet layouts remain unchanged. Archived `/preview-*` mockups opt out.

Home, language flags and previous/next controls stay centered within the appropriate half-width content panel or 30% cover menu. Arrow-to-button gaps are 1cm on the reference layout; the cover gap reduces only when a narrower desktop cannot fit the full gap. The WhatsApp inset is measured from the content area's right edge, not from the browser's outer margin. It stays on the cover's local-time row and on the title row elsewhere.

Self-hosted **Guide Sans** (Arimo subset) and **Guide Serif** (Gelasio subset) prevent system-font substitutions. They are metrically compatible alternatives to the original Arial and Georgia families. The original SVG title artwork, handwritten signatures and Courgette font are preserved. Font licenses and source links are in `assets/fonts/desktop-ui/`. The desktop-only font selectors do not trigger font downloads on phone or iPad layouts.

Validation compares normalized element geometry and computed typography at 1440×900, 1920×1080, 2560×1440 and 3840×2160. Include a coarse-pointer/no-touch TV profile, a high-DPI desktop profile, smaller windows, and phone/iPad baseline comparisons when changing this file.
