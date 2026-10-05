# Wooplix Academy · curriculum and teaching workspace

This repository contains the Wooplix Academy public website, editable curriculum workspace, a local content-drafting agent, and offline trainer guides for all five Academy courses. Course content, hours, assessment rules, references and public claims need review by the Wooplix team before delivery or enrollment.

## Start here

- Open [`Wooplix_Learning_Studio.html`](Wooplix_Learning_Studio.html) for the four detailed practitioner and workshop programs.
- Open [`teaching-pack/START_HERE.html`](teaching-pack/START_HERE.html) for the five course teaching guides, including Zoho Business Process & Corporate Automation.
- Read [`Wooplix_Academy_Practical_Teaching_Guide.md`](Wooplix_Academy_Practical_Teaching_Guide.md) for how to deliver the lessons.
- Read [`team/V2_REVIEW_AND_CHANGES.md`](team/V2_REVIEW_AND_CHANGES.md) and [`teaching-pack/CONTENT_REVIEW.md`](teaching-pack/CONTENT_REVIEW.md) for current review status and open decisions.

The Academy website is served from the repository root and is configured for Vercel. See [`website/LAUNCH.md`](website/LAUNCH.md) for deployment and editing instructions. Offline trainer guides are available by opening the HTML files in a browser.

## What is in this repository

| Area | Contents |
|---|---|
| `curriculum/`, `data/` | Four course syllabi, learning outcomes, hours and module sequence |
| `materials/lesson_plans/`, `materials/trainer_keys/` | 36 practical lessons and matching trainer guidance |
| `materials/` | Assessment banks, worksheets, synthetic datasets, diagrams, worked examples and Deluge starters |
| `Wooplix_Learning_Studio.html` | Offline learning studio for Courses 2–5 |
| `agent/` | Optional local content-drafting runner with review and approval steps |
| `practice/` | Local synthetic exercises and expected results |
| `operations/`, `team/` | Draft policies, delivery checklists, review registers and team workflow |
| `index.html`, `styles.css`, `script.js` | Public-facing Academy website, designed for static Vercel hosting |
| `website/` | Website editing and launch notes plus draft source copy |
| `teaching-pack/` | Five branded, printable/offline HTML trainer guides and course-specific resources |

The four programs in the editable workspace total 204 hours. Course 1 currently has 18 chapters, but its duration and assessment policy still need owner decisions. Customer-facing course names in the guide pack also need alignment with the approved offer names.

## Edit and rebuild

The editable root workspace is the main source for Courses 2–5. Follow [`AGENTS.md`](AGENTS.md) and [`team/TEAM_WORKFLOW.md`](team/TEAM_WORKFLOW.md) before changing content. Keep examples synthetic unless the owner has approved sanitized company material.

Install the document-build dependencies:

```bash
python3 -m pip install -r tools/requirements.txt
```

Rebuild the practical guide, PDF/Word guide, and learning studio:

```bash
python3 tools/rebuild_learning_materials.py
```

Rebuild the separate course guides for Courses 2–5:

```bash
python3 teaching-pack/Courses_02_to_05/build_guides.py
```

Rebuild the Course 1 guide:

```bash
cd teaching-pack/Course_01_Zoho_Business_Process_Automation
python3 build_course1.py
```

The scripts use local content and create files in this repository. Product steps, API examples, account editions and vendor limits still need trainer verification in the selected training organization.

## Optional content agent

The agent drafts Markdown for human review; it does not connect to Zoho or publish to a website. Use Python 3.10 or newer. First run its offline check:

```bash
python3 agent/academy_agent.py doctor
```

Live drafting is optional and uses billable model API calls. Set `OPENAI_API_KEY` and `WOOPLIX_MODEL` in your shell environment only. Never add keys, real client data, generated drafts or local approval records to Git.

## Draft and source policy

Use synthetic records in examples. Do not claim official Zoho certification, employment, client results, approved savings, prices or trainer experience without documented owner approval. Keep expected results distinct from observed results. No license file is included; ask Wooplix before reusing these materials outside the team.

See [`VERIFICATION_V2.md`](VERIFICATION_V2.md) for the checks documented for this workspace and their limits.

## Student Course Book

Course 1 has a public student reader at `/course-book/course-01/`. Course 4, Corporate AI & Automation Opportunity Workshop, has a public reader at `/course-book/course-04/` with all ten chapters. Course 4 source chapters are in `materials/student_books/course_04/`; rebuild them with `python3 tools/build_student_coursebook_04.py`. Only student-facing chapter text is rendered; source metadata is excluded. Both readers include section menus, explained solutions and print/save as PDF.

### Course 5 student book

All 16 chapters are available at `/course-book/course-05`. Edit the separate files in `materials/student_books/course_05/`, then run `python3 tools/sync_public_syllabi.py` and `python3 tools/build_student_coursebook_05.py`. Student downloads and the three local Python reference programs are generated with the reader. The book preserves fictional Evergreen inputs and separates paper/local examples from actual Zoho execution.
