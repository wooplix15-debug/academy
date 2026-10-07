"""Apply shared learner navigation and reading improvements to published course books."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = {
    '02': {'total': 20, 'ready': 20, 'course': 'zoho-developer-implementation-engineer'},
    '01': {'total': 18, 'ready': 18, 'course': 'zoho-business-process-automation'},
    '03': {'total': 20, 'ready': 20, 'course': 'ai-agentic-ai-builder'},
    '04': {'total': 10, 'ready': 10, 'course': 'corporate-ai-automation-workshop'},
    '05': {'total': 16, 'ready': 16, 'course': 'zoho-implementation-consulting-practicum'},
}

for course, info in BOOKS.items():
    folder = ROOT / 'public/course-book' / f'course-{course}'
    progress = round(info['ready'] / info['total'] * 100)
    bar = f'''<section class="book-coursebar" data-coursebook-polish="coursebar" aria-label="Course Book progress"><strong>Course {int(course)} · {info['ready']} of {info['total']} chapters ready</strong><div class="book-progress" aria-hidden="true"><i style="width:{progress}%"></i></div><a href="/courses/{info['course']}">Full syllabus →</a></section>'''
    index = folder / 'index.html'
    page = index.read_text()
    page = re.sub(r'<section class="book-coursebar" data-coursebook-polish="coursebar".*?</section>', '', page, flags=re.S)
    page = page.replace('<ol class="book-chapters">', bar+'<ol class="book-chapters">', 1)
    index.write_text(page)

    for chapter in sorted(folder.glob('chapter-*.html')):
        m = re.fullmatch(r'chapter-(\d{2})\.html', chapter.name)
        if not m:
            continue
        number = int(m.group(1))
        page = chapter.read_text()
        page = re.sub(r'<div class="chapter-strip" data-coursebook-polish="chapter-strip">.*?</div>', '', page, flags=re.S)
        # Older cleanup passes may remove the data attribute. Remove every
        # existing guide so rebuilds always leave exactly one concise guide.
        page = re.sub(r'<section class="book-reading-guide"[^>]*>.*?</section>', '', page, flags=re.S)
        strip = f'''<div class="chapter-strip" data-coursebook-polish="chapter-strip"><b>Course {int(course)} · Chapter {number} of {info['total']}</b><a href="/course-book/course-{course}">Course contents →</a></div>'''
        guide = '''<section class="book-reading-guide" data-coursebook-polish="reading-guide" aria-label="How to use this chapter"><p><strong>Study path:</strong> read the lesson, complete the practice, then open the solutions.</p></section>'''
        page = page.replace('<div class="book-layout">', strip+'<div class="book-layout">', 1)
        page = page.replace('<article class="book-content">', '<article class="book-content">'+guide, 1)
        chapter.write_text(page)
print('Polished Course Books 1–5.')
