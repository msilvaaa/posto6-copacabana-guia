#!/usr/bin/env python3
"""Build all three covers from one layout. Run from any working directory."""
import json
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
template = Template((ROOT / "templates/cover.html").read_text())
content = json.loads((ROOT / "templates/cover-content.json").read_text())
for lang, values in content.items():
    buttons = []
    for index, button in enumerate(values["buttons"]):
        key, label, href = (escape(button[k], quote=True) for k in ("key", "label", "href"))
        buttons.append(
            f'        <a class="cover-html-button" data-row="{index // 3 + 1}" '
            f'data-column="{index % 3 + 1}" aria-label="{label}" href="{href}">'
            f'<img src="/assets/cover-icons/{key}.png" width="70" height="70" alt=""/></a>'
        )
    nav_links = "".join(
        f'<a href="{escape(item["href"], quote=True)}"'
        + (' aria-current="page"' if index == 0 else "")
        + f'>{escape(item["label"])}</a>'
        for index, item in enumerate(values["nav"])
    )
    flags = []
    for code, label in [("es", "Español"), ("pt", "Português"), ("en", "English")]:
        active = " active" if code == lang else ""
        current = ' aria-current="page"' if code == lang else ""
        flags.append(
            f'<a class="detail-modern-flag{active}"{current} href="/{code}/" '
            f'aria-label="{label}" title="{label}">'
            f'<img src="/assets/flag-{code}.png" alt="{label}"/></a>'
        )
    text = {k: escape(v, quote=True) for k, v in values.items() if isinstance(v, str)}
    # Inline line breaks are deliberately retained from the approved translations.
    text["heading"] = values["heading"]
    result = template.substitute(
        lang=lang, **text, nav_links=nav_links, flags="\n        ".join(flags),
        **{f"stat_{i}": v for i, v in enumerate(values["stats"])},
        buttons="\n".join(buttons), next_href=values["buttons"][0]["href"]
    )
    (ROOT / lang / "index.html").write_text(result)
