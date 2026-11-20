#!/usr/bin/env python3
"""Compose the news-image-20261120 front page: "The World in One Day —
Friday 20 November 2026".

Stories (all verified against reputable reporting before they were drawn):
  hero  Cyclone Akvan makes landfall near Gopalpur, Odisha, at noon IST,
        winds 90-100 km/h gusting 110; tens of thousands evacuated (IMD).
  GTA   Sensor Tower: 19.05m copies, about $1.84bn on day one; 7.9m peak
        concurrent viewers; Rockstar has released no official figures
        (Reuters, 19 Nov).
  ICJ   The Hague finds Myanmar committed genocide against the Rohingya
        in 2017 — the first state ever held guilty; reparations ordered
        (CNN / Le Monde, 19 Nov).
  Han   South Korea's top court overturns ex-PM Han Duck-soo's 15-year
        term over the 2024 martial-law bid, orders a retrial; detention
        extended two months (19 Nov).
  Ven   Hegseth signs a US-Venezuela military-cooperation deal in Caracas
        — joint training, intelligence sharing — 10 months after the
        capture of Nicolas Maduro (CNN / AP, 18 Nov).
  Yong   IAEA chief Grossi tells the Board of Governors that North Korea
        finished another extension to its Yongbyon enrichment plant;
        weapons-grade output keeps growing (Reuters, 18 Nov).
  Briefs: Fiji state of disaster (Reuters), Sensex +700 / Nifty past
        25,400, Anthropic valued at $1.5tn after its $83 Nasdaq debut,
        Nicholls 113* as NZ reach 243-5 in Wellington, Modi meets the
        Prince and Princess of Wales in New Delhi, Australia sanctions
        Israeli settlers, LPG tanker off Bulgaria hit by projectiles.

Deterministic: fixed seed, no timestamps, JPEG q92, no EXIF. Running
this script twice produces identical bytes. Writes entry.png next to it.
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (16, 20, 36)
NAVY = (16, 28, 58)
GOLD = (217, 164, 65)
RED = (178, 34, 34)
BODY = (40, 40, 40)
RULE = (120, 100, 60)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def vgrad(img, box, top, bottom):
    """Paint a vertical gradient into box by stretching a 1px-wide ramp."""
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    ramp = Image.new("RGB", (1, h))
    px = ramp.load()
    for y in range(h):
        t = y / (h - 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    img.paste(ramp.resize((x1 - x0, h)), (x0, y0))


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns the list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star_pts(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def buildings(d, box, rng, color, windows, h_lo=16, h_hi=64):
    """A deterministic row of lit buildings across the bottom of box."""
    x0, y0, x1, y1 = box
    x = x0
    while x < x1:
        bw = rng.randint(20, 44)
        bh = rng.randint(h_lo, h_hi)
        d.rectangle([x, y1 - bh, min(x + bw, x1), y1], fill=color)
        for _ in range(rng.randint(2, 6)):
            wx = rng.randint(x + 3, max(x + 4, min(x + bw - 5, x1 - 4)))
            wy = rng.randint(y1 - bh + 4, y1 - 8)
            d.rectangle([wx, wy, wx + 3, wy + 4], fill=rng.choice(windows))
        x += bw + rng.randint(2, 8)


def cyclone_hero(img, box, rng):
    """Akvan: spiral storm over a teal sea, coast and town on the right."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (14, 58, 78), (28, 104, 124))
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = (x0 + x1) // 2 - 90, (y0 + y1) // 2
    # spiral bands, tightening toward the eye
    for r in range(72, 12, -7):
        start = (r * 13) % 360
        d.arc([cx - r, cy - r, cx + r, cy + r], start=start,
              end=start + 255, fill=(235, 245, 245), width=5)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=GOLD)
    # coastline and a small coastal town on the right
    d.polygon([(x1 - 58, y0), (x1, y0), (x1, y1), (x1 - 82, y1),
               (x1 - 66, y0 + 40)], fill=(46, 80, 62))
    d.line([x1 - 58, y0, x1 - 66, y0 + 40, x1 - 82, y1],
           fill=(240, 240, 220), width=2)
    for bx in range(x1 - 120, x1 - 8, 16):
        bh = rng.randint(8, 22)
        d.rectangle([bx, y1 - 30 - bh, bx + 11, y1 - 30], fill=(20, 34, 28))
    # storm surge at the bottom
    d.rectangle([x0, y1 - 22, x1, y1], fill=(10, 26, 51))
    for _ in range(12):
        sx = rng.randint(x0 + 8, x1 - 50)
        sy = y1 - rng.randint(4, 18)
        d.line([sx, sy, sx + rng.randint(16, 40), sy], fill=(235, 245, 245),
               width=2)
    # rain streaks
    for _ in range(30):
        rx = rng.randint(x0 + 4, x1 - 8)
        ry = rng.randint(y0 + 4, y1 - 20)
        d.line([rx, ry, rx - 5, ry + 12], fill=(200, 225, 225), width=2)
    # tags: red alert top-left, kicker chip bottom-left
    d.rectangle([x0 + 8, y0 + 6, x0 + 100, y0 + 24], fill=RED)
    d.text((x0 + 14, y0 + 8), "RED ALERT", font=fnt(SANS_B, 12),
           fill=(255, 255, 255))
    d.rectangle([x0 + 10, y1 - 52, x0 + 236, y1 - 26], fill=NAVY)
    d.text((x0 + 20, y1 - 49), "CYCLONE AKVAN · ODISHA",
           font=fnt(SANS_B, 15), fill=GOLD)


