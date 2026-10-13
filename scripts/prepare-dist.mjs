import { cp, mkdir, readdir, rm } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
const source = join(root, 'public');
const destination = join(root, 'dist');
const reactRoutes = new Set(['index.html', 'ai-consulting.html', 'ai-speaking.html', 'contact.html']);

await rm(destination, { recursive: true, force: true });
await mkdir(destination, { recursive: true });

for (const entry of await readdir(source, { withFileTypes: true })) {
  if (reactRoutes.has(entry.name)) continue;
  await cp(join(source, entry.name), join(destination, entry.name), {
    recursive: true,
    force: true,
  });
}

console.log('Copied static Academy/course pages and assets into dist; personal-brand pages are React-rendered.');
