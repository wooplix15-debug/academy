# Vivek Pandey website and Academy

The main website is the independent Vivek Pandey personal brand, organised around AI consulting, speaking and courses. Wooplix Academy is the education section. This replaces the Academy as the root landing page while retaining its design and all existing chapter URLs.

## Public routes

| Route | Purpose |
| --- | --- |
| `/` | Vivek Pandey main website |
| `/enquire` | Consulting, speaking and course enquiries |
| `/academy` | Preserved Wooplix Academy landing page |
| `/syllabus` | Full Academy syllabus directory |
| `/course-book/course-01` through `/course-book/course-05` | Existing complete student books |

The temporary deployment is academy-tools-jade.vercel.app. Connecting vivekpandey.ai requires access to its domain/DNS and adding the domain to the Vercel project. This change does not configure that domain or publish to wooplix.com.

## Contact and session requests

The owner supplied `wooplix15@gmail.com` as the recipient. The local enquiry page preselects the requested service and 30-minute/60-minute option. It opens an email draft; the visitor reviews and sends it through their own email app. The copy button is a fallback. There is no server submission, calendar reservation, payment or automatic confirmation. Form data is not stored on the site.

When a booking provider is chosen, replace the session request links with the owner's real booking links. Confirm fees, time-zone settings, availability, reminders and cancellation terms before offering paid booking.

## Editing

- Main page: `public/index.html`
- Main styling: `public/personal-brand.css`
- Enquiry page and behaviour: `public/enquire.html`, `public/personal-brand.js`
- Academy page and styling: `public/academy.html`, `public/academy-home.css`
- Academy library generator: `tools/sync_public_syllabi.py`
- Route maintenance after rebuilding older course templates: `python3 tools/migrate_academy_routes.py`

The 19-year experience statement comes from the owner's meeting summary. No client logos, testimonials, speaker engagements, accreditation, revenue figures or measured AI savings were invented. The AI Lab and multi-agent delivery system are labelled as development directions.

All 84 chapter HTML pages and student Markdown downloads retain their content. Chapter-page changes are confined to navigation destinations so Academy links return to `/academy` and enquiry links stay on this website. Course source materials and assessment rules are unaffected.
