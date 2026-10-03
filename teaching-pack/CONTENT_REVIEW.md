# Wooplix Academy teaching pack · content audit

**Review date:** 3 October 2026  
**Scope:** All 145 files in the extracted pack: five HTML guides, both build scripts, four syllabi, the course catalog, 36 lesson plans, 36 trainer keys, 72 assessment items, resource notes, worksheets, datasets, logo/badge and the package instructions.

## Guide update in this version

The four HTML guides for Courses 2–5 now present their existing lesson plans in a Course 1-style numbered chapter format. Each module brings the concept, example, teaching sequence, lab steps, expected result, failure/recovery, independent practice, learner reflection, sources and trainer key into a consistent teaching order. The diagrams are built from the actual lab steps in each lesson. The syllabus order and underlying lesson content remain editable in `source_workspace`.

## Overall assessment

This is a useful **trainer draft library**. It has a clear progression from requirements to design, implementation, negative-case handling, evidence and handover. The course 2–5 lessons usually include a concrete case, a lab, a failure test, a recovery action, a learner reflection and trainer guidance. The synthetic CRM migration file matches its stated classification: 50 records divide into 42 accepted, 5 rejected and 3 duplicate exclusions.

It is **not ready to give to prospective learners as the final course promise**. It is trainer-facing, some course terms remain unapproved, and the assessment guidance needs more specific marking detail. Keep the distinction between proposed teaching content and verified Wooplix delivery facts.

## High-priority improvements

### 1. Align the offer names

The pack’s course 2–5 names are not the five course names previously supplied for the offer/master sheet. The pack currently calls them “Zoho Creator Deluge and Integration Developer,” “AI and Agentic Business Automation Builder,” “Corporate AI and Automation Discovery Workshop,” and “Zoho CRM Implementation Practitioner.” Before sharing, choose the approved customer-facing names and use them consistently on the cover, start page, master sheet and course guide. If these are deliberate sub-program names, show the relationship to the offer title clearly.

### 2. Finish Course 1’s delivery and assessment design

Course 1 has 18 detailed chapters, but no total hours, weekly sequence, independent practice budget, entry requirements, final assessment weighting, pass threshold or completion rule. This makes it difficult to price, schedule or compare with the other courses. Set these with the academic lead rather than inferring hours from the chapter count.

### 3. Replace repeated trainer-key boilerplate with module-specific marking guidance

All 36 trainer keys repeat the same “Common misconception” and independent-task review paragraphs. They tell trainers to distinguish rules from features and simulated from live evidence, but do not say what a strong, partial or failing response looks like for that module. Keep shared safety rules once in the rubric; use each key for specific acceptable alternatives, required evidence, likely errors, follow-up questions and scoring examples.

### 4. Make assessments usable as assessments

There are two 5-point items per module (72 in total): one oral prompt and one failure/recovery scenario. This is a good review prompt set, but too small to function by itself as a stable quiz or measure broad coverage. Several scenario rows copy the lesson’s expected result and negative case into the answer-guidance field, which mixes the marking standard with the scenario. Expand the item pool, add a distinct scoring rubric and accepted answer criteria, vary scenario inputs, and create a trainer-only answer file. Keep learner question sheets separate from answer guidance.

### 5. Produce separate trainer and learner editions

The guides include expandable trainer keys. Assessment CSV files also contain answer guidance. A learner who opens the package can reveal the answers. Keep the current guides as trainer editions and create learner editions with keys and answer columns removed, clear assignment instructions, blank templates and the approved course terms.

### 6. Set clear routes for the AI Builder course

The syllabus allows a coded route and a supervised workflow/no-code route, but the weekly plan does not yet make the alternatives, prerequisites, equivalent outcomes or separate evidence explicit. Add an entry diagnostic, a route selection point, route-specific labs and a common capstone rubric. State what depth differs between the routes so learners know what they are buying.

### 7. Add a worked example and instructions to the templates

