"""Remove repeated availability labels from the complete Course Book indexes."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
for index in (ROOT / 'public/course-book').glob('course-*/index.html'):
    page = index.read_text()
    page = re.sub(r'<span class="chapter-status">Ready to read</span>', '', page)
    page = page.replace('Read chapter →', 'Open chapter →')
    index.write_text(page)
print('Simplified Course Book indexes.')
