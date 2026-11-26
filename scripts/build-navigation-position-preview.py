"""Build isolated placement mockups without changing production navigation."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'pt/bem-vindos/index.html').read_text()
match=re.search(r'<nav class="site-pagination[^>]*>.*?</nav>',source,re.S)
if match:
 nav=match.group()
else:
 # Production P1 already has links in the toolbar; recover them for the archived mockups.
 controls=re.findall(r'<a\b[^>]*class="[^"]*\bsite-step\b[^"]*"[^>]*>.*?</a>',source,re.S)
 nav='<nav class="site-pagination guide-pagination" aria-label="Navegação">'+''.join(controls)+'</nav>'
 for control in controls:source=source.replace(control,'',1)
 source=re.sub(r'<span class="navigation-space"[^>]*></span>','',source)
links=re.findall(r'<a\b[^>]*>.*?</a>',nav,re.S)
assert len(links)==2
previous,following=links
source=source.replace(nav,'',1)
# Preserve the source body classes whatever their order.
source=re.sub(r'<body class="([^"]*)"',lambda m:'<body class="'+m[1]+' navigation-position-preview"',source,count=1)
source=source.replace('<meta charset="utf-8"/>','<meta charset="utf-8"/><meta name="robots" content="noindex,nofollow"/>')
common='''<style>
body.navigation-position-preview .site-step { flex:0 0 52px; width:52px; min-width:52px; }
.preview-title-row { display:grid; grid-template-columns:52px minmax(0,1fr) 52px; align-items:center; gap:12px; margin-bottom:24px; }
.preview-title-row h1 { margin:0 auto; max-width:100%; }
body.navigation-position-preview .preview-title-row .site-step { justify-self:center; }
.preview-message { position:fixed; bottom:12px; left:12px; max-width:calc(100% - 100px); padding:7px 10px; border-radius:8px; background:#fff; color:#163b42; font:12px/1.4 Arial; box-shadow:0 2px 12px #0002; z-index:100; }
@media(max-width:760px) {
 body.navigation-position-preview .native-toolbar .site-toolbar { gap:4px; }
 body.navigation-position-preview .site-toolbar .site-step { width:32px; min-width:32px; flex-basis:32px; }
 body.navigation-position-preview .site-toolbar .page-turn-arrow { width:28px; }
 .preview-title-row { grid-template-columns:40px minmax(0,1fr) 40px; gap:4px; }
}
</style>'''
variants={
 'p1':('P1 · Setas nas pontas das bandeiras','Antes de Home e depois da bandeira dos EUA.'),
 'p2':('P2 · Setas nas laterais do título','Título centralizado entre Anterior e Próximo.'),
 'p3':('P3 · Setas abaixo das bandeiras','Navegação agrupada, com as bandeiras livres. Minha sugestão.')}
for code,(title,desc) in variants.items():
 output=source
 if code=='p1':
  toolbar=re.search(r'<nav class="site-toolbar guide-toolbar"[^>]*>.*?</nav>',output,re.S).group()
  modified=toolbar.replace('>', '>'+previous,1).replace('</nav>',following+'</nav>')
  output=output.replace(toolbar,modified,1)
 elif code=='p2':
  heading=re.search(r'<h1\b.*?</h1>',output,re.S).group()
  output=output.replace(heading,'<div class="preview-title-row">'+previous+heading+following+'</div>',1)
 else:
  toolbar_end=output.index('</nav></div>')+len('</nav>')
  output=output[:toolbar_end]+nav+output[toolbar_end:]
  common_extra='''<style>body.navigation-position-preview .native-toolbar { min-height:124px; }body.navigation-position-preview .native-toolbar>.site-pagination {position:fixed;top:82px;right:0;left:auto;width:50%;height:56px;margin:0;gap:24px;z-index:89;}@media(max-width:760px){body.navigation-position-preview .native-toolbar{min-height:76px;height:76px;}body.navigation-position-preview .native-toolbar>.site-pagination{width:100%;}}</style>'''
  output=output.replace('</head>',common_extra+'</head>')
 output=output.replace('</head>',common+'</head>')
 output=output.replace('</body>','<div class="preview-message" role="status">'+title+' · Apenas demonstração.</div><script>document.querySelectorAll(".site-step").forEach(a=>a.addEventListener("click",e=>e.preventDefault()));</script></body>')
 dest=ROOT/f'preview-posicao-setas/pt/{code}/index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(output)
hub='''<!doctype html><html lang="pt"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Posição das setas · Posto 6 Copacabana</title><style>*{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif;background:#f4f6f8;color:#17353d}header{padding:20px 24px 12px;max-width:1500px;margin:auto}h1{font:700 25px Georgia,serif;margin:0 0 8px}p{margin:0 0 14px;font-size:14px;line-height:1.5}nav{display:flex;flex-wrap:wrap;gap:8px}button{border:1px solid #b5c7cc;background:white;border-radius:9px;padding:10px 15px;color:inherit;font:700 14px Arial;cursor:pointer}button[aria-pressed="true"]{background:#143e43;color:white}iframe{display:block;width:100%;height:calc(100dvh - 200px);min-height:600px;border:0;background:white}a{color:#006d89}.hint{margin-top:12px}footer{padding:12px 24px;font-size:13px}@media(max-width:760px){header{padding:16px}iframe{height:800px}button{padding:9px 10px;font-size:12px}}</style><header><h1>Onde ficam melhor as setas?</h1><p>Compare as três posições na página Bem-vindos. Esta prévia preserva a foto, os títulos, Home e as bandeiras.</p><nav aria-label="Escolher exemplo">'''
for code,(title,desc) in variants.items():
 hub+=f'<button data-variant="{code}" aria-pressed="{str(code=="p1").lower()}">{title.split(" · ")[0]} · {title.split(" · ")[1]}</button>'
hub+='''</nav><p class="hint" data-description>Antes de Home e depois da bandeira dos EUA.</p></header><iframe title="Exemplo de posição das setas" src="p1/"></iframe><footer>As setas são demonstrativas. Informe no chat P1, P2 ou P3 para aplicar. <a data-full href="p1/" target="_blank" rel="noopener">Abrir exemplo em tela inteira</a> · <a href="/pt/">Voltar ao site</a></footer><script>const descriptions='''+repr({k:v[1] for k,v in variants.items()})+''';document.querySelectorAll('[data-variant]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-variant]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelector('iframe').src=b.dataset.variant+'/';document.querySelector('[data-full]').href=b.dataset.variant+'/';document.querySelector('[data-description]').textContent=descriptions[b.dataset.variant];}));</script></html>'''
(ROOT/'preview-posicao-setas/pt/index.html').write_text(hub)
