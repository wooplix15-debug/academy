"""Keep Academy navigation on its own landing page beneath the main brand site.

This changes link destinations only. Course text and learning assets stay intact.
Run after importing or rebuilding older course templates.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
REPLACEMENTS = {
    'href="/#programmes"': 'href="/academy#courses"',
    'href="/#curriculum"': 'href="/academy#courses"',
    'href="/#approach"': 'href="/academy#method"',
    'href="/#teams"': 'href="/academy#teams"',
    'href="/#enquire"': 'href="/enquire?service=Course%20enquiry"',
    'href="/"': 'href="/academy"',
    'href="https://www.wooplix.com/contact-us/" target="_blank" rel="noopener"': 'href="/enquire?service=Course%20enquiry"',
}


def migrate_links(page):
    for old, new in REPLACEMENTS.items():
        page = page.replace(old, new)
    return page


if __name__ == '__main__':
    changed = 0
    for path in PUBLIC.rglob('*.html'):
        if path.name in {'index.html', 'academy.html', 'enquire.html'} and path.parent == PUBLIC:
            continue
        page = path.read_text()
        updated = migrate_links(page)
        if updated != page:
            path.write_text(updated)
            changed += 1
    print(f'Updated Academy navigation in {changed} pages; lesson content preserved.')
