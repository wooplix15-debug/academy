# Draft · Vivek Pandey website feedback impact report

Prepared for the website feedback pass on 14 October 2026.

## User-visible changes

- The existing homepage sections were retained; no route or new top-level section was added.
- The hero now leads with “Make AI useful in the work that matters,” adds a concise positioning line and uses the existing Zoholics India photograph as the primary visual.
- The existing services section no longer uses “Three ways to move forward.” It now positions AI Consulting around Generative AI, Agentic AI and business automation, while keeping Speaking and AI Learning links working.
- The existing Speaking page has clearer positioning and two “Book Vivek Pandey” calls to action.
- The existing Journey section now combines practical AI learning language with a concise career timeline and an authentic event photograph.
- The existing Experience section now includes an evidence-led credibility image strip with event, NASSCOM and half-marathon photographs.
- The existing Contact page now captures event type, event date, location, expected audience size and speaking topic when the enquiry topic is Speaking.

## Affected files

- `home-react/src/App.jsx` — homepage copy, imagery and existing-section layout.
- `home-react/src/BrandPages.jsx` — consulting, speaking and contact copy/form fields.
- `home-react/src/enquiryEmail.js` — speaking enquiry email body fields.
- `home-react/src/styles.css` — final responsive typography, spacing, image and credibility treatments.
- `home-react/index.html` and `scripts/prerender-home.mjs` — updated homepage description metadata.
- `public/assets/personal-brand/life-at-wooplix-05.jpg`, `life-at-wooplix-06.jpg`, `life-at-wooplix-09.jpg`, `life-at-wooplix-24.jpg` — downloaded from the public Wooplix Life at Wooplix gallery for draft use.

## Accuracy and review notes

- The downloaded photographs are first-party hosted images, but public hosting does not independently prove photographer rights, event-brand permissions or consent from every identifiable attendee. Confirm clearance with the owner before publishing.
- Captions avoid unsupported awards, outcomes or accreditation claims. The half-marathon image is presented as a lifestyle photograph rather than a quantified achievement.
- The current 19-year, Zoholics India and Wooplix experience wording was preserved from the existing site rather than expanded with new claims.
- The website still uses a local `mailto:wooplix15@gmail.com` flow. It opens a prefilled draft for the visitor’s email app; it does not provide server-side delivery, storage, CRM capture or automatic confirmation. Confirm the mailbox and test it in the intended production environment before launch.

## Content-owner checklist

- [ ] Confirm photo permissions and preferred captions.
- [ ] Confirm the final hero photograph and whether the Zoholics date should remain in public copy.
- [ ] Confirm the receiving mailbox and test a speaking enquiry end to end.
- [ ] Review the event form wording, required fields and privacy notice before publishing.
- [ ] Have the owner and content reviewer approve the final public copy.
