"""Create original learning diagrams and add them to selected course-book lessons.

The diagrams explain a decision or system boundary. They are intentionally not
copied product screenshots, which become stale as Zoho changes its interface.
Run after rebuilding course-book HTML.
"""
from html import escape
from pathlib import Path
import re
import textwrap

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'public' / 'assets' / 'learning-diagrams'
ASSETS.mkdir(parents=True, exist_ok=True)

DIAGRAMS = {
    ('01', '09'): ('workflow-control.svg', 'Workflow control', 'A workflow acts only after its trigger and criteria both match.', ['Record event', 'Check trigger', 'Test criteria', 'Controlled action'], 'Criteria true?'),
    ('01', '14'): ('cross-app-boundary.svg', 'Cross-application handoff', 'A validated record crosses an application boundary with evidence and recovery.', ['Source record', 'Validate data', 'Send approved payload', 'Record outcome'], 'Safe to send?'),
    ('02', '03'): ('creator-data-model.svg', 'Creator data model', 'A well-designed app starts with records, relationships and validation before screens.', ['Core record', 'Related data', 'Validation rules', 'Usable form'], 'Valid structure?'),
    ('02', '11'): ('crm-api-boundary.svg', 'CRM API boundary', 'The application validates context before calling CRM and records the returned result.', ['Application context', 'Validate request', 'CRM API call', 'Store outcome'], 'Allowed and complete?'),
    ('02', '15'): ('reliable-event-flow.svg', 'Reliable event flow', 'Events are deduplicated, processed and reconciled as controlled business work.', ['Receive event', 'Check duplicate key', 'Process once', 'Write evidence'], 'Already processed?'),
    ('03', '01'): ('ai-system-choices.svg', 'Choosing an AI system', 'Start with the simplest dependable mechanism and add agency only when it is needed.', ['Rule', 'Workflow', 'Assistant', 'Bounded agent'], 'Who chooses next step?'),
    ('03', '07'): ('rag-safety-path.svg', 'Grounded retrieval path', 'Permissions and source status are checked before evidence reaches the model.', ['User request', 'Authorize access', 'Retrieve approved evidence', 'Cited answer'], 'Enough evidence?'),
    ('03', '14'): ('approved-write-path.svg', 'Controlled business action', 'A proposed change becomes a live action only after approval and record revalidation.', ['Draft proposal', 'Human approval', 'Revalidate record', 'Execute and audit'], 'Still current?'),
    ('04', '03'): ('opportunity-funnel.svg', 'Opportunity selection', 'Evidence is narrowed into a pilot only when the problem, value and controls are clear.', ['Observed problem', 'Candidate option', 'Readiness check', 'Pilot decision'], 'Worth testing?'),
    ('05', '14'): ('release-recovery.svg', 'Conditional release', 'A release uses explicit go/no-go checks and a known recovery boundary.', ['Release checklist', 'Go / no-go', 'Controlled release', 'Verify or recover'], 'Acceptance met?'),
}


def lines(label):
    return textwrap.wrap(label, width=17)[:2]


def diagram_svg(title, description, steps, decision):
    width, height = 960, 335
    boxes = [(42, 120), (270, 120), (498, 120), (726, 120)]
    chunks = []
    for (x, y), label in zip(boxes, steps):
        text = ''.join(f'<text x="{x+92}" y="{y+43+i*19}" text-anchor="middle" class="label">{escape(row)}</text>' for i, row in enumerate(lines(label)))
        chunks.append(f'<rect x="{x}" y="{y}" width="184" height="82" rx="13" class="box"/>{text}')
    arrows = ''.join(f'<path d="M{x+184} {y+41} H{nx-13}" class="arrow" marker-end="url(#arrow)"/>' for (x,y),(nx,ny) in zip(boxes,boxes[1:]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#2a6556"/></marker>
<style>.label{{font:600 16px Arial,sans-serif;fill:#163d34}}.small{{font:500 13px Arial,sans-serif;fill:#5a7068}}.box{{fill:#f3f8f5;stroke:#78a58f;stroke-width:1.5}}.arrow{{fill:none;stroke:#2a6556;stroke-width:2.2}}</style></defs>
<rect width="960" height="335" rx="18" fill="#fcfdfa"/><text x="42" y="50" class="label" font-size="21">{escape(title)}</text><text x="42" y="78" class="small">{escape(description)}</text>
{''.join(chunks)}{arrows}
<path d="M480 246 L540 286 L480 326 L420 286 Z" fill="#fff2d9" stroke="#c29543" stroke-width="1.5"/>
<text x="480" y="282" text-anchor="middle" class="label" font-size="13">{escape(decision)}</text><text x="480" y="300" text-anchor="middle" class="small" font-size="11">check before continuing</text>
</svg>'''


def figure(filename, title, description):
    return f'''<figure class="book-figure learning-figure" data-learning-visual="{filename}"><img src="/assets/learning-diagrams/{filename}" alt="{escape(description, quote=True)}" width="960" height="335"><figcaption><b>{escape(title)}.</b> {escape(description)}</figcaption></figure>'''


for (course, chapter), (filename, title, description, steps, decision) in DIAGRAMS.items():
    (ASSETS / filename).write_text(diagram_svg(title, description, steps, decision))
    path = ROOT / 'public' / 'course-book' / f'course-{course}' / f'chapter-{chapter}.html'
    page = path.read_text()
    page = re.sub(r'<figure class="book-figure learning-figure" data-learning-visual="'+re.escape(filename)+r'">.*?</figure>', '', page, flags=re.S)
    visual = figure(filename, title, description)
    # Replace the first raw Mermaid code block when it exists; otherwise put
    # the visual after the first instructional section.
    updated, count = re.subn(r'<pre><code class="language-mermaid">.*?</code></pre>', visual, page, count=1, flags=re.S)
    if not count:
        updated, count = re.subn(r'(<section class="book-section"[^>]*>.*?</h2>)', r'\1'+visual, page, count=1, flags=re.S)
    if not count:
        raise ValueError(f'Could not place visual in {path}')
    path.write_text(updated)

# One concise, reusable accuracy notice per technical course book. It gives
# learners a real preparation action without repeating a warning in every page.
notice = '''<aside class="environment-note"><b>Before live configuration</b><p>Match the exercise to your product edition, data centre and assigned role. Confirm the current menu, permission and API behaviour in the official reference before changing a shared environment.</p><a href="/lab-verification.html">Use the live-lab verification checklist →</a></aside>'''
for course in ('01', '02', '03'):
    path = ROOT / 'public' / 'course-book' / f'course-{course}' / 'index.html'
    page = path.read_text()
    page = re.sub(r'<aside class="environment-note">.*?</aside>', '', page, flags=re.S)
    page = page.replace('<ol class="book-chapters">', notice+'<ol class="book-chapters">', 1)
    path.write_text(page)

print(f'Created and placed {len(DIAGRAMS)} learning diagrams.')
