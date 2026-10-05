"""Build the public student reader. Run after sync_public_syllabi.py; requires Markdown."""
import json
import re
from html import escape
from pathlib import Path
import markdown
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'public/course-book/course-01'
SOURCE = ROOT/'materials/student_books/course_01/chapter_01.md'
COURSE = json.loads((ROOT/'website/doc_syllabi.json').read_text())['courses'][0]
OUT.mkdir(parents=True, exist_ok=True)
page = (ROOT/'public/courses/zoho-business-process-automation.html').read_text()
head = page[:page.index('<main id="main">')]
head = re.sub(r'<title>.*?</title>', '<title>Course Book · Course 1 | Wooplix Academy</title>', head)
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Read the Course 1 student book: explanations, diagrams, worked examples and practice with explained solutions.">', head)
if '/course-book.css' not in head:
    head = head.replace('</head>', '<link rel="stylesheet" href="/course-book.css"></head>')
footer = page[page.index('<footer'):]
raw = SOURCE.read_text()
body = re.sub(r'^---\n.*?\n---\n', '', raw, count=1, flags=re.S)
body = body.split('## Chapter continuity')[0].strip()
body = re.sub(r'^# Chapter 1 — Business Process Discovery\n', '', body)
body = body.replace('1 Zoho, Business Process Management (https://www.zoho.com/creator/business-process-management-software/),', '1. [Zoho — Business Process Management](https://www.zoho.com/creator/business-process-management-software/),')
# Keep raw datasets available for practice and render a readable table alongside them.
def csv_block(match):
    import csv, io
    text=match[1].strip(); rows=list(csv.reader(io.StringIO(text)))
    number=csv_block.count; csv_block.count+=1
    name=['billing_packets.csv','order_events.csv'][number]
    (OUT/name).write_text(text+'\n')
    table='<div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+escape(c.replace('_',' '))+'</th>' for c in rows[0])+'</tr></thead><tbody>'
    table+=''.join('<tr>'+''.join('<td>'+escape(c or '—')+'</td>' for c in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>'
    return '\n\n'+table+'\n\n<p><a class="download-link" download href="/course-book/course-01/'+name+'">Download this dataset (CSV) ↓</a></p>\n\n'
csv_block.count=0
body=re.sub(r'```csv\n(.*?)\n```', csv_block, body, flags=re.S)
body=re.sub(r'```mermaid\n.*?\n```', '<figure class="book-figure"><img src="/assets/course-book/current-handoff.svg" alt="Written confirmation moves through Sales preparation and submission to Finance review. A complete packet is accepted; missing information returns to Sales for correction and resubmission." width="720" height="410"><figcaption>Current process: the correction loop is part of the work.</figcaption></figure>', body, flags=re.S)
# Preserve each explanation as a paragraph instead of merging adjacent prose into a wall of text.
lines=body.splitlines(); adjusted=[]
for i,line in enumerate(lines):
    if i and line and not line.startswith(('- ', ' ', '|', '<')) and not re.match(r'^\d+\. ', line) and (lines[i-1].startswith('- ') or re.match(r'^\d+\. ', lines[i-1])):
        adjusted.append('')
    adjusted.append(line)
    if line and not line.startswith(('#','|','<','- ','  ')) and not re.match(r'^\d+\. ',line): adjusted.append('')
body='\n'.join(adjusted)
html=markdown.markdown(body, extensions=['tables','fenced_code','sane_lists'])
html=re.sub(r'<table>', '<div class="table-wrap"><table>', html).replace('</table>','</table></div>')
html=html.replace('<div class="table-wrap"><div class="table-wrap">','<div class="table-wrap">').replace('</table></div></div>','</table></div>')
sections=re.split(r'(?=<h2>)',html)
nav=[]; chunks=[]
for block in sections:
    m=re.match(r'<h2>(.*?)</h2>',block)
    if not m: chunks.append(block); continue
    title=m[1]; num=re.match(r'(\d+)\.',title)[1]; id='section-'+num
    block=block.replace('<h2>', f'<h2 id="{id}">',1)
    nav.append(f'<a href="#{id}">{title}</a>')
    if num=='9': block=f'<section class="book-section" aria-labelledby="{id}"><h2 id="{id}">{title}</h2><p>Try the questions first. Open the solutions when you are ready to compare your reasoning.</p><details class="solutions"><summary>Show solutions and explanations</summary><div>{block[block.index("</h2>")+5:]}</div></details></section>'
    else: block=f'<section class="book-section" aria-labelledby="{id}">{block}</section>'
    chunks.append(block)
reader=''.join(chunks)
hero='''<div class="book-breadcrumb"><a href="/courses/zoho-business-process-automation">Course 1</a><span>/</span><a href="/course-book/course-01/">Course Book</a><span>/</span><span>Chapter 1</span></div><header class="book-hero"><p class="eyebrow">COURSE BOOK · CHAPTER 01</p><h1>Business Process Discovery</h1><p>Understand how work moves, find the causes of delay and design a process you can measure.</p><div class="book-tags"><span>No coding needed</span><span>Paper or spreadsheet practice</span><span>Fictional business examples</span></div><div class="reader-actions"><button type="button" data-print>Print / save PDF</button><a href="/course-book/course-01/chapter-01-student.md" download>Download chapter (Markdown) ↓</a></div></header>'''
(OUT/'chapter-01-student.md').write_text('# Chapter 1 — Business Process Discovery\n\n'+re.sub(r'^# Chapter 1 — Business Process Discovery\n','',re.sub(r'^---\n.*?\n---\n','',raw,count=1,flags=re.S).split('## Chapter continuity')[0]).strip()+'\n')
(OUT/'chapter-01.html').write_text(head+'<main id="main" class="book-page">'+hero+'<div class="book-layout"><aside class="reader-sidebar"><details open><summary>In this chapter</summary><nav aria-label="Chapter sections">'+''.join(nav)+'</nav></details><p class="save-note">Your reading position is saved on this browser.</p></aside><article class="book-content">'+reader+'<div class="book-end"><h2>Keep your work for Chapter 2</h2><p>Save your maps, measurements and acceptance criteria. You will use them to choose the right applications.</p><a href="/course-book/course-01/">Back to the Course Book →</a></div></article></div></main>'+footer.replace('</body>','<script src="/course-book.js" defer></script></body>'))
items=[]
for n,ch in enumerate(COURSE['chapters'],1):
    available=n==1
    items.append(f'<li class="book-chapter {"available" if available else "pending"}"><span class="chapter-num">{n:02}</span><div><h2>'+ (f'<a href="/course-book/course-01/chapter-01">{escape(ch["title"])}</a>' if available else escape(ch['title']))+f'</h2><p>{escape(ch["topics"])}</p><span class="chapter-status">'+('Ready to read' if available else 'Coming next')+'</span></div>'+('<a class="button button-dark" href="/course-book/course-01/chapter-01">Read chapter →</a>' if available else '')+'</li>')
(OUT/'index.html').write_text(head+'''<main id="main" class="book-directory"><div class="book-breadcrumb"><a href="/courses/zoho-business-process-automation">Course 1</a><span>/</span><span>Course Book</span></div><header class="book-hero"><p class="eyebrow">COURSE 01 · STUDENT LEARNING</p><h1>Course Book</h1><p>Zoho Business Process &amp; Corporate Automation</p><p class="book-description">Read the explanations, follow the examples and practise what you learn. Chapter 1 is available now; the remaining chapters are listed below.</p><a class="button button-dark" href="/course-book/course-01/chapter-01">Start Chapter 1 →</a></header><ol class="book-chapters">'''+''.join(items)+'</ol></main>'+footer)
# Accessible inline-SVG illustration: no third-party scripts or image service needed.
def box(x,y,w,h,label,fill='#e9f5f2'):
    if label == 'Complete information?':
        return f'<path d="M{x+w/2},{y-8} L{x+w},{y+h/2} L{x+w/2},{y+h+8} L{x},{y+h/2} Z" fill="{fill}" stroke="#275d52"/><text x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" fill="#102f29">Complete?</text>'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="#275d52"/><text x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" fill="#102f29">{label}</text>'
svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 410" role="img" aria-labelledby="title desc"><title id="title">Current order-to-finance handoff</title><desc id="desc">Sales prepares and submits a confirmed order. Finance reviews it. Complete packets are accepted. Missing information returns to Sales and is resubmitted.</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#275d52"/></marker></defs><rect width="720" height="410" rx="16" fill="#f7faf8"/>'
for args in [(25,35,200,65,'Written confirmation'),(260,35,200,65,'Sales prepares packet'),(495,35,200,65,'Sales sends packet'),(495,155,200,65,'Finance reviews'),(260,155,200,65,'Complete information?','#fff2da'),(25,155,200,65,'Finance accepts'),(260,300,200,65,'Sales corrects packet','#ffece9')]: svg+=box(*args)
for d in ['M225 67 H255','M460 67 H490','M595 100 V150','M495 188 H465','M260 188 H230','M360 220 V295','M460 332 H595 V225']:
    svg+=f'<path d="{d}" fill="none" stroke="#275d52" stroke-width="2" marker-end="url(#arrow)"/>'
svg+='<text x="233" y="173" font-family="Arial" font-size="12">Yes</text><text x="370" y="264" font-family="Arial" font-size="12">No: return with reason</text><text x="605" y="287" font-family="Arial" font-size="12">Resend</text></svg>'
(ROOT/'public/assets/course-book/current-handoff.svg').write_text(svg)
# Put course-book discovery in the source generator so future syllabus rebuilds preserve it.
sync=ROOT/'tools/sync_public_syllabi.py'
s=sync.read_text()
s=s.replace("    return f'''<section class=\"course-syllabus\" id=\"syllabus\">", "    book_link = '<p><a class=\"text-link\" href=\"/course-book/course-01/\">Course Book · read Chapter 1 →</a></p>' if course['id'] == 1 else ''\n    return f'''<section class=\"course-syllabus\" id=\"syllabus\">") if '    book_link = ' not in s else s
s=s.replace('<h2>Course syllabus.</h2><p>Read the topics', '<h2>Course syllabus.</h2>{book_link}<p>Read the topics')
old="    cards.append(f'''<article class=\"curriculum-course\""
if '    book_action = ' not in s:
    s=s.replace(old,"    book_action = '<p><a class=\"text-link\" href=\"/course-book/course-01/\">Course Book · start learning →</a></p>' if course['id'] == 1 else ''\n"+old)
s=s.replace("Topics and practice tasks →</a></article>''')", "Topics and practice tasks →</a>{book_action}</article>''')")
sync.write_text(s)
# Course-page hero and prominent book section (outside replaced syllabus).
coursepath=ROOT/'public/courses/zoho-business-process-automation.html'
p=coursepath.read_text()
if 'id="course-book"' not in p:
    section='''<section class="course-book-promo" id="course-book"><div><p class="eyebrow">READ &amp; PRACTISE</p><h2>Course Book</h2><p>Student explanations, worked examples, diagrams and practice with answers. Start with Chapter 1: Business Process Discovery.</p></div><a class="button button-dark" href="/course-book/course-01/">Open the Course Book →</a></section>'''
    p=p.replace('<section class="course-syllabus"',section+'<section class="course-syllabus"',1)
    p=p.replace('<a class="text-link" href="#syllabus">','<a class="text-link" href="/course-book/course-01/">Course Book →</a><a class="text-link" href="#syllabus">',1)
if '/course-book.css' not in p: p=p.replace('</head>','<link rel="stylesheet" href="/course-book.css"></head>')
coursepath.write_text(p)
print('Built Course 1 book directory, complete Chapter 1 reader, datasets and diagram.')
