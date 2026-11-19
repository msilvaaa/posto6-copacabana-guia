"""Resolution-independent guest-guide illustrations; no embedded raster labels."""
ALIASES={'hospital':'medical','pharmacy':'medical','samu':'medical','travel-clock':'clock','rule':'shield','parking':'car','coffee-bars':'coffee','craft':'gift','market':'cart','checkin':'key','uber':'car','wifi-monitor':'tv','wifi-qr':'wifi','plane-trail':'plane'}
EXTRA={
 'dog':'<path d="m4 8-2-4 7 1 3-2 6 3 4-1-2 7-3 1v8h-3v-6H9v6H6V11Z"/><path d="M15 7h.1M3 13l3-2"/>',
 'moon':'<path d="M21 14A9 9 0 0 1 10 3a9 9 0 1 0 11 11Z"/>',
 'smoke':'<path d="M3 14h15v6H3ZM15 14v6M18 17h3M9 10c-4-2 3-3 0-6m5 6c-4-2 3-3 0-7"/>',
 'sound':'<path d="M3 9h4l5-5v16l-5-5H3Zm12-2c4 3 4 7 0 10m3-13c7 5 7 11 0 16"/>',
 'phone-map':'<rect x="3" y="2" width="12" height="20" rx="2" fill="#e5f3ee"/><path d="M7 18h4M6 5h6M6 8l4 5 3-2"/><path d="M22 8c0 4-5 8-5 8s-5-4-5-8a5 5 0 1 1 10 0Z" fill="#f05b55" stroke="#b63d38"/><circle cx="17" cy="8" r="1.5" fill="#ffdb70" stroke="none"/>',
 'bank':'<path d="m2 8 10-6 10 6Z" fill="#dfeaf4"/><path d="M3 22h18M4 18h16M6 9v9m6-9v9m6-9v9"/><circle cx="12" cy="5.8" r="1" fill="#e9b65b" stroke="none"/>',
 'money':'<rect x="2" y="6" width="20" height="13" rx="2" fill="#e6f5df"/><circle cx="12" cy="12.5" r="3.2"/><path d="M5 10v5m14-5v5M12 8v1m0 7v1"/>',
 'pencil':'<path d="m5 10 2 12h10l2-12Z" fill="#f4ddea"/><path d="m7 10-2-7 3-1 3 8m2 0 2-8 3 1-2 7M3 10h18"/>',
 'mail':'<rect x="2" y="5" width="20" height="15" rx="3" fill="#e5eef8"/><path d="m3 7 9 7 9-7m-18 9 6-5m12 5-6-5"/>',
 'case':'<rect x="5" y="6" width="14" height="15" rx="3" fill="#f6e7d5"/><path d="M9 6V2h6v4M9 10v7m6-7v7M8 21v2m8-2v2"/>',
 'landmark':'<path d="M3 22V8h4V4h3v4h4V4h3v4h4v14Z" fill="#e5eae8"/><path d="M9 22v-6h6v6"/>',
 'plane':'<path d="m2 15 8-5V3c0-2 4-2 4 0v7l8 5v3l-8-3v5l3 2H7l3-2v-5l-8 3Z" fill="#e7eff5"/>',
}
# Saturated duotone artwork: filled surfaces stay clear at small display sizes.
EXTRA.update({
 'bin':'<path d="M5 7h14l-1 15H6Z" fill="#43b6d6"/><path d="M3 6h18M9 3h6v3M9 10v8m6-8v8"/><path d="M5 7h14" stroke="#ffcf57" stroke-width="2.8"/>',
 'tv':'<rect x="2" y="3" width="20" height="15" rx="3" fill="#334b78"/><rect x="4" y="5" width="16" height="11" rx="1" fill="#52c9e3" stroke="none"/><path d="m5 15 5-5 4 3 5-6" stroke="#facc58"/><path d="M8 22h8m-4-4v4"/>',
 'snow':'<rect x="1" y="3" width="22" height="12" rx="3" fill="#bfeafc"/><path d="M5 7h14M5 11h14M7 18v3m5-3v5m5-5v3" stroke="#098fcb"/>',
 'fridge':'<rect x="5" y="1" width="14" height="22" rx="3" fill="#b1ddf7"/><path d="M5 9h14M8 4v2m0 7v4" stroke="#227eb7"/><path d="M16 3v17" stroke="white"/>',
 'bulb':'<path d="M8 17c0-3-4-4-4-9a8 8 0 0 1 16 0c0 5-4 6-4 9Z" fill="#ffd451"/><path d="M8 20h8m-6 3h4M9 8l3 3 3-3m-3 3v6" stroke="#cd8a16"/>',
 'wash':'<rect x="3" y="1" width="18" height="22" rx="3" fill="#a7def2"/><path d="M3 6h18M6 3h1m3 0h1"/><circle cx="12" cy="14" r="5" fill="#358bd6"/><path d="M8 14q4-3 8 0" stroke="#fff"/>',
 'dishwasher':'<rect x="3" y="1" width="18" height="22" rx="3" fill="#a7def2"/><path d="M3 6h18M6 3h1m10 0h1"/><circle cx="11" cy="14" r="5" fill="#fff"/><path d="M17 10v9M8 14h6" stroke="#23a88b"/>',
 'sofa':'<path d="M5 13V5q0-2 3-2h8q3 0 3 2v8" fill="#43c2ad"/><path d="M2 11h4v6h12v-6h4v10H2Z" fill="#168f99"/><path d="M5 21v2m14-2v2M12 5v10"/>',
 'door':'<path d="M4 23V2h16v21" fill="#ace0e9"/><path d="m4 2 12 3v18H4Z" fill="#f8b65b"/><circle cx="12" cy="13" r="1" fill="#fff"/>',
 'lock':'<rect x="6" y="8" width="12" height="15" rx="3" fill="#526493"/><path d="M9 8V5a3 3 0 0 1 6 0v3" stroke="#f7b941"/><g fill="#75e3ce" stroke="none"><circle cx="10" cy="12" r="1"/><circle cx="14" cy="12" r="1"/><circle cx="10" cy="16" r="1"/><circle cx="14" cy="16" r="1"/></g><path d="M10 20h4" stroke="#f7b941"/>',
 'iron':'<path d="M2 19h20l-3-9H8c-4 0-6 5-6 9Z" fill="#b99cf0"/><path d="M10 6h6l3 4M5 22h14"/><path d="M7 16h10" stroke="#fff"/>',
 'lamp':'<path d="M8 2h8l5 12H3Z" fill="#3ac5c2"/><path d="M12 14v8M7 22h10" stroke="#df9a29"/><path d="m17 14 1 5" stroke="#e8b43d"/><circle cx="18" cy="20" r="1" fill="#ffce55"/>',
 'safe':'<rect x="2" y="2" width="20" height="20" rx="3" fill="#b5c6e5"/><rect x="5" y="5" width="14" height="14" rx="2" fill="#6578a9"/><circle cx="13" cy="12" r="3" fill="#ffce55"/><path d="M7 9v6M13 9v6m-3-3h6"/>',
 'bank':'<path d="m2 8 10-6 10 6Z" fill="#65b6eb"/><path d="M4 10h16v9H4Z" fill="#b9dff8" stroke="none"/><path d="M3 22h18M4 18h16M6 10v8m6-8v8m6-8v8"/><circle cx="12" cy="5.8" r="1.3" fill="#ffcb45" stroke="none"/>',
 'money':'<rect x="5" y="3" width="17" height="13" rx="2" fill="#9de8b9"/><rect x="2" y="7" width="18" height="13" rx="2" fill="#37c583"/><circle cx="11" cy="13.5" r="3.3" fill="#ffe17c"/><path d="M5 11v5m12-5v5" stroke="#fff"/>',
 'pencil':'<path d="m4 11 2 12h12l2-12Z" fill="#f48db8"/><path d="m7 11-3-8 3-1 4 9" fill="#ffc757"/><path d="m13 11 3-9 3 1-3 8" fill="#a18be7"/><path d="M3 11h18"/>',
 'mail':'<rect x="2" y="5" width="20" height="15" rx="3" fill="#7cb9f4"/><path d="m3 7 9 7 9-7" fill="#c4e4ff"/><path d="m3 18 6-6m12 6-6-6"/>',
 'case':'<rect x="5" y="6" width="14" height="15" rx="3" fill="#ffab61"/><path d="M9 6V2h6v4M9 10v7m6-7v7M8 21v2m8-2v2"/><path d="M7 9h3v3H7Z" fill="#60d0cb" stroke="none"/>',
 'medical':'<path d="M8 2h8v6h6v8h-6v6H8v-6H2V8h6Z" fill="#ff6e7e"/><path d="M10 12h4m-2-2v4" stroke="white"/>',
 'hospital':'<rect x="4" y="5" width="16" height="18" rx="2" fill="#addcf8"/><rect x="8" y="1" width="8" height="8" rx="2" fill="#ff7180"/><path d="M10 5h4m-2-2v4" stroke="white"/><path d="M10 23v-6h4v6M7 12h2m6 0h2"/>',
 'pharmacy':'<rect x="2" y="6" width="20" height="16" rx="3" fill="#61d5b2"/><path d="M8 6V3h8v3"/><path d="M12 10v8m-4-4h8" stroke="white" stroke-width="3"/>',
 'fire':'<path d="M12 2c1 6 8 7 8 13a8 8 0 0 1-16 0c0-3 3-6 5-8-1 5 2 6 2 6s3-5 1-11Z" fill="#ff7950"/><path d="M12 12c-5 5-4 9 0 9s5-3 0-9Z" fill="#ffd25a" stroke="none"/>',
 'shield':'<path d="m12 2 9 4v6c0 6-9 10-9 10S3 18 3 12V6Z" fill="#699df0"/><path d="m12 7 1.5 3 3.5.5-2.5 2.5.5 3.5-3-1.5-3 1.5.5-3.5L7 10.5l3.5-.5Z" fill="#ffe079" stroke="none"/>',
 'water':'<path d="M12 2S4 11 4 16a8 8 0 0 0 16 0c0-5-8-14-8-14Z" fill="#65c8ee"/><path d="M8 16a4 4 0 0 0 4 4" stroke="white"/>',
 'car':'<path d="m3 10 2-6h14l2 6" fill="#7cd5e7"/><rect x="2" y="10" width="20" height="10" rx="3" fill="#ffc04d"/><path d="M5 20v2m14-2v2M5 14h2m10 0h2"/>',
 'coffee':'<path d="M3 7h14v8a6 6 0 0 1-6 6H9a6 6 0 0 1-6-6Z" fill="#f2af79"/><path d="M17 8h2a3 3 0 0 1 0 6h-2M6 2v2m5-2v2m5-2v2"/>',
 'glass':'<path d="M5 2h14v6a7 7 0 0 1-14 0Z" fill="#bd91e8"/><path d="M12 15v7M6 22h12M5 7h14"/><path d="M7 4h10" stroke="#fff"/>',
 'leaf':'<path d="M20 3C3 1-1 17 8 21c8 4 13-6 12-18Z" fill="#59cb8a"/><path d="m4 22 12-14" stroke="#168b68"/>',
 'bag':'<path d="M4 7h16l2 15H2Z" fill="#ffb461"/><path d="M8 8V6a4 4 0 0 1 8 0v2"/><path d="M7 12h10" stroke="#fff"/>',
 'info':'<circle cx="12" cy="12" r="10" fill="#73bafa"/><path d="M12 10v7m0-11v1" stroke="white" stroke-width="2.3"/>',
})
EXTRA.update({
 'bus':'<rect x="4" y="2" width="16" height="18" rx="3" fill="#ffba58"/><path d="M6 5h12v6H6Z" fill="#79d5ea"/><path d="M7 20v2m10-2v2M7 15h1m8 0h1"/>',
 'transport':'<rect x="5" y="2" width="14" height="17" rx="4" fill="#7ab7ef"/><path d="M7 5h10v6H7Z" fill="#ccf1fa"/><path d="M8 15h1m6 0h1M8 19l-3 4m11-4 3 4M7 21h10"/>',
 'bread':'<path d="M5 10a4 4 0 0 1 1-7 7 7 0 0 1 12 0 4 4 0 0 1 1 7v12H5Z" fill="#f6bb72"/><path d="M8 8v10m4-11v11m4-10v10" stroke="#d59441"/>',
 'cart':'<path d="M5 6h17l-3 11H8Z" fill="#5fc8c0"/><path d="M1 2h3l4 15h12"/><circle cx="9" cy="21" r="1.5" fill="#ffb450"/><circle cx="18" cy="21" r="1.5" fill="#ffb450"/>',
 'people':'<circle cx="8" cy="7" r="4" fill="#f7b76e"/><path d="M1 22v-5a7 7 0 0 1 14 0v5Z" fill="#8ba4ee"/><path d="M17 3a4 4 0 0 1 0 8" stroke="#e3a05b"/><path d="M18 14q5 1 5 8h-5" fill="#70cebc"/>',
 'clock':'<circle cx="12" cy="12" r="10" fill="#9bdff0"/><path d="M12 5v7l5 3"/><circle cx="12" cy="12" r="1.3" fill="#ffb651" stroke="none"/>',
 'check':'<rect x="2" y="2" width="20" height="20" rx="6" fill="#b2efd3"/><path d="m6 12 4 4 8-9" stroke="#169a60" stroke-width="2.5"/>',
 'bed':'<path d="M3 10V4h18v6" fill="#83cddf"/><path d="M2 11h20v7H2Z" fill="#ad9ae9"/><path d="M2 9v13m20-13v13M6 8h4m4 0h4"/>',
 'landmark':'<path d="M3 22V8h4V4h3v4h4V4h3v4h4v14Z" fill="#eabf84"/><path d="M9 22v-6h6v6" fill="#9fcbd8"/>',
 'mountain':'<path d="m1 22 8-16 5 8 3-6 6 14Z" fill="#69c6a8"/><path d="m6 12 3 3 3-3" fill="#e3f6f3"/>',
 'gift':'<path d="M2 8h20v5H2Z" fill="#ffd166"/><path d="M4 13h16v9H4Z" fill="#ee89a6"/><path d="M12 8v14m0-14S1 8 4 3s8 5 8 5 5-10 8-5-8 5-8 5Z" stroke="#9268bc"/>',
})
EXTRA.update({
 'key':'<circle cx="8" cy="8" r="5" fill="#ffd05c"/><circle cx="7" cy="7" r="1.4" fill="white" stroke="none"/><path d="m12 12 9 9m-5-5 3-3m0 6 3-3" stroke="#da9a24" stroke-width="2.4"/>',
 'wifi':'<path d="M2 7a17 17 0 0 1 20 0M5 11a12 12 0 0 1 14 0m-11 4a7 7 0 0 1 8 0" stroke="#248cd0" stroke-width="2"/><circle cx="12" cy="20" r="2" fill="#28b99b" stroke="none"/>',
 'moon':'<path d="M21 14A9 9 0 0 1 10 3a9 9 0 1 0 11 11Z" fill="#a58ae6"/><path d="m18 3 .6 1.4L20 5l-1.4.6L18 7l-.6-1.4L16 5l1.4-.6Z" fill="#ffcf66" stroke="none"/>',
 'dog':'<path d="m4 8-2-4 7 1 3-2 6 3 4-1-2 7-3 1v8h-3v-6H9v6H6V11Z" fill="#e9b16b"/><path d="M15 7h.1M3 13l3-2"/><path d="m3 3 18 18" stroke="#ec526b" stroke-width="2.3"/>',
 'smoke':'<path d="M3 14h15v6H3Z" fill="#ffcf79"/><path d="M15 14v6M18 17h3M9 10c-4-2 3-3 0-6m5 6c-4-2 3-3 0-7"/><path d="m3 3 18 18" stroke="#ec526b" stroke-width="2.3"/>',
})
# Keep independently recognisable symbols rather than sharing hospital artwork.
ALIASES.pop('hospital',None)
ALIASES.pop('pharmacy',None)
COLORS={'bank':'#2f609b','money':'#188361','pencil':'#ad4e83','mail':'#3478bd','case':'#af642c','medical':'#bc3c56','fire':'#c25130','shield':'#375fa7','leaf':'#168b68','glass':'#8054ac','coffee':'#935732','food':'#139b89','snow':'#098fcb','tv':'#334b78','lamp':'#168c9a','wash':'#287cab','fridge':'#227eb7','sofa':'#147b89','water':'#198db9','bulb':'#cd8a16'}
def symbol(name, paths):
 name=ALIASES.get(name,name)
 body=EXTRA.get(name,paths.get(name,paths['info']))
 color=COLORS.get(name,'#315878')
 if name not in EXTRA:
  body='<g fill="#74d3d2">'+body+'</g>'
 return f'<svg class="sharp-symbol colorful-symbol" data-symbol="{name}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
