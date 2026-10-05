"""Build all 16 Course 5 student chapters, using the Academy course-book reader."""
import csv
import html
import io
import json
import re
import shutil
from pathlib import Path
import markdown
ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT/'materials/student_books/course_05'
OUT = ROOT/'public/course-book/course-05'
OUT.mkdir(parents=True, exist_ok=True)
SYLLABUS = json.loads((ROOT/'website/doc_syllabi.json').read_text())['courses'][4]
COURSE_PAGE = ROOT/'public/courses/zoho-implementation-consulting-practicum.html'
page = COURSE_PAGE.read_text()
head = page[:page.index('<main id="main">')]
head = re.sub(r'<title>.*?</title>', '<title>Course Book · Course 5 | Wooplix Academy</title>',head)
head = re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="Sixteen student chapters on Zoho implementation and consulting: discovery, architecture, migration, testing, release and handover.">',head)
for css in ['/course-book.css','/course-book/course-05/reader.css']:
    if css not in head: head=head.replace('</head>',f'<link rel="stylesheet" href="{css}"></head>')
footer = page[page.index('<footer'):]
book_js=(ROOT/'public/course-book.js').read_text().replace("'wooplix-course01-chapter01-section'", "'wooplix-course05-' + location.pathname + '-section'")
(OUT/'course-book.js').write_text(book_js)
(OUT/'reader.css').write_text(".book-content pre{max-width:100%;overflow:auto;padding:20px;border-radius:10px;background:#142c28;color:#edf5f0;font: .83rem/1.65 ui-monospace,SFMono-Regular,Consolas,monospace;tab-size:4}.book-content pre code{white-space:pre}.book-content :not(pre)>code{font-size:.9em;background:#eaf2ed;padding:2px 5px;border-radius:4px;overflow-wrap:anywhere}.book-content blockquote{margin:20px 0;padding:14px 20px;border-left:4px solid #5b8c74;background:#f0f6ed;font-size:.96rem}.book-content blockquote p{margin:0}.book-downloads{padding:20px;background:#eaf2ed;border-radius:10px;margin:20px 0}.map-label{font-size:.85rem;color:#53655e}.book-overview{margin:30px 0}.book-overview img{width:100%;height:auto}@media print{.book-content pre{white-space:pre-wrap;background:#f2f4ef;color:#142c28;overflow:visible;font-size:8pt}.book-content pre code{white-space:pre-wrap;overflow-wrap:anywhere}}")

def flow_table(code):
    labels, groups, edges = {}, {}, []
    group=''
    for line in code.splitlines():
        sub=re.match(r'\s*subgraph\s+\w+\["([^\"]+)"\]',line)
        if sub: group=sub[1];continue
        if line.strip()=='end':group='';continue
        for node,square,diamond in re.findall(r'(\w+)(?:\[([^\]]*)\]|\{([^}]*)\})',line):
            labels[node]=(square or diamond).strip('"')
            if group: groups[node]=group
    for line in code.splitlines():
        line=re.sub(r'\s+--\s+(.+?)\s+-->',r' -->|\1|',line)
        edge=re.match(r'^\s*(\w+)(?:\[[^\]]*\]|\{[^}]*\})?\s*(-->|-\.->)(?:\|([^|]*)\|)?\s*(\w+)(?:\[[^\]]*\]|\{[^}]*\})?\s*$',line)
        if edge:
            a,arrow,condition,b=edge.groups()
            edges.append((groups.get(a,'—'),labels.get(a,a),condition or ('Reference / boundary' if arrow=='-.->' else 'Continue'),labels.get(b,b)))
        elif '-->' in line or '-.->' in line:
            raise ValueError('Unparsed flow edge: '+line)
    assert edges, 'Diagram has no parsed transitions'
    return '| Part / owner | From | Route / condition | To |\n| --- | --- | --- | --- |\n'+'\n'.join('| '+' | '.join(v.replace('|','\\|') for v in row)+' |' for row in edges)

