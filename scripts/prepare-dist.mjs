import { cp, mkdir, readdir, rm } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
const source = join(root, 'public');
const destination = join(root, 'dist');

await rm(destination, { recursive: true, force: true });
await mkdir(destination, { recursive: true });

for (const entry of await readdir(source, { withFileTypes: true })) {
  if (entry.name === 'index.html') continue;
  await cp(join(source, entry.name), join(destination, entry.name), {
    recursive: true,
    force: true,
  });
}

console.log('Copied the existing static pages and assets into dist (homepage is React-rendered).');
