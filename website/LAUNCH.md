# Wooplix Academy website

The public site source lives in `public/`: `index.html`, `styles.css`, `script.js`, and `assets/`. `vercel.json` selects Vercel’s Other framework preset and publishes only `public/`, keeping curriculum work files outside the deployed site. It is a static site; no framework, build command, database, or environment variables are required.

## Publish with Vercel

1. Sign in to Vercel with the Wooplix account that owns the Vercel project.
2. Import `https://github.com/wooplix15-debug/academy` and select the `main` branch.
3. Set the project root to `.` (repository root). The checked-in `vercel.json` selects **Other**, disables a build command, and publishes the `public/` directory.
4. Deploy. Later pushes to `main` will update the production deployment; branches and pull requests can create previews.
5. Add a Wooplix-owned domain in Vercel when ready. The default `*.vercel.app` address is available after the first deployment.

## Before announcing a cohort

The page intentionally leaves pricing, start dates, trainer biographies, fixed duration and enrollment terms out until Wooplix confirms them. Review each course outline with the assigned trainer and update the five programme summaries in `index.html`. The contact button links to Wooplix's existing contact page. Confirm the partner badge and affiliation wording remain current before publishing.

To edit: change the course wording in `public/index.html`, visual styles in `public/styles.css`, and the mobile menu behavior in `public/script.js`. The supplied partner artwork is `public/assets/wooplix-partner-badge.png`.
