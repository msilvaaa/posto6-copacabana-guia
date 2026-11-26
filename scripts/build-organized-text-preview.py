"""Preview compact left-aligned copy and title-level WhatsApp on one page only."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'pt/bem-vindos/index.html').read_text()
source=source.replace('<meta charset="utf-8"/>','<meta charset="utf-8"/><meta name="robots" content="noindex,nofollow"/>')
source=re.sub(r'<body class="([^"]*)"',r'<body class="\1 organized-text-preview"',source,count=1)
style='''<style>
:root body.organized-text-preview .native-card { margin-bottom:14px; text-align:left; }
:root body.organized-text-preview .native-card h2,
:root body.organized-text-preview .native-card p { text-align:left; }
:root body.organized-text-preview .illustrated-card { display:grid; grid-template-columns:76px minmax(0,1fr); gap:4px 12px; align-items:start; min-height:76px; }
:root body.organized-text-preview .illustrated-card .native-card-heading { display:contents; }
:root body.organized-text-preview .illustrated-card .native-icon { grid-column:1; grid-row:1 / span 2; align-self:start; }
:root body.organized-text-preview .illustrated-card h2 { grid-column:2; grid-row:1; align-self:end; }
:root body.organized-text-preview .illustrated-card .native-card-copy { grid-column:2; grid-row:2; padding:0; }
:root body.organized-text-preview .illustrated-card .native-card-copy p { margin:0; }
:root body.organized-text-preview>.site-contact-corner { top:var(--preview-whatsapp-top,90px); bottom:auto; right:2cm; animation:none; }
.organized-preview-controls { position:fixed; left:12px; bottom:12px; z-index:100; max-width:calc(100% - 24px); padding:10px 12px; border:1px solid #ccd9de; border-radius:10px; background:#fff; color:#173b43; box-shadow:0 3px 16px #0002; font:12px/1.4 Arial,sans-serif; }
.organized-preview-controls strong { display:block; margin-bottom:6px; }
.organized-preview-controls button { padding:7px 9px; border:1px solid #b4c7cd; border-radius:6px; background:white; color:#173b43; cursor:pointer; }
.organized-preview-controls button[aria-pressed="true"] { background:#173b43; color:#fff; }
.organized-preview-controls a { margin-left:8px; color:#176d85; }
@media(max-width:1100px) {
 /* Reserve space for the requested 2 cm inset without overlapping the heading. */
 :root body.organized-text-preview .native-title { margin-left:0; max-width:calc(100% - 2cm - 68px); }
 .organized-preview-controls { font-size:11px; }
}
</style>'''
source=source.replace('</head>',style+'</head>')
controls='''<aside class="organized-preview-controls" aria-label="Comparar organização"><strong>Mostruário · Texto organizado + WhatsApp na linha do título.</strong><button data-preview-mode="original" aria-pressed="false">Original</button> <button data-preview-mode="organized" aria-pressed="true">Organizado</button><a href="/pt/bem-vindos/">Ver página atual</a></aside><script>
(()=>{
 const heading=document.querySelector('h1');
 const contact=document.querySelector('body>.site-contact-corner');
 if(!heading||!contact)return;
 let frame;
 function align(){const title=heading.getBoundingClientRect();const box=contact.getBoundingClientRect();document.body.style.setProperty('--preview-whatsapp-top',`${title.y+(title.height-box.height)/2}px`);}
 function schedule(){cancelAnimationFrame(frame);frame=requestAnimationFrame(align);}
 document.querySelectorAll('[data-preview-mode]').forEach(b=>b.addEventListener('click',()=>{document.body.classList.toggle('organized-text-preview',b.dataset.previewMode==='organized');document.querySelectorAll('[data-preview-mode]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));schedule();}));
 const observer=new ResizeObserver(schedule);observer.observe(heading);observer.observe(contact);
 window.addEventListener('resize',schedule);document.querySelector('.site-reading').addEventListener('scroll',schedule,{passive:true});document.fonts.ready.then(schedule);schedule();
})();</script>'''
source=source.replace('</body>',controls+'</body>')
dest=ROOT/'preview-textos/pt/organizado/index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(source)