The CSV worksheets are intentionally blank templates. Add one clearly marked fictional sample row and a short “how to complete this” note for each high-use template. This is especially useful for UAT, access testing, migration reconciliation, change requests and baseline/pilot measurement. Keep the actual-result fields blank in the learner copy.

### 8. Expand and label the AI knowledge/evaluation fixtures

The included knowledge set has six records, which is enough to demonstrate basic eligibility and abstention but too small to teach retrieval quality across paraphrases, near matches, conflicting versions, stale sources and permission boundaries in depth. Add a larger synthetic corpus and explain which cases it covers. Keep model-generated actuals blank until a trainer runs them; a designed test case is not an observed result.

### 9. Clarify boundaries between overlapping Zoho courses

Course 1 covers broad Zoho operations, CRM setup, migration, automation, reporting, Books, Desk, People and Flow. The CRM Practitioner course separately covers CRM implementation, migration, workflows, permissions, reporting, UAT and handover. Add a one-page course map that tells a buyer which course to choose and which topics are introductory, repeated for practice, or advanced. This will reduce duplicated teaching and unclear course choice.

### 10. Add a delivery-ready workshop closeout

The corporate workshop has a useful baseline-to-pilot structure. Make its final output explicit: sponsor and process owner, baseline definition, data/access dependencies, pilot scope, success and stop criteria, decision date and implementation handoff owner. Keep savings and business impact framed as hypotheses until measured.

## Technical and source handling

- The Deluge material appropriately emphasizes API versions, scopes, connections, quotas and training environments. Keep credentials in named Connections. Zoho continues to document the `invokeUrl` task and recommends Connections for authentication; its release notes state that embedded URL credentials were deprecated in 2025. See [Zoho invokeUrl task documentation](https://www.zoho.com/deluge/help/webhook/invokeurl-api-task.html) and [Zoho Deluge release notes](https://www.zoho.com/deluge/help/release-notes.html).
- The CRM record-creation example is disabled by default and uses synthetic data. It is a reading/rehearsal starter, not an executed integration. Trainers should verify field API names, required fields, scopes, connection behavior and the actual response in a training organization before live demonstration.
- The 50-row CRM fixture’s classification matches its stated lab rule, but the accepted set is not a ready-to-import file. Make the lab policy (including duplicate definition and first-valid-row rule) visible on the worksheet and teach target import results separately from offline validation.
- The AI lesson set is careful about permission filtering, prompt injection, abstention, human review, bounded tools, evaluation and observed-vs-estimated results. Preserve these as required learning outcomes. Add a worked end-to-end example so they are not only safety statements.
- Recheck all product and AI source links before each cohort. Add a “checked on / trainer observed on / edition” line to each live product demonstration. Avoid presenting internal Wooplix decisions, proposed examples or synthetic numbers as official product behavior.

## Strengths to preserve

- The teaching flow asks learners to predict, build, break, recover, document and explain.
- Negative and recovery cases appear across all 36 lessons, not just as a final checklist.
- The ZDV examples distinguish a stable business key from a delivery event ID and treat a timeout as an unknown outcome until reconciled.
- The ZIM migration lesson distinguishes offline accepted rows from actual CRM import success; the fixture reconciles to 50 = 42 + 5 + 3.
- The AAB content separates structured output validity from factual support and makes publication a separate reviewed action.
- The CAW lessons measure review and correction time alongside generation time and do not promise savings.
- The rubric has critical gates for access, data exposure and unintended writes, and calls for trainer calibration.

## Recommended order of work

1. Approve customer-facing names and Course 1 duration, audience, prerequisites and completion rules.
2. Agree assessment policy and develop the separate learner edition.
3. Rewrite trainer keys around module-specific scoring and add worked exemplars.
4. Clarify AI route options and the Course 1 vs CRM Practitioner pathway.
5. Add examples to templates, broaden the AI fixture and rehearse the technical labs in the actual editions.
6. Ask a trainer and one representative learner to review a complete course end to end; record gaps and update the next version.

The package is an editable internal draft. Do not describe proposed hours, thresholds, certificates, savings, integrations or client outcomes as approved Wooplix commitments until the responsible owner confirms them.
