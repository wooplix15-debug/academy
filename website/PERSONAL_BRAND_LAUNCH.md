# Vivek Pandey website and Academy

The main website is the independent Vivek Pandey personal brand, organised around AI consulting, speaking and courses. Wooplix Academy is the education section. This replaces the Academy as the root landing page while retaining its design and all existing chapter URLs.

## Public routes

| Route | Purpose |
| --- | --- |
| `/` | Vivek Pandey main website |
| `/about` | Vivek Pandey's experience, approach and areas of interest |
| `/contact` | Consulting, speaking and course enquiries |
| `/ai-consulting` | Consulting scope, examples and session requests |
| `/ai-speaking` | Speaking topics, formats and event enquiries |
| `/ai-courses` | Learning offers and links to all five Course Books |
| `/enquire` | Compatibility redirect to `/contact`, retaining query parameters |
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
- Shared vector icons: `public/assets/brand-icons.svg` (arrows, service symbols and session clocks)
- Contact page and behaviour: `public/contact.html`, `public/personal-brand.js`
- Service page content: `website/personal-brand-pages.json`
- Page builder: `python3 tools/build_personal_brand_pages.py` (rebuilds the five detail pages and Home navigation)
- Word document builder: `tools/build_personal_brand_document.py` (run using the bundled document Python runtime)
- Academy page and styling: `public/academy.html`, `public/academy-home.css`
- Academy library generator: `tools/sync_public_syllabi.py`
- Route maintenance after rebuilding older course templates: `python3 tools/migrate_academy_routes.py`

The 19-year experience statement comes from the owner's meeting summary. No client logos, testimonials, speaker engagements, accreditation, revenue figures or measured AI savings were invented. The AI Lab and multi-agent delivery system are labelled as development directions.

All 84 chapter HTML pages and student Markdown downloads retain their content. Chapter-page changes are confined to navigation destinations so Academy links return to `/academy` and enquiry links stay on this website. Course source materials and assessment rules are unaffected.

The personal website uses shared SVG icons, rounded button badges, distinct service cards and numbered delivery stages. Hover motion respects the visitor's reduced-motion preference. This visual styling is scoped to the main website and enquiry page; the Academy keeps its existing styling.

## Six page website update

Home links to dedicated About, Contact, Consulting, Speaking and Courses pages. Each service page explains its audience, scope and next action. The courses page links directly to all five existing Course Books. There are no changes to Academy styling, student chapters, assessments or commercial terms.

The editable website brief is saved separately from the public site at `../Vivek_Pandey_Website/Vivek_Pandey_Website_Content_and_Plan.docx`. It contains the website direction, content for the six pages and their live addresses. The Word file and its render previews are not published as website assets.
