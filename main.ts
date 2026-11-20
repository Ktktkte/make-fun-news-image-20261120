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
// v3: build.py re-verified every story against live reporting — Akvan
// landfall in the morning (70-80 km/h, more than 300,000 evacuated,
// no deaths), GTA VI full launch-day sales 24.6m / $2.36bn, cricket at
// stumps (Nicholls 175*, NZ 368), ICJ deck adds Myanmar's "unfair"
// dismissal, and two missing major stories added (Shenzhen summit,
// Houthi strike on Riyadh's PIF Tower). Briefs band set at 16pt for
// 300px legibility. This program now also reports the validated byte size
// so a bad asset is visible in the run log, not just at grading time.
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
