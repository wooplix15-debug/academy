import { readFile, writeFile, rm } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
const htmlPath = resolve(root, 'dist/index.html');
const serverPath = resolve(root, 'dist/server/entry-server.js');
const { render } = await import(pathToFileURL(serverPath).href);
const html = await readFile(htmlPath, 'utf8');
const content = render();

if (!html.includes('<div id="root"></div>')) {
  throw new Error('Could not find the React root in the generated homepage.');
}

await writeFile(htmlPath, html.replace('<div id="root"></div>', `<div id="root">${content}</div>`));
await rm(dirname(serverPath), { recursive: true, force: true });
console.log('Pre-rendered the React homepage to static HTML.');
