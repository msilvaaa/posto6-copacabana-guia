"""Place the page navigation immediately after its main title, preserving artwork markup."""
import re

def below_title(source):
 match=re.search(r'<nav\b[^>]*class="[^"]*\bsite-pagination\b[^"]*"[^>]*>.*?</nav>',source,re.S)
 if match is None or '</h1>' not in source:raise ValueError('Missing page title or navigation')
 navigation=match.group()
 source=source[:match.start()]+source[match.end():]
 source=re.sub(r'<div class="(?:native-actions|section-actions)">\s*</div>','',source)
 return re.sub(r'(?m)^[ \t]+$','',source.replace('</h1>','</h1>'+navigation,1))
