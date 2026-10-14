import { readFile, writeFile, rm } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
const htmlPath = resolve(root, 'dist/index.html');
const serverPath = resolve(root, 'dist/server/entry-server.js');
const { render } = await import(pathToFileURL(serverPath).href);
const html = await readFile(htmlPath, 'utf8');
const pages = [
  {
    path: '/',
    file: htmlPath,
    title: 'Practical AI for Business | Vivek Pandey',
    description: 'Make AI useful in the work that matters. Vivek Pandey brings practical consulting, speaking and learning to Generative AI, Agentic AI and business automation.',
  },
  {
    path: '/ai-consulting',
    file: resolve(root, 'dist/ai-consulting.html'),
    title: 'AI Consulting | Vivek Pandey',
    description: 'Bring a process, a recurring problem or an implementation idea. Compare practical options and identify a useful first step.',
  },
  {
    path: '/ai-speaking',
    file: resolve(root, 'dist/ai-speaking.html'),
    title: 'AI Speaking and Workshops | Vivek Pandey',
    description: 'Practical AI talks and workshops for conferences, universities, colleges and corporate teams.',
  },
  {
    path: '/contact',
    file: resolve(root, 'dist/contact.html'),
    title: 'Contact Vivek Pandey',
    description: 'Contact Vivek Pandey about AI consulting, speaking or Academy courses.',
  },
];

for (const page of pages) {
  let pageHtml = html;
  const canonical = `https://academy-tools-jade.vercel.app${page.path === '/' ? '/' : page.path}`;
  const jsonLd = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: page.title,
    url: canonical,
    description: page.description,
    about: { '@type': 'Person', name: 'Vivek Pandey', url: 'https://academy-tools-jade.vercel.app/', jobTitle: 'AI Consultant, Speaker and Educator' },
  });
  pageHtml = pageHtml
    .replace(/<title>.*?<\/title>/, `<title>${page.title}</title>`)
    .replace(/<meta name="description" content="[^"]*"\s*\/>/, `<meta name="description" content="${page.description}" />`)
    .replace(/<link rel="canonical" href="[^"]*"\s*\/>/, `<link rel="canonical" href="${canonical}" />`)
    .replace(/<meta property="og:title" content="[^"]*"\s*\/>/, `<meta property="og:title" content="${page.title}" />`)
    .replace(/<meta property="og:description" content="[^"]*"\s*\/>/, `<meta property="og:description" content="${page.description}" />`)
    .replace(/<meta property="og:url" content="[^"]*"\s*\/>/, `<meta property="og:url" content="${canonical}" />`)
    .replace(/<script type="application\/ld\+json">.*?<\/script>/, `<script type="application/ld+json">${jsonLd}</script>`);

  if (!pageHtml.includes('<div id="root"></div>')) {
    throw new Error(`Could not find the React root for ${page.path}.`);
  }

  const content = render(page.path);
  await writeFile(page.file, pageHtml.replace('<div id="root"></div>', `<div id="root">${content}</div>`));
}

await rm(dirname(serverPath), { recursive: true, force: true });
console.log('Pre-rendered the homepage and three personal-brand pages to static HTML.');
