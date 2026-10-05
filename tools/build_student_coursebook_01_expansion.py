"""Turn verified Course 1 student chapters 2–8 into the public Course Book."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASTE = Path('/Users/ankitapandey/.codex/attachments/db023b1d-ee71-411f-9e84-c6b226ee4a82/Pasted text.txt')
SOURCE_DIR = ROOT / 'materials/student_books/course_01'
OUT = ROOT / 'public/course-book/course-01'
COURSE = json.loads((ROOT/'website/doc_syllabi.json').read_text())['courses'][0]
COURSE_PAGE = ROOT/'public/courses/zoho-business-process-automation.html'
SOURCE_DIR.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

text = PASTE.read_text()
blocks = re.split(r'(?=^schema_version:)', text, flags=re.M)
section_head = re.compile(r'^(?:1\. What you will learn|2\. Lessons|3\. Visual explanation.*|4\. Worked case.*|5\. Try it yourself.*|6\. Independent challenge.*|7\. Common problems and recovery|8\. Check your understanding|9\. Solutions and explanations|10\. Chapter recap and next step|11\. Glossary and further reading)$', re.I)

def tabulate(lines):
    """Convert contiguous tab-separated source rows into readable Markdown tables."""
    result=[]; i=0
    while i < len(lines):
        if '\t' not in lines[i]:
            result.append(lines[i]); i += 1; continue
        rows=[]
        while i < len(lines) and '\t' in lines[i]:
            rows.append([c.strip() for c in lines[i].split('\t')]); i += 1
        if len(rows) < 2:
            result.extend(' | '.join(r) for r in rows); continue
        width=len(rows[0])
        rows=[r+['']*(width-len(r)) if len(r)<width else r[:width] for r in rows]
        esc=lambda c:c.replace('|','\\|')
        result.append('| '+' | '.join(esc(c) for c in rows[0])+' |')
        result.append('| '+' | '.join('---' for _ in rows[0])+' |')
        result.extend('| '+' | '.join(esc(c) for c in row)+' |' for row in rows[1:])
        result.append('')
    return result

def clean_chapter(number):
    choices=[b for b in blocks if f'chapter_id: "C01-CH{number:02d}"' in b and f'END OF C01-CH{number:02d}' in b]
    if not choices:
        raise ValueError(f'No complete source found for chapter {number}')
    raw=choices[-1]
    body=raw.split('---', 1)[1]
    body=body.split('\ncontinuity:', 1)[0].strip()
    lines=body.splitlines()
    while lines and not lines[0].strip(): lines.pop(0)
    title=re.sub(r'^Chapter \d+\s*[—–-]\s*', '', lines.pop(0).strip())
    if title != COURSE['chapters'][number-1]['title']:
        raise ValueError((number,title,COURSE['chapters'][number-1]['title']))
    out=['# '+title, '']
    for line in tabulate(lines):
        s=line.strip()
        if section_head.match(s):
            out.extend(['## '+s, ''])
        elif re.match(r'^Lesson \d+\s*[—–-]',s):
            out.extend(['### '+s, ''])
        else:
            out.append(line)
    cleaned='\n'.join(out).rstrip()+'\n'
    (SOURCE_DIR/f'chapter_{number:02d}.md').write_text(cleaned)
    return title, cleaned

sources={n:clean_chapter(n) for n in range(2,9)}
page=COURSE_PAGE.read_text()
head=page[:page.index('<main id="main">')]
head=re.sub(r'<title>.*?</title>', '<title>Course Book · Course 1 | Wooplix Academy</title>', head)
head=re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Read Course 1 student chapters on business process design, Zoho solution selection, CRM data and access, migration, leads and sales operations.">', head)
for css in ['/course-book.css','/course-book/course-05/reader.css']:
    if css not in head: head=head.replace('</head>',f'<link rel="stylesheet" href="{css}"></head>')
footer=page[page.index('<footer'):]

# Course 5's enhanced reader CSS is generic and makes code, maps and tables readable in this book too.
reader_css = ROOT/'public/course-book/course-05/reader.css'
if reader_css.exists(): (OUT/'reader.css').write_text(reader_css.read_text())
book_js=(ROOT/'public/course-book.js').read_text().replace("'wooplix-course01-chapter01-section'", "'wooplix-course01-' + location.pathname + '-section'")
(OUT/'course-book.js').write_text(book_js)

def linkify(value):
    """Escape course prose, retaining readable official-reference links."""
    escaped = html.escape(value)
    return re.sub(r'(https?://[^\s)&lt;]+)', r'<a href="\1" target="_blank" rel="noopener">\1</a>', escaped)


def render_markdown(body):
    """Small, dependency-free renderer for this controlled learner content."""
    out=[]; lines=body.splitlines(); i=0
    def paragraph(values):
        if values: out.append('<p>'+linkify(' '.join(v.strip() for v in values))+'</p>')
    while i < len(lines):
        line=lines[i]
        if not line.strip(): i+=1; continue
        if line.startswith('### '): out.append('<h3>'+linkify(line[4:].strip())+'</h3>'); i+=1; continue
        if line.startswith('## '): out.append('<h2>'+linkify(line[3:].strip())+'</h2>'); i+=1; continue
        if line.startswith('# '): out.append('<h1>'+linkify(line[2:].strip())+'</h1>'); i+=1; continue
        if line.startswith('| '):
            table=[]
            while i < len(lines) and lines[i].startswith('| '):
                cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                table.append(cells); i+=1
            if len(table) >= 2:
                header, rows=table[0], table[2:] if all(re.match(r'^-+$',c) for c in table[1]) else table[1:]
                out.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+linkify(c)+'</th>' for c in header)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+linkify(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>')
            continue
        if line.startswith('- '):
            values=[]
            while i < len(lines) and lines[i].startswith('- '): values.append(lines[i][2:]); i+=1
            out.append('<ul>'+''.join('<li>'+linkify(v)+'</li>' for v in values)+'</ul>'); continue
        if re.match(r'^\d+\. ',line):
            values=[]
            while i < len(lines) and re.match(r'^\d+\. ',lines[i]): values.append(re.sub(r'^\d+\. ','',lines[i])); i+=1
            out.append('<ol>'+''.join('<li>'+linkify(v)+'</li>' for v in values)+'</ol>'); continue
        values=[line]; i+=1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(('#','| ','- ')) and not re.match(r'^\d+\. ',lines[i]):
            values.append(lines[i]); i+=1
        paragraph(values)
    return ''.join(out)


def render(body):
    rendered=render_markdown(body)
    nav=[]; sections=[]
    for block in re.split(r'(?=<h2>)', rendered):
        found=re.match(r'<h2>(.*?)</h2>',block,re.S)
        if not found:
            if block.strip(): sections.append(block)
            continue
        title=re.sub(r'<[^>]+>','',found.group(1))
        n=re.match(r'(\d+)\.',title)
        if not n:
            sections.append(block);continue
        ident='section-'+n.group(1)
        block=block.replace('<h2>',f'<h2 id="{ident}">',1)
        nav.append(f'<a href="#{ident}">{html.escape(title)}</a>')
        if n.group(1)=='9':
            inner=block[block.index('</h2>')+5:]
            block=f'<section class="book-section" aria-labelledby="{ident}"><h2 id="{ident}">{html.escape(title)}</h2><p>Try the questions first. Open the solutions when you are ready to compare your reasoning.</p><details class="solutions"><summary>Show solutions and explanations</summary><div>{inner}</div></details></section>'
        else: block=f'<section class="book-section" aria-labelledby="{ident}">{block}</section>'
        sections.append(block)
    return ''.join(nav), ''.join(sections)

for n,(title,raw) in sources.items():
    body=re.sub(r'^# .+\n','',raw,count=1).strip()
    nav, content=render(body)
    chapter=COURSE['chapters'][n-1]
    previous=f'<a href="/course-book/course-01/chapter-{n-1:02d}">← Previous chapter</a>'
    next_link=f'<a href="/course-book/course-01/chapter-{n+1:02d}">Next chapter →</a>' if n<8 else '<a href="/course-book/course-01">Back to Course Book →</a>'
    hero=f'''<div class="book-breadcrumb"><a href="/courses/zoho-business-process-automation">Course 1</a><span>/</span><a href="/course-book/course-01">Course Book</a><span>/</span><span>Chapter {n}</span></div><header class="book-hero"><p class="eyebrow">COURSE 01 · CHAPTER {n:02d}</p><h1>{html.escape(title)}</h1><p>{html.escape(chapter['practice'])}</p><div class="book-tags"><span>Student course book</span><span>Fictional Meridian case</span><span>Worked examples &amp; practice</span></div><div class="reader-actions"><button type="button" data-print>Print / save PDF</button><a download href="/course-book/course-01/chapter-{n:02d}-student.md">Download chapter (Markdown) ↓</a></div></header>'''
    ending=f'''<div class="book-end"><h2>Keep your project work</h2><p>{html.escape(chapter['practice'])}</p><div class="reader-actions">{previous}{next_link}</div><p><a href="/course-book/course-01">All Course 1 chapters →</a></p></div>'''
    output=head+f'<main id="main" class="book-page">{hero}<div class="book-layout"><aside class="reader-sidebar"><details open><summary>In this chapter</summary><nav aria-label="Chapter sections">{nav}</nav></details><p class="save-note">Your reading position is saved on this browser.</p></aside><article class="book-content">{content}{ending}</article></div></main>'+footer.replace('</body>','<script src="/course-book/course-01/course-book.js" defer></script></body>')
    (OUT/f'chapter-{n:02d}.html').write_text(output)
    (OUT/f'chapter-{n:02d}-student.md').write_text(raw)

items=[]
for n,ch in enumerate(COURSE['chapters'],1):
    available=n<=8
    url=f'/course-book/course-01/chapter-{n:02d}'
    title=html.escape(ch['title']); topics=html.escape(ch['topics'])
    items.append(f'<li class="book-chapter {"available" if available else "pending"}"><span class="chapter-num">{n:02d}</span><div><h2>{f"<a href=\"{url}\">{title}</a>" if available else title}</h2><p>{topics}</p><span class="chapter-status">{"Ready to read" if available else "Coming next"}</span></div>{f"<a class=\"button button-dark\" href=\"{url}\">Read chapter →</a>" if available else ""}</li>')
index=head+'''<main id="main" class="book-directory"><div class="book-breadcrumb"><a href="/courses/zoho-business-process-automation">Course 1</a><span>/</span><span>Course Book</span></div><header class="book-hero"><p class="eyebrow">COURSE 01 · STUDENT LEARNING</p><h1>Course Book</h1><p>Zoho Business Process &amp; Corporate Automation</p><p class="book-description">The first eight chapters are ready to read. Learn how to understand a process, choose a solution, manage users and access, model CRM data, prepare migration data and run sales work.</p><a class="button button-dark" href="/course-book/course-01/chapter-01">Start Chapter 1 →</a></header><ol class="book-chapters">'''+''.join(items)+'</ol></main>'+footer
(OUT/'index.html').write_text(index)
print('Built Course 1 chapters 2–8 and updated the Course Book index.')
