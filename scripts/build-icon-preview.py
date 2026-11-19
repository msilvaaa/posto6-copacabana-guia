#!/usr/bin/env python3
"""Build the owner's standalone icon comparison; never apply a choice to the guide."""
from pathlib import Path
import re
from guide_symbols import symbol
from guide_native import PATHS
ROOT=Path(__file__).resolve().parents[1]
ICONS=[('bank','Bancos','#357bb9'),('money','Câmbio','#16865d'),('mail','Correios','#4288c6'),('fire','Bombeiros','#e16e35'),('hospital','Hospital','#ce5474'),('wifi','Wi-Fi / sinal','#238cc6'),('bin','Lixeira','#1b9a8c'),('lamp','Iluminação','#9273bd')]
STYLES=[
 (1,'Colorido preenchido','Padrão atual do guia: traço com áreas de cor.',None),
 (2,'Traço colorido','Mais leve: apenas linhas coloridas, sem preenchimento.',None),
 (3,'Cor com fundo suave','Linhas coloridas sobre uma base arredondada clara.',None),
 (4,'Flat','Formas sólidas e simples. Coleção Microsoft Fluent, versão flat.','flat'),
 (5,'Ilustrado','Desenhos expressivos com contorno escuro. Coleção OpenMoji.','openmoji'),
 (6,'3D colorido','Volume, textura e sombras reais da coleção Microsoft Fluent 3D.','fluent'),
 (7,'Adesivo','Contorno branco e sombra, como uma figurinha.',None),
 (8,'Animado suave','O desenho colorido com um movimento leve e contínuo.',None),
]
sections=[]
for mode,title,description,collection in STYLES:
 items=[]
 for name,label,color in ICONS:
  if collection:
   path=f'assets/icon-preview/{collection}-{name}.svg'
   if not (ROOT/path).is_file():raise FileNotFoundError(path)
   drawing=f'<img src="/{path}" width="64" height="64" alt="" loading="lazy"/>'
  else:
   drawing=symbol(name,PATHS)
   if mode in (2,3):
    drawing=re.sub(r' fill="[^"]+"',' fill="none"',drawing)
    drawing=re.sub(r' stroke="[^"]+"',f' stroke="{color}"',drawing)
  items.append(f'<li class="item" style="--color:{color}"><span class="icon">{drawing}</span><span class="label">{label}</span></li>')
 extra='<div id="novas-opcoes" class="anchor"></div>' if mode==4 else ''
 sections.append(f'{extra}<section class="mode-{mode}" id="estilo-{mode}" aria-labelledby="title-{mode}"><h2 id="title-{mode}">{mode}. {title}</h2><p class="desc">{description}</p><ul class="grid">'+''.join(items)+'</ul></section>')
nav=''.join(f'<a href="#estilo-{n}">{n}. {title}</a>' for n,title,_,_ in STYLES)
html='''<!doctype html>
<html lang="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>8 estilos de ícones — Posto 6 Copacabana</title><style>
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0 auto;padding:28px 32px;max-width:1050px;background:#fff;color:#16232b;font-family:Arial,Helvetica,sans-serif}h1{font-size:28px;margin:0 0 10px}h2{font-size:22px;margin:0 0 8px}p{margin:0;line-height:1.55}.intro,.desc{font-size:15px;color:#58646b}.intro{max-width:750px}.back{display:inline-block;margin:0 0 22px;color:#315878;font-size:14px}.options{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0}.options a{display:flex;align-items:center;min-height:44px;padding:10px 13px;color:#22475e;background:#edf5f8;border-radius:9px;font-size:14px;text-decoration:none}.options a:hover{background:#d9edf3}a:focus-visible{outline:3px solid #238cc6;outline-offset:3px}section{padding:26px 0 30px;border-top:1px solid #e4e8ea;scroll-margin-top:16px}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px 16px;margin:25px 0 0;padding:0;list-style:none}.item{display:flex;align-items:center;gap:12px;min-width:0}.icon{display:flex;align-items:center;justify-content:center;width:68px;height:68px;flex-shrink:0}.icon svg{width:44px;height:44px;overflow:visible}.icon img{display:block;width:64px;height:64px;object-fit:contain}.label{font-size:14px;line-height:1.35}.mode-3 .icon{background:color-mix(in srgb,var(--color) 13%,white);border-radius:17px}.mode-3 svg{width:34px;height:34px}.mode-6 img{width:68px;height:68px}.mode-7 .icon{background:color-mix(in srgb,var(--color) 15%,white);border-radius:18px}.mode-7 svg{transform:rotate(-7deg);filter:drop-shadow(2px 0 0 white) drop-shadow(-2px 0 0 white) drop-shadow(0 2px 0 white) drop-shadow(0 -2px 0 white) drop-shadow(1px 3px 2px #0003)}.mode-8 .icon svg{animation:float-icon 2.8s ease-in-out infinite}.mode-8 .item:nth-child(even) svg{animation-delay:-1.4s}@keyframes float-icon{0%,100%{transform:translateY(2px) rotate(-2deg)}50%{transform:translateY(-3px) rotate(2deg)}}footer{border-top:1px solid #e4e8ea;padding-top:24px;font-size:13px;color:#58646b}footer a{color:#315878}.anchor{scroll-margin-top:12px}@media(max-width:700px){body{padding:22px 16px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 8px}.item{gap:8px}.label{font-size:13px}h1{font-size:25px}.icon{width:60px;height:64px}.icon img{max-width:60px}.options{gap:6px}.options a{font-size:13px;padding:9px 10px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.mode-8 .icon svg{animation:none}}
</style></head><body>
<a class="back" href="/pt/">← Voltar ao guia</a>
<h1>Escolha o estilo dos ícones</h1>
<p class="intro">Veja os mesmos temas em oito estilos. As opções 4 a 8 são novas. Diga o número ou o nome do estilo que você prefere; também podemos escolher por item. Esta página é apenas uma prévia.</p>
<nav class="options" aria-label="Ir para um estilo">'''+nav+'</nav><main>'+''.join(sections)+'''</main>
<footer><p>Créditos: <a href="https://github.com/microsoft/fluentui-emoji">Microsoft Fluent Emoji</a> (flat e 3D, licença MIT); <a href="https://openmoji.org/">OpenMoji</a> — estudantes e docentes da HfG Schwäbisch Gmünd e colaboradores (CC BY-SA 4.0). As demais opções usam os desenhos do guia.</p><p><a href="/assets/icon-preview/LICENSES.txt">Licenças e fontes das imagens</a></p></footer>
</body></html>
'''
(ROOT/'preview-icones/index.html').write_text(html)
print('Built 8 icon styles / 64 examples; main guide unchanged.')
