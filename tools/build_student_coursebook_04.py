"""Build the Course 4 student reader from its reviewed Markdown chapters."""
import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "materials/student_books/course_04"
OUT = ROOT / "public/course-book/course-04"
SYLLABUS = json.loads((ROOT / "website/doc_syllabi.json").read_text(encoding="utf-8"))["courses"][3]
COURSE_PAGE = ROOT / "public/courses/corporate-ai-automation-workshop.html"
OUT.mkdir(parents=True, exist_ok=True)

page = COURSE_PAGE.read_text(encoding="utf-8")
head = page[:page.index('<main id="main">')]
head = re.sub(r"<title>.*?</title>", "<title>Course Book · Course 4 | Wooplix Academy</title>", head)
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Read the Course 4 student book: ten chapters on choosing a business process and preparing a measured automation pilot proposal.">', head)
if '/course-book.css' not in head:
    head = head.replace('</head>', '<link rel="stylesheet" href="/course-book.css"></head>')
footer = page[page.index('<footer'):]
book_js = (ROOT / "public/course-book.js").read_text(encoding="utf-8")
book_js = book_js.replace("wooplix-course01-chapter01-section", "wooplix-course04-' + location.pathname + '-section")
(OUT / "course-book.js").write_text(book_js, encoding="utf-8")

SECTION_RE = re.compile(
    r"^(?:1\. What you will learn|2\. Lessons|3\. Visual explanation — .+|"
    r"4\. Worked case — .+|5\. Try it yourself — Guided practice|"
    r"6\. Independent challenge|7\. Common problems and recovery|"
    r"8\. Check your understanding|9\. Solutions and explanations|"
    r"10\. Chapter recap and next step|11\. Glossary and further reading)$"
)

def read_source(number):
    text = (SOURCE_DIR / f"chapter_{number:02d}.md").read_text(encoding="utf-8")
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    text = text.split("## Chapter continuity")[0].strip()
    title_match = re.search(r"^# (.+)$", text, flags=re.M)
    title = title_match.group(1).strip() if title_match else SYLLABUS["chapters"][number - 1]["title"]
    text = re.sub(r"^# .+\n", "", text, count=1)
    lines = []
    previous_kind = "blank"
    in_fence = False
    for original in text.splitlines():
        line = original.rstrip()
        if line.startswith("```"):
            in_fence = not in_fence
        if SECTION_RE.match(line.strip()):
            line = "## " + line.strip()
        elif re.match(r"^(?:What you need|Your contribution to the course project|Lesson \d+ — .+|Guided practice(?: — .+)?|Independent challenge(?: — .+)?|Worked example(?: — .+)?|Step \d+:.+)$", line.strip()):
            line = "### " + line.strip()
        if not line.strip():
            lines.append("")
            previous_kind = "blank"
            continue
        if in_fence:
            kind = "fence"
        elif line.lstrip().startswith("|"):
            kind = "table"
        elif re.match(r"^\s*(?:[-*+]\s+|\d+\.\s+)", line):
            kind = "list"
        elif re.match(r"^\s{2,}\S", line):
            kind = "continuation"
        elif line.startswith("#") or line.startswith(">") or line.startswith("<"):
            kind = "block"
        else:
            kind = "text"
        if lines and lines[-1] and not in_fence:
            if (kind == "text" and previous_kind in {"text", "list", "table", "block"}) or (kind in {"list", "table", "block"} and previous_kind in {"text", "list", "table", "block"} and kind != previous_kind):
                lines.append("")
        lines.append(line)
        previous_kind = kind
    return title, "\n".join(lines).strip()

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

