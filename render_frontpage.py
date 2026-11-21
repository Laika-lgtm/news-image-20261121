#!/usr/bin/env python3
"""Render the Saturday 21 November 2026 front page (v4).

v4 format: 13 illustrated cards (3 big + 10 small). Every picture is an
original flat illustration drawn in code here -- no photographs. The
stories are the verified Saturday 21 November 2026 stories from
SOURCES.md, numbered 1-13 on cards and 14-35 in the 'also' list, with a
numbered world map tying them to places. Masthead names the day in the
largest type; a stat strip, a region bar and a DATE CHECK box complete
the page. Output is entry.jpg (1024x1024, deterministic).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (169, 28, 28)
DARKRED = (139, 21, 21)
GRAY = (100, 100, 96)
LIGHT_LINE = (180, 172, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)


def wrap(d, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, font, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def chip(d, x, y, text, font, bg=RED, fg=(255, 255, 255), pad=5):
    w = d.textlength(text, font=font) + pad * 2
    h = font.size + pad
    d.rectangle([x, y, x + w, y + h], fill=bg)
    d.text((x + pad, y + pad // 2 - 1), text, font=font, fill=fg)
    return w


# ---------------------------------------------------------------- illustrations
# Each draws a simple flat scene inside box (x, y, w, h). All original.

def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(213, 231, 240))
    # globe
    cx, cy, r = x + w * 0.30, y + h * 0.52, min(w, h) * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(72, 130, 182))
    d.ellipse([cx - r * 0.55, cy - r * 0.75, cx + r * 0.15, cy - r * 0.05],
              fill=(110, 170, 90))
    d.ellipse([cx - r * 0.15, cy + r * 0.15, cx + r * 0.65, cy + r * 0.75],
              fill=(110, 170, 90))
    # thermometer
    tx = x + w * 0.62
    d.rectangle([tx, y + h * 0.18, tx + w * 0.07, y + h * 0.72],
                fill=(255, 255, 255), outline=(150, 150, 150))
    d.rectangle([tx + 2, y + h * 0.45, tx + w * 0.07 - 2, y + h * 0.72],
                fill=(200, 40, 40))
    d.ellipse([tx - w * 0.02, y + h * 0.66, tx + w * 0.09, y + h * 0.88],
              fill=(200, 40, 40))
    # clock
    kx, ky, kr = x + w * 0.85, y + h * 0.30, min(w, h) * 0.22
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255),
              outline=(60, 60, 60))
    d.line([kx, ky, kx, ky - kr * 0.65], fill=(30, 30, 30), width=2)
    d.line([kx, ky, kx + kr * 0.55, ky + kr * 0.25], fill=(30, 30, 30), width=2)


def ill_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    # moon
    d.ellipse([x + w * 0.86, y + h * 0.10, x + w * 0.94, y + h * 0.10 + w * 0.08],
              fill=(240, 230, 190))
    # skyline
    base = y + h
    for i, (bx, bw, bh) in enumerate([(0.02, 0.10, 0.42), (0.14, 0.08, 0.55),
                                      (0.24, 0.12, 0.38), (0.38, 0.09, 0.62),
                                      (0.50, 0.11, 0.45), (0.63, 0.08, 0.58),
                                      (0.73, 0.12, 0.40), (0.87, 0.10, 0.50)]):
        d.rectangle([x + w * bx, base - h * bh, x + w * (bx + bw), base],
                    fill=(38, 48, 78))
        for wy in range(3):
            for wx in range(2):
                d.rectangle([x + w * (bx + 0.015 + wx * 0.04),
                             base - h * bh + 6 + wy * 10,
                             x + w * (bx + 0.035 + wx * 0.04),
                             base - h * bh + 11 + wy * 10],
                            fill=(250, 210, 90))
    # missile trails: three ascending arcs with bursts
    for (sx, sy, ex, ey) in [(0.15, 0.95, 0.30, 0.25),
                             (0.45, 0.98, 0.58, 0.30),
                             (0.70, 0.95, 0.82, 0.35)]:
        x0, y0 = x + w * sx, y + h * sy
        x1, y1 = x + w * ex, y + h * ey
        mx, my = (x0 + x1) / 2 + w * 0.06, (y0 + y1) / 2
        pts = []
        for t in range(11):
            tt = t / 10.0
            px = (1 - tt) ** 2 * x0 + 2 * (1 - tt) * tt * mx + tt ** 2 * x1
            py = (1 - tt) ** 2 * y0 + 2 * (1 - tt) * tt * my + tt ** 2 * y1
            pts.append((px, py))
        d.line(pts, fill=(250, 220, 120), width=2)
        bx, by, br = x1, y1, 7
        d.polygon([(bx, by - br), (bx + br * 0.4, by - br * 0.4),
                   (bx + br, by), (bx + br * 0.4, by + br * 0.4),
                   (bx, by + br), (bx - br * 0.4, by + br * 0.4),
                   (bx - br, by), (bx - br * 0.4, by - br * 0.4)],
                  fill=(255, 215, 90))


def ill_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 205))
    # mountains
    d.polygon([(x, y + h * 0.85), (x + w * 0.25, y + h * 0.30),
               (x + w * 0.50, y + h * 0.85)], fill=(150, 125, 95))
    d.polygon([(x + w * 0.35, y + h * 0.85), (x + w * 0.62, y + h * 0.18),
               (x + w * 0.90, y + h * 0.85)], fill=(120, 100, 78))
    d.polygon([(x + w * 0.56, y + h * 0.32), (x + w * 0.62, y + h * 0.18),
               (x + w * 0.68, y + h * 0.32)], fill=(245, 245, 240))
    # seismograph zigzag
    pts = []
    xx = x + w * 0.05
    while xx < x + w * 0.95:
        pts.append((xx, y + h * 0.55))
        pts.append((xx + w * 0.03, y + h * 0.38))
        pts.append((xx + w * 0.06, y + h * 0.68))
        pts.append((xx + w * 0.09, y + h * 0.45))
        xx += w * 0.11
    d.line(pts, fill=(200, 40, 40), width=3)
    # houses
    for hx in (0.08, 0.72):
        d.rectangle([x + w * hx, y + h * 0.72, x + w * (hx + 0.16), y + h * 0.88],
                    fill=(250, 246, 235), outline=(120, 100, 80))
        d.polygon([(x + w * (hx - 0.02), y + h * 0.72),
                   (x + w * (hx + 0.08), y + h * 0.60),
                   (x + w * (hx + 0.18), y + h * 0.72)], fill=(170, 80, 60))


def ill_denmark(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(198, 12, 48))
    d.rectangle([x + w * 0.30, y, x + w * 0.40, y + h], fill=(255, 255, 255))
    d.rectangle([x, y + h * 0.42, x + w, y + h * 0.58], fill=(255, 255, 255))
    # envelope, bottom right, clear of the white cross
    ex, ey, ew, eh = x + w * 0.60, y + h * 0.58, w * 0.32, h * 0.32
    d.rectangle([ex, ey, ex + ew, ey + eh], fill=(238, 234, 224),
                outline=(70, 60, 50), width=2)
    d.line([(ex, ey), (ex + ew / 2, ey + eh * 0.55), (ex + ew, ey)],
           fill=(120, 100, 80), width=2)
    d.ellipse([ex + ew * 0.42, ey + eh * 0.42, ex + ew * 0.58, ey + eh * 0.62],
              fill=(169, 28, 28))


def ill_protest(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(236, 234, 222))
    skins = [(222, 184, 150), (190, 140, 100), (150, 105, 75),
             (232, 200, 170), (170, 120, 88)]
    shirts = [(169, 28, 28), (46, 90, 140), (60, 120, 70),
              (200, 140, 40), (110, 70, 130)]
    for i in range(5):
        cx = x + w * (0.10 + i * 0.20)
        r = min(w, h) * 0.11
        d.ellipse([cx - r, y + h * 0.42 - r, cx + r, y + h * 0.42 + r],
                  fill=skins[i])
        d.rectangle([cx - r * 1.15, y + h * 0.55, cx + r * 1.15, y + h * 0.95],
                    fill=shirts[i])
    # placards
    for px, py, pw in [(0.16, 0.12, 0.20), (0.62, 0.08, 0.22)]:
        d.rectangle([x + w * px, y + h * py, x + w * (px + pw), y + h * (py + 0.22)],
                    fill=(255, 255, 255), outline=(90, 90, 90))
        d.line([x + w * (px + pw / 2), y + h * (py + 0.22),
                x + w * (px + pw / 2), y + h * 0.55], fill=(90, 90, 90), width=2)
        d.line([x + w * (px + 0.04), y + h * (py + 0.11),
                x + w * (px + pw - 0.04), y + h * (py + 0.11)],
               fill=(169, 28, 28), width=2)


def ill_hospital(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 238, 232))
    d.rectangle([x + w * 0.18, y + h * 0.30, x + w * 0.82, y + h * 0.92],
                fill=(250, 250, 248), outline=(140, 140, 140))
    for wy in (0.42, 0.60):
        for wx in (0.26, 0.46, 0.66):
            d.rectangle([x + w * wx, y + h * wy, x + w * (wx + 0.08),
                         y + h * (wy + 0.10)], fill=(120, 170, 210))
    d.rectangle([x + w * 0.44, y + h * 0.80, x + w * 0.56, y + h * 0.92],
                fill=(90, 110, 130))
    # red cross sign, top right so it never meets the label chip
    cx, cy = x + w * 0.86, y + h * 0.20
    d.rectangle([cx - w * 0.03, cy - h * 0.12, cx + w * 0.03, cy + h * 0.12],
                fill=(200, 40, 40))
    d.rectangle([cx - w * 0.07, cy - h * 0.05, cx + w * 0.07, cy + h * 0.05],
                fill=(200, 40, 40))


def ill_candle(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(44, 48, 60))
    cx = x + w * 0.50
    d.ellipse([cx - w * 0.10, y + h * 0.10, cx + w * 0.10, y + h * 0.38],
              fill=(250, 215, 120))
    d.ellipse([cx - w * 0.05, y + h * 0.16, cx + w * 0.05, y + h * 0.34],
              fill=(255, 240, 180))
    d.line([cx, y + h * 0.36, cx, y + h * 0.44], fill=(20, 20, 20), width=2)
    d.rectangle([cx - w * 0.09, y + h * 0.44, cx + w * 0.09, y + h * 0.90],
                fill=(245, 242, 235))
    d.rectangle([cx - w * 0.13, y + h * 0.88, cx + w * 0.13, y + h * 0.93],
                fill=(200, 195, 185))


def ill_crystal(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 234, 244))
    cx, cy = x + w * 0.38, y + h * 0.52
    pts = [(cx, y + h * 0.10), (cx + w * 0.20, y + h * 0.35),
           (cx + w * 0.14, y + h * 0.85), (cx - w * 0.14, y + h * 0.85),
           (cx - w * 0.20, y + h * 0.35)]
    d.polygon(pts, fill=(140, 190, 220), outline=(60, 110, 160))
    for p in pts[1:]:
        d.line([cx, cy, p[0], p[1]], fill=(90, 140, 190), width=1)
    # rising arrow
    ax, ay = x + w * 0.68, y + h * 0.62
    d.line([(ax, ay + h * 0.25), (ax + w * 0.10, ay),
            (ax + w * 0.20, ay - h * 0.20)], fill=(40, 140, 70), width=4)
    d.polygon([(ax + w * 0.20, ay - h * 0.20), (ax + w * 0.14, ay - h * 0.16),
               (ax + w * 0.24, ay - h * 0.08)], fill=(40, 140, 70))


def ill_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 235, 224))
    bx, by, bw, bh = x + w * 0.30, y + h * 0.42, w * 0.42, h * 0.48
    d.rectangle([bx, by, bx + bw, by + bh], fill=(46, 90, 140))
    d.rectangle([bx + bw * 0.20, by - h * 0.06, bx + bw * 0.80, by],
                fill=(30, 60, 100))
    d.line([bx + bw * 0.30, by - h * 0.02, bx + bw * 0.70, by - h * 0.02],
           fill=(20, 20, 20), width=2)
    # ballot paper going in
    d.polygon([(bx + bw * 0.32, by - h * 0.34), (bx + bw * 0.62, by - h * 0.34),
               (bx + bw * 0.58, by - h * 0.04), (bx + bw * 0.36, by - h * 0.04)],
              fill=(255, 255, 255), outline=(120, 120, 120))
    # check mark
    d.line([(bx + bw * 0.38, by - h * 0.20), (bx + bw * 0.46, by - h * 0.12),
            (bx + bw * 0.58, by - h * 0.28)], fill=(200, 40, 40), width=3)


def ill_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 232, 242))
    cx, cy = x + w * 0.40, y + h * 0.55
    for r in (0.12, 0.24, 0.36, 0.48):
        rr = min(w, h) * r
        d.arc([cx - rr, cy - rr * 0.8, cx + rr, cy + rr * 0.8],
              start=200, end=60, fill=(60, 110, 180), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(40, 90, 160))
    # islands
    d.ellipse([x + w * 0.74, y + h * 0.70, x + w * 0.86, y + h * 0.82],
              fill=(110, 170, 90))
    d.ellipse([x + w * 0.82, y + h * 0.60, x + w * 0.90, y + h * 0.68],
              fill=(140, 190, 110))
    # rain
    for rx in (0.10, 0.22, 0.62, 0.72):
        d.line([(x + w * rx, y + h * 0.12), (x + w * (rx - 0.03), y + h * 0.28)],
               fill=(90, 140, 190), width=2)


def ill_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 232, 228))
    s = min(w, h) * 0.62
    cx, cy = x + w * 0.50, y + h * 0.52
    # pins
    for i in range(3):
        off = (i - 1) * s * 0.30
        d.rectangle([cx - s / 2 - 8, cy + off - 3, cx - s / 2, cy + off + 3],
                    fill=(120, 120, 120))
        d.rectangle([cx + s / 2, cy + off - 3, cx + s / 2 + 8, cy + off + 3],
                    fill=(120, 120, 120))
        d.rectangle([cx + off - 3, cy - s / 2 - 8, cx + off + 3, cy - s / 2],
                    fill=(120, 120, 120))
        d.rectangle([cx + off - 3, cy + s / 2, cx + off + 3, cy + s / 2 + 8],
                    fill=(120, 120, 120))
    d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2],
                fill=(40, 40, 48))
    f = SANS_B(max(10, int(s * 0.34)))
    t = "AI"
    d.text((cx - d.textlength(t, font=f) / 2, cy - f.size / 2 - 2), t,
           font=f, fill=(255, 255, 255))


def ill_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 238, 220))
    # stumps
    for i in range(3):
        sx = x + w * (0.72 + i * 0.05)
        d.rectangle([sx, y + h * 0.30, sx + 3, y + h * 0.80], fill=(220, 180, 60))
    d.rectangle([x + w * 0.72, y + h * 0.26, x + w * 0.86, y + h * 0.30],
                fill=(220, 180, 60))
    # bat
    d.polygon([(x + w * 0.18, y + h * 0.78), (x + w * 0.30, y + h * 0.72),
               (x + w * 0.52, y + h * 0.18), (x + w * 0.60, y + h * 0.24),
               (x + w * 0.38, y + h * 0.80)], fill=(210, 180, 130),
              outline=(140, 110, 70))
    # ball
    d.ellipse([x + w * 0.10, y + h * 0.18, x + w * 0.10 + w * 0.10,
               y + h * 0.18 + w * 0.10], fill=(185, 40, 40))
    # ground line
    d.line([(x, y + h * 0.86), (x + w, y + h * 0.86)], fill=(120, 150, 90),
           width=2)


def ill_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 235, 235))
    # track oval
    d.ellipse([x + w * 0.06, y + h * 0.18, x + w * 0.94, y + h * 0.82],
              outline=(60, 60, 60), width=8)
    d.ellipse([x + w * 0.14, y + h * 0.28, x + w * 0.86, y + h * 0.72],
              outline=(200, 200, 200), width=2)
    # race car
    cx, cy = x + w * 0.50, y + h * 0.50
    d.rectangle([cx - w * 0.10, cy - h * 0.10, cx + w * 0.10, cy + h * 0.10],
                fill=(200, 40, 40))
    d.rectangle([cx - w * 0.14, cy - h * 0.06, cx - w * 0.10, cy + h * 0.06],
                fill=(160, 30, 30))
    d.ellipse([cx - w * 0.08, cy + h * 0.08, cx - w * 0.03, cy + h * 0.18],
              fill=(25, 25, 25))
    d.ellipse([cx + w * 0.03, cy + h * 0.08, cx + w * 0.08, cy + h * 0.18],
              fill=(25, 25, 25))
    # checkered flag
    fx, fy = x + w * 0.80, y + h * 0.14
    d.line([fx, fy, fx, fy + h * 0.30], fill=(40, 40, 40), width=2)
    for r in range(2):
        for c in range(3):
            if (r + c) % 2 == 0:
                d.rectangle([fx + c * 7, fy + r * 7, fx + c * 7 + 7, fy + r * 7 + 7],
                            fill=(20, 20, 20))


ILLUSTRATIONS = {
    "cop31": ill_cop31, "riyadh": ill_riyadh, "peru": ill_peru,
    "denmark": ill_denmark, "protest": ill_protest, "hospital": ill_hospital,
    "candle": ill_candle, "crystal": ill_crystal, "ballot": ill_ballot,
    "cyclone": ill_cyclone, "chip": ill_chip, "cricket": ill_cricket,
    "f1": ill_f1,
}

CHIP_COLORS = [RED, (24, 48, 96), (14, 110, 110), (90, 55, 140),
               (30, 110, 55), (150, 70, 20), (110, 30, 60), (60, 90, 40)]


# ---------------------------------------------------------------- data
# All 35 stories verified Saturday 21 November 2026 (see SOURCES.md).
# Cards 1-13 carry a picture; 14-35 are the numbered 'also' list.

CARDS = [
    dict(n=1, place="ANTALYA, TÜRKIYE", topic="CLIMATE", chip="COP31: OVERTIME",
         time="01:44 UTC · ANTALYA",
         head="Climate summit runs into overtime",
         deck="COP31 missed its Friday close with no deal; a draft with no mention of fossil fuels split nearly 200 countries.",
         src="Reuters, Al Jazeera", ill="cop31", big=True),
    dict(n=2, place="RIYADH", topic="WAR", chip="SAUDI: MISSILES",
         time="04:32 UTC · RIYADH",
         head="Three missiles downed over Riyadh",
         deck="The Saudi-led coalition intercepted three Houthi ballistic missiles before dawn, the third straight night of alerts. No damage was reported.",
         src="Al Jazeera, Reuters", ill="riyadh", big=True),
    dict(n=3, place="JUNÍN, PERU", topic="EARTHQUAKE", chip="PERU: QUAKE 6.8",
         time="00:09 UTC · LIMA",
         head="Magnitude 6.8 quake shakes central Peru",
         deck="The deep quake near Carhuamayo was felt in Lima and along the coast. No deaths, damage or tsunami risk were reported.",
         src="USGS, IGP", ill="peru", big=True),
    dict(n=4, place="COPENHAGEN", topic="ESPIONAGE", chip="DENMARK: PLOT",
         head="Denmark expels diplomat over plot",
         deck="Russia 'planned to kill' a Ukrainian rapper, Denmark says.",
         src="Al Jazeera", ill="denmark"),
    dict(n=5, place="EUROPE", topic="PROTEST", chip="GEN Z: MARCH",
         head="Gen Z protests in 25 countries",
         deck="Young people marched over war, living costs and the climate.",
         src="Al Jazeera", ill="protest"),
    dict(n=6, place="BRASÍLIA", topic="POLITICS", chip="BOLSONARO: ILL",
         head="Bolsonaro hospitalised with blockage",
         deck="Ex-president in hospital with severe abdominal pain. He is stable.",
         src="Reuters, CNN", ill="hospital"),
    dict(n=7, place="SOUTH AFRICA", topic="CRIME", chip="600 KILLED",
         head="About 600 women killed in 3 months",
         deck="Nearly 600 women killed in South Africa in three months.",
         src="Premium Times", ill="candle"),
    dict(n=8, place="TOKYO", topic="DIPLOMACY", chip="MINERALS: DEAL",
         head="Japan partners ASEAN on minerals",
         deck="Japan and ASEAN agreed to work on critical-minerals supply.",
         src="Clash Report", ill="crystal"),
    dict(n=9, place="RAJASTHAN, INDIA", topic="POLITICS", chip="POLLS: SWEEP",
         head="Congress sweeps Rajasthan polls",
         deck="Congress won 33 of 37 districts and 3,701 seats in local polls.",
         src="World in 60", ill="ballot"),
    dict(n=10, place="COOK ISLANDS", topic="WEATHER", chip="CYCLONE: CAT 5",
         head="Cyclone Xavier weakens from Cat 5",
         deck="The cyclone peaked as a Category 5 near the Cook Islands.",
         src="Marco Island Naples News", ill="cyclone"),
    dict(n=11, place="WASHINGTON", topic="TECHNOLOGY", chip="TRUMP: NVIDIA",
         head="Trump asks Nvidia to bring back Huang",
         deck="Trump asked Nvidia to bring back chief executive Jensen Huang.",
         src="Al Jazeera", ill="chip"),
    dict(n=12, place="WELLINGTON", topic="CRICKET", chip="RAHUL: 100",
         head="Rahul hits century against New Zealand",
         deck="KL Rahul's 100 completes his SENA set; India 344 for 2 at tea.",
         src="IANS", ill="cricket"),
    dict(n=13, place="LAS VEGAS", topic="FORMULA ONE", chip="RUSSELL: P1",
         head="Russell fastest in rainy Las Vegas GP",
         deck="George Russell fastest in a rainy Las Vegas Grand Prix practice.",
         src="careerindia", ill="f1"),
]

ALSO = [
    (14, "French police convicted over Zecler attack", "AJ"),
    (15, "New African credit-rating agency launches", "AJ"),
    (16, "Record ₹1.22 lakh crore into Indian stocks", "Daily Short"),
    (17, "ASEAN summit and Quad meet in Manila", "Morning Sun"),
    (18, "Pochettino's Man Utd debut on Sunday", "AJ"),
    (19, "US declassifies UFO footage", "Jabulani"),
    (20, "Obi vows to end kidnapping in Nigeria", "Punch"),
    (21, "Springboks face Ireland without Erasmus", "News24"),
    (22, "Kane out for months with ankle injury", "IANS"),
    (23, "India women beat Malaysia 4–1", "careerindia"),
    (24, "Ghana: unfit nurses must not graduate", "GhanaWeb"),
    (25, "Kenya: court case over IEBC chief", "Standard"),
    (26, "Eswatini foam sparks pollution probe", ""),
    (27, "Mali: 120 votes pass textile law", ""),
    (28, "Malawi pregnancies expose exploitation", ""),
    (29, "Mauritius: Alex Ng Kong dies at 99", ""),
    (30, "Uganda: 26 journalism fellows graduate", ""),
    (31, "Debate: NZ as Australia's 7th state?", "HM"),
    (32, "World Television and Fisheries Days", ""),
    (33, "Troyes 3–1 Le Havre; Athletic 0–1 Espanyol", "ScoreZaap"),
    (34, "Boca face Atlético Mineiro in final", "CONMEBOL"),
    (35, "Liga MX: Juárez 3–3 Atlas; Tijuana 1–0 Atlante", "Vavel"),
]

STATS = [
    ("M6.8", "PERU QUAKE"),
    ("3", "MISSILES DOWNED"),
    ("25", "NATIONS PROTEST"),
    ("$120bn", "CLIMATE CASH CUT"),
    ("33", "DISTRICTS SWEPT"),
    ("₹1.22L cr", "RECORD INFLOW · INDIA"),
]

REGIONS = [
    ("EUROPE 6", 6, (46, 90, 136)),
    ("MIDEAST 1", 1, (185, 28, 28)),
    ("AFRICA 11", 11, (46, 125, 50)),
    ("ASIA 6", 6, (123, 31, 59)),
    ("N.AMERICA 3", 3, (14, 124, 123)),
    ("LATIN AM. 4", 4, (106, 63, 160)),
    ("OCEANIA 2", 2, (74, 123, 166)),
    ("GLOBAL 2", 2, (107, 114, 128)),
]

# (lon, lat) of each card story, for the map dots
DOTS = {
    1: (30.7, 36.9), 2: (46.7, 24.7), 3: (-75.2, -11.0),
    4: (12.6, 55.7), 5: (13.4, 52.5), 6: (-47.9, -15.8),
    7: (28.0, -26.2), 8: (139.7, 35.7), 9: (75.8, 26.9),
    10: (-159.8, -21.2), 11: (-77.0, 38.9), 12: (174.8, -41.3),
    13: (-115.1, 36.2),
}

CONTINENTS = [
    [(-165, 66), (-150, 70), (-135, 71), (-120, 72), (-105, 73), (-90, 74),
     (-80, 73), (-70, 68), (-60, 58), (-55, 50), (-60, 45), (-70, 42),
     (-75, 35), (-80, 30), (-85, 29), (-92, 28), (-97, 26), (-102, 23),
     (-108, 24), (-114, 29), (-120, 34), (-125, 42), (-130, 52),
     (-140, 60), (-155, 58), (-165, 60)],
    [(-58, 64), (-48, 60), (-42, 65), (-40, 72), (-50, 76), (-58, 74)],
    [(-79, 9), (-72, 11), (-62, 8), (-52, 4), (-50, 0), (-42, -5),
     (-37, -10), (-40, -18), (-47, -25), (-55, -33), (-62, -40),
     (-68, -50), (-70, -54), (-72, -45), (-73, -35), (-75, -22),
     (-79, -12), (-81, -3), (-80, 5)],
    [(-17, 15), (-13, 27), (-6, 33), (0, 36), (10, 37), (20, 32),
     (30, 31), (35, 28), (40, 18), (48, 11), (50, 5), (44, -2),
     (38, -12), (32, -25), (24, -33), (17, -31), (13, -22), (11, -12),
     (9, -2), (9, 4), (0, 5), (-8, 5), (-14, 9)],
    [(-10, 36), (-9, 43), (-4, 48), (0, 50), (6, 54), (12, 57), (18, 56),
     (24, 59), (30, 62), (38, 66), (48, 69), (60, 71), (72, 73), (85, 75),
     (100, 77), (115, 76), (130, 72), (145, 71), (160, 69), (175, 66),
     (178, 64), (170, 60), (162, 59), (156, 53), (150, 58), (142, 52),
     (138, 46), (132, 42), (128, 37), (124, 32), (120, 27), (114, 22),
     (109, 18), (105, 10), (102, 6), (99, 10), (96, 15), (92, 21),
     (88, 21), (84, 18), (80, 12), (77, 8), (74, 15), (70, 22),
     (66, 25), (61, 25), (57, 26), (53, 28), (49, 30), (45, 29),
     (41, 27), (38, 23), (35, 19), (32, 15), (29, 12), (32, 16),
     (35, 21), (35, 28), (36, 36), (30, 36), (26, 38), (22, 37),
     (18, 40), (14, 38), (12, 44), (8, 44), (3, 43), (0, 38),
     (-2, 37), (-6, 36)],
    [(114, -22), (122, -14), (130, -12), (136, -12), (142, -11),
     (146, -19), (150, -23), (153, -27), (150, -37), (146, -39),
     (140, -38), (135, -35), (130, -32), (124, -33), (118, -35),
     (113, -26)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51), (-3, 50)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (140, 38),
     (141, 40), (142, 42), (140, 44), (138, 40), (136, 37), (133, 35),
     (131, 33)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38),
     (175, -41), (172, -43), (169, -46)],
    [(44, -16), (48, -16), (50, -20), (48, -25), (44, -25), (43, -20)],
]


# ---------------------------------------------------------------- render

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    def proj(lon, lat):
        px = x + (lon + 180.0) / 360.0 * w
        py = y + (78.0 - lat) / 136.0 * h
        return (px, py)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(226, 210, 175), outline=(190, 175, 140))
    nf = SANS_B(10)
    for n, (lon, lat) in sorted(DOTS.items()):
        px, py = proj(lon, lat)
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255))
        t = str(n)
        d.text((px - d.textlength(t, font=nf) / 2, py - 5), t, font=nf,
               fill=(255, 255, 255))


def draw_big_card(d, c, x, y, w, h):
    ill_h = 134
    ILLUSTRATIONS[c["ill"]](d, x, y, w, ill_h)
    chip(d, x + 6, y + 6, c["chip"], SANS_B(11))
    chip(d, x + 6, y + ill_h - 24, c["time"], SANS_B(9),
         bg=(30, 30, 30), pad=4)
    ly = y + ill_h + 6
    d.text((x, ly), "%d %s · %s" % (c["n"], c["place"], c["topic"]),
           font=SANS_B(11), fill=RED)
    hy = ly + 16
    hl = wrap(d, c["head"], SERIF_B(23), w)
    draw_lines(d, x, hy, hl, SERIF_B(23), INK, 25)
    dy = hy + len(hl) * 25 + 3
    dl = wrap(d, c["deck"], SANS(11.5), w)
    draw_lines(d, x, dy, dl, SANS(11.5), (50, 50, 50), 14)
    sy = dy + len(dl) * 14 + 4
    d.text((x, sy), "(%s)" % c["src"], font=SANS(10), fill=GRAY)


def draw_small_card(d, c, x, y, w, h, color_idx):
    ill_h = 56
    ILLUSTRATIONS[c["ill"]](d, x, y, w, ill_h)
    chip(d, x + 4, y + 4, c["chip"], SANS_B(9),
         bg=CHIP_COLORS[color_idx % len(CHIP_COLORS)], pad=4)
    ly = y + ill_h + 4
    d.text((x, ly), "%d %s · %s" % (c["n"], c["place"], c["topic"]),
           font=SANS_B(10), fill=RED)
    hy = ly + 14
    hl = wrap(d, c["head"], SERIF_B(14), w)
    draw_lines(d, x, hy, hl, SERIF_B(14), INK, 16)
    dy = hy + len(hl) * 16 + 2
    dl = wrap(d, c["deck"], SANS(10), w)
    draw_lines(d, x, dy, dl, SANS(10), (50, 50, 50), 12)
    sy = dy + len(dl) * 12 + 3
    d.text((x, sy), "(%s)" % c["src"], font=SANS(8), fill=GRAY)


def render():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    # kicker
    d.text((12, 8), "THE WORLD IN ONE DAY", font=SANS_B(13), fill=RED)
    rt = "35 STORIES · 7 REGIONS · EVERY ONE DATED"
    d.text((W - 12 - d.textlength(rt, font=SANS_B(13)), 8), rt,
           font=SANS_B(13), fill=INK)
    d.line([(12, 28), (W - 12, 28)], fill=INK, width=2)
    # masthead: the day itself is the title
    title = "Saturday 21 November 2026"
    tf = SERIF_B(58)
    d.text(((W - d.textlength(title, font=tf)) / 2, 32), title, font=tf,
           fill=INK)
    sub = ("Climate summit runs past its deadline · Missiles downed over "
           "Riyadh · Quake shakes Peru")
    sf = SERIF(17)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 100), sub, font=sf, fill=INK)
    d.line([(12, 122), (W - 12, 122)], fill=INK, width=2)
    d.line([(12, 125), (W - 12, 125)], fill=INK, width=1)
    # stat strip
    cell_w = 1000 // 6
    for i, (num, lab) in enumerate(STATS):
        cx = 12 + i * cell_w
        nf = SERIF_B(26)
        d.text((cx + 8, 130), num, font=nf, fill=INK)
        lf = SANS_B(10)
        for j, ln in enumerate(wrap(d, lab, lf, cell_w - 16)):
            d.text((cx + 8, 162 + j * 12), ln, font=lf, fill=INK)
        if i:
            d.line([(cx, 130), (cx, 172)], fill=LIGHT_LINE, width=1)
    d.line([(12, 176), (W - 12, 176)], fill=INK, width=1)
    # region bar (min width, rescaled to fit)
    raw = [max(c / 35.0 * 1000, 80) for _, c, _ in REGIONS]
    scale = 1000.0 / sum(raw)
    widths = [r * scale for r in raw]
    rx = 12
    rf = SANS_B(10)
    for (label, _, color), wd in zip(REGIONS, widths):
        d.rectangle([rx, 180, rx + wd, 200], fill=color)
        d.text((rx + (wd - d.textlength(label, font=rf)) / 2, 184), label,
               font=rf, fill=(255, 255, 255))
        rx += wd
    # 3 big cards
    big = [c for c in CARDS if c.get("big")]
    for i, c in enumerate(big):
        draw_big_card(d, c, 12 + i * 336, 206, 328, 266)
    # 10 small cards, 2 rows of 5
    small = [c for c in CARDS if not c.get("big")]
    for i, c in enumerate(small):
        row, col = divmod(i, 5)
        draw_small_card(d, c, 12 + col * 201, 478 + row * 158, 193, 154,
                        i)
    # map + also list
    d.text((12, 800), "WHERE IT HAPPENED", font=SANS_B(11), fill=INK)
    draw_map(d, 12, 816, 310, 132)
    d.text((12, 950), "Each number is the story with that number on this page.",
           font=SANS(8), fill=GRAY)
    ax = 332
    d.text((ax, 800), "ALSO ON SATURDAY 21 NOVEMBER — 22 MORE STORIES",
           font=SANS_B(11), fill=INK)
    af = SANS(10)
    anf = SANS_B(10)
    col_w = 338
    for i, (n, text, src) in enumerate(ALSO):
        col, row = divmod(i, 11)
        x0 = ax + col * (col_w + 4)
        y0 = 818 + row * 12
        num = "%d " % n
        d.text((x0, y0), num, font=anf, fill=RED)
        tx = x0 + d.textlength(num, font=anf)
        line = text + (" (%s)" % src if src else "")
        d.text((tx, y0), line, font=af, fill=INK)
    # DATE CHECK
    d.rectangle([12, 962, W - 12, 1000], outline=RED, width=1)
    d.text((20, 968), "DATE CHECK", font=SANS_B(11), fill=RED)
    dc = ("Left out as Friday 20 November's news: Russian missile in Poland · "
          "Kyiv bridge attacks · UK–EU deal · Hague ruling on Myanmar · "
          "Cyclone Akvan · Pete Rose pardon · Fiona the hippo dies · "
          "GTA VI's $3.79bn first day · Riemann proof claim.")
    dl = wrap(d, dc, SANS(11), W - 24 - d.textlength("DATE CHECK  ", font=SANS_B(11)))
    draw_lines(d, 20 + d.textlength("DATE CHECK  ", font=SANS_B(11)), 968,
               dl, SANS(11), INK, 13)
    # footer
    d.text((12, 1006), "Every story here happened, or was first reported, on "
           "Saturday 21 November 2026. Sources named beside each story.",
           font=SANS(9), fill=GRAY)
    ft = "Pictures and map: original, drawn in code."
    d.text((W - 12 - d.textlength(ft, font=SANS(9)), 1006), ft,
           font=SANS(9), fill=GRAY)
    return im


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.jpg")
    render().save(out, quality=88)
    print("wrote", out, os.path.getsize(out), "bytes")