def neon_city(img, box, rng):
    """Vice City at dusk: sunset, neon skyline, palms, neon sign."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (30, 12, 52), (150, 52, 110))
    d = ImageDraw.Draw(img, "RGBA")
    # setting sun, half behind the skyline
    sx, sy = (x0 + x1) // 2 + 120, y1 - 34
    d.ellipse([sx - 34, sy - 34, sx + 34, sy + 34], fill=(255, 166, 66))
    d.ellipse([sx - 22, sy - 22, sx + 22, sy + 22], fill=(255, 205, 110))
    buildings(d, (x0, y0 + 22, x1, y1), rng, (16, 8, 34),
              [(0, 229, 255), (255, 0, 153), (255, 214, 64), (120, 255, 120)],
              22, 66)
    # neon sign across the top
    d.rounded_rectangle([x0 + 96, y0 + 10, x0 + 318, y0 + 44], radius=4,
                        outline=(255, 0, 153), width=3)
    d.text((x0 + 112, y0 + 14), "VICE CITY", font=fnt(SANS_B, 24),
           fill=(255, 92, 199))
    # palm silhouettes at both edges
    for px in (x0 + 24, x1 - 28):
        d.line([px, y1, px + 8, y0 + 48], fill=(8, 4, 18), width=5)
        for a in range(-70, 71, 35):
            rad = math.radians(a - 90)
            ex = px + 8 + 32 * math.cos(rad)
            ey = y0 + 48 + 28 * math.sin(rad)
            d.line([px + 8, y0 + 48, ex, ey], fill=(8, 4, 18), width=4)
    d.rectangle([x0, y1 - 5, x1, y1], fill=(255, 0, 153))


def scales_art(img, box, rng):
    """The Hague: gold scales of justice over a night-blue court."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (12, 22, 64), (30, 48, 110))
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(26):
        sx = rng.randint(x0 + 4, x1 - 6)
        sy = rng.randint(y0 + 4, y0 + 34)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    cx = (x0 + x1) // 2
    top = y0 + 12
    base = y1 - 14
    # post, beam and base
    d.rectangle([cx - 3, top + 8, cx + 3, base], fill=GOLD)
    d.rectangle([cx - 62, top, cx + 62, top + 5], fill=GOLD)
    d.ellipse([cx - 5, top - 2, cx + 5, top + 8], fill=GOLD)
    d.rectangle([cx - 26, base - 4, cx + 26, base + 2], fill=GOLD)
    # two pans hanging from the beam
    for px in (cx - 62, cx + 62):
        d.line([px, top + 5, px - 16, base - 34], fill=GOLD, width=2)
        d.line([px, top + 5, px + 16, base - 34], fill=GOLD, width=2)
        d.pieslice([px - 18, base - 36, px + 18, base - 6], 0, 180,
                   fill=(217, 164, 65))
        d.line([px - 18, base - 21, px + 18, base - 21], fill=(176, 128, 42),
               width=2)
    # Peace Palace silhouette along the bottom
    d.rectangle([x0, y1 - 10, x1, y1], fill=(10, 16, 44))
    d.rectangle([cx - 90, y1 - 22, cx + 90, y1 - 10], fill=(10, 16, 44))


