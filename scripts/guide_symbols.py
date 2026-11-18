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
COLORS={'bank':'#4a627d','money':'#428152','pencil':'#a4598d','mail':'#567eae','case':'#966b43','medical':'#d54e55','fire':'#da583e','shield':'#4775ad','leaf':'#3d8861','glass':'#5c7d8d','coffee':'#926d4d','food':'#568b78'}
def symbol(name, paths):
 name=ALIASES.get(name,name)
 body=EXTRA.get(name,paths.get(name,paths['info']))
 color=COLORS.get(name,'#173f45')
 return f'<svg class="sharp-symbol" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