def sequence_table(code):
    labels={};rows=[]
    for line in code.splitlines():
        p=re.match(r'\s*participant (\w+) as (.+)',line)
        if p:labels[p[1]]=p[2]
    for line in code.splitlines():
        e=re.match(r'\s*(\w+)(->>|-->>|--x)(\w+):\s*(.+)',line)
        if e:rows.append((str(len(rows)+1),labels.get(e[1],e[1]),labels.get(e[3],e[3]),e[4], 'Lost acknowledgement' if e[2]=='--x' else 'Message'))
    assert rows
    return '| Step | From | To | Information | Meaning |\n| --- | --- | --- | --- | --- |\n'+'\n'.join('| '+' | '.join(v.replace('|','\\|') for v in row)+' |' for row in rows)

def diagram(match):
    code=match[1]
    table=sequence_table(code) if code.lstrip().startswith('sequenceDiagram') else flow_table(code)
    return '\n\n**Process map** — read each row as one arrow in the supplied diagram.\n\n'+table+'\n\n'

def render_sections(body):
    rendered = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists"])
    rendered = re.sub(r"<table>", '<div class="table-wrap"><table>', rendered).replace("</table>", "</table></div>")
    rendered = rendered.replace('<div class="table-wrap"><div class="table-wrap">', '<div class="table-wrap">').replace("</table></div></div>", "</table></div>")
    blocks = re.split(r"(?=<h2>)", rendered)
    nav, sections = [], []
    for block in blocks:
        m = re.match(r"<h2>(.*?)</h2>", block, flags=re.S)
        if not m:
            if block.strip(): sections.append(block)
            continue
        title = re.sub(r"<[^>]+>", "", m.group(1))
        number = re.match(r"(\d+)\.", title)
        if not number:
            sections.append(block)
            continue
        ident = "section-" + number.group(1)
        block = block.replace("<h2>", f'<h2 id="{ident}">', 1)
        nav.append(f'<a href="#{ident}">{html.escape(title)}</a>')
        if number.group(1) == "9":
            inner = block[block.index("</h2>") + 5:]
            block = f'<section class="book-section" aria-labelledby="{ident}"><h2 id="{ident}">{html.escape(title)}</h2><p>Try the questions first. Open the solutions when you are ready to compare your reasoning.</p><details class="solutions"><summary>Show solutions and explanations</summary><div>{inner}</div></details></section>'
        else:
            block = f'<section class="book-section" aria-labelledby="{ident}">{block}</section>'
        sections.append(block)
    return "".join(nav), "".join(sections)

source_links=[]
examples={'evergreen_prototype.py':10,'evergreen_interface.py':11,'evergreen_reporting.py':13}
for filename,number in examples.items():
    shutil.copyfile(SOURCE_DIR/'examples'/filename,OUT/filename)

