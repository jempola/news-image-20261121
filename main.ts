// news-image-20261121 entry — Node 22, standard library only.
//
// The entry image is entry.png in this repository: a front page that sums
// up the world news of Saturday 21 November 2026. This program copies it
// to the grader's output directory as entry.png.
//
// The image itself was drawn by generate.py (PIL, vector shapes + text,
// no network, no external photos) and is bundled here so the program is
// fully deterministic: the same bytes out on every run.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// (the grader sets MAKEFUN_OUTPUT_DIR to /output itself).

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });

const sourcePath = new URL('./entry.png', import.meta.url);
const outPath = join(outDir, 'entry.png');
copyFileSync(sourcePath, outPath);

// Determinism guard: the grader runs this program twice and requires
// byte-identical output, so read the written file back and refuse to
// pass silently if it ever differs from the bundled source.
const written = readFileSync(outPath);
const source = readFileSync(sourcePath);
if (!written.equals(source)) {
  throw new Error('entry.png mismatch: written output differs from source');
}
