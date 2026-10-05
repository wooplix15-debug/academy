# Public syllabus update — 5 October 2026

The owner requested that the five linked Google Docs syllabi be published on the GitHub/Vercel website. Public course pages now use their course titles, audience, prerequisites, chapter topics, practice tasks, final project and assessment descriptions.

Chapter counts are 18, 22, 20, 10 and 16. The consulting page replaces its earlier six-part proposed outline with the supplied 16-chapter syllabus. The new public curriculum directory links to each chapter and the master Google Doc. Public chapter links open their corresponding chapter automatically.

Following the owner's visibility review, the homepage also displays every chapter name under its course, directly after the programme cards. The old broad coverage summaries are removed. Home navigation and the hero link jump to the full syllabus section. Course topics and practice tasks are expanded by default, and programme cards state their chapter count.

The captured editable content is `website/doc_syllabi.json`. Internal document URLs and revision IDs are excluded from this repository's current content. Run `python3 tools/sync_public_syllabi.py` after editing this source to rebuild the public pages. Google Docs changes are not automatically synchronized. The builder rejects Google Docs or Drive links in deployed text assets.

The owner's public/private correction removes every Google Docs link and document button from the course and curriculum pages. Public pages retain only course content. Course titles, browser titles and breadcrumbs now match; course hero cards show their specific chapter counts. Tablet navigation uses the mobile menu before it can crowd the header. The desktop syllabus introduction stays visible while readers scroll through chapters.

Existing offline trainer guides, the older four-program catalog, hours and assessment weights are preserved. They are a separate version of the teaching material and have not been expanded or relabeled as the newly published 86 chapters. Trainers should use the linked syllabus when aligning those materials. No enrollment terms or active cohort rules are changed by this website update.

This update publishes the supplied syllabus content. It does not assert that technical labs have been rehearsed in Zoho. Wooplix trainers retain responsibility for product-specific delivery review.
