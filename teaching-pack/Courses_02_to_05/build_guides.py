#!/usr/bin/env python3
"""Build four standalone Wooplix trainer guides from the reviewed course files.

The generator assembles the approved draft catalog, the 36 authored lesson plans,
trainer answer keys, and synthetic worksheets into offline HTML files. It does not
connect to Zoho or make external changes.
"""
from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LOCAL_SOURCE = HERE / "source_workspace"
SOURCE = LOCAL_SOURCE if LOCAL_SOURCE.exists() else ROOT / "outputs" / "Wooplix_Academy_Workspace_V2"
CATALOG = json.loads((SOURCE / "data" / "catalog.json").read_text(encoding="utf-8"))
PROGRAMS = {p["id"]: p for p in CATALOG["programs"]}
COURSE_IDS = ["ZDV", "AAB", "CAW", "ZIM"]
COURSE_ASSETS = {
    "ZDV": ["worksheets/data_dictionary.csv", "worksheets/sync_contract.csv", "worksheets/uat_log.csv", "worksheets/access_tests.csv", "assessment_ZDV.csv", "code_examples/normalize_requests.deluge", "code_examples/create_training_lead.deluge", "Practical_Assessment_Rubric.md"],
    "AAB": ["datasets/knowledge_records.json", "worksheets/change_request.csv", "worksheets/baseline_and_pilot.csv", "worksheets/uat_log.csv", "assessment_AAB.csv", "Practical_Assessment_Rubric.md"],
    "CAW": ["worksheets/baseline_and_pilot.csv", "worksheets/requirements.csv", "worksheets/change_request.csv", "assessment_CAW.csv", "Practical_Assessment_Rubric.md"],
    "ZIM": ["datasets/leads_50.csv", "worksheets/requirements.csv", "worksheets/data_dictionary.csv", "worksheets/migration_reconciliation.csv", "worksheets/automation_register.csv", "worksheets/access_tests.csv", "worksheets/uat_log.csv", "assessment_ZIM.csv", "Practical_Assessment_Rubric.md"],
}
RESOURCES = HERE / "resources"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def inline_md(value: str) -> str:
    value = esc(value)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", value)
    return value


def markdown_html(source: str) -> str:
    """Small renderer for the authored lesson/key Markdown used by this library."""
    out: list[str] = []
    paragraph: list[str] = []
    list_kind: str | None = None
    in_code = False
    code: list[str] = []

    def flush_p() -> None:
        if paragraph:
            out.append("<p>" + " ".join(inline_md(x.strip()) for x in paragraph) + "</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_kind
        if list_kind:
            out.append(f"</{list_kind}>")
            list_kind = None

    for raw in source.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            flush_p(); close_list()
            if in_code:
                out.append("<pre><code>" + esc("\n".join(code)) + "</code></pre>")
                code.clear()
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        if not line.strip():
            flush_p(); close_list()
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            flush_p(); close_list()
            level = min(len(heading.group(1)) + 1, 6)
            out.append(f"<h{level}>{inline_md(heading.group(2))}</h{level}>")
            continue
        item = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.+)$", line)
        if item:
            flush_p()
            ordered = bool(re.match(r"^\s*\d+\.", line))
            wanted = "ol" if ordered else "ul"
            if list_kind != wanted:
                close_list(); list_kind = wanted; out.append(f"<{wanted}>")
            out.append(f"<li>{inline_md(item.group(1))}</li>")
            continue
        if line.startswith("> "):
            flush_p(); close_list()
            out.append(f"<blockquote>{inline_md(line[2:])}</blockquote>")
            continue
        paragraph.append(line)
    flush_p(); close_list()
    if in_code:
        out.append("<pre><code>" + esc("\n".join(code)) + "</code></pre>")
    return "\n".join(out)


def source_info(source_id: str) -> tuple[str, str | None, str]:
    path = SOURCE / "knowledge" / f"{source_id}_reference.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        title = next((line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("# ")), source_id)
        match = re.search(r"https?://\S+", text)
        return title, match.group(0).rstrip(".,)") if match else None, "verified public reference"
    if source_id == "S01":
        return "User-supplied Wooplix Academy Business Automation Plan", None, "internal strategy source; not technical product evidence"
    return source_id, None, "source note not present in this package"


