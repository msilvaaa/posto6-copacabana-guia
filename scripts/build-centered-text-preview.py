"""Create a single isolated page to review text alignment against its title."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'pt/bem-vindos/index.html').read_text()
source=source.replace('<meta charset="utf-8"/>','<meta charset="utf-8"/><meta name="robots" content="noindex,nofollow"/>')
source=re.sub(r'<body class="([^"]*)"',r'<body class="\1 centered-text-preview"',source,count=1)
styles='''<style>
/* Equal side space keeps the text center on the title's center, not on the icon offset. */
body.centered-text-preview .native-panel { text-align:center; }
body.centered-text-preview .native-card h2,
:root body.centered-text-preview .native-card p { text-align:center; }
body.centered-text-preview .native-card-heading { justify-content:center; }
body.centered-text-preview .illustrated-card { display:block; position:relative; padding:0 90px; min-height:76px; margin-bottom:24px; }
body.centered-text-preview .illustrated-card .native-card-heading { display:block; }
body.centered-text-preview .illustrated-card .native-icon { position:absolute; left:0; top:0; }
body.centered-text-preview .illustrated-card .native-card-copy { padding:0; }
body.centered-text-preview .native-link { justify-content:center; }
.alignment-preview-controls { position:fixed; bottom:12px; left:12px; z-index:100; max-width:calc(100% - 96px); padding:10px 12px; border:1px solid #cddade; border-radius:10px; background:#fff; color:#173b43; font:12px/1.4 Arial,sans-serif; box-shadow:0 3px 16px #0002; }
.alignment-preview-controls strong { display:block; margin-bottom:6px; }
.alignment-preview-controls button { padding:7px 9px; border:1px solid #b4c7cd; border-radius:6px; color:#173b43; background:#fff; cursor:pointer; }
.alignment-preview-controls button[aria-pressed="true"] { color:#fff; background:#173b43; }
.alignment-preview-controls a { color:#176d85; margin-left:8px; }
@media(max-width:760px) {
 body.centered-text-preview .illustrated-card { padding:0; }
 body.centered-text-preview .illustrated-card .native-icon { position:static; margin:0 auto 10px; }
 .alignment-preview-controls { font-size:11px; }
}
</style>'''
source=source.replace('</head>',styles+'</head>')
controls='''<aside class="alignment-preview-controls" aria-label="Comparar alinhamento"><strong>Mostruário · A página normal permanece igual.</strong><button type="button" data-alignment="original" aria-pressed="false">Original</button> <button type="button" data-alignment="centered" aria-pressed="true">Centralizado</button><a href="/pt/bem-vindos/">Ver página atual</a></aside><script>document.querySelectorAll('[data-alignment]').forEach(b=>b.addEventListener('click',()=>{document.body.classList.toggle('centered-text-preview',b.dataset.alignment==='centered');document.querySelectorAll('[data-alignment]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));}));</script>'''
source=source.replace('</body>',controls+'</body>')
dest=ROOT/'preview-textos/pt/bem-vindos/index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(source)
