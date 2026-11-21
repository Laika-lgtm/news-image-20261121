#!/usr/bin/env python3
"""Render the Saturday 21 November 2026 front page (news-image-20261121, round 7 / v5).

Draws a 1024x1024 newspaper front page with PIL only: masthead, stat strip,
region bar, 3 big illustrated cards + 10 small illustrated cards, a numbered
world map, an ALSO list (stories 14-35) and a DATE CHECK box.

Deterministic: no clock, no randomness, fixed JPEG quality, no EXIF.
Run:  python3 render_frontpage.py   -> writes entry.jpg next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.jpg")

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (26, 26, 26)
RED = (179, 39, 30)
DARKRED = (143, 29, 22)
MUTED = (107, 101, 88)
RULE = (26, 26, 26)
CARD_BG = (255, 253, 246)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"  # DejaVu has no serif italic; Noto Serif Italic matches the masthead style
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for i, ln in enumerate(lines):
        draw.text((x, y + i * leading), ln, font=fnt, fill=fill)
    return y + len(lines) * leading


def fit_font(draw, text, path, start, max_w):
    size = start
    while size > 10 and draw.textlength(text, font=font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def star(draw, cx, cy, r_out, r_in, points, fill):
    import math
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- illustrations
def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(213, 232, 212))
    # globe
    gx, gy, gr = x + w * 0.30, y + h * 0.52, h * 0.34
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(52, 120, 180))
    d.ellipse([gx - gr * 0.55, gy - gr * 0.6, gx - gr * 0.05, gy - gr * 0.05], fill=(76, 175, 80))
    d.ellipse([gx + gr * 0.1, gy + gr * 0.15, gx + gr * 0.6, gy + gr * 0.6], fill=(76, 175, 80))
    # thermometer
    tx = x + w * 0.62
    d.rounded_rectangle([tx, y + h * 0.18, tx + 16, y + h * 0.78], radius=8, fill=(255, 255, 255), outline=(120, 120, 120))
    d.ellipse([tx - 5, y + h * 0.72, tx + 21, y + h * 0.98], fill=(211, 47, 47))
    d.rectangle([tx + 5, y + h * 0.32, tx + 11, y + h * 0.78], fill=(211, 47, 47))
    # clock
    cx, cy, cr = x + w * 0.85, y + h * 0.32, h * 0.22
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 255, 255), outline=(26, 26, 26), width=2)
    d.line([cx, cy, cx, cy - cr * 0.7], fill=(26, 26, 26), width=3)
    d.line([cx, cy, cx + cr * 0.55, cy + cr * 0.3], fill=(26, 26, 26), width=3)


def ill_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(15, 31, 61))
    # moon
    d.ellipse([x + w * 0.84, y + h * 0.10, x + w * 0.94, y + h * 0.30], fill=(240, 230, 180))
    # skyline
    import random
    rnd = random.Random(7)
    base = y + h
    bx = x + 6
    while bx < x + w - 14:
        bw = rnd.randint(18, 34)
        bh = rnd.randint(int(h * 0.35), int(h * 0.72))
        d.rectangle([bx, base - bh, bx + bw, base], fill=(28, 48, 88))
        for wy in range(int(base - bh + 6), int(base - 6), 9):
            for wx in range(int(bx + 4), int(bx + bw - 3), 8):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    # missile trails: dotted arcs
    for (sx, sy, ex, ey) in [(0.08, 0.95, 0.38, 0.18), (0.45, 0.95, 0.68, 0.12), (0.72, 0.95, 0.92, 0.30)]:
        for t in range(0, 11):
            tt = t / 10.0
            px = x + w * (sx + (ex - sx) * tt)
            py = y + h * (sy + (ey - sy) * tt - 0.25 * (1 - tt) * tt * 4 * 0.12)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 214, 90))
        star(d, x + w * ex, y + h * ey, 9, 4, 8, (255, 200, 60))


def ill_ukraine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 28, 46))
    # moon
    d.ellipse([x + w * 0.86, y + h * 0.08, x + w * 0.95, y + h * 0.26], fill=(235, 228, 190))
    # buildings
    builds = [(0.04, 0.42, 0.20, 0.62), (0.24, 0.30, 0.38, 0.55), (0.44, 0.48, 0.58, 0.68),
              (0.62, 0.34, 0.76, 0.58), (0.80, 0.50, 0.96, 0.72)]
    for (fx0, fy0, fx1, fy1) in builds:
        d.rectangle([x + w * fx0, y + h * fy0, x + w * fx1, y + h * fy1], fill=(52, 66, 96))
        for wy in range(int(y + h * fy0 + 6), int(y + h * fy1 - 4), 10):
            for wx in range(int(x + w * fx0 + 4), int(x + w * fx1 - 4), 9):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
    # fire bursts
    for (fx, fy, r) in [(0.31, 0.30, 16), (0.69, 0.34, 13)]:
        star(d, x + w * fx, y + h * fy, r, r * 0.45, 8, (255, 140, 0))
        star(d, x + w * fx, y + h * fy, r * 0.55, r * 0.25, 8, (255, 220, 80))
    # smoke
    for (fx, fy, r) in [(0.31, 0.16, 12), (0.69, 0.20, 10), (0.50, 0.12, 9)]:
        d.ellipse([x + w * fx - r, y + h * fy - r, x + w * fx + r, y + h * fy + r], fill=(120, 120, 130))
    # small Ukrainian flag on a building
    d.rectangle([x + w * 0.45, y + h * 0.44, x + w * 0.53, y + h * 0.48], fill=(0, 91, 187))
    d.rectangle([x + w * 0.45, y + h * 0.48, x + w * 0.53, y + h * 0.52], fill=(255, 213, 0))


def ill_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(242, 227, 198))
    # mountains
    d.polygon([(x, y + h), (x + w * 0.30, y + h * 0.30), (x + w * 0.58, y + h)], fill=(122, 102, 78))
    d.polygon([(x + w * 0.35, y + h), (x + w * 0.62, y + h * 0.18), (x + w * 0.95, y + h)], fill=(94, 80, 62))
    d.polygon([(x + w * 0.55, y + h * 0.30), (x + w * 0.62, y + h * 0.18), (x + w * 0.70, y + h * 0.32)], fill=(255, 255, 255))
    # seismograph zigzag
    pts = []
    import math
    for i in range(25):
        px = x + w * (0.06 + 0.88 * i / 24.0)
        py = y + h * 0.62 + (10 if i % 4 == 1 else -12 if i % 4 == 3 else 0)
        pts.append((px, py))
    d.line(pts, fill=(211, 47, 47), width=3)
    # small house
    hx, hy = x + w * 0.74, y + h * 0.74
    d.rectangle([hx, hy, hx + 26, hy + 16], fill=(255, 255, 255), outline=(90, 70, 50))
    d.polygon([(hx - 3, hy), (hx + 13, hy - 10), (hx + 29, hy)], fill=(179, 39, 30))


def ill_davao(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(188, 216, 234))
    # clouds
    for (fx, fy, r) in [(0.18, 0.22, 12), (0.80, 0.30, 10), (0.55, 0.14, 8)]:
        d.ellipse([x + w * fx - r, y + h * fy - r * 0.6, x + w * fx + r, y + h * fy + r * 0.6], fill=(255, 255, 255))
    # plane: fuselage + wings + tail
    cx, cy = x + w * 0.50, y + h * 0.52
    d.ellipse([cx - 62, cy - 9, cx + 62, cy + 9], fill=(255, 255, 255))
    d.polygon([(cx - 8, cy - 6), (cx + 18, cy - 34), (cx + 30, cy - 34), (cx + 14, cy - 6)], fill=(230, 230, 230))
    d.polygon([(cx - 2, cy + 6), (cx + 12, cy + 28), (cx + 22, cy + 28), (cx + 10, cy + 6)], fill=(230, 230, 230))
    d.polygon([(cx + 48, cy - 8), (cx + 62, cy - 26), (cx + 70, cy - 26), (cx + 60, cy - 6)], fill=(230, 230, 230))
    d.rectangle([cx - 58, cy - 2, cx + 40, cy + 2], fill=(30, 90, 160))
    for wx in range(-50, 36, 12):
        d.ellipse([cx + wx, cy - 5, cx + wx + 4, cy - 1], fill=(30, 90, 160))
    # runway
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(90, 90, 90))
    for i in range(6):
        d.rectangle([x + 8 + i * 32, y + h - 6, x + 24 + i * 32, y + h - 4], fill=(255, 255, 255))


def ill_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(11, 11, 30))
    # stars
    for (fx, fy) in [(0.10, 0.15), (0.22, 0.45), (0.85, 0.12), (0.92, 0.55), (0.60, 0.08), (0.35, 0.75)]:
        d.ellipse([x + w * fx - 1.5, y + h * fy - 1.5, x + w * fx + 1.5, y + h * fy + 1.5], fill=(255, 255, 255))
    # Mercury
    mx, my, mr = x + w * 0.34, y + h * 0.52, h * 0.36
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(150, 148, 140))
    for (fx, fy, r) in [(-0.4, -0.3, 0.16), (0.25, 0.2, 0.12), (0.05, -0.45, 0.10), (-0.15, 0.35, 0.13)]:
        d.ellipse([mx + mr * fx - mr * r, my + mr * fy - mr * r,
                   mx + mr * fx + mr * r, my + mr * fy + mr * r], fill=(120, 118, 110))
    # spacecraft (kept left of the tag pill)
    sx, sy = x + w * 0.60, y + h * 0.42
    d.rectangle([sx - 26, sy - 6, sx + 26, sy + 6], fill=(30, 90, 180))
    d.rectangle([sx - 14, sy - 4, sx + 14, sy + 4], fill=(220, 220, 220))
    d.polygon([(sx - 4, sy + 6), (sx + 4, sy + 6), (sx, sy + 20)], fill=(255, 140, 0))
    d.polygon([(sx - 4, sy + 6), (sx + 4, sy + 6), (sx, sy + 14)], fill=(255, 220, 80))


def ill_warsaw(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 247))
    # NATO star
    cx, cy, r = x + w * 0.30, y + h * 0.50, h * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 51, 102))
    star(d, cx, cy, r * 0.82, r * 0.30, 4, (255, 255, 255))
    # Polish flag
    fx0, fy0, fw, fh = x + w * 0.58, y + h * 0.28, w * 0.34, h * 0.44
    d.rectangle([fx0, fy0, fx0 + fw, fy0 + fh / 2], fill=(255, 255, 255), outline=(120, 120, 120))
    d.rectangle([fx0, fy0 + fh / 2, fx0 + fw, fy0 + fh], fill=(220, 20, 60), outline=(120, 120, 120))
    # small stars
    for (sx, sy) in [(0.88, 0.80), (0.12, 0.82)]:
        star(d, x + w * sx, y + h * sy, 5, 2, 5, (0, 51, 102))


def ill_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 111, 158))
    # waves
    for wy in [0.78, 0.88]:
        for i in range(5):
            d.arc([x + i * 40 - 8, y + h * wy - 8, x + i * 40 + 24, y + h * wy + 8], 180, 360, fill=(255, 255, 255), width=2)
    # drone silhouette (quad-rotor) — light grey so it reads on the blue sea
    cx, cy = x + w * 0.50, y + h * 0.44
    d.ellipse([cx - 30, cy - 8, cx + 30, cy + 8], fill=(80, 80, 80))
    for (ox, oy) in [(-28, -15), (28, -15), (-28, 15), (28, 15)]:
        d.line([cx, cy, cx + ox, cy + oy], fill=(80, 80, 80), width=3)
        d.ellipse([cx + ox - 9, cy + oy - 3, cx + ox + 9, cy + oy + 3], fill=(150, 150, 150))
    # down arrow
    d.line([cx + 44, cy - 26, cx + 44, cy + 8], fill=(255, 255, 255), width=4)
    d.polygon([(cx + 36, cy + 4), (cx + 52, cy + 4), (cx + 44, cy + 18)], fill=(255, 255, 255))


def ill_bitcoin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 26, 46))
    # big B coin
    cx, cy, r = x + w * 0.30, y + h * 0.50, h * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(247, 147, 26))
    d.text((cx - 8, cy - 13), "B", font=font(SANS_B, 26), fill=(255, 255, 255))
    # falling chart
    pts = [(x + w * 0.52, y + h * 0.22), (x + w * 0.64, y + h * 0.34),
           (x + w * 0.74, y + h * 0.30), (x + w * 0.86, y + h * 0.62),
           (x + w * 0.95, y + h * 0.78)]
    d.line(pts, fill=(230, 60, 60), width=4)
    d.polygon([(x + w * 0.95, y + h * 0.78), (x + w * 0.88, y + h * 0.72), (x + w * 0.90, y + h * 0.84)], fill=(230, 60, 60))


def ill_nigeria(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(127, 179, 213))
    # sun
    d.ellipse([x + w * 0.82, y + h * 0.10, x + w * 0.94, y + h * 0.30], fill=(255, 220, 90))
    # boat
    bx, by = x + w * 0.50, y + h * 0.55
    d.polygon([(bx - 52, by), (bx + 52, by), (bx + 38, by + 16), (bx - 38, by + 16)], fill=(120, 72, 20))
    d.rectangle([bx - 30, by - 18, bx + 30, by], fill=(240, 240, 230))
    d.line([bx, by - 34, bx, by - 18], fill=(90, 60, 20), width=3)
    d.polygon([(bx, by - 34), (bx + 16, by - 24), (bx, by - 18)], fill=(179, 39, 30))
    # waves
    for wy in [0.82, 0.92]:
        for i in range(5):
            d.arc([x + i * 40 - 8, y + h * wy - 7, x + i * 40 + 24, y + h * wy + 7], 180, 360, fill=(255, 255, 255), width=2)


def ill_genz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 230, 200))
    # placards
    for (fx, col) in [(0.16, (179, 39, 30)), (0.50, (30, 90, 160)), (0.84, (30, 130, 60))]:
        d.rectangle([x + w * fx - 16, y + h * 0.10, x + w * fx + 16, y + h * 0.38], fill=col)
        d.rectangle([x + w * fx - 2, y + h * 0.38, x + w * fx + 2, y + h * 0.62], fill=(90, 70, 40))
    # crowd heads
    import random
    rnd = random.Random(11)
    for row, fy in enumerate([0.68, 0.84]):
        for i in range(7):
            hx = x + w * (0.08 + i * 0.14 + (0.07 if row else 0))
            d.ellipse([hx - 7, y + h * fy - 7, hx + 7, y + h * fy + 7],
                      fill=rnd.choice([(179, 39, 30), (30, 90, 160), (30, 130, 60), (220, 140, 30), (120, 60, 140)]))
            d.rectangle([hx - 9, y + h * fy + 7, hx + 9, y + h], fill=(60, 60, 60))


def ill_rahul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(61, 139, 64))
    # pitch strip
    d.rectangle([x + w * 0.30, y, x + w * 0.70, y + h], fill=(210, 180, 120))
    # stumps
    for i in range(3):
        sx = x + w * 0.60 + i * 7
        d.rectangle([sx, y + h * 0.18, sx + 4, y + h * 0.42], fill=(255, 240, 200))
    # bat (angled)
    d.line([x + w * 0.28, y + h * 0.80, x + w * 0.48, y + h * 0.42], fill=(222, 184, 135), width=9)
    d.line([x + w * 0.48, y + h * 0.42, x + w * 0.54, y + h * 0.30], fill=(180, 140, 90), width=5)
    # ball
    d.ellipse([x + w * 0.78 - 8, y + h * 0.62 - 8, x + w * 0.78 + 8, y + h * 0.62 + 8], fill=(200, 30, 30))


def ill_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(17, 17, 17))
    # checkered strip
    for i in range(8):
        for j in range(2):
            if (i + j) % 2 == 0:
                d.rectangle([x + i * 24, y + 6 + j * 12, x + (i + 1) * 24, y + 18 + j * 12], fill=(255, 255, 255))
    # race car silhouette
    cx, cy = x + w * 0.50, y + h * 0.58
    d.rounded_rectangle([cx - 62, cy - 12, cx + 62, cy + 8], radius=8, fill=(200, 30, 30))
    d.polygon([(cx - 20, cy - 12), (cx - 8, cy - 26), (cx + 26, cy - 26), (cx + 38, cy - 12)], fill=(160, 20, 20))
    d.polygon([(cx + 52, cy - 26), (cx + 66, cy - 26), (cx + 66, cy - 18), (cx + 52, cy - 14)], fill=(200, 30, 30))
    for wx in [-38, 38]:
        d.ellipse([cx + wx - 12, cy + 4, cx + wx + 12, cy + 28], fill=(20, 20, 20))
        d.ellipse([cx + wx - 5, cy + 11, cx + wx + 5, cy + 21], fill=(120, 120, 120))
    # speed lines
    for i, fy in enumerate([0.30, 0.45, 0.62]):
        d.line([x + 8, y + h * fy, x + w * 0.22, y + h * fy], fill=(255, 255, 255), width=2)


# ------------------------------------------------------------------- cards
def draw_banner(d, x, y, w, text, size=14):
    d.rectangle([x, y, x + w, y + 24], fill=RED)
    f = font(SANS_B, size)
    d.text((x + 8, y + 4), text, font=f, fill=(255, 255, 255))
    return y + 24


def draw_loc(d, x, y, num, text, size=10):
    r = 8
    d.ellipse([x, y - 1, x + 2 * r, y + 2 * r - 1], fill=RED)
    nf = font(SANS_B, 10)
    tw = d.textlength(str(num), font=nf)
    d.text((x + r - tw / 2, y + 1), str(num), font=nf, fill=(255, 255, 255))
    f = font(SANS_B, size)
    d.text((x + 2 * r + 5, y + 1), text, font=f, fill=DARKRED)
    return y + 17


def draw_tag(d, x, y, label, color):
    f = font(SANS_B, 9)
    tw = d.textlength(label, font=f) + 10
    d.rounded_rectangle([x - tw, y, x, y + 15], radius=4, fill=color)
    d.text((x - tw + 5, y + 2), label, font=f, fill=(255, 255, 255))


def big_card(img, d, x, y, w, h, num, banner, loc, headline, deck, ill):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=(200, 192, 170))
    ill_h = 118
    ill(d, x + 1, y + 1, w - 2, ill_h)
    ty = draw_banner(d, x + 1, y + 1 + ill_h, w - 2, banner, size=14)
    ly = draw_loc(d, x + 8, ty + 6, num, loc, size=10)
    hf = font(SERIF_B, 20)
    lines = wrap(d, headline, hf, w - 16)
    text_block(d, x + 8, ly + 2, lines[:2], hf, INK, 23)
    df = font(SANS, 11)
    dlines = wrap(d, deck, df, w - 16)
    text_block(d, x + 8, ly + 2 + 2 * 23 + 3, dlines[:3], df, (60, 58, 50), 14)


def small_card(img, d, x, y, w, h, num, banner, loc, headline, deck, ill, tag=None, tag_color=None):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=(200, 192, 170))
    ill_h = 56
    ill(d, x + 1, y + 1, w - 2, ill_h)
    if tag:
        draw_tag(d, x + w - 6, y + 5, tag, tag_color)
    ty = draw_banner(d, x + 1, y + 1 + ill_h, w - 2, banner, size=11)
    ly = draw_loc(d, x + 6, ty + 4, num, loc, size=9)
    hf = font(SERIF_B, 15)
    lines = wrap(d, headline, hf, w - 12)
    text_block(d, x + 6, ly + 1, lines[:2], hf, INK, 17)
    df = font(SANS, 10)
    dlines = wrap(d, deck, df, w - 12)
    text_block(d, x + 6, ly + 1 + 2 * 17 + 2, dlines[:3], df, (60, 58, 50), 13)


# ------------------------------------------------------------------- map
def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 232, 236), outline=(200, 192, 170))
    land = (216, 207, 174)
    # rough continents (schematic)
    d.polygon([(x + 18, y + 22), (x + 60, y + 12), (x + 105, y + 18), (x + 110, y + 48),
               (x + 88, y + 62), (x + 60, y + 58), (x + 28, y + 48)], fill=land)          # N America
    d.polygon([(x + 62, y + 72), (x + 92, y + 70), (x + 104, y + 96), (x + 88, y + 126),
               (x + 70, y + 118), (x + 58, y + 92)], fill=land)                           # S America
    d.polygon([(x + 148, y + 26), (x + 172, y + 18), (x + 188, y + 30), (x + 182, y + 52),
               (x + 160, y + 56), (x + 146, y + 42)], fill=land)                          # Europe
    d.polygon([(x + 152, y + 62), (x + 182, y + 58), (x + 196, y + 82), (x + 184, y + 112),
               (x + 164, y + 108), (x + 150, y + 84)], fill=land)                         # Africa
    d.polygon([(x + 192, y + 16), (x + 260, y + 10), (x + 300, y + 26), (x + 296, y + 58),
               (x + 250, y + 66), (x + 210, y + 58), (x + 190, y + 36)], fill=land)        # Asia
    d.ellipse([x + 288, y + 92, x + 312, y + 112], fill=land)                              # Oceania
    dots = {
        1: (190, 52), 2: (212, 56), 3: (178, 34), 4: (76, 96), 5: (272, 78),
        7: (160, 26), 8: (236, 74), 10: (162, 84), 11: (146, 46), 12: (302, 106), 13: (48, 48),
    }
    nf = font(SANS_B, 9)
    for n, (dx, dy) in dots.items():
        d.ellipse([x + dx - 8, y + dy - 8, x + dx + 8, y + dy + 8], fill=RED, outline=(255, 255, 255))
        tw = d.textlength(str(n), font=nf)
        d.text((x + dx - tw / 2, y + dy - 6), str(n), font=nf, fill=(255, 255, 255))
    # space stories: Mercury (6) and Bitcoin (9) shown as icons, top-right
    d.ellipse([x + w - 52, y + 8, x + w - 30, y + 30], fill=(150, 148, 140), outline=(255, 255, 255))
    d.text((x + w - 45, y + 12), "6", font=nf, fill=(255, 255, 255))
    d.ellipse([x + w - 24, y + 8, x + w - 2, y + 30], fill=(247, 147, 26), outline=(255, 255, 255))
    d.text((x + w - 17, y + 12), "9", font=nf, fill=(255, 255, 255))


# ------------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14
    CW = W - 2 * M  # 996

    # kicker
    d.text((M, 10), "THE WORLD IN ONE DAY", font=font(SANS_B, 13), fill=RED)
    right = "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    rf = font(SANS_B, 11)
    d.text((W - M - d.textlength(right, font=rf), 11), right, font=rf, fill=INK)
    d.line([(M, 30), (W - M, 30)], fill=RULE, width=2)

    # masthead
    title = "Saturday 21 November 2026"
    tf = fit_font(d, title, SERIF_B, 74, CW)
    d.text(((W - d.textlength(title, font=tf)) / 2, 34), title, font=tf, fill=INK)
    sub = ("Climate summit runs past its deadline \u00b7 Three missiles shot down over Riyadh "
           "\u00b7 Russian strikes kill 12 in Ukraine")
    sf = font(SERIF_I, 17)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 112), sub, font=sf, fill=(60, 58, 50))

    # stat strip
    stats = [
        ("0", "climate deal agreed at COP31"),
        ("12", "killed in Ukraine strikes"),
        ("42", "hurt in the Kryvyi Rih strike"),
        ("146", "safe after a jet's engine-fire alert"),
        ("6.7", "magnitude of the Peru quake"),
        ("3", "missiles downed over Riyadh"),
    ]
    sy, sh = 136, 52
    cell = CW / 6
    nf = font(SANS_B, 30)
    cf = font(SANS, 10)
    for i, (num, cap) in enumerate(stats):
        cx0 = M + i * cell
        if i:
            d.line([(cx0, sy + 4), (cx0, sy + sh - 4)], fill=(180, 172, 150), width=1)
        d.text((cx0 + 8, sy), num, font=nf, fill=RED)
        lines = wrap(d, cap, cf, cell - 16)
        text_block(d, cx0 + 8, sy + 32, lines[:2], cf, (60, 58, 50), 12)
    d.line([(M, sy + sh + 2), (W - M, sy + sh + 2)], fill=RULE, width=1)

    # region bar
    regions = [("Europe", 9, (31, 78, 121)), ("Asia", 3, (176, 58, 46)),
               ("Middle East", 5, (125, 102, 8)), ("Africa", 3, (30, 132, 73)),
               ("Americas", 10, (108, 52, 131)), ("Oceania", 2, (20, 143, 119)),
               ("Global", 3, (93, 109, 126))]
    ry, rh = 196, 18
    total = sum(c for _, c, _ in regions)
    rx = M
    bf = font(SANS_B, 10)
    for name, cnt, col in regions:
        seg = CW * cnt / total
        d.rectangle([rx, ry, rx + seg - 1, ry + rh], fill=col)
        label = f"{name} {cnt}"
        tw = d.textlength(label, font=bf)
        if tw < seg - 6:
            d.text((rx + (seg - tw) / 2, ry + 3), label, font=bf, fill=(255, 255, 255))
        rx += seg

    # big cards
    by, bh = 222, 262
    bw = 322
    gap = (CW - 3 * bw) / 2
    big = [
        (1, "COP31: OVERTIME", "ANTALYA, T\u00dcRKIYE \u00b7 CLIMATE",
         "Climate summit runs into Saturday with no deal",
         "COP31 missed its Friday close; a draft with no fossil-fuel mention split nearly 200 countries. (AFP, Al Jazeera)",
         ill_cop31),
        (2, "SAUDI: MISSILES", "RIYADH \u00b7 WAR",
         "Three Houthi missiles shot down over Riyadh",
         "The Saudi-led coalition said three were destroyed over Riyadh before dawn, a day after it bombed Hodeidah port. (AFP, Reuters)",
         ill_riyadh),
        (3, "UKRAINE: STRIKES", "KRYVYI RIH \u00b7 WAR",
         "Russian strikes kill 12 in Ukraine",
         "A double-tap strike kills a boy and a medic in Kryvyi Rih; 42 hurt, officials say. Podil burns after a dawn missile. (Kyiv Post)",
         ill_ukraine),
    ]
    for i, (num, banner, loc, head, deck, ill) in enumerate(big):
        big_card(img, d, M + i * (bw + gap), by, bw, bh, num, banner, loc, head, deck, ill)

    # small cards: 2 rows x 5
    sw, sh2 = 192, 166
    sgap = (CW - 5 * sw) / 4
    GREEN = (30, 132, 73)
    BLUE = (31, 78, 121)
    small1 = [
        (4, "PERU: QUAKE 6.7", "JUN\u00cdN, PERU \u00b7 EARTHQUAKE",
         "Magnitude 6.7 earthquake shakes central Peru",
         "Deep quake near Carhuamayo, felt in Lima. No deaths. (USGS)",
         ill_peru, "OFFICIAL", GREEN),
        (5, "DAVAO: 146 SAFE", "DAVAO \u00b7 AVIATION",
         "Jet lands safely after engine-fire alert",
         "PX19 diverts to Davao; all 146 safe, evacuated by slides. (AP)",
         ill_davao, "OFFICIAL", GREEN),
        (6, "MERCURY: DUE 19:24 CET", "SPACE \u00b7 ESA",
         "BepiColombo closes on Mercury",
         "Capture due ~19:24 CET, after eight years. Two orbiters. (ESA)",
         ill_mercury, "OFFICIAL", GREEN),
        (7, "WARSAW: NATO", "WARSAW \u00b7 DIPLOMACY",
         "NATO chief in Warsaw after missiles land",
         "Rutte visits after the incursion; Warsaw seeks more NATO. (AP)",
         ill_warsaw, "OFFICIAL", GREEN),
        (8, "HORMUZ: DRONE", "STRAIT OF HORMUZ \u00b7 WAR",
         "Iran says it shot down a US drone",
         "The 58th MQ-9 claimed, IRGC says; no US confirmation. (Al Jazeera)",
         ill_hormuz, "CLAIM", RED),
    ]
    small2 = [
        (9, "BITCOIN: $58,983", "WORLD \u00b7 MARKETS",
         "Bitcoin trades below $59,000 on Saturday",
         "Down 3.9% in 24 hours; ether $1,625. (CoinGecko, 02:08 UTC)",
         ill_bitcoin, "OFFICIAL", GREEN),
        (10, "NIGERIA: BOAT", "BAYELSA \u00b7 DISASTER",
         "Nigeria funeral boat capsizes",
         "4 dead, 24 rescued, 100+ missing in Bayelsa. Search on. (Reuters)",
         ill_nigeria, "REPORTED", BLUE),
        (11, "GEN Z: 400 CITIES", "EUROPE \u00b7 PROTEST",
         "Youth march across Europe",
         "Rallies planned in 400 cities; protests go on Saturday. (AFP)",
         ill_genz, "REPORTED", BLUE),
        (12, "RAHUL: 136", "WELLINGTON \u00b7 CRICKET",
         "Rahul's 136 puts India in charge",
         "India 486-4 at stumps, 118 ahead of New Zealand. (Reuters)",
         ill_rahul, "OFFICIAL", GREEN),
        (13, "F1: VERSTAPPEN POLE", "LAS VEGAS \u00b7 FORMULA 1",
         "Verstappen takes Las Vegas pole",
         "Antonelli fastest but takes a 5-place grid penalty. (FIA)",
         ill_f1, "OFFICIAL", GREEN),
    ]
    for row, cards in enumerate([small1, small2]):
        y0 = 492 + row * (sh2 + 8)
        for i, (num, banner, loc, head, deck, ill, tag, tcol) in enumerate(cards):
            small_card(img, d, M + i * (sw + sgap), y0, sw, sh2, num, banner, loc, head, deck, ill, tag, tcol)

    # bottom: map + ALSO list
    my = 838
    mh = 142
    d.text((M, my), "WHERE IT HAPPENED", font=font(SANS_B, 11), fill=INK)
    draw_map(d, M, my + 16, 322, mh - 16)
    ax = M + 322 + 12
    aw = W - M - ax
    d.text((ax, my), "ALSO ON SATURDAY 21 NOVEMBER 2026 \u2014 22 MORE STORIES", font=font(SANS_B, 11), fill=INK)
    also = [
        ("Kyiv", "Zelensky: Crimea bridge \u201cwill not stay\u201d (NBC)"),
        ("Missouri", "Judge approves $7.25bn Roundup settlement (AFP)"),
        ("Bara, Sudan", "Army says it retook the city (claim) (Reuters)"),
        ("Geneva", "\u201cKiller robot\u201d talks end with 2028 aim (Reuters)"),
        ("Sejong", "Freight train derails, five cars off (Yonhap)"),
        ("Iraq", "Forces retake Jurf al-Sakhar (Reports)"),
        ("South Africa", "ANC wins 31%, worst since 1994 (BBC)"),
        ("Los Angeles", "LA fire suspect found guilty (AP)"),
        ("Washington", "Trump upbeat on Putin talks (AP)"),
        ("Washington", "US clears ~900,000 AI chips for China (House panel)"),
        ("Brussels", "EU pays out nearly \u20ac8bn to Ukraine (EU)"),
        ("Hodeidah", "Strikes hit port; UN warns aid lifeline (UN, AP)"),
        ("New York", "Banks hit in cyberattack on outside vendors (Reports)"),
        ("Brasilia", "Jailed Bolsonaro taken to hospital (DW)"),
        ("Atlantic", "Storm Xavier gale warnings narrow (Marine warning)"),
        ("California", "AG subpoenas Nvidia (Reuters)"),
        ("Canberra", "Australia and China agree to AI talks (ABC)"),
        ("Beijing", "China tells Japan to \u201ccorrect\u201d Taiwan words (AFP)"),
        ("Tehran", "Iran says uranium stock stays in country (Reuters)"),
        ("Washington", "Trump vows tax on data centres abroad (ABC)"),
        ("Turin", "Medvedev meets Zverev in tonight's semi (ATP)"),
        ("Antalya", "Panama threatens to block climate deal (Al Jazeera)"),
    ]
    af = font(SANS, 10)
    abf = font(SANS_B, 10)
    col_w = aw / 2
    for i, (place, txt) in enumerate(also):
        col = i // 11
        row = i % 11
        ix = ax + col * col_w
        iy = my + 16 + row * 11
        num = 14 + i
        d.text((ix, iy), f"{num} ", font=abf, fill=RED)
        nw = d.textlength(f"{num} ", font=abf)
        d.text((ix + nw, iy), f"{place}: ", font=abf, fill=INK)
        pw = d.textlength(f"{place}: ", font=abf)
        d.text((ix + nw + pw, iy), txt, font=af, fill=(60, 58, 50))

    # DATE CHECK
    dy = 984
    d.rectangle([M, dy, W - M, dy + 28], outline=RED, width=2)
    dcf = font(SANS, 10)
    dcb = font(SANS_B, 10)
    d.text((M + 6, dy + 3), "DATE CHECK", font=dcb, fill=RED)
    tw = d.textlength("DATE CHECK  ", font=dcb)
    body = ("Left out as Friday's news: Wall Street's correction, the Kyiv bridge barrage, missiles in "
            "Poland, the UK\u2013EU reset deal, Gaza strikes that killed six, Cyclone Akvan's landfall. "
            "Older: Voyager 1's light-day (18 Nov). Not yet happened: BepiColombo's capture "
            "(~19:24 CET today), any final COP31 text.")
    lines = wrap(d, body, dcf, CW - 12 - tw)
    text_block(d, M + 6 + tw, dy + 3, lines[:2], dcf, INK, 12)

    # footer
    d.text((M, 1014), "Every story here happened, or was first reported, on Saturday 21 November 2026. "
                      "Officials' counts and claims are attributed.",
           font=font(SANS, 9), fill=MUTED)
    src = "Sources named beside each story \u00b7 original drawings"
    d.text((W - M - d.textlength(src, font=font(SANS, 9)), 1014), src, font=font(SANS, 9), fill=MUTED)

    img.save(OUT, "JPEG", quality=88)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