source_links = []
for number, chapter in enumerate(SYLLABUS["chapters"], start=1):
    title, body = read_source(number)
    nav, reader = render_sections(body)
    lead = re.search(r"<h2 id=\"section-1\">.*?</h2>\s*<p>(.*?)</p>", reader, flags=re.S)
    intro = re.sub(r"<[^>]+>", "", lead.group(1)) if lead else chapter.get("practice", "Read the lessons and complete the exercises.")
    intro = html.escape(re.sub(r"\s+", " ", intro).strip())
    slug = f"chapter-{number:02d}"
    prev_link = f'<a class="text-link" href="/course-book/course-04/chapter-{number-1:02d}">← Previous chapter</a>' if number > 1 else '<a class="text-link" href="/courses/corporate-ai-automation-workshop">Course 4 overview</a>'
    next_link = f'<a class="button button-dark" href="/course-book/course-04/chapter-{number+1:02d}">Next chapter →</a>' if number < len(SYLLABUS["chapters"]) else '<a class="button button-dark" href="/courses/corporate-ai-automation-workshop#syllabus">Back to the course →</a>'
    hero = f'''<div class="book-breadcrumb"><a href="/courses/corporate-ai-automation-workshop">Course 4 · Corporate AI &amp; Automation Opportunity Workshop</a><span>/</span><a href="/course-book/course-04/">Course Book</a><span>/</span><span>Chapter {number}</span></div><header class="book-hero"><p class="eyebrow">COURSE 04 · CHAPTER {number:02d}</p><h1>{html.escape(title)}</h1><p>{intro}</p><div class="reader-actions"><button type="button" data-print>Print / save PDF</button><a href="/course-book/course-04/{slug}-student.md" download>Download chapter (Markdown) ↓</a></div></header>'''
    end = f'''<div class="book-end"><h2>Chapter {number} complete</h2><p>{html.escape(chapter.get("practice", "Keep your work for the final proposal."))}</p><div class="reader-actions">{prev_link}{next_link}</div><p><a href="/course-book/course-04/">All Course 4 chapters →</a></p></div>'''
    nav_html = f'<nav aria-label="Chapter sections">{nav}</nav>'
    content = f'''{head}<main id="main" class="book-page">{hero}<div class="book-layout"><aside class="reader-sidebar"><details open><summary>In this chapter</summary>{nav_html}</details><p class="save-note">Your reading position is saved on this browser.</p></aside><article class="book-content">{reader}{end}</article></div></main>{footer.replace('</body>', '<script src="/course-book/course-04/course-book.js" defer></script></body>')}'''
    (OUT / f"{slug}.html").write_text(content, encoding="utf-8")
    # The download is student-facing text with no YAML/frontmatter.
    (OUT / f"{slug}-student.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
    source_links.append((number, title, chapter.get("topics", "")))

items = []
for number, title, description in source_links:
    slug = f"chapter-{number:02d}"
    items.append(f'''<li class="book-chapter available"><span class="chapter-num">{number:02d}</span><div><h2><a href="/course-book/course-04/{slug}">{html.escape(title)}</a></h2><p>{html.escape(description)}</p><span class="chapter-status">Ready to read</span></div><a class="button button-dark" href="/course-book/course-04/{slug}">Read chapter →</a></li>''')
index = f'''{head}<main id="main" class="book-directory"><div class="book-breadcrumb"><a href="/courses/corporate-ai-automation-workshop">Course 4</a><span>/</span><span>Course Book</span></div><header class="book-hero"><p class="eyebrow">COURSE 04 · STUDENT LEARNING</p><h1>Course Book</h1><p>Corporate AI &amp; Automation Opportunity Workshop</p><p class="book-description">Ten chapters take you from understanding the process to presenting a measured business automation pilot proposal. All examples and project data are identified as fictional training material.</p><a class="button button-dark" href="/course-book/course-04/chapter-01">Start Chapter 1 →</a></header><ol class="book-chapters">{''.join(items)}</ol></main>{footer}'''
(OUT / "index.html").write_text(index, encoding="utf-8")
print(f"Built Course 4 reader with {len(source_links)} chapters in {OUT.relative_to(ROOT)}")
