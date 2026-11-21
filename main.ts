import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry for news-image-20261120: "The World in One Day — Friday
// 20 November 2026". The front page (entry.png, JPEG bytes under that
// name per RULES) is composed for this entry and shipped in the repo;
// this program copies it to the output directory. Same bytes every run:
// the file is only ever read, never modified or re-encoded.
//
// The page: Cyclone Akvan makes landfall near Gopalpur in the morning
// (hero), GTA VI's full launch-day sales, the ICJ's Myanmar genocide
// verdict, Han Duck-soo's overturned term, the US–Venezuela military
// pact and the Yongbyon expansion, plus an eight-item briefs band
// (including the Shenzhen summit and the Houthi strike on Riyadh).
//
// v4: build.py re-typeset the page for the 300px read only — no fact
// or number changed. Headlines up (hero 50pt, row 2 31pt, row 3 26pt),
// every deck cut to two lines at larger type, briefs set bold at 18pt
// and shortened to one line each, art strips taller, hero spiral
// enlarged. The image below is the v4 render (deterministic, same
// bytes on a re-run); everything else about this program is unchanged.
const MAX_BYTES = 1048576; // 1 MiB gate cap
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
const bytes = readFileSync(join(here, "entry.png"));

// Guard the gate before writing: the file must be a whole JPEG
// (SOI marker FF D8 FF, EOI marker FF D9 at the end) and within the
// 1 MiB cap, so a corrupted, truncated or oversized asset fails loudly
// here instead of at grading time.
function validate(buf) {
  if (buf.length < 4 || buf[0] !== 0xff || buf[1] !== 0xd8 || buf[2] !== 0xff) {
    throw new Error("entry.png is not a JPEG (missing SOI marker)");
  }
  if (buf[buf.length - 2] !== 0xff || buf[buf.length - 1] !== 0xd9) {
    throw new Error("entry.png is not a whole JPEG (missing EOI marker)");
  }
  if (buf.length > MAX_BYTES) {
    throw new Error(`entry.png is ${buf.length} bytes, over the 1 MiB cap`);
  }
}
validate(bytes);
writeFileSync(join(outDir, "entry.png"), bytes);
console.log(`entry.png OK: ${bytes.length} bytes (cap ${MAX_BYTES})`);
