from pathlib import Path
from html import escape
root=Path(__file__).resolve().parents[1]
icons=[
('S1','Seta simples','<path d="m12 7 9 9-9 9"/>'),
('S2','Seta com haste','<path d="M5 16h22m-9-9 9 9-9 9"/>'),
('S3','Setas duplas','<path d="m8 8 8 8-8 8m10-16 8 8-8 8"/>'),
('S4','Seta circular','<circle cx="16" cy="16" r="13"/><path d="M9 16h14m-6-6 6 6-6 6"/>'),
('S5','Folha com canto dobrado','<path d="M8 3h12l7 7v19H8zM20 3v8h7M12 20h10m-4-4 4 4-4 4"/>'),
('S6','Livro aberto','<path d="M16 8c-4-3-9-3-13-2v21c4-1 9-1 13 2 4-3 9-3 13-2V6c-4-1-9-1-13 2Zm0 0v21m4-12h6m-3-3 3 3-3 3"/>'),
('S7','Virada de página','<path d="M5 3h21v14L15 29H5zM26 17H15v12M10 10h11m-4-4 4 4-4 4"/>'),
('S8','Seta em quadrado','<rect x="3" y="3" width="26" height="26" rx="7"/><path d="M9 16h14m-6-6 6 6-6 6"/>')]
def card(code,title,art,style=''):
 previous=art.replace(code+'-',code+'-back-')
 return f'<article class="{style}" data-choice="{code}"><h2>{code} <span>{escape(title)}</span></h2><div class="examples"><button type="button" class="back" aria-label="Anterior">{previous}</button><button type="button" aria-label="Próximo">{art}</button></div><div class="captions"><span>Anterior</span><span>Próximo</span></div></article>'

colorful=[
 ('C1','Seta em degradê azul e violeta','#22d3ee','#7850ed','<path d="M9 24h26V13l21 19-21 19V40H9z"/>'),
 ('C2','Página laranja com seta','#ffc85a','#f06a30','<path d="M14 5h25l12 12v42H14z"/><path d="M39 5v14h12" fill="#fff5c5"/><path d="M23 36h19m-7-7 7 7-7 7" fill="none" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'),
 ('C3','Seta curva verde e turquesa','#5bdf87','#008fa4','<path d="M6 45c0-20 13-27 30-27V7l23 23-23 22V39C23 37 13 39 6 52z"/>'),
 ('C4','Chevron rosa e violeta','#ff76ac','#8e48df','<path d="m18 8 25 24-25 24-10-10 15-14L8 18z"/>')]
color_cards=[]
for code,title,start,end,shape in colorful:
 svg=f'<svg aria-hidden="true" viewBox="0 0 64 64"><defs><linearGradient id="{code}-fill" x2="1" y2="1"><stop stop-color="{start}"/><stop offset="1" stop-color="{end}"/></linearGradient><filter id="{code}-shadow" x="-40%" y="-30%" width="180%" height="180%"><feDropShadow dx="0" dy="3" stdDeviation="2" flood-opacity=".2"/></filter></defs><g fill="url(#{code}-fill)" filter="url(#{code}-shadow)">{shape}</g></svg>'
 color_cards.append(card(code,title,svg,'vivid'))
three_d=[]
for code,title,asset in [('D1','Seta 3D azul','right-arrow'),('D2','Triângulo 3D','play'),('D3','Avanço duplo 3D','fast-forward'),('D4','Próxima página 3D','next-track')]:
 three_d.append(card(code,title,f'<img src="/assets/navigation-preview/{asset}.png" width="64" height="64" alt=""/>','vivid'))
cards=[]
for code,title,paths in icons:
 svg=f'<svg aria-hidden="true" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{paths}</svg>'
 cards.append(f'<article><h2>{code} <span>{escape(title)}</span></h2><div class="examples"><button type="button" class="back" aria-label="Anterior">{svg}</button><button type="button" aria-label="Próximo">{svg}</button></div><div class="captions"><span>Anterior</span><span>Próximo</span></div></article>')
page='''<!doctype html><html lang="pt"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Opções de setas · Posto 6 Copacabana</title><style>
*{box-sizing:border-box}body{margin:0;background:#f5f7fa;color:#172a32;font-family:Arial,sans-serif}main{max-width:1120px;margin:auto;padding:32px 26px}header{margin-bottom:24px}h1{font:700 28px Georgia,serif;margin:0 0 10px}p{font-size:15px;line-height:1.5;margin:0;color:#485e69}.group-title{font-size:21px;margin:28px 0 18px}nav{display:flex;gap:16px;margin-top:14px}section{scroll-margin-top:16px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}article{background:white;border:1px solid #dde5e9;border-radius:18px;padding:20px 16px;box-shadow:0 5px 16px #142f3b08}h2{font-size:19px;margin:0 0 24px}h2 span{display:block;font-size:13px;font-weight:400;margin-top:7px;color:#51616a;min-height:30px}.examples,.captions{display:flex;justify-content:center;gap:22px}button{display:grid;place-items:center;width:64px;height:60px;border:1px solid #c8dde6;border-radius:12px;background:#edf6fa;color:#00779c;cursor:pointer;transition:transform .18s,background .18s}button:hover,button:focus-visible{transform:translateY(-3px);background:#dceff6}button svg{width:34px;height:34px}.back svg,.back img{transform:scaleX(-1)}.vivid button{width:72px;height:68px;border:0;background:transparent}.vivid button:hover,.vivid button:focus-visible{background:#f1f5fa}.vivid button svg{width:60px;height:60px}.vivid img{width:64px;height:64px;object-fit:contain}.captions{gap:22px;margin-top:12px;font-size:11px;color:#53666f}.captions span{width:64px;text-align:center}footer{margin-top:24px;font-size:13px}a{color:#006e91}output{display:block;min-height:24px;margin-top:18px;font-weight:700;color:#00617d}@media(max-width:760px){section{grid-template-columns:repeat(2,minmax(0,1fr))}main{padding:24px 14px}.examples,.captions{gap:10px}button{width:54px}h1{font-size:24px}}@media(prefers-reduced-motion:reduce){button{transition:none}}
</style><main><header><h1>Escolha o estilo das setas</h1><p>Veja os pares de Anterior e Próximo. Novas opções coloridas C1–C4 e em 3D D1–D4. Diga no chat o código da sua preferência.</p><nav aria-label="Estilos"><a href="#coloridos">Coloridos</a><a href="#tres-d">3D</a><a href="#simples">Simples</a></nav></header><h2 class="group-title">Coloridos · C1 a C4</h2><section id="coloridos">'''+''.join(color_cards)+'''</section><h2 class="group-title">3D · D1 a D4</h2><section id="tres-d">'''+''.join(three_d)+'''</section><h2 class="group-title">Estilos simples · S1 a S8</h2><section id="simples">'''+''.join(cards)+'''</section><output aria-live="polite"></output><footer>Esta é uma prévia. A escolha será aplicada depois da sua confirmação no chat. <a href="/pt/">Voltar ao guia</a> · Ícones 3D: <a href="https://github.com/microsoft/fluentui-emoji" target="_blank" rel="noopener">Microsoft Fluent Emoji</a> (<a href="/assets/navigation-preview/LICENSE.txt">MIT</a>).</footer></main><script>document.querySelectorAll('article button').forEach(b=>b.addEventListener('click',()=>{document.querySelector('output').textContent='Opção '+b.closest('article').querySelector('h2').firstChild.textContent.trim()+': informe este código no chat.'}));</script></html>'''
dest=root/'preview-setas/pt/index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page)
