"""Import reviewed student chapters from the teaching-pack source into the public Course Book."""
from pathlib import Path
from html import escape
import json, re

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = Path('/Users/ankitapandey/Downloads/Wooplix_Academy_Teaching_Pack')
PASTE_C03 = Path('/Users/ankitapandey/.codex/attachments/2fb0ea53-c791-457f-9d1b-7cfb991a71be/Pasted text.txt')
DATA = json.loads((ROOT / 'website/doc_syllabi.json').read_text())['courses']
SLUGS = {1:'zoho-business-process-automation', 2:'zoho-developer-implementation-engineer', 3:'ai-agentic-ai-builder'}
READY = {1: range(1,19), 2: range(1,21), 3: range(1,21)}

# Keep generated course text but discard metadata, continuation records and generator end markers.
def strip_source(text, cid, number):
    # Astra exports may begin directly with YAML fields or with an opening fence.
    # In both cases, the first standalone --- ends the front matter.
    if '\n---\n' in text:
        text = text.split('\n---\n', 1)[1]
    elif text.startswith('---'):
        text = text.split('---', 1)[1]
    text = re.split(r'\n(?:```yaml\n)?continuity:', text, maxsplit=1)[0]
    text = re.sub(r'\n?END OF ' + re.escape(f'{cid}-CH{number:02d}') + r'.*$', '', text, flags=re.M)
    return text.strip() + '\n'

def c03_from_paste(number):
    raw = PASTE_C03.read_text()
    marker = f'chapter_id: "C03-CH{number:02d}"'
    at = raw.rfind(marker)
    if at < 0: raise ValueError(marker)
    start = raw.rfind('schema_version:', 0, at)
    end = raw.find(f'END OF C03-CH{number:02d}', start)
    if start < 0 or end < 0: raise ValueError(f'incomplete C03 {number}')
    return strip_source(raw[start:end], 'C03', number)

def source_for(course, number):
    cid = f'C{course:02d}'
    if course == 3 and number >= 14:
        return c03_from_paste(number)
    matches = list(DOWNLOADS.glob(f'{cid}_CH{number:02d}_*_Student.md'))
    if len(matches) == 1:
        return strip_source(matches[0].read_text(), cid, number)
    existing = ROOT / 'materials' / 'student_books' / f'course_{course:02d}' / f'chapter_{number:02d}.md'
    if existing.exists():
        return existing.read_text().strip() + '\n'
    raise ValueError(f'{cid} {number}: {matches}')

