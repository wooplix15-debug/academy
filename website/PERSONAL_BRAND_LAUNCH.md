# Vivek Pandey website and Academy

The main website presents Vivek Pandey’s consulting, speaking and education work. Academy is its education page, with five programmes, syllabi and Course Books.

## Public pages

| Page | Route |
| --- | --- |
| Home | `/` |
| AI Consulting | `/ai-consulting` |
| Speaking | `/ai-speaking` |
| Academy | `/academy` |
| Contact | `/contact` |

The Academy page contains the five programmes, syllabi and Course Books. Course books and syllabi remain available as linked learning materials, not as extra top-level pages. `/ai-courses` redirects to `/academy`; `/about` redirects to the experience section on Home; `/enquire` redirects to Contact.

The temporary deployment is academy-tools-jade.vercel.app. Connecting vivekpandey.ai requires access to its domain/DNS and adding the domain to the Vercel project. This change does not configure that domain or publish to wooplix.com.

## Contact and session requests

The owner supplied `wooplix15@gmail.com` as the recipient. The contact page asks only for name, phone number, email and topic. Consulting links may prefill the requested 30-minute/60-minute option in the email draft. It opens an email draft; the visitor reviews and sends it through their own email app. There is no server submission, calendar reservation, payment or automatic confirmation. Form data is not stored on the site.

When a booking provider is chosen, replace the session request links with the owner's real booking links. Confirm fees, time-zone settings, availability, reminders and cancellation terms before offering paid booking.

## Editing

- Main page: `public/index.html`
- Main styling: `public/personal-brand.css`
- Shared vector icons: `public/assets/brand-icons.svg` (arrows, service symbols and session clocks)
- Contact page and behaviour: `public/contact.html`, `public/personal-brand.js`
- Service page content: `website/personal-brand-pages.json`
- Page builder: `python3 tools/build_personal_brand_pages.py` (rebuilds Consulting and Speaking pages and aligns Home navigation)
- Word document builder: `tools/build_personal_brand_document.py` (run using the bundled document Python runtime)
- Academy page and styling: `public/academy.html`, `public/academy-home.css`
- Academy library generator: `tools/sync_public_syllabi.py`
- Route maintenance after rebuilding older course templates: `python3 tools/migrate_academy_routes.py`

The 19-year experience statement comes from the owner's meeting summary. No client logos, testimonials, speaker engagements, accreditation, revenue figures or measured AI savings were invented. The AI Lab and multi-agent delivery system are labelled as development directions.

All 84 chapter HTML pages and student Markdown downloads retain their content. Chapter-page changes are confined to navigation destinations so Academy links return to `/academy` and enquiry links stay on this website. Course source materials and assessment rules are unaffected.

The personal website uses shared SVG icons, rounded button badges, distinct service cards and numbered delivery stages. Hover motion respects the visitor's reduced-motion preference. This visual styling is scoped to the main website and enquiry page; the Academy keeps its existing styling.

## Five-page structure

The top navigation is Home, Consulting, Speaking, Academy and Contact. Academy contains the five programmes and their Course Books. Legacy About and Courses URLs redirect to the relevant pages.

The editable website brief is saved separately from the public site at `../Vivek_Pandey_Website/Vivek_Pandey_Website_Content_and_Plan.docx`. It contains the website direction, the five-page structure and its live addresses. The Word file and its render previews are not published as website assets.
