"""Build the public syllabus sections from the saved Google Docs course content."""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
DATA = json.loads((ROOT / 'website/doc_syllabi.json').read_text())
SLUGS = [
    'zoho-business-process-automation',
    'zoho-developer-implementation-engineer',
    'ai-agentic-ai-builder',
    'corporate-ai-automation-workshop',
    'zoho-implementation-consulting-practicum',
]


def replace_section(page, class_name, replacement):
    pattern = rf'<section class="{class_name}"[^>]*>.*?</section>'
    page, count = re.subn(pattern, lambda _: replacement, page, flags=re.S)
    if count != 1:
        raise ValueError(f'Expected one {class_name} section, found {count}')
    return page


def chapter_id(number):
    return f'chapter-{number:02}'


def syllabus(course):
    blocks = []
    for number, chapter in enumerate(course['chapters'], 1):
        blocks.append(f'''<details class="module" id="{chapter_id(number)}" open>
<summary><span class="module-number">{number:02}</span><span class="module-title">{escape(chapter['title'])}</span><span class="module-plus" aria-hidden="true">+</span></summary>
<div class="module-content"><p><b>Topics:</b> {escape(chapter['topics'])}</p><p><b>Practice:</b> {escape(chapter['practice'])}</p></div></details>''')
    book_link = '<p><a class="text-link" href="/course-book/course-01/">Course Book · read Chapter 1 →</a></p>' if course['id'] == 1 else ''
    return f'''<section class="course-syllabus" id="syllabus">
<div class="syllabus-intro"><p class="eyebrow">{len(blocks)} CHAPTERS</p><h2>Course syllabus.</h2>{book_link}<p>Read the topics and practice task for each chapter. Expand or collapse chapters as you read.</p><p>Ask us about the course duration, schedule and delivery format.</p><p><a class="text-link" href="/#curriculum">Browse all five courses →</a></p></div>
<div><div class="chapter-controls"><button type="button" data-chapters="open">Expand all chapters</button><button type="button" data-chapters="close">Collapse all</button></div><div class="module-list">{''.join(blocks)}</div></div></section>'''


def project_section(course):
    project = course['project']
    title = project[0]
    brief = next(t for t in project if t.startswith('Project brief:')).removeprefix('Project brief: ').strip()
    work = [t.removeprefix('• ').strip() for t in project if t.startswith('• ')]
    assessment = project[project.index('How learning is assessed') + 1]
    return f'''<section class="course-project"><div><p class="eyebrow eyebrow-light">FINAL PROJECT</p><h2>{escape(title)}</h2><p>{escape(brief)}</p></div><div class="project-evidence"><h3>What you will produce</h3><ul>{''.join('<li>'+escape(t)+'</li>' for t in work)}</ul><h3>How learning is assessed</h3><p>{escape(assessment)}</p></div></section>'''


for course, slug in zip(DATA['courses'], SLUGS):
    path = PUBLIC / 'courses' / f'{slug}.html'
    page = path.read_text()
    if 'href="/syllabus.css"' not in page:
        page = page.replace('</head>', '<link rel="stylesheet" href="/syllabus.css"></head>', 1)
    page = replace_section(page, 'course-syllabus', syllabus(course))
    page = replace_section(page, 'course-project', project_section(course))
    project_brief = next(t for t in course['project'] if t.startswith('Project brief:')).removeprefix('Project brief: ').strip()
    facts = f'''<section class="course-facts"><article><span>WHO IT’S FOR</span><p>{escape(course['audience'])}</p></article><article><span>WHAT TO BRING</span><p>{escape(course['prerequisites'])}</p></article><article><span>COURSE PROJECT</span><p>{escape(course['project'][0])}: {escape(project_brief)}</p></article></section>'''
    page = replace_section(page, 'course-facts', facts)
    page = re.sub(r'<p class="course-summary">.*?</p>', lambda _: '<p class="course-summary">'+escape(course['summary'])+'</p>', page)
    page = re.sub(r'<h1>.*?</h1>', lambda _: '<h1>'+escape(course['title'])+'</h1>', page)
    page = re.sub(r'<title>.*?</title>', lambda _: '<title>'+escape(course['title'])+' | Wooplix Academy</title>', page)
    page = re.sub(r'<meta name="description" content="[^"]*">', lambda _: '<meta name="description" content="'+escape(course['summary'], quote=True)+'">', page)
    page = re.sub(r'(<div class="course-breadcrumb">.*?<span>›</span><span>)(.*?)(</span></div>)', lambda m: m[1]+escape(course['title'])+m[3], page)
    page = re.sub(r'<div class="course-hero-aside">.*?</div>', lambda _: f'<div class="course-hero-aside"><span>PROGRAMME {course["id"]:02}</span><b>{len(course["chapters"])} chapters.<br>Practice tasks.<br>Final project.</b><small>WOOPLIX ACADEMY</small></div>', page)
    if 'href="/syllabus.html">Curriculum' not in page:
        page = page.replace('<a href="/#programmes">Programmes</a>', '<a href="/#programmes">Programmes</a><a href="/syllabus.html">Curriculum</a>', 1)
    path.write_text(page)