def module_html(course: dict, module: dict) -> str:
    lesson_path = SOURCE / module["practical_lab_path"]
    key_path = SOURCE / module["trainer_key_path"]
    lesson_text = lesson_path.read_text(encoding="utf-8")
    boilerplate = "Verify the current edition, account metadata and API signature before a live product demonstration. Examples and thresholds are proposed lab rules."
    guidance = {
        "ZDV": "Verify the Creator or CRM edition, event, API scope or quota used by this module. Examples and thresholds are proposed lab rules.",
        "AAB": "Check model, retrieval and tool behavior in the approved environment. Examples and thresholds are proposed lab rules.",
        "CAW": "Use approved synthetic examples; label estimates and any tool behavior that has not been verified. Examples and thresholds are proposed lab rules.",
        "ZIM": "Verify the CRM feature, edition, profile or sandbox behavior used by this module. Examples and thresholds are proposed lab rules.",
    }
    lesson_text = lesson_text.replace(boilerplate, guidance[course["id"]])
    lesson = markdown_html(lesson_text)
    key = markdown_html(key_path.read_text(encoding="utf-8"))
    number = module["id"]
    deps = ", ".join(module.get("depends_on", [])) or "Course entry module"
    outcomes = "".join(f"<li>{esc(x)}</li>" for x in module["outcomes"])
    checks = "".join(f"<li>{esc(x)}</li>" for x in module["acceptance_checks"])
    topics = "".join(f"<li>{esc(x)}</li>" for x in module["topics"])
    code_html = ""
    if course["id"] == "ZDV" and number in {"ZDV-M03", "ZDV-M08"}:
        code_name = "normalize_requests.deluge" if number == "ZDV-M03" else "create_training_lead.deluge"
        code_path = SOURCE / "materials" / "code_examples" / code_name
        if code_path.exists():
            safety = "Review the synthetic inputs and expected results. This starter has not been executed in a connected Zoho editor." if number == "ZDV-M03" else "External write is disabled by default. Do not enable it before confirming the training account, connection, field names and approval. It has not been executed in a connected Zoho editor."
            code_html = f'<details class="code-example"><summary>Open Deluge teaching example · {esc(code_name)}</summary><p>{esc(safety)}</p><pre><code>{esc(code_path.read_text(encoding="utf-8"))}</code></pre></details>'
    return f'''<article class="module" id="{esc(number)}" data-search="{esc(module['title']+' '+' '.join(module['topics'])+' '+module['lab'])}">
      <header class="module-head"><div class="module-code">{esc(number)}</div><div><p class="eyebrow">{esc(module['live_hours'])} FACILITATED HOURS · {esc(module['practice_hours'])} PRACTICE HOURS</p><h2>{esc(module['title'])}</h2><p class="muted">Builds on: {esc(deps)}</p></div></header>
      <div class="outcomes"><strong>By the end, learners can</strong><ul>{outcomes}</ul></div>
      <h3>Topics to teach</h3><ul class="topics">{topics}</ul>
      <div class="lesson-content">{lesson}</div>{code_html}
      <section class="module-check"><h3>Review against the module outcomes</h3><ul>{checks}</ul><p><strong>Evidence to collect:</strong> {esc(module['evidence'])}</p></section>
      <details class="trainer-key"><summary>Trainer answer guide and review notes</summary><div>{key}</div></details>
      <p class="source-line"><strong>Lesson source:</strong> {esc(lesson_path.name)} · <strong>Trainer key:</strong> {esc(key_path.name)}. Use the source links in the lesson to confirm product behavior before a live demonstration.</p>
      <label class="prepared"><input type="checkbox" data-module="{esc(number)}"> Mark trainer preparation complete</label>
    </article>'''