def markdown_html(body):
    out=[]; lines=body.splitlines(); i=0
    def links(s):
        value=escape(s)
        return re.sub(r'(https?://[^\s<]+)', r'<a href="\1" target="_blank" rel="noopener">\1</a>', value)
    def para(parts):
        if parts: out.append('<p>'+links(' '.join(x.strip() for x in parts))+'</p>')
    while i < len(lines):
        line=lines[i]
        if not line.strip(): i+=1; continue
        if line.startswith('```'):
            lang=line[3:].strip(); i+=1; code=[]
            while i<len(lines) and not lines[i].startswith('```'): code.append(lines[i]); i+=1
            i+=1; out.append(f'<pre><code class="language-{escape(lang)}">{escape(chr(10).join(code))}</code></pre>'); continue
        if line.strip() == '---': out.append('<hr>'); i+=1; continue
        if line.startswith('#### '): out.append('<h4>'+links(line[5:].strip())+'</h4>'); i+=1; continue
        if line.startswith('### '): out.append('<h3>'+links(line[4:].strip())+'</h3>'); i+=1; continue
        if line.startswith('## '): out.append('<h2>'+links(line[3:].strip())+'</h2>'); i+=1; continue
        if line.startswith('# '): i+=1; continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                rows.append([x.strip() for x in lines[i].strip().strip('|').split('|')]); i+=1
            header=rows[0]; data=rows[2:] if len(rows)>1 and all(re.fullmatch(r':?-+:?',x) for x in rows[1]) else rows[1:]
            out.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+links(x)+'</th>' for x in header)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+links(x)+'</td>' for x in row)+'</tr>' for row in data)+'</tbody></table></div>'); continue
        if '\t' in line:
            rows=[]
            while i<len(lines) and '\t' in lines[i]: rows.append([x.strip() for x in lines[i].split('\t')]); i+=1
            width=len(rows[0]); rows=[r[:width]+['']*max(0,width-len(r)) for r in rows]
            out.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+links(x)+'</th>' for x in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+links(x)+'</td>' for x in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>'); continue
        if line.startswith('- '):
            vals=[]
            while i<len(lines) and lines[i].startswith('- '): vals.append(lines[i][2:]); i+=1
            out.append('<ul>'+''.join('<li>'+links(x)+'</li>' for x in vals)+'</ul>'); continue
        if re.match(r'^\d+\. ',line):
            vals=[]
            while i<len(lines) and re.match(r'^\d+\. ',lines[i]): vals.append(re.sub(r'^\d+\. ','',lines[i])); i+=1
            out.append('<ol>'+''.join('<li>'+links(x)+'</li>' for x in vals)+'</ol>'); continue
        vals=[line]; i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','- ','```')) and '\t' not in lines[i] and not re.match(r'^\d+\. ',lines[i]): vals.append(lines[i]); i+=1
        para(vals)
    return ''.join(out)

def sections(markup):
    nav=[]; result=[]
    for b in re.split(r'(?=<h2>)', markup):
        hit=re.match(r'<h2>(.*?)</h2>',b,re.S)
        if not hit:
            if b.strip(): result.append(b)
            continue
        title=re.sub('<[^>]+>','',hit.group(1)); n=len(nav)+1; ident=f'section-{n}'
        b=b.replace('<h2>',f'<h2 id="{ident}">',1)
        nav_title=re.sub(r'^\d+\.\s*', '', title)
        nav.append(f'<a href="#{ident}">{n}. {escape(nav_title)}</a>')
        if title.lower().startswith('solutions'):
            inside=b.split('</h2>',1)[1]
            b=f'<section class="book-section" aria-labelledby="{ident}"><h2 id="{ident}">{escape(title)}</h2><p>Try the exercises before opening the worked explanations.</p><details class="solutions"><summary>Show solutions and explanations</summary><div>{inside}</div></details></section>'
        else: b=f'<section class="book-section" aria-labelledby="{ident}">{b}</section>'
        result.append(b)
    return ''.join(nav), ''.join(result)

for course in (1,2,3):
    definition=DATA[course-1]; cid=f'C{course:02d}'; folder=ROOT/'materials'/'student_books'/f'course_{course:02d}'; public=ROOT/'public'/'course-book'/f'course-{course:02d}'
    folder.mkdir(parents=True,exist_ok=True); public.mkdir(parents=True,exist_ok=True)
    course_page=(ROOT/'public'/'courses'/f'{SLUGS[course]}.html').read_text(); head=course_page.split('<main id="main">',1)[0]
    head=re.sub(r'<title>.*?</title>',f'<title>Course Book · Course {course} | Wooplix Academy</title>',head)
    for css in ('/course-book.css','/course-book/course-05/reader.css'):
        if css not in head: head=head.replace('</head>',f'<link rel="stylesheet" href="{css}"></head>')
    footer='<footer'+course_page.split('<footer',1)[1]
    for number in READY[course]:
        body=source_for(course,number); chapter=definition['chapters'][number-1]; expected=chapter['title']
        # Use the approved title; imported headings and YAML metadata are internal formatting only.
        body=re.sub(r'^' + re.escape(expected) + r'\n', '', body, count=1)
        body=re.sub(r'^#\s*' + re.escape(expected) + r'\n', '', body, count=1)
        clean=f'# {expected}\n\n'+body.strip()+'\n'
        (folder/f'chapter_{number:02d}.md').write_text(clean)
        nav, content=sections(markdown_html(clean))
        prev=f'<a href="/course-book/course-{course:02d}/chapter-{number-1:02d}">← Previous chapter</a>' if number>1 else f'<a href="/courses/{SLUGS[course]}">Course overview</a>'
        nxt=f'<a href="/course-book/course-{course:02d}/chapter-{number+1:02d}">Next chapter →</a>' if number<len(definition['chapters']) else f'<a href="/course-book/course-{course:02d}">Back to Course Book →</a>'
        hero=f'<div class="book-breadcrumb"><a href="/courses/{SLUGS[course]}">Course {course}</a><span>/</span><a href="/course-book/course-{course:02d}">Course Book</a><span>/</span><span>Chapter {number}</span></div><header class="book-hero"><p class="eyebrow">COURSE {course:02d} · CHAPTER {number:02d}</p><h1>{escape(expected)}</h1><p>{escape(chapter["practice"])}</p><div class="book-tags"><span>Student course book</span><span>Worked examples</span><span>Practice and solutions</span></div><div class="reader-actions"><button type="button" data-print>Print / save PDF</button><a download href="/course-book/course-{course:02d}/chapter-{number:02d}-student.md">Download chapter (Markdown) ↓</a></div></header>'
        end=f'<div class="book-end"><h2>Continue your course work</h2><p>{escape(chapter["practice"])}</p><div class="reader-actions">{prev}{nxt}</div><p><a href="/course-book/course-{course:02d}">Course Book index →</a></p></div>'
        page=head+f'<main id="main" class="book-page">{hero}<div class="book-layout"><aside class="reader-sidebar"><details open><summary>In this chapter</summary><nav aria-label="Chapter sections">{nav}</nav></details><p class="save-note">Your reading position is saved on this browser.</p></aside><article class="book-content">{content}{end}</article></div></main>'+footer.replace('</body>',f'<script src="/course-book/course-{course:02d}/course-book.js" defer></script></body>')
        (public/f'chapter-{number:02d}.html').write_text(page); (public/f'chapter-{number:02d}-student.md').write_text(clean)
    # Full index uses approved curriculum titles, showing that the complete book is available.
    items=[]
    for n,ch in enumerate(definition['chapters'],1):
        url=f'/course-book/course-{course:02d}/chapter-{n:02d}'
        items.append(f'<li class="book-chapter available"><span class="chapter-num">{n:02d}</span><div><h2><a href="{url}">{escape(ch["title"])}</a></h2><p>{escape(ch["topics"])}</p><span class="chapter-status">Ready to read</span></div><a class="button button-dark" href="{url}">Read chapter →</a></li>')
    first=f'/course-book/course-{course:02d}/chapter-01'
    index=head+f'<main id="main" class="book-directory"><div class="book-breadcrumb"><a href="/courses/{SLUGS[course]}">Course {course}</a><span>/</span><span>Course Book</span></div><header class="book-hero"><p class="eyebrow">COURSE {course:02d} · STUDENT LEARNING</p><h1>Course Book</h1><p>{escape(definition["title"])}</p><p class="book-description">Read the full course chapter by chapter. Each lesson includes explanations, a worked case, practice, checks and student solutions.</p><a class="button button-dark" href="{first}">Start Chapter 1 →</a></header><ol class="book-chapters">{"".join(items)}</ol></main>'+footer
    (public/'index.html').write_text(index); (public/'reader.css').write_text((ROOT/'public/course-book/course-05/reader.css').read_text()); (public/'course-book.js').write_text((ROOT/'public/course-book.js').read_text())
print('Imported Course 1–3 student chapters.')