def court_art(img, box, rng):
    """Seoul's top court: pediment, columns and steps, Korean flag."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (40, 54, 96), (140, 150, 190))
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(20):
        sx = rng.randint(x0 + 4, x1 - 6)
        sy = rng.randint(y0 + 4, y0 + 26)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    cx = (x0 + x1) // 2 - 30
    # pediment, columns, steps
    d.polygon([(cx - 72, y0 + 34), (cx + 72, y0 + 34), (cx, y0 + 8)],
              fill=(232, 226, 210))
    d.rectangle([cx - 72, y0 + 34, cx + 72, y0 + 40], fill=(210, 202, 182))
    for i in range(-2, 3):
        d.rectangle([cx + i * 28 - 5, y0 + 40, cx + i * 28 + 5, y1 - 16],
                    fill=(240, 236, 224))
    d.rectangle([cx - 84, y1 - 16, cx + 84, y1 - 10], fill=(220, 214, 196))
    d.rectangle([cx - 92, y1 - 10, cx + 92, y1 - 4], fill=(200, 192, 172))
    d.rectangle([cx - 10, y0 + 48, cx + 10, y1 - 16], fill=(60, 50, 44))
    # Korean flag on a pole at the right
    fx = x1 - 52
    d.line([fx, y0 + 6, fx, y1 - 4], fill=(70, 70, 70), width=2)
    d.rectangle([fx + 2, y0 + 8, fx + 34, y0 + 28], fill=(255, 255, 255))
    d.pieslice([fx + 12, y0 + 12, fx + 24, y0 + 24], 180, 360,
               fill=(205, 46, 58))
    d.pieslice([fx + 12, y0 + 12, fx + 24, y0 + 24], 0, 180,
               fill=(0, 71, 160))
    for tx, ty in [(fx + 5, y0 + 10), (fx + 27, y0 + 10),
                   (fx + 5, y0 + 22), (fx + 27, y0 + 22)]:
        d.rectangle([tx, ty, tx + 5, ty + 2], fill=(20, 20, 20))


def flags_art(img, box, rng):
    """Two flags, one deal: US stars and stripes beside Venezuela's
    yellow-blue-red, with a gold seal across the seam."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    mid = (x0 + x1) // 2
    # US flag, left half
    stripe = (y1 - y0) / 13
    for i in range(13):
        d.rectangle([x0, y0 + i * stripe, mid, y0 + (i + 1) * stripe],
                    fill=(178, 34, 52) if i % 2 == 0 else (240, 240, 240))
    cw, ch = (mid - x0) * 0.4, stripe * 7
    d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            d.ellipse([x0 + 3 + c * (cw - 6) / 4 - 1, y0 + 3 + r * (ch - 6) / 3 - 1,
                       x0 + 3 + c * (cw - 6) / 4 + 1, y0 + 3 + r * (ch - 6) / 3 + 1],
                      fill=(255, 255, 255))
    # Venezuelan flag, right half
    vw = x1 - mid
    for i, c in enumerate([(252, 209, 22), (0, 56, 147), (207, 20, 43)]):
        d.rectangle([mid, y0 + i * (y1 - y0) / 3, x1,
                     y0 + (i + 1) * (y1 - y0) / 3], fill=c)
    for i in range(8):
        a = math.radians(200 + i * 20)
        sx = mid + vw * 0.5 + 26 * math.cos(a)
        sy = y0 + (y1 - y0) * 0.5 + 12 * math.sin(a)
        d.polygon(star_pts(sx, sy, 4, 2), fill=(255, 255, 255))
    # gold seal across the seam
    d.ellipse([mid - 24, y0 + 8, mid + 24, y0 + 56], fill=GOLD,
              outline=(176, 128, 42), width=2)
    d.text((mid, y0 + 22), "DEAL", font=fnt(SANS_B, 15), fill=NAVY,
           anchor="ma")
    d.rectangle([x0, y1 - 6, x1, y1], fill=(16, 28, 58))


