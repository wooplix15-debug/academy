"""Apply presentation fixes shared by every public student course book.

The course books are produced by several generators. This final pass keeps the
live reading experience consistent without changing any lesson text.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

for chapter in sorted((ROOT / "public" / "course-book").glob("course-*/chapter-*.html")):
    page = chapter.read_text()
    page = re.sub(r'(<a href="#section-\d+">\d+\. )\d+\.\s*', r'\1', page)
    page = re.sub(r'<div class="book-tags">.*?</div>', '', page, flags=re.S)
    page = re.sub(
        r'<section class="book-reading-guide"[^>]*>.*?</section>',
        '<section class="book-reading-guide" aria-label="How to use this chapter">'
        '<p><strong>Study path:</strong> read the lesson, complete the practice, then open the solutions.</p>'
        '</section>', page, flags=re.S,
    )
    page = page.replace('View all available chapters →', 'Course contents →')
    page = page.replace('<h2>Continue your course work</h2>', '<h2>Next step</h2>')
    page = re.sub(r'<p>####\s+(.+?)</p>', r'<h4>\1</h4>', page, flags=re.S)
    page = page.replace('<p>---</p>', '<hr>')
    chapter.write_text(page)

print("Cleaned public course-book reader pages.")
