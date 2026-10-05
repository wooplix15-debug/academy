# Course 1 student-book release — 5 October 2026

User requested publication to the live app. Published content: the reviewed Chapter 1 v0.3 student draft, fictional datasets, explained exercises and diagram. Earlier drafts remain outside the public tree. Internal Docs, prompt files, generation traces, source metadata and continuity blocks are not published.

Impacts: adds student-book routes and course links on homepage, syllabus directory and Course 1. Does not change syllabus chapter order, course duration, price or cohort assessment policy. Only Chapter 1 has book content; 17 others clearly say Coming next.

Key review: baseline arithmetic agrees with supplied input, interview/mapping instructions were added, deadline ambiguity was corrected. This version uses six order records; future chapters must continue its case rather than merge older baselines. No live Zoho configuration is claimed.

Build source: materials/student_books/course_01/chapter_01.md. Renderer: tools/build_student_coursebook.py. Dependencies: tools/requirements.txt. Runtime is static HTML/CSS/JS with no AI API or server requirement.


## Course 4 student course book — 5 October 2026

Published the reviewed student chapters C04-CH01 through C04-CH10 at `/course-book/course-04/`, linked from the Course 4 programme page. Course 4 is Corporate AI & Automation Opportunity Workshop; the chapter sequence matches its ten listed syllabus chapters and ends with the Business Automation Pilot Proposal.

Impact: adds ten reader pages and a chapter directory, download/print actions, and a Course Book link on Programme 04. Existing syllabus, hours, assessment rules and Course 1 pages are unchanged. Examples are synthetic; business-case amounts are forecasts, not actual savings. Product editions, licensing and price details remain items to verify for the learner's account and region.

Build source: `materials/student_books/course_04/chapter_01.md` through `chapter_10.md`. Renderer: `tools/build_student_coursebook_04.py`. Output: `public/course-book/course-04/`.