template = (PUBLIC / 'courses' / (SLUGS[0] + '.html')).read_text()
head = template[:template.index('<main id="main">')]
head = re.sub(r'<title>.*?</title>', '<title>All Course Syllabi | Wooplix Academy</title>', head)
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Read the chapters, topics, practice tasks and final projects for all five Wooplix Academy Zoho and AI courses.">', head)
footer = template[template.index('<footer'):]
cards = []
for course, slug in zip(DATA['courses'], SLUGS):
    chapters = ''.join(f'<li><a href="/courses/{slug}.html#{chapter_id(n)}"><span>{n:02}</span>{escape(ch["title"])}</a></li>' for n, ch in enumerate(course['chapters'], 1))
    book_action = '<p><a class="text-link" href="/course-book/course-01/">Course Book · start learning →</a></p>' if course['id'] == 1 else ''
    cards.append(f'''<article class="curriculum-course" id="course-{course['id']}"><p class="eyebrow">COURSE {course['id']:02} · {len(course['chapters'])} CHAPTERS</p><h2><a href="/courses/{slug}.html">{escape(course['title'])}</a></h2><p>{escape(course['summary'])}</p><p><b>For:</b> {escape(course['audience'])}</p><ol class="chapter-index">{chapters}</ol><a class="button button-dark" href="/courses/{slug}.html#syllabus">Topics and practice tasks →</a>{book_action}</article>''')
main = f'''<main id="main"><section class="curriculum-header"><p class="eyebrow">WOOPLIX ACADEMY · ZOHO &amp; AI</p><h1>Course syllabi.</h1><p>Five courses. Choose a course or chapter to see what you will learn and practise.</p><nav class="curriculum-jump" aria-label="Choose a course">{''.join(f'<a href="#course-{c["id"]}">Course {c["id"]:02} · {len(c["chapters"])} chapters</a>' for c in DATA['courses'])}</nav></section><section class="curriculum-directory" aria-label="Course chapter directory">{''.join(cards)}</section></main>'''
(PUBLIC / 'syllabus.html').write_text(head + main + footer)

# Keep the home page chapter directory in sync with exactly the same source.
home_path = PUBLIC / 'index.html'
home = home_path.read_text()
home_section = f'''<section class="curriculum-home" id="curriculum" aria-labelledby="curriculum-title"><div class="curriculum-home-heading"><p class="eyebrow">FIVE COURSES · 86 CHAPTERS</p><h2 id="curriculum-title">Full course syllabus.</h2><p>Every chapter from our five course syllabi is listed here. Select a chapter to read its topics and practice task.</p><nav class="curriculum-jump" aria-label="Jump to a course">{''.join(f'<a href="#course-{c["id"]}">Course {c["id"]:02} · {len(c["chapters"])} chapters</a>' for c in DATA['courses'])}</nav></div>{''.join(cards)}</section>'''
if 'id="curriculum"' in home:
    home = replace_section(home, 'curriculum-home', home_section)
else:
    home = re.sub(r'<section class="detail-section section-pad"[^>]*>.*?</section>', '', home, flags=re.S)
    anchor = '<section class="approach-section section-pad"'
    if home.count(anchor) != 1:
        raise ValueError('Could not locate the home page curriculum insertion point')
    home = home.replace(anchor, home_section+'\n\n    '+anchor, 1)
if 'href="/syllabus.css"' not in home:
    home = home.replace('</head>', '<link rel="stylesheet" href="/syllabus.css"></head>', 1)
home = home.replace('href="/syllabus.html">Curriculum', 'href="#curriculum">Curriculum')
home = home.replace('href="/syllabus.html">Browse all 86 chapters', 'href="#curriculum">Browse all 86 chapters')
home = home.replace('<a class="text-link" href="#approach">See how learning works <span aria-hidden="true">→</span></a>', '<a class="text-link" href="#curriculum">Browse all 86 chapters <span aria-hidden="true">↓</span></a>')
for course, slug in zip(DATA['courses'], SLUGS):
    home = home.replace(f'href="/courses/{slug}.html" class="card-link">View course outline', f'href="/courses/{slug}.html#syllabus" class="card-link">Read all {len(course["chapters"])} chapters')
home = home.replace('AI &amp; Agentic AI Builder</h3>', 'AI &amp; Agentic AI Builder for Business Systems</h3>')
home = home.replace('Corporate AI &amp; Automation Workshop</h3>', 'Corporate AI &amp; Automation Opportunity Workshop</h3>')
home_path.write_text(re.sub(r'^ +$', '', home, flags=re.M))
for asset in PUBLIC.rglob('*'):
    if asset.suffix in {'.html', '.js', '.json', '.css'}:
        content = asset.read_text()
        if any(host in content for host in ('docs.google.com', 'drive.google.com')):
            raise ValueError(f'Internal document link found in public asset: {asset}')
print('Updated home page, five course pages and curriculum directory: 86 chapters.')