def reactor_art(img, box, rng):
    """Yongbyon: cooling tower and reactor hall under a grey sky,
    with a hazard band along the bottom."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (24, 28, 40), (62, 68, 86))
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(22):
        sx = rng.randint(x0 + 4, x1 - 6)
        sy = rng.randint(y0 + 4, y0 + 28)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(200, 200, 200))
    cx = (x0 + x1) // 2 - 46
    # cooling tower: wide top and base, narrow waist
    d.polygon([(cx - 34, y0 + 10), (cx + 34, y0 + 10), (cx + 20, y1 - 22),
               (cx - 20, y1 - 22)], fill=(150, 150, 155))
    d.polygon([(cx - 34, y0 + 10), (cx + 34, y0 + 10), (cx + 26, y0 + 22),
               (cx - 26, y0 + 22)], fill=(110, 110, 116))
    d.rectangle([cx - 36, y0 + 8, cx + 36, y0 + 12], fill=(120, 120, 126))
    # reactor hall with dome, right of the tower
    rx = cx + 52
    d.rectangle([rx, y0 + 34, rx + 58, y1 - 22], fill=(120, 118, 110))
    d.pieslice([rx - 2, y0 + 10, rx + 60, y0 + 44], 180, 360,
               fill=(150, 148, 140))
    for wy in range(y0 + 44, y1 - 26, 12):
        d.rectangle([rx + 8, wy, rx + 16, wy + 6], fill=(60, 58, 52))
        d.rectangle([rx + 34, wy, rx + 42, wy + 6], fill=(60, 58, 52))
    # ground + hazard band
    d.rectangle([x0, y1 - 22, x1, y1 - 10], fill=(40, 42, 48))
    # shading ribs on the tower for depth
    d.line([cx - 12, y0 + 14, cx - 8, y1 - 22], fill=(120, 120, 126), width=2)
    d.line([cx + 12, y0 + 14, cx + 8, y1 - 22], fill=(120, 120, 126), width=2)
    for i in range(0, x1 - x0, 16):
        d.polygon([(x0 + i, y1 - 10), (x0 + i + 8, y1 - 10),
                   (x0 + i + 16, y1), (x0 + i + 8, y1)], fill=(252, 209, 22))


def grain(img, seed=20261120, alpha=9):
    """Paper grain: a small seeded noise field, resized and blended."""
    rng = random.Random(seed)
    small = Image.new("L", (128, 128))
    px = small.load()
    for y in range(128):
        for x in range(128):
            px[x, y] = 118 + rng.randint(-18, 18)
    noise = small.resize((W, H)).convert("RGB")
    return Image.blend(img, noise, alpha / 255.0)


def tile_pair(img, d, rng, x0, x1, art_y0, art_y1, kick_y, h_y, deck_y,
              kicker, h1, h2, deck, art, kick_size, head_size, deck_size,
              deck_w, deck_lead):
    """Draw one illustrated tile: art strip, kicker, two-line headline,
    wrapped deck. Returns nothing; draws in place."""
    art(img, (x0, art_y0, x1, art_y1), rng)
    d = ImageDraw.Draw(img)
    d.rectangle([x0, art_y1 + 6, x0 + 52, art_y1 + 10], fill=GOLD)
    d.text((x0, kick_y), kicker, font=fnt(SANS_B, kick_size), fill=NAVY)
    d.text((x0, h_y), h1, font=fnt(SERIF_B, head_size), fill=INK)
    d.text((x0, h_y + head_size + 2), h2, font=fnt(SERIF_B, head_size),
           fill=INK)
    y = deck_y
    for line in wrap(d, deck, fnt(SANS, deck_size), deck_w):
        d.text((x0, y), line, font=fnt(SANS, deck_size), fill=BODY)
        y += deck_lead


def main():
    rng = random.Random(20261120)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 76], fill=NAVY)
    d.text((W // 2, 2), "THE WORLD IN ONE DAY", font=fnt(SERIF_B, 46),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 52), "FRIDAY 20 NOVEMBER 2026", font=fnt(SANS_B, 20),
           fill=GOLD, anchor="ma")
    d.rectangle([0, 76, W, 80], fill=GOLD)
    d.rounded_rectangle([W - 196, 8, W - 12, 32], radius=4, fill=GOLD)
    d.text((W - 104, 12), "FINAL EDITION", font=fnt(SANS_B, 14),
           fill=NAVY, anchor="ma")

    # ---- hero: cyclone art, headline, deck ----
    cyclone_hero(img, (24, 92, 1000, 240), rng)
    d = ImageDraw.Draw(img)
    d.text((24, 248), "AKVAN MAKES", font=fnt(SERIF_B, 44), fill=INK)
    d.text((24, 294), "LANDFALL", font=fnt(SERIF_B, 44), fill=INK)
    deck = ("Severe Cyclonic Storm Akvan comes ashore near Gopalpur at "
            "noon, winds of 100 km/h; tens of thousands evacuated as "
            "heavy rain lashes the coast.")
    y = 344
    for line in wrap(d, deck, fnt(SANS, 19), 976):
        d.text((24, y), line, font=fnt(SANS, 19), fill=BODY)
        y += 23
    d.line([24, 398, 1000, 398], fill=RULE, width=1)

    # ---- row 2: two tiles ----
    row2 = [
        ("CULTURE · GAMING", "GTA VI: 19M COPIES", "ON DAY ONE",
         "Sensor Tower puts day-one sales at 19.05m copies, about $1.84bn; "
         "7.9m watch at once. Rockstar silent on official figures.",
         neon_city),
        ("THE HAGUE · JUSTICE", "COURT: MYANMAR", "GUILTY OF GENOCIDE",
         "The Hague finds Myanmar committed genocide against the Rohingya "
         "in 2017 — the first state ever held guilty. Reparations ordered.",
         scales_art),
    ]
    for i, (kick, h1, h2, deck, art) in enumerate(row2):
        x0 = 24 + i * 494
        tile_pair(img, d, rng, x0, x0 + 470, 410, 502, 508, 526, 586,
                  kick, h1, h2, deck, art, 14, 27, 18, 470, 22)
    d = ImageDraw.Draw(img)
    d.line([24, 656, 1000, 656], fill=RULE, width=1)

    # ---- row 3: three tiles ----
    row3 = [
        ("SOUTH KOREA · POLITICS", "EX-PM'S 15-YEAR TERM", "OVERTURNED",
         "Top court overturns Han Duck-soo's 15-year term over the "
         "martial-law bid; retrial ordered.",
         court_art),
        ("VENEZUELA · DEFENCE", "US AND VENEZUELA", "SIGN MILITARY PACT",
         "Hegseth signs a Caracas deal restoring defence ties — training "
         "and intelligence sharing.",
         flags_art),
        ("NORTH KOREA · NUCLEAR", "NORTH KOREA BUILDS", "MORE OF YONGBYON",
         "UN watchdog says Pyongyang finished another extension to its "
         "Yongbyon enrichment plant.",
         reactor_art),
    ]
    for i, (kick, h1, h2, deck, art) in enumerate(row3):
        x0 = 24 + i * 326
        tile_pair(img, d, rng, x0, x0 + 310, 668, 736, 748, 766, 818,
                  kick, h1, h2, deck, art, 13, 24, 16, 310, 20)
    d = ImageDraw.Draw(img)
    d.line([24, 894, 1000, 894], fill=RULE, width=1)

    # ---- briefs band ----
    d.rectangle([0, 900, W, H], fill=NAVY)
    d.text((24, 906), "ALSO FRIDAY", font=fnt(SANS_B, 19), fill=GOLD)
    briefs = [
        "FIJI DECLARES DISASTER — El Niño drought at crisis level",
        "SENSEX JUMPS 700 — Nifty crosses 25,400 in Thursday rally",
        "ANTHROPIC AT $1.5TN — valued at $1.5tn after Nasdaq debut",
        "NICHOLLS 113* — New Zealand 243-5 on day one in Wellington",
        "MODI MEETS THE WALESSES — royals in New Delhi for India-UK talks",
        "AUSTRALIA SANCTIONS SETTLERS — over West Bank expansion",
        "TANKER HIT IN BLACK SEA — LPG tanker struck by projectiles",
    ]
    for i, b in enumerate(briefs):
        col = 0 if i < 4 else 1
        row = i if i < 4 else i - 4
        d.text((24 + col * 500, 928 + row * 17), "•  " + b,
               font=fnt(SANS, 15), fill=(235, 235, 235))

    img = grain(img)
    img.save(HERE / "entry.png", "JPEG", quality=92)
    print("wrote", HERE / "entry.png")


if __name__ == "__main__":
    main()
