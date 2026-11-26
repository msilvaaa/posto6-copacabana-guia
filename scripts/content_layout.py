"""Keep the reading column centered without moving page titles or navigation."""
from activities_topics import Node, parse


def with_centered_content(source):
    if 'class="native-panel"' not in source and 'class="section-panel"' not in source:
        return source
    doc = parse(source)
    for panel in doc.all(lambda node: node.has('native-panel') or node.has('section-panel')):
        content = Node('div', {'class': 'guide-content'})
        for child in list(panel.children):
            if isinstance(child, Node) and (child.tag == 'h1' or any(child.has(name) for name in ('native-toolbar', 'native-actions', 'section-actions'))):
                continue
            panel.children.remove(child)
            content.add(child)
        panel.add(content)
    head = doc.all(lambda node: node.tag == 'head')[0]
    version = '20261126-wifi-photo-bold' if 'class="wifi-connection"' in source else '20261126-centered-content'
    head.add(Node('link', {'rel': 'stylesheet', 'href': '/reading-layout.css?v=' + version}))
    return doc.html()
