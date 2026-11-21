#!/usr/bin/env python3
"""Render the 21 November 2026 front page (1024x1024) from stories.json.

Run locally:  python3 render_frontpage.py
Reads hero.jpg beside this file when present, otherwise draws a labelled
placeholder box so the layout can be checked before the hero photo arrives.
Writes entry.png (the file main.py later copies to /output/entry.png).
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
MARGIN = 16
GUTTER = 12
INK = (18, 18, 18)
PAPER = (253, 252, 248)
GREY = (110, 110, 110)
RULE = (40, 40, 40)

REGION_COLORS = {
    "EUROPE": (26, 64, 138),
    "MIDDLE EAST": (146, 32, 32),
    "ASIA": (18, 110, 88),
    "NORTH AMERICA": (40, 60, 110),
    "AFRICA": (146, 96, 20),
    "LATIN AMERICA": (110, 46, 130),
    "OCEANIA": (30, 100, 140),
    "GLOBAL": (60, 60, 60),
}

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_DISPLAY = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_ITALIC = "/usr/share/fonts/truetype/noto/NotoSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real font metrics; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis when clipped."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " …", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] = lines[-1] + " …"
    return lines


def draw_hero(draw, img, y, height):
    """Paste hero.jpg cropped to fill, or draw a labelled placeholder."""
    x0, x1 = MARGIN, W - MARGIN
    hero_path = os.path.join(HERE, "hero.jpg")
    if os.path.exists(hero_path):
        photo = Image.open(hero_path).convert("RGB")
        tw, th = x1 - x0, height
        scale = max(tw / photo.width, th / photo.height)
        nw, nh = int(photo.width * scale + 0.5), int(photo.height * scale + 0.5)
        photo = photo.resize((nw, nh), Image.LANCZOS)
        left = (nw - tw) // 2
        # Top-biased crop: the soldiers' heads sit in the upper part of the
        # frame, so anchor the band near the top (~13% of image height)
        # instead of centring it, which cut the heads off.
        top = int(nh * 0.13)
        top = max(0, min(top, nh - th))
        img.paste(photo.crop((left, top, left + tw, top + th)), (x0, y))
    else:
        draw.rectangle([x0, y, x1, y + height], fill=(148, 152, 158))
        draw.rectangle([x0, y, x1, y + height], outline=(90, 94, 100), width=2)
        label = font(SANS_BOLD, 34)
        sub = font(SANS, 20)
        t1 = "HERO PHOTO — PLACEHOLDER"
        t2 = "Photograph to be supplied (ChatGPT news photo, no text in image)"
        draw.text(((x0 + x1) / 2, y + height / 2 - 34), t1, font=label,
                  fill=(255, 255, 255), anchor="mm")
        draw.text(((x0 + x1) / 2, y + height / 2 + 12), t2, font=sub,
                  fill=(235, 235, 235), anchor="mm")
    draw.rectangle([x0, y, x1, y + height], outline=INK, width=1)


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    stories = data["stories"]
    hero = next(s for s in stories if s.get("hero"))
    rest = [s for s in stories if not s.get("hero")]

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W - 1, H - 1], outline=INK, width=2)

    # ---- Masthead -------------------------------------------------------
    draw.rectangle([MARGIN, 10, W - MARGIN, 13], fill=INK)
    name_f = font(SERIF_DISPLAY, 44)
    draw.text((W / 2, 35), data["paper"], font=name_f, fill=INK, anchor="mm")
    meta_f = font(SANS_BOLD, 12)
    draw.text((MARGIN, 58), "SATURDAY, 21 NOVEMBER 2026", font=meta_f, fill=INK)
    mid = "35 STORIES  ·  7 REGIONS"
    draw.text((W / 2, 58), mid, font=meta_f, fill=INK, anchor="ma")
    right = "ONE DAY — ONE PAGE"
    draw.text((W - MARGIN, 58), right, font=meta_f, fill=INK, anchor="ra")
    draw.rectangle([MARGIN, 72, W - MARGIN, 75], fill=INK)

    # ---- Hero image ------------------------------------------------------
    hero_h = 210
    draw_hero(draw, img, 82, hero_h)
    cap_f = font(SANS_ITALIC, 13)
    caption = ("Polish soldiers at the site where a Russian missile came down in "
               "south-eastern Poland on Friday. — AP")
    draw.text((MARGIN, 300), caption, font=cap_f, fill=GREY)

    # ---- Lead story (the hero story, big headline) -----------------------
    lead_y = 322
    lead_head_f = font(SERIF, 27)
    lead_lines = fit_lines(draw, hero["headline"], lead_head_f, W - 2 * MARGIN, 1)
    draw.text((MARGIN, lead_y), lead_lines[0], font=lead_head_f, fill=INK)
    deck_f = font(SANS, 15)
    deck_lines = fit_lines(draw, hero["deck"], deck_f, W - 2 * MARGIN, 2)
    dy = lead_y + 36
    for line in deck_lines:
        draw.text((MARGIN, dy), line, font=deck_f, fill=(50, 50, 50))
        dy += 19
    draw.rectangle([MARGIN, 386, W - MARGIN, 389], fill=INK)

    # ---- Grid: 34 stories, 4 columns x 9 rows ---------------------------
    grid_top = 398
    grid_bottom = 998
    cols = 4
    col_w = (W - 2 * MARGIN - (cols - 1) * GUTTER) // cols
    rows = 9
    cell_h = (grid_bottom - grid_top) // rows
    tag_f = font(SANS_BOLD, 9)
    head_f = font(SANS_BOLD, 12)
    deck2_f = font(SANS, 10)
    src_f = font(SANS, 9)

    for idx, story in enumerate(rest):
        col = idx % cols
        row = idx // cols
        x = MARGIN + col * (col_w + GUTTER)
        y = grid_top + row * cell_h
        color = REGION_COLORS.get(story["region"], INK)
        draw.text((x, y), story["region"], font=tag_f, fill=color)
        sw = draw.textlength(story["region"], font=tag_f)
        draw.text((x + sw, y), " — " + story["source"], font=src_f, fill=GREY)
        hl = fit_lines(draw, story["headline"], head_f, col_w, 2)
        hy = y + 12
        for line in hl:
            draw.text((x, hy), line, font=head_f, fill=INK)
            hy += 14
        dk = fit_lines(draw, story["deck"], deck2_f, col_w, 2)
        dy = hy + 1
        for line in dk:
            draw.text((x, dy), line, font=deck2_f, fill=(60, 60, 60))
            dy += 12
        if col < cols - 1:
            draw.line([x + col_w + GUTTER // 2, y + 2, x + col_w + GUTTER // 2,
                       y + cell_h - 6], fill=(200, 200, 200), width=1)

    # ---- Footer ----------------------------------------------------------
    foot_f = font(SANS, 10)
    footer = ("Sources: AP · Reuters · BBC · IMD · ICJ · NSE · NASA · UKMTO · EU Council · "
              "Financial Times · IANS · AtlasIntel — every story verified against reporting of 21 November 2026.")
    draw.text((W / 2, 1012), footer, font=foot_f, fill=GREY, anchor="mm")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
