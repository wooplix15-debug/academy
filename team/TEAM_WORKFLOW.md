# Team Editing Workflow

Choose one shared home for the workspace using your existing team drive or version control. Keep one agreed current copy; the downloaded ZIP itself is a snapshot. No shared drive or external repository has been connected by this task.

The catalog JSON is the source for course IDs, modules, outcomes and hours. The Markdown syllabi, lessons and website copy are editable narrative assets. After changing structured facts, update related copy and log the change. The Word handbook is a readable snapshot and must be refreshed separately; it will not update when a teammate changes JSON.

Assign an author and reviewer for each asset in content_register.csv; use practical_content_register.csv for the 36 revised lessons and their technical and teaching reviewers. Work in a draft or versioned copy. Trainers add their expertise using the actual products, editions and permission cleared examples. The reviewer checks correctness, workload, outcome and assessment alignment. Record the decision in change_log.csv and only then publish the corresponding website or learner asset.

For product changes, attach the current official reference and record the affected edition and review date. For Wooplix examples, record ownership and permission, sanitize confidential information and separate measured outcomes from estimates. Keep active cohort rules stable or document the correction and learner notice.

The AI can expand a lesson, create an assessment, rewrite website copy or propose a corporate adaptation. Supply the relevant asset, audience, time budget and approved sources. It drafts rather than inventing company expertise. Exact UI steps and runnable product code need trainer verification in the real training environment.

Suggested weekly review: the content manager checks the next two scheduled modules, overdue reviews, learner issues and stale technical references. Use agent/quality_checklist.md for an individual asset. Credentials, commercial terms and client publication still require the responsible owner’s decision.

For version 0.2, run tools/rebuild_learning_materials.py to refresh the studio and course overview after catalog or Markdown lesson changes. Maintain visual coaching pages and assessment prose in that builder when teaching rules change, then inspect rendered outputs. Use assessment_bank_v2.csv for the current primary question bank.
