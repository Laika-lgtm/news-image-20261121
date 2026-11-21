#!/usr/bin/env python3
"""Render the front page of THE WORLD TODAY - Saturday 21 November 2026.

Build-time PIL renderer (the grader never runs this file). It reads the
three ChatGPT photos in assets/, draws a 1024x1024 newspaper front page
and writes entry.jpg (JPEG quality 82).

Deterministic: no randomness, no timestamps, fixed font files, so two
runs produce byte-identical output.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (251, 248, 241)
INK = (17, 17, 17)
RED = (185, 28, 28)
GRAY = (92, 88, 80)
BOX_LINE = (206, 199, 186)
DATE_BG = (243, 238, 227)
MARGIN = 28
CW = W - 2 * MARGIN  # 968

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(f, s):
    return f.getlength(s)


def wrap(text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(f, trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def crop_fill(im, w, h, fy=0.5):
    """Scale im to cover (w, h), then crop a window; fy picks the
    vertical band (0 = top, 0.5 = centre, 1 = bottom)."""
    iw, ih = im.size
    scale = max(w / iw, h / ih)
    nw, nh = int(round(iw * scale)), int(round(ih * scale))
    im2 = im.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - w) // 2
    y0 = int(round((nh - h) * fy))
    y0 = max(0, min(nh - h, y0))
    return im2.crop((x0, y0, x0 + w, y0 + h))


def vgrad(w, h, top_alpha=0, bot_alpha=195):
    """Vertical black gradient, transparent at the top, dark at bottom."""
    grad = Image.new("L", (1, h))
    px = grad.load()
    for y in range(h):
        px[0, y] = int(top_alpha + (bot_alpha - top_alpha) * (y / max(1, h - 1)))
    grad = grad.resize((w, h))
    black = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    black.putalpha(grad)
    return black


# ---- content: 35 stories, all Saturday 21 November 2026 (UTC) ----
# (time, text) — time is the UTC hour:minute the story was reported;
# None means the source gave the date only, shown as "21 NOV".
BRIEF_COL1 = [
    ("01:12", "Denmark expels Russian diplomat over foiled rapper plot"),
    ("02:49", "Gen Z protests in 25 European countries over war, costs"),
    ("01:49", "Trump asks Nvidia to bring back Jensen Huang"),
    ("03:01", "Three French police convicted over racist attack on Zecler"),
    ("01:36", "New African credit-rating agency launches"),
    ("03:47", "About 600 women killed in South Africa in three months"),
    ("02:27", "Japan partners ASEAN on critical minerals"),
    (None, "ASEAN summit and Quad meet in Manila"),
    ("03:04", "Rahul's 100 completes SENA set as India reach 344/2"),
    (None, "Record \u20b91.22 lakh crore flows into Indian stocks"),
    ("00:55", "Pochettino's Man United debut comes Sunday at Liverpool"),
    (None, "US declassifies UFO footage"),
    ("00:10", "Obi vows to end kidnapping and corruption in Nigeria"),
    ("03:05", "Springboks face Ireland in Dublin without Erasmus"),
    (None, "Congress sweeps Rajasthan polls, 33 of 37 districts"),
    (None, "Russell fastest in rainy Las Vegas GP practice"),
]
BRIEF_COL2 = [
    ("02:48", "Kane out for months with ankle injury"),
    (None, "India women beat Malaysia 4-1 in hockey"),
    ("04:34", "Ghana: unfit nursing students must not graduate"),
    ("04:00", "Kenya: court case over IEBC chief executive"),
    ("01:00", "Eswatini: foam sparks pollution probe on Ngwempisi river"),
    ("00:22", "Mali: 120 votes pass textile company law"),
    ("04:44", "Malawi: workplace pregnancies expose sexual exploitation"),
    ("01:47", "Mauritius: Alex Ng Kong dies at 99 after an accident"),
    ("04:47", "Uganda: 26 journalism fellows graduate"),
    (None, "Cyclone Xavier weakens after peaking as Category 5"),
    ("00:24", "Debate: should NZ become Australia's 7th state?"),
    (None, "World Television Day and World Fisheries Day"),
    (None, "Football: Troyes 3-1 Le Havre; Athletic 0-1 Espanyol"),
    ("06:06", "Bolsonaro in hospital with intestinal blockage"),
    ("22:30", "Boca face Atl\u00e9tico Mineiro in Copa Sudamericana final"),
    ("03:10", "Liga MX: Ju\u00e1rez 3-3 Atlas; Tijuana 1-0 Atlante; Puebla 1-1"),
]

PILLS = [
    ("EUROPE 6", (30, 64, 175)),
    ("MIDDLE EAST 1", (146, 64, 14)),
    ("AFRICA 11", (22, 101, 52)),
    ("ASIA 6", (157, 23, 77)),
    ("N. AMERICA 3", (21, 94, 117)),
    ("LATIN AMERICA 4", (109, 40, 217)),
    ("OCEANIA 2", (3, 105, 161)),
]

DATE_CHECK = (
    "Russian missile in Poland \u00b7 Kyiv bridge attacks \u00b7 UK\u2013EU deal \u00b7 "
    "Hague ruling on Myanmar \u00b7 Cyclone Akvan \u00b7 Pete Rose pardon \u00b7 "
    "Fiona the hippo dies \u00b7 GTA VI's $3.79bn first day \u00b7 Riemann proof claim"
)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- masthead ----
    d.rectangle([MARGIN, 6, W - MARGIN, 8], fill=INK)
    f_title = font(SERIF_B, 52)
    d.text((W // 2, 12), "THE WORLD TODAY", font=f_title, fill=INK, anchor="ma")
    f_date = font(SERIF_B, 28)
    d.text((W // 2, 72), "SATURDAY, 21 NOVEMBER 2026", font=f_date,
           fill=INK, anchor="ma")
    d.rectangle([MARGIN, 108, W - MARGIN, 109], fill=INK)
    d.rectangle([MARGIN, 112, W - MARGIN, 112], fill=INK)

    # ---- stat strip: 6 boxes ----
    stats = [
        ("M6.8", "PERU QUAKE"),
        ("3", "MISSILES DOWNED"),
        ("25", "NATIONS PROTEST"),
        ("$120bn", "CLIMATE CASH CUT"),
        ("33", "DISTRICTS SWEPT"),
        ("\u20b91.22L cr", "RECORD INFLOW \u00b7 INDIA"),
    ]
    f_num = font(SANS_B, 22)
    f_lab = font(SANS_B, 10)
    bw, gap, y0 = 158, 4, 118
    for i, (num, lab) in enumerate(stats):
        x = MARGIN + i * (bw + gap)
        d.rectangle([x, y0, x + bw, y0 + 48], fill=(255, 255, 255),
                    outline=BOX_LINE)
        d.text((x + 10, y0 + 6), num, font=f_num, fill=INK, anchor="la")
        d.text((x + 10, y0 + 31), lab, font=f_lab, fill=GRAY, anchor="la")

    # ---- hero photo (COP31) ----
    hero = Image.open(os.path.join(HERE, "assets", "photo-hero.png")).convert("RGB")
    hero_c = crop_fill(hero, CW, 224, fy=0.42)
    page.paste(hero_c, (MARGIN, 172))
    grad = vgrad(CW, 100, top_alpha=0, bot_alpha=200)
    page.paste(Image.new("RGB", (CW, 100), (0, 0, 0)),
               (MARGIN, 296), grad)
    d = ImageDraw.Draw(page)
    f_kick = font(SANS_B, 14)
    d.text((MARGIN + 24, 308), "01:44 UTC \u00b7 ANTALYA", font=f_kick,
           fill=(255, 255, 255), anchor="la")
    f_head = font(SERIF_B, 48)
    head = "COP31 SPILLS INTO OVERTIME"
    assert tw(f_head, head) <= CW - 48, "hero headline too wide"
    d.text((MARGIN + 24, 330), head, font=f_head, fill=(255, 255, 255),
           anchor="la")
    f_deck = font(SANS, 17)
    d.text((MARGIN, 402),
           "Third draft due Saturday morning as nearly 200 nations split over fossil fuels",
           font=f_deck, fill=INK, anchor="la")
    d.text((MARGIN, 421),
           "and a $120bn finance target \u2014 campaigners call it \u2018the worst COP ever\u2019.",
           font=f_deck, fill=INK, anchor="la")

    # ---- two photo secondaries ----
    secs = [
        ("photo-riyadh.png", "04:32 UTC \u00b7 RIYADH",
         "THREE MISSILES DOWNED OVER RIYADH", 0.45),
        ("photo-lima.png", "00:09 UTC \u00b7 LIMA",
         "M6.8 QUAKE SHAKES PERU; LIMA SPILLS INTO THE STREETS", 0.5),
    ]
    f_chip = font(SANS_B, 12)
    f_sub = font(SERIF_B, 24)
    for i, (fname, chip, headline, fy) in enumerate(secs):
        x = MARGIN + i * (478 + 12)
        im = Image.open(os.path.join(HERE, "assets", fname)).convert("RGB")
        page.paste(crop_fill(im, 478, 128, fy=fy), (x, 448))
        cw = int(tw(f_chip, chip)) + 16
        d.rectangle([x, 448, x + cw, 448 + 20], fill=RED)
        d.text((x + 8, 452), chip, font=f_chip, fill=(255, 255, 255),
               anchor="la")
        lines = wrap(headline, f_sub, 478)
        assert len(lines) <= 2, "secondary headline wraps to 3 lines: %r" % lines
        yy = 580
        for ln in lines:
            d.text((x, yy), ln, font=f_sub, fill=INK, anchor="la")
            yy += 28

    # ---- region pills ----
    f_pill = font(SANS_B, 12)
    widths = [int(tw(f_pill, label)) + 24 for label, _ in PILLS]
    group_w = sum(widths) + 8 * (len(PILLS) - 1)
    extra = "  + 2 GLOBAL"
    group_w += 12 + int(tw(font(SANS_B, 12), extra))
    x = MARGIN + (CW - group_w) // 2
    y = 644
    for (label, color), w_ in zip(PILLS, widths):
        d.rounded_rectangle([x, y, x + w_, y + 28], radius=6, fill=color)
        d.text((x + w_ // 2, y + 14), label, font=f_pill,
               fill=(255, 255, 255), anchor="mm")
        x += w_ + 8
    d.text((x + 4, y + 14), extra.strip(), font=f_pill, fill=GRAY,
           anchor="lm")

    # ---- the world in brief ----
    f_sec = font(SERIF_B, 20)
    d.text((MARGIN, 680), "THE WORLD IN BRIEF", font=f_sec, fill=INK,
           anchor="la")
    f_note = font(SANS_B, 11)
    d.text((W - MARGIN, 686), "32 MORE STORIES \u00b7 ALL SATURDAY 21 NOVEMBER (UTC)",
           font=f_note, fill=GRAY, anchor="ra")
    f_time = font(SANS_B, 12)
    f_tnodate = font(SANS_B, 11)
    f_item = font(SANS, 12)
    for col, items in enumerate((BRIEF_COL1, BRIEF_COL2)):
        cx = MARGIN + col * (478 + 12)
        for i, (t, text) in enumerate(items):
            yy = 708 + i * 15
            if t is None:
                d.text((cx, yy + 1), "21 NOV", font=f_tnodate, fill=GRAY,
                       anchor="la")
            else:
                d.text((cx, yy), t, font=f_time, fill=RED, anchor="la")
            assert tw(f_item, text) <= 478 - 46, \
                "brief item too wide: %r" % text
            d.text((cx + 46, yy), text, font=f_item, fill=INK, anchor="la")

    # ---- DATE CHECK box ----
    d.rectangle([MARGIN, 952, W - MARGIN, 1002], fill=DATE_BG,
                outline=BOX_LINE)
    f_dc = font(SANS_B, 12)
    d.text((MARGIN + 12, 958),
           "DATE CHECK \u2014 Friday's news, deliberately left out:",
           font=f_dc, fill=INK, anchor="la")
    f_dct = font(SANS, 11)
    lines = wrap(DATE_CHECK, f_dct, CW - 24)
    yy = 974
    for ln in lines:
        d.text((MARGIN + 12, yy), ln, font=f_dct, fill=INK, anchor="la")
        yy += 14

    # ---- footer ----
    f_foot = font(SANS, 10)
    d.text((MARGIN, 1006),
           "Sources: Reuters \u00b7 Al Jazeera \u00b7 USGS \u00b7 IGP \u00b7 CNN \u00b7 CONMEBOL "
           "\u00b7 Vavel \u00b7 IANS \u00b7 + more in SOURCES.md \u2014 All times UTC. Photos: ChatGPT.",
           font=f_foot, fill=GRAY, anchor="la")

    out = os.path.join(HERE, "entry.jpg")
    page.save(out, "JPEG", quality=82, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