for number,chapter in enumerate(SYLLABUS['chapters'],1):
    raw=(SOURCE_DIR/f'chapter_{number:02d}.md').read_text()
    title=re.search(r'^# (.+)$',raw,re.M)[1]
    assert title==chapter['title']
    body=re.sub(r'^# .+\n','',raw,count=1).strip()
    downloads=[]
    def csv_download(m):
        text=m[1].strip(); list(csv.reader(io.StringIO(text)))
        name=f'chapter-{number:02d}-dataset-{len(downloads)+1:02d}.csv'
        (OUT/name).write_text(text+'\n');downloads.append(name)
        return m[0]
    body=re.sub(r'```csv\n(.*?)\n```',csv_download,body,flags=re.S)
    body=re.sub(r'```mermaid\n(.*?)\n```',diagram,body,flags=re.S)
    nav,reader=render_sections(body)
    extra=[]
    for name in downloads:extra.append(f'<a download href="/course-book/course-05/{name}">Practice dataset (CSV) ↓</a>')
    for name,n in examples.items():
        if n==number:extra.append(f'<a download href="/course-book/course-05/{name}">Download {name} ↓</a>')
    if number in (13,15):extra.append('<a download href="/course-book/course-05/evergreen_prototype.py">Chapter 10 reference prototype ↓</a>')
    resources='<div class="book-downloads"><b>Practice resources</b><div class="reader-actions">'+''.join(extra)+'</div></div>' if extra else ''
    slug=f'chapter-{number:02d}'
    previous=f'<a href="/course-book/course-05/chapter-{number-1:02d}">← Previous chapter</a>' if number>1 else '<a href="/courses/zoho-implementation-consulting-practicum">Course 5 overview</a>'
    next_link=f'<a href="/course-book/course-05/chapter-{number+1:02d}">Next chapter →</a>' if number<16 else '<a href="/course-book/course-05">Back to Course Book →</a>'
    hero=f'<div class="book-breadcrumb"><a href="/courses/zoho-implementation-consulting-practicum">Course 5</a><span>/</span><a href="/course-book/course-05">Course Book</a><span>/</span><span>Chapter {number}</span></div><header class="book-hero"><p class="eyebrow">COURSE 05 · CHAPTER {number:02d}</p><h1>{html.escape(title)}</h1><p>{html.escape(chapter["practice"])}</p><div class="book-tags"><span>Student course book</span><span>Fictional Evergreen case</span><span>Worked examples &amp; practice</span></div><div class="reader-actions"><button type="button" data-print>Print / save PDF</button><a download href="/course-book/course-05/{slug}-student.md">Download chapter (Markdown) ↓</a></div></header>'
    end=f'<div class="book-end"><h2>Keep your project work</h2><p>{html.escape(chapter["practice"])}</p><div class="reader-actions">{previous}{next_link}</div><p><a href="/course-book/course-05">All 16 chapters →</a></p></div>'
    content=head+f'<main id="main" class="book-page">{hero}<div class="book-layout"><aside class="reader-sidebar"><details open><summary>In this chapter</summary><nav aria-label="Chapter sections">{nav}</nav></details><p class="save-note">Your reading position is saved on this browser.</p></aside><article class="book-content">{resources}{reader}{end}</article></div></main>'+footer.replace('</body>','<script src="/course-book/course-05/course-book.js" defer></script></body>')
    (OUT/f'{slug}.html').write_text(content)
    (OUT/f'{slug}-student.md').write_text(raw)
    source_links.append((number,title,chapter['topics']))
items=[]
for n,title,topics in source_links:
    url=f'/course-book/course-05/chapter-{n:02d}'
    items.append(f'<li class="book-chapter available"><span class="chapter-num">{n:02d}</span><div><h2><a href="{url}">{html.escape(title)}</a></h2><p>{html.escape(topics)}</p><span class="chapter-status">Ready to read</span></div><a class="button button-dark" href="{url}">Read chapter →</a></li>')
index=head+'<main id="main" class="book-directory"><div class="book-breadcrumb"><a href="/courses/zoho-implementation-consulting-practicum">Course 5</a><span>/</span><span>Course Book</span></div><header class="book-hero"><p class="eyebrow">COURSE 05 · STUDENT LEARNING</p><h1>Course Book</h1><p>Zoho Implementation &amp; Consulting Practicum</p><p class="book-description">Sixteen chapters follow an implementation engagement from the sales handoff to client presentation. Read the lessons, work through the Evergreen examples and build your own project pack.</p><a class="button button-dark" href="/course-book/course-05/chapter-01">Start Chapter 1 →</a></header><figure class="book-overview"><img src="/assets/course-book/course05-engagement.svg" alt="Engagement learning path: understand the client, design the solution, plan and validate delivery, then release and hand over. Chapters 1–4, 5–8, 9–12 and 13–16 support these four stages." width="960" height="250"></figure><ol class="book-chapters">'+''.join(items)+'</ol></main>'+footer
(OUT/'index.html').write_text(index)
print('Built Course 5 book: 16 chapters, student downloads, reference programs and process maps.')