def course_page(course: dict) -> str:
    course_id = course["id"]
    modules = course["modules"]
    nav = "".join(f'<a href="#{esc(m["id"])}"><span>{esc(m["id"].split("-")[-1])}</span>{esc(m["title"])}</a>' for m in modules)
    cards = "".join(f'<div class="fact"><strong>{esc(label)}</strong><span>{esc(value)}</span></div>' for label, value in [
        ("Audience", course["audience"]),
        ("Entry requirements", course["prerequisites"]),
        ("Course outcome", course["outcome"]),
        ("Class environment", course["tools"]),
        ("Duration", f"{course['weeks']} weeks · {course['total_hours']} hours total"),
        ("Time split", f"{course['live_hours']} facilitated · {course['practice_hours']} independent practice hours"),
    ])
    weights = "".join(f"<li><strong>{esc(k.replace('_',' ').title())}:</strong> {esc(v)}%</li>" for k, v in course["assessment_weights"].items())
    tests = "".join(f"<li>{esc(item.strip())}</li>" for item in course["tests"].split(";") if item.strip())
    deliverables = "".join(f"<li>{esc(item.strip())}</li>" for item in re.split(r",\s*", course["deliverables"]) if item.strip())
    sources = []
    for sid in course.get("sources", []):
        title, url, status = source_info(sid)
        if url:
            sources.append(f'<li><a href="{esc(url)}" target="_blank" rel="noopener">{esc(title)}</a> <span class="muted">({esc(sid)} · {esc(status)})</span></li>')
        else:
            sources.append(f'<li><strong>{esc(title)}</strong> <span class="muted">({esc(sid)} · {esc(status)})</span></li>')
    asset_links = "".join(f'<li><a href="resources/{esc(path)}" download>{esc(Path(path).name)}</a></li>' for path in COURSE_ASSETS[course_id])
    lesson_html = "\n".join(module_html(course, m) for m in modules)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(course['title'])} | Wooplix Academy Trainer Guide</title>
