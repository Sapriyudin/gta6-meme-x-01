// gta6-meme-x-01: the entry is the X post itself, so this program has
// exactly one job — hand POST.json (the post's address) to the grader.
// Node 22, standard library only. No network, no clock, no files
// outside the repository: run it twice and it writes the same bytes.
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(OUTPUT_DIR, { recursive: true });

try {
  copyFileSync(join(BOT_DIR, "POST.json"), join(OUTPUT_DIR, "POST.json"));
} catch (err) {
  console.error(
    `could not copy POST.json from ${BOT_DIR} to ${OUTPUT_DIR}: ${
      (err as Error).message
    }`,
  );
  process.exit(1);
}
