"""Extract verified Course 2 chapters 14–20 into the public student reader."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASTE = Path('/Users/ankitapandey/.codex/attachments/5144117a-f157-468e-af33-c81e701ecc28/Pasted text.txt')
SOURCE = ROOT / 'materials/student_books/course_02'
OUT = ROOT / 'public/course-book/course-02'
COURSE = json.loads((ROOT / 'website/doc_syllabi.json').read_text())['courses'][1]
SOURCE.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

raw = PASTE.read_text()

def chapter_block(number):
    start = raw.rfind(f'chapter_id: "C02-CH{number:02d}"')
    if start < 0:
        raise ValueError(f'Chapter {number} not found')
    start = raw.rfind('schema_version:', 0, start)
    end = raw.find(f'END OF C02-CH{number:02d}', start)
    if end < 0:
        raise ValueError(f'Chapter {number} is incomplete')
    value = raw[start:end]
    body = value.split('---', 1)[1].split('\ncontinuity:', 1)[0].strip()
    lines = body.splitlines()
    supplied_title = lines.pop(0).strip()
    supplied_title = re.sub(r'^C02-CH\d+\s*[—–-]\s*', '', supplied_title)
    expected = COURSE['chapters'][number - 1]['title'] if number <= len(COURSE['chapters']) else supplied_title
    if supplied_title != expected and supplied_title not in {'What you will learn', 'Extensions and Reusable Solutions'}:
        raise ValueError((number, supplied_title, expected))
    if supplied_title == 'What you will learn':
        lines.insert(0, supplied_title)
    if number == 20:
        _, testing_lines = chapter_block(21)
        # Chapter 21 was merged into the final approved 20-chapter syllabus.
        # Keep the useful testing material, but remove the old chapter identity.
        replacements = {
            'This chapter builds on Chapter 20. The previous chapter packaged reusable extension components and installation-aware configuration. This chapter verifies that those components behave correctly under normal load, invalid input, API failure, quota pressure, duplicate delivery, and version changes.': 'This testing module extends the extension design you have just completed. It verifies reusable components under normal load, invalid input, API failure, quota pressure, duplicate delivery and version changes.',
            'Chapter 21 uses an in-memory test ledger': 'This chapter uses an in-memory test ledger',
            'Chapter 21 local scenario and budget cases': 'local scenario and budget cases for this chapter',
            'What does the Chapter 21 lab claim about live Zoho requests?': 'What does the local lab claim about live Zoho requests?',
            'The local Chapter 21 harness passed': 'The local harness passed',
            'In the next chapter, you will plan environments, releases, deployment promotion, rollback, and operational handover.': 'Use the evidence in this module to decide whether an extension is ready for controlled release and operational handover.',
            'c02_ch21_harness.cjs': 'c02_ch20_harness.cjs',
            'c02_ch21_verify.cjs': 'c02_ch20_verify.cjs',
            'NOVCH21LAB': 'NOVCH20LAB',
        }
        testing_text = '\n'.join(testing_lines)
        for old, new in replacements.items():
            testing_text = testing_text.replace(old, new)
        testing_lines = testing_text.splitlines()
        lines.extend(['', '### Testing, performance and release readiness', ''])
        major = {'What you will learn', 'Lessons', 'Visual explanation', 'Worked case', 'Try it yourself', 'Independent challenge', 'Common problems and recovery', 'Check your understanding', 'Solutions and explanations', 'Chapter recap and next step', 'Glossary and further reading'}
        for test_line in testing_lines:
            label = re.sub(r'^(?:[1-9]|1[01])\.\s*', '', test_line.strip())
            if label in major or any(label.startswith(prefix + ' —') or label.startswith(prefix + ':') for prefix in major):
                lines.append('### Testing module — ' + label)
            elif re.match(r'^Lesson \d+\s*[—–-]', label):
                lines.append('### Testing module — ' + label)
            else:
                lines.append(test_line)
    return expected, lines

def clean(number):
    title, lines = chapter_block(number)
    result = ['# ' + title, '']
    major_labels = ('What you will learn', 'Lessons', 'Visual explanation', 'Worked case', 'Try it yourself', 'Independent challenge', 'Common problems and recovery', 'Check your understanding', 'Solutions and explanations', 'Chapter recap and next step', 'Glossary and further reading')
    for line in lines:
        stripped = line.strip()
        label = re.sub(r'^(?:[1-9]|1[01])\.\s*', '', stripped)
        if label in major_labels or any(label.startswith(prefix + ' —') or label.startswith(prefix + ':') for prefix in major_labels):
            result.extend(['## ' + label, ''])
        elif re.match(r'^Lesson \d+\s*[—–-]', stripped):
            result.extend(['### ' + stripped, ''])
        else:
            result.append(line)
    result = '\n'.join(line.rstrip() for line in result).rstrip() + '\n'
    (SOURCE / f'chapter_{number:02d}.md').write_text(result)
    return title, result

chapters = {number: clean(number) for number in range(14, 21)}
course_page = (ROOT / 'public/courses/zoho-developer-implementation-engineer.html').read_text()
head = course_page[:course_page.index('<main id="main">')]
head = re.sub(r'<title>.*?</title>', '<title>Course Book · Course 2 | Wooplix Academy</title>', head)
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Student chapters on advanced Zoho CRM APIs, reliable integrations, CRM customisation, widgets, extensions and testing.">', head)
for css in ('/course-book.css', '/course-book/course-05/reader.css'):
    if css not in head:
        head = head.replace('</head>', f'<link rel="stylesheet" href="{css}"></head>')
footer = course_page[course_page.index('<footer'):]
(OUT / 'reader.css').write_text((ROOT / 'public/course-book/course-05/reader.css').read_text())
(OUT / 'course-book.js').write_text((ROOT / 'public/course-book.js').read_text().replace("'wooplix-course01-chapter01-section'", "'wooplix-course02-' + location.pathname + '-section'"))

def linked(value):
    value = html.escape(value)
    return re.sub(r'(https?://[^\s)&lt;]+)', r'<a href="\1" target="_blank" rel="noopener">\1</a>', value)

def as_html(body):
    out, lines, index = [], body.splitlines(), 0
    def paragraph(values):
        if values:
            out.append('<p>' + linked(' '.join(v.strip() for v in values)) + '</p>')
    while index < len(lines):
        line = lines[index]
        if not line.strip(): index += 1; continue
        if line.startswith('### '): out.append('<h3>' + linked(line[4:].strip()) + '</h3>'); index += 1; continue
        if line.startswith('## '): out.append('<h2>' + linked(line[3:].strip()) + '</h2>'); index += 1; continue
        if line.startswith('```'):
            language = line[3:].strip(); index += 1; code=[]
            while index < len(lines) and not lines[index].startswith('```'): code.append(lines[index]); index += 1
            index += 1
            out.append(f'<pre><code class="language-{html.escape(language)}">' + html.escape('\n'.join(code)) + '</code></pre>'); continue
        if line.startswith('| '):
            rows=[]
            while index < len(lines) and lines[index].startswith('| '):
                rows.append([cell.strip() for cell in lines[index].strip().strip('|').split('|')]); index += 1
            header, data = rows[0], rows[2:] if len(rows)>1 and all(re.match(r'^-+$', cell) for cell in rows[1]) else rows[1:]
            out.append('<div class="table-wrap"><table><thead><tr>' + ''.join('<th scope="col">'+linked(cell)+'</th>' for cell in header) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+linked(cell)+'</td>' for cell in row)+'</tr>' for row in data) + '</tbody></table></div>'); continue
        if '\t' in line:
            rows=[]
            while index < len(lines) and '\t' in lines[index]: rows.append([cell.strip() for cell in lines[index].split('\t')]); index += 1
            if len(rows) > 1:
                width=len(rows[0]); rows=[row[:width]+['']*max(0,width-len(row)) for row in rows]
                out.append('<div class="table-wrap"><table><thead><tr>' + ''.join('<th scope="col">'+linked(cell)+'</th>' for cell in rows[0]) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+linked(cell)+'</td>' for cell in row)+'</tr>' for row in rows[1:]) + '</tbody></table></div>')
            else: paragraph([' | '.join(rows[0])])
            continue
        if line.startswith('- '):
            values=[]
            while index < len(lines) and lines[index].startswith('- '): values.append(lines[index][2:]); index += 1
            out.append('<ul>'+''.join('<li>'+linked(value)+'</li>' for value in values)+'</ul>'); continue
        if re.match(r'^\d+\. ', line):
            values=[]
            while index < len(lines) and re.match(r'^\d+\. ', lines[index]): values.append(re.sub(r'^\d+\. ', '', lines[index])); index += 1
            out.append('<ol>'+''.join('<li>'+linked(value)+'</li>' for value in values)+'</ol>'); continue
        values=[line]; index += 1
        while index < len(lines) and lines[index].strip() and not lines[index].startswith(('#', '| ', '- ', '```')) and '\t' not in lines[index] and not re.match(r'^\d+\. ', lines[index]): values.append(lines[index]); index += 1
        paragraph(values)
    return ''.join(out)

def reader_sections(markup):
    nav, sections = [], []
    for block in re.split(r'(?=<h2>)', markup):
        found = re.match(r'<h2>(.*?)</h2>', block, re.S)
        if not found:
            if block.strip(): sections.append(block)
            continue
        title = re.sub(r'<[^>]+>', '', found.group(1))
        number = len(nav) + 1
        ident = f'section-{number}'
        block = block.replace('<h2>', f'<h2 id="{ident}">', 1)
        nav.append(f'<a href="#{ident}">{number}. {html.escape(title)}</a>')
        if title.lower().startswith('solutions'):
            inside = block[block.index('</h2>')+5:]
            block = f'<section class="book-section" aria-labelledby="{ident}"><h2 id="{ident}">{html.escape(title)}</h2><p>Work through the questions before opening the model answers.</p><details class="solutions"><summary>Show solutions and explanations</summary><div>{inside}</div></details></section>'
        else:
            block = f'<section class="book-section" aria-labelledby="{ident}">{block}</section>'
        sections.append(block)
    return ''.join(nav), ''.join(sections)

for number, (title, source) in chapters.items():
    nav, content = reader_sections(as_html(re.sub(r'^# .+\n', '', source, count=1)))
    syllabus = COURSE['chapters'][number-1]
    previous = f'<a href="/course-book/course-02/chapter-{number-1:02d}">← Previous chapter</a>' if number > 14 else '<a href="/courses/zoho-developer-implementation-engineer">Course 2 overview</a>'
    next_link = f'<a href="/course-book/course-02/chapter-{number+1:02d}">Next chapter →</a>' if number < 20 else '<a href="/course-book/course-02">Back to Course Book →</a>'
    hero = f'''<div class="book-breadcrumb"><a href="/courses/zoho-developer-implementation-engineer">Course 2</a><span>/</span><a href="/course-book/course-02">Course Book</a><span>/</span><span>Chapter {number}</span></div><header class="book-hero"><p class="eyebrow">COURSE 02 · CHAPTER {number:02d}</p><h1>{html.escape(title)}</h1><p>{html.escape(syllabus['practice'])}</p><div class="book-tags"><span>Student course book</span><span>Fictional Nova case</span><span>Technical examples &amp; practice</span></div><div class="reader-actions"><button type="button" data-print>Print / save PDF</button><a download href="/course-book/course-02/chapter-{number:02d}-student.md">Download chapter (Markdown) ↓</a></div></header>'''
    ending = f'<div class="book-end"><h2>Keep your engineering notes</h2><p>{html.escape(syllabus["practice"])}</p><div class="reader-actions">{previous}{next_link}</div><p><a href="/course-book/course-02">Available Course 2 chapters →</a></p></div>'
    page = head + f'<main id="main" class="book-page">{hero}<div class="book-layout"><aside class="reader-sidebar"><details open><summary>In this chapter</summary><nav aria-label="Chapter sections">{nav}</nav></details><p class="save-note">Your reading position is saved on this browser.</p></aside><article class="book-content">{content}{ending}</article></div></main>' + footer.replace('</body>', '<script src="/course-book/course-02/course-book.js" defer></script></body>')
    (OUT / f'chapter-{number:02d}.html').write_text(page)
    (OUT / f'chapter-{number:02d}-student.md').write_text(source)

items=[]
for number, chapter in enumerate(COURSE['chapters'], 1):
    available = 14 <= number <= 20
    url=f'/course-book/course-02/chapter-{number:02d}'
    link=f'<a href="{url}">{html.escape(chapter["title"])}</a>' if available else html.escape(chapter['title'])
    button=f'<a class="button button-dark" href="{url}">Read chapter →</a>' if available else ''
    items.append(f'<li class="book-chapter {"available" if available else "pending"}"><span class="chapter-num">{number:02d}</span><div><h2>{link}</h2><p>{html.escape(chapter["topics"])}</p><span class="chapter-status">{"Ready to read" if available else "Planned chapter"}</span></div>{button}</li>')
index = head + '''<main id="main" class="book-directory"><div class="book-breadcrumb"><a href="/courses/zoho-developer-implementation-engineer">Course 2</a><span>/</span><span>Course Book</span></div><header class="book-hero"><p class="eyebrow">COURSE 02 · STUDENT LEARNING</p><h1>Course Book</h1><p>Zoho Developer &amp; Implementation Engineer</p><p class="book-description">Read the advanced CRM engineering chapters on data APIs, dependable event handling, server-side work, client scripts, widgets, extensions, testing and release readiness.</p><a class="button button-dark" href="/course-book/course-02/chapter-14">Start Chapter 14 →</a></header><ol class="book-chapters">'''+''.join(items)+'</ol></main>'+footer
(OUT / 'index.html').write_text(index)
print('Built Course 2 Chapters 14–20 from completed student source.')