<style>
:root{{--ink:#1c303a;--muted:#526973;--blue:#096b9b;--teal:#16878a;--red:#c52c40;--line:#dbe4e7;--paper:#fff;--canvas:#f3f6f7;--pale:#eaf5f4}}*{{box-sizing:border-box}}body{{margin:0;background:var(--canvas);color:var(--ink);font:16px/1.68 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}.bar{{position:sticky;top:0;z-index:3;background:white;border-bottom:1px solid var(--line);padding:11px 20px;display:flex;justify-content:space-between;gap:12px;align-items:center}}.brand{{font-weight:800;letter-spacing:.08em;color:var(--blue)}}.brand b{{color:var(--red)}}.brand-badge{{height:32px;max-width:210px;object-fit:contain;vertical-align:middle;margin-right:9px}}.tools{{display:flex;gap:8px;align-items:center}}input[type=search]{{border:1px solid var(--line);border-radius:8px;padding:9px 12px;min-width:230px;font:inherit}}button{{border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:8px;padding:9px 12px;font:inherit;cursor:pointer}}.wrap{{max-width:1280px;margin:24px auto;padding:0 20px;display:grid;grid-template-columns:280px minmax(0,900px);gap:24px;align-items:start}}nav{{position:sticky;top:67px;max-height:calc(100vh - 84px);overflow:auto;background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px}}nav h2{{font-size:.85rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);padding:4px 9px}}nav a{{display:flex;gap:9px;padding:8px 9px;text-decoration:none;color:var(--ink);font-size:.88rem;line-height:1.35;border-radius:7px}}nav a:hover{{background:var(--pale)}}nav span{{color:var(--teal);font-weight:800}}main{{min-width:0}}.cover,.overview,.module,.references{{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:clamp(20px,4vw,38px);margin-bottom:18px;box-shadow:0 8px 25px #102b3b0a}}.cover{{border-top:5px solid var(--teal)}}.eyebrow{{font-size:.74rem;letter-spacing:.12em;font-weight:800;color:var(--blue);text-transform:uppercase;margin:0 0 7px}}h1{{font-size:clamp(2rem,5vw,3.3rem);line-height:1.08;letter-spacing:-.035em;margin:4px 0 15px}}h2{{font-size:clamp(1.5rem,3vw,2.15rem);line-height:1.2;margin:3px 0 8px}}h3{{font-size:1.14rem;line-height:1.35;margin:24px 0 8px}}h4{{font-size:1rem;margin:20px 0 7px}}.muted,.cover p{{color:var(--muted)}}.summary-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:20px 0}}.fact{{padding:12px 14px;border:1px solid var(--line);border-radius:10px;background:#fcfdfd}}.fact strong{{display:block;color:var(--blue);font-size:.8rem;text-transform:uppercase;letter-spacing:.05em}}.fact span{{display:block;margin-top:3px}}.module-head{{display:grid;grid-template-columns:62px 1fr;gap:14px;align-items:start}}.module-code{{font-size:1.15rem;font-weight:800;color:var(--teal);padding-top:9px}}.outcomes,.module-check{{background:#f4f9f9;border:1px solid var(--line);border-radius:11px;padding:13px 17px;margin:20px 0}}.outcomes ul,.module-check ul{{margin:6px 0 0;padding-left:21px}}ul,ol{{padding-left:1.35rem}}li{{margin:4px 0}}.lesson-content h2{{font-size:1.36rem;margin-top:27px}}.lesson-content h3{{font-size:1.1rem}}.lesson-content p{{margin:9px 0 14px}}code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#f1f4f5;padding:1px 4px;border-radius:4px}}pre{{overflow:auto;background:#172b35;color:#f5f8f9;padding:14px;border-radius:10px}}blockquote{{border-left:3px solid var(--teal);padding-left:14px;color:var(--muted)}}.trainer-key{{border:1px solid #ead8dc;border-radius:11px;padding:0 15px;background:#fffafa;margin:20px 0}}.trainer-key summary{{padding:13px 0;cursor:pointer;font-weight:750;color:#9f2f45}}.trainer-key[open]{{padding-bottom:14px}}.source-line{{font-size:.85rem;color:var(--muted);border-top:1px solid var(--line);padding-top:12px}}.prepared{{display:flex;gap:9px;align-items:center;color:var(--muted);font-size:.88rem}}.prepared input{{accent-color:var(--teal);width:17px;height:17px}}.hidden{{display:none!important}}.references a{{color:var(--blue)}}.references li{{padding:4px 0}}.notice{{border-left:4px solid var(--teal);padding:11px 15px;background:#eff8f7;margin:20px 0}}footer{{text-align:center;color:var(--muted);font-size:.83rem;padding:16px}}@media(max-width:900px){{.wrap{{grid-template-columns:1fr}}nav{{position:static;max-height:270px;display:flex;flex-wrap:wrap;align-content:start}}nav h2{{width:100%}}nav a{{width:49%}}}}@media(max-width:600px){{.wrap{{padding:0 10px;margin:12px auto;gap:12px}}.bar{{padding:9px 11px}}.tools{{flex-wrap:wrap;justify-content:end}}input[type=search]{{min-width:120px;width:40vw}}button{{padding:7px}}.summary-grid{{grid-template-columns:1fr}}nav a{{width:100%}}}}@media print{{body{{background:#fff;font-size:10.5pt}}.bar,nav,.prepared{{display:none!important}}.wrap{{display:block;margin:0;padding:0}}.cover,.overview,.module,.references{{box-shadow:none;border:0;border-radius:0;margin:0;padding:12mm;break-after:page}}.module{{break-before:page}}.trainer-key:not([open])>*:not(summary){{display:block!important}}.trainer-key>summary{{list-style:none}}a{{color:inherit;text-decoration:none}}}}
</style></head><body><header class="bar"><div class="brand"><img class="brand-badge" src="wooplix_partner_badge.png" alt="Wooplix authorized partner and NASSCOM member"> · {esc(course_id)}</div><div class="tools"><input id="search" type="search" placeholder="Find a module or topic"><button id="expand" type="button">Open trainer keys</button><button onclick="window.print()" type="button">Print</button></div></header>
<div class="wrap"><nav><h2>{len(modules)} modules</h2>{nav}</nav><main>
<section class="cover"><p class="eyebrow">TRAINER GUIDE · DRAFT FOR TEAM REVIEW</p><h1>{esc(course['title'])}</h1><p>{esc(course['outcome'])}</p><div class="summary-grid">{cards}</div><div class="notice"><strong>Trainer note.</strong> Course examples and test values are synthetic teaching material. Use current official documentation and the actual training organization for product steps; distinguish mock results from observed results. Do not claim vendor certification, employment or client outcomes.</div><p><strong>Capstone:</strong> {esc(course['capstone'])}</p></section>
<section class="overview"><p class="eyebrow">ASSESSMENT AND PROJECT</p><h2>What learners build</h2><p>{esc(course['deliverables'])}</p><h3>Capstone scenarios to demonstrate</h3><ul>{tests}</ul><h3>Assessment weighting</h3><ul>{weights}</ul><p class="muted">The syllabus contains proposed completion rules. Confirm current grading, attendance, resubmission and credential wording with the academic lead before enrollment.</p><h3>How to use the trainer guide</h3><p>Each module contains the authored lesson plan followed by its trainer key. Use the linked module navigation, search, and print controls. Check the stated prerequisites and time budget; retain one portfolio of evidence through the capstone.</p></section>
<section class="overview"><p class="eyebrow">CLASS MATERIALS</p><h2>Download synthetic worksheets and datasets</h2><p>These files support the guided labs. They contain synthetic training material and should not be treated as live-system import files.</p><ul>{asset_links}</ul></section>
{lesson_html}
<section class="references"><p class="eyebrow">SOURCE NOTES</p><h2>Official references used by these modules</h2><p>The lesson source records a reference ID for each product or AI claim. Check the cited pages again before teaching, especially where editions, API versions, event support, account access or usage limits can change.</p><ul>{''.join(sources)}</ul><p class="muted">Source status and review date are recorded in the course workspace knowledge manifest. Trainer rehearsal is required before a live product demonstration.</p></section>
<footer>Wooplix Academy · {esc(course_id)} trainer guide · Draft for trainer and academic review</footer></main></div><script>
const q=document.getElementById('search'),mods=[...document.querySelectorAll('.module')],links=[...document.querySelectorAll('nav a')];q.addEventListener('input',()=>{{const s=q.value.toLowerCase().trim();mods.forEach((m,i)=>{{let show=!s||m.innerText.toLowerCase().includes(s);m.classList.toggle('hidden',!show);links[i].classList.toggle('hidden',!show)}})}});document.getElementById('expand').addEventListener('click',e=>{{const ds=[...document.querySelectorAll('.trainer-key')],open=ds.some(d=>!d.open);ds.forEach(d=>d.open=open);e.currentTarget.textContent=open?'Close trainer keys':'Open trainer keys'}});const marks=[...document.querySelectorAll('[data-module]')],key='wooplix_{course_id}_trainer_prep';try{{const saved=JSON.parse(localStorage.getItem(key)||'[]');marks.forEach(x=>x.checked=saved.includes(x.dataset.module))}}catch{{}}marks.forEach(x=>x.addEventListener('change',()=>{{try{{localStorage.setItem(key,JSON.stringify(marks.filter(y=>y.checked).map(y=>y.dataset.module)))}}catch{{}}}}));
</script></body></html>'''


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    RESOURCES.mkdir(exist_ok=True)
    for folder in ["datasets", "worksheets", "code_examples"]:
        src = SOURCE / "materials" / folder
        dst = RESOURCES / folder
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    shutil.copy2(SOURCE / "materials" / "Practical_Assessment_Rubric.md", RESOURCES / "Practical_Assessment_Rubric.md")
    import csv
    bank_path = SOURCE / "materials" / "assessment_bank_v2.csv"
    with bank_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for course_id in COURSE_IDS:
        selected = [row for row in rows if row["module_id"].startswith(course_id + "-")]
        with (RESOURCES / f"assessment_{course_id}.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader(); writer.writerows(selected)
    built = []
    for course_id in COURSE_IDS:
        course = PROGRAMS[course_id]
        filename = f"{course_id}_{re.sub(r'[^a-z0-9]+','_',course['title'].lower()).strip('_')}_Trainer_Guide.html"
        (HERE / filename).write_text(course_page(course), encoding="utf-8")
        built.append((course, filename))
    cards = "".join(f'<a class="course" href="{esc(filename)}"><span>{esc(course["id"])}</span><h2>{esc(course["title"])}</h2><p>{esc(course["audience"])}</p><strong>{len(course["modules"])} modules · {course["total_hours"]} hours</strong></a>' for course, filename in built)
    (HERE / "index.html").write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Wooplix Academy · Trainer Guides 2–5</title><style>:root{{--ink:#19313d;--muted:#506773;--teal:#16878a;--blue:#096b9b;--red:#c52c40;--line:#dbe4e7;--pale:#f3f7f8}}*{{box-sizing:border-box}}body{{margin:0;background:var(--pale);color:var(--ink);font:16px/1.6 system-ui,sans-serif}}.brand-badge{{height:36px;max-width:250px;object-fit:contain;vertical-align:middle;margin-right:10px}}header{{background:#fff;border-bottom:1px solid var(--line);padding:26px max(calc((100vw - 1020px)/2),22px)}}.brand{{font-weight:850;letter-spacing:.09em;color:var(--blue)}}.brand b{{color:var(--red)}}main{{max-width:1020px;margin:40px auto;padding:0 22px}}h1{{font-size:clamp(2rem,5vw,3.3rem);line-height:1.12;margin:10px 0}}.intro{{color:var(--muted);max-width:740px}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:28px}}.course{{display:block;background:#fff;border:1px solid var(--line);border-top:4px solid var(--teal);border-radius:14px;padding:23px;color:inherit;text-decoration:none}}.course:hover{{transform:translateY(-2px);box-shadow:0 12px 26px #152d380f}}.course span{{font-size:.78rem;color:var(--teal);font-weight:800;letter-spacing:.1em}}.course h2{{font-size:1.35rem;line-height:1.25;margin:8px 0}}.course p{{color:var(--muted)}}.course strong{{color:var(--blue)}}.note{{margin-top:27px;padding:15px 18px;border-left:4px solid var(--teal);background:#eaf5f4}}footer{{text-align:center;color:var(--muted);margin:40px}}@media(max-width:650px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><header><div class="brand"><img class="brand-badge" src="wooplix_partner_badge.png" alt="Wooplix authorized partner and NASSCOM member"> ACADEMY</div></header><main><p class="brand">TRAINER CONTENT · DRAFTS</p><h1>Course teaching guides</h1><p class="intro">Open a course to view its modules, classroom materials and trainer answer guidance. The guides are built from the current local syllabus, lesson plans and trainer keys.</p><div class="grid">{cards}</div><p class="note"><strong>Before delivery:</strong> Confirm the account edition, rehearse exact product steps, verify source links and set any course pass or attendance rules with the academic lead.</p></main><footer>Wooplix Academy · Courses 2–5 · Local draft library</footer></body></html>''', encoding="utf-8")
    readme = """# Wooplix Academy trainer guides for Courses 2–5

Open the four HTML guides in a current browser. Each is self-contained and works offline; external official source links need internet. The guides are assembled from the version 0.2 catalog, all 36 authored lesson plans and their matching trainer answer keys. Course hours and module order follow the catalog.

`resources/datasets` and `resources/worksheets` contain the synthetic class materials. Do not use them as production imports. For edits, update the source syllabus, lesson plan or trainer key in `outputs/Wooplix_Academy_Workspace_V2`, then run `python3 build_guides.py` to refresh the HTML files.

All files are drafts for trainer and academic review. Product steps and feature access must be rehearsed in the chosen Zoho edition. This pack does not claim official vendor certification or client outcomes.

## Source impact

This build creates separate trainer-facing views for ZDV, AAB, CAW and ZIM. It does not change the source syllabi, lesson plans, trainer keys, catalog hours, assessment policy or public website copy. Reference identifiers and review dates remain in the source files and knowledge manifest.
"""
    (HERE / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
