"""Shared option-6 illustrations. Keep photos, brand marks and navigation semantics separate."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
ALIASES={'lamp':'bulb','travel-clock':'clock','rule':'shield','parking':'car','coffee-bars':'coffee','craft':'gift','market':'cart','checkin':'key','uber':'car','wifi-monitor':'tv','wifi-qr':'wifi','plane-trail':'plane','checkout-check':'check','checkout-luggage':'case','samu':'medical'}

def icon_3d(name):
    key=ALIASES.get(name,name)
    source=f'/assets/icons-3d/{key}.svg'
    if not (ROOT/source.lstrip('/')).is_file():raise ValueError(f'Missing 3D icon: {name}')
    extra='<path d="M43 38 213 218" stroke="#f44f68" stroke-width="15" stroke-linecap="round"/>' if name=='dog' else ''
    return (f'<svg class="guide-icon-3d" data-symbol="{escape(name)}" viewBox="0 0 256 256" aria-hidden="true">'
            f'<image href="{source}" width="256" height="256"/>{extra}</svg>')
