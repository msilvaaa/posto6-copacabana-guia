"""Place C3 previous/next links at the two ends of the Home/language toolbar."""
import re
from content_layout import with_centered_content


def with_toolbar_navigation(source):
    navigation = re.search(r'<nav\b[^>]*class="[^"]*\bsite-pagination\b[^"]*"[^>]*>.*?</nav>', source, re.S)
    if navigation is None:
        raise ValueError('Missing page navigation')
    links = re.findall(r'<a\b[^>]*>.*?</a>', navigation.group(), re.S)
    previous = [link for link in links if 'rel="prev"' in link or 'translate(64 0) scale(-1 1)' in link]
    following = [link for link in links if link not in previous]
    if len(previous) > 1 or len(following) > 1:
        raise ValueError('Unexpected page navigation links')
    source = source[:navigation.start()] + source[navigation.end():]
    source = re.sub(r'<div class="(?:native-actions|section-actions)">\s*</div>', '', source)
    toolbar = re.search(r'<(?P<tag>nav|div)\b[^>]*class="[^"]*\b(?:site-toolbar|main-html-topbar)\b[^"]*"[^>]*>', source)
    if toolbar is None:
        raise ValueError('Missing Home/language toolbar')
    end = source.index('</' + toolbar['tag'] + '>', toolbar.end())
    placeholder = '<span class="navigation-space" aria-hidden="true"></span>'
    controls = (previous[0] if previous else placeholder) + source[toolbar.end():end] + (following[0] if following else placeholder)
    source = source[:toolbar.end()] + controls + source[end:]
    return with_centered_content(re.sub(r'(?m)^[ \t]+$', '', source))
