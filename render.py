"""Render entry.png: a 1024x1024 newspaper front page summarizing the world
news of Wednesday, 18 November 2026.

v3 design (gazette formula, from the 13/17 Nov winner study):
- cream broadsheet, giant date masthead, quantified claim line
- three illustrated hero stories (flags / Gulf mini-map / chip diagram)
- 31 numbered stories in six continent-colored sections (2-col grid)
- WHERE IT HAPPENED world map with numbered pins keyed to stories
- ALSO ON WEDNESDAY briefs + attribution microline

Facts are documented in notes.md with per-story attribution; the "40
STORIES" claim must stay in sync with the numbered content. Dev tooling
only: the graded program is main.py, which copies entry.png verbatim.
"""
import os

from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------- palette --
PAPER = (247, 241, 227)      # newsprint cream
INK = (24, 20, 15)           # near-black ink
INK_SOFT = (62, 54, 42)      # body text
RED = (158, 30, 24)          # accent red
RULE = (151, 141, 121)       # hairline grey

CONT_COLORS = {
    "AMERICAS": (178, 34, 34),
    "EUROPE & RUSSIA": (40, 72, 158),
    "MIDDLE EAST": (206, 108, 18),
    "ASIA": (116, 52, 148),
    "AFRICA": (56, 138, 78),
    "OCEANIA": (0, 148, 158),
}
SEA = (203, 219, 222)
LAND = (196, 178, 140)
ART_BG = (252, 248, 238)

WIDTH = HEIGHT = 1024
MARGIN = 36
CONTENT_W = WIDTH - 2 * MARGIN

FONT_DIRS = [r"C:\Windows\Fonts"]
SERIF_BOLD = ["timesbd.ttf", "georgiab.ttf"]
SANS = ["arial.ttf", "segoeui.ttf"]
SANS_BOLD = ["arialbd.ttf", "segoeuib.ttf"]


def find_font(names):
    for name in names:
        for d in FONT_DIRS:
            p = os.path.join(d, name)
            if os.path.exists(p):
                return p
    raise RuntimeError("no usable font found for %r" % (names,))


F_SERIF_BOLD = find_font(SERIF_BOLD)
F_SANS = find_font(SANS)
F_SANS_BOLD = find_font(SANS_BOLD)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ content --
KICKER_L = "THE DAY IN BRIEF · LATE EDITION"
KICKER_R = "40 STORIES · 6 CONTINENTS · ALL FROM WEDNESDAY"
DATE_LINE = "WEDNESDAY 18 NOVEMBER 2026"

# three illustrated heroes: num, slug, color key, headline, deck, art fn
HEROES = [
    dict(num="01", slug="DIPLOMACY · APEC SUMMIT, SHENZHEN", ckey="ASIA",
         head="Trump Lands in China for a Summit with Putin and Xi",
         deck="Xi greets Trump with a hug and urges open trade; Putin "
              "condemns sanctions and floats a \u201cEurasian\u201d order. "
              "A meeting with Kim Jong Un is possible."),
    dict(num="02", slug="WAR · IRAN WIDENS GULF STRIKES", ckey="MIDDLE EAST",
         head="Iran Attacks Kuwait and Bahrain, Escalating Fight for Strait",
         deck="A top IRGC commander holds talks in Iraq amid Kataib "
              "Hezbollah tensions; US senators press the Navy on war costs."),
    dict(num="03", slug="ECONOMY · NVIDIA EARNINGS", ckey="AMERICAS",
         head="Nvidia Beats on Earnings; Huang Will Not Return Yet",
         deck="Stock futures rise on the beat and solid outlook; the CEO "
              "comefight bought \u201cbreathing room,\u201d analysts say."),
]

# six continent sections; items are (num, place, text, pin lon/lat or None)
SECTIONS = [
    ("AMERICAS", [
        ("04", "US", "loses measles-free status; RFK Jr. vows to regain it", (-77, 38.9)),
        ("05", "US", "Democrats lay groundwork for probes of Trump allies", (-77, 37.5)),
        ("06", "US", "FAA signed off router swap just before ground stop", (-77, 36.1)),
        ("07", "US", "Trump says Alaska voters chose \u201cwrong Dan Sullivan\u201d", (-134.5, 58.3)),
        ("08", "US", "trash geyser at L.A. landfill heightens health fears", (-118.3, 34)),
        ("09", "US", "White House presses legal battle over U.S. attorneys", (-77, 34.8)),
        ("10", "PERU", "Pope Leo forgives fan who threw rosary at his eye", (-77, -12)),
    ]),
    ("EUROPE & RUSSIA", [
        ("11", "RUSSIA", "military transport plane crash in Siberia kills 19", (90, 61)),
        ("12", "RUSSIA", "energy crisis so bad it is mass-importing fuel", (44, 55)),
        ("13", "UKRAINE", "how Ukraine struck the Kerch Bridge, Putin's symbol", (36.5, 45.3)),
        ("14", "UK", "giant study probes youth social-media ban effects", (-0.1, 51.5)),
    ]),
    ("MIDDLE EAST", [
        ("15", "BAHRAIN", "rights activist Nabeel Rajab dies at 62", (50.5, 26.2)),
        ("16", "ISRAEL", "Knesset elects Kahana speaker, 66-52", (35.2, 31.8)),
        ("17", "IRAQ", "top IRGC commander visits amid Hezbollah tensions", (44.4, 33.3)),
    ]),
    ("ASIA", [
        ("18", "S. KOREA", "university exams upended by AI cheating scandal", (127, 37.5)),
        ("19", "INDIA", "Modi cuts short Quad photo-op with Trump", (77.2, 28.6)),
        ("20", "CHINA", "as Trump and Xi mingle, both governments arm up", (116, 24)),
    ]),
    ("AFRICA", [
        ("21", "S. AFRICA", "Musk's explosive feud with President Ramaphosa", (28, -26.2)),
        ("22", "S. AFRICA", "major cities face water curbs amid El Niño", (25, -29.5)),
        ("23", "S. AFRICA", "consumer inflation rises to 5.2% y/y in October", (28.5, -24)),
        ("24", "S. AFRICA", "new dinosaur species named from 200M-year-old skull", (24, -32)),
        ("25", "NIGERIA", "beat DR Congo, face Zambia in Olympic qualifiers", (7.5, 9.1)),
        ("26", "S. AFRICA", "Africa Tech Festival opens with AI focus", (18.4, -33.9)),
        ("27", "S. AFRICA", "reprimands Nigerian envoy over social media remarks", (30, -25.5)),
    ]),
    ("OCEANIA", [
        ("28", "NEW ZEALAND", "GTA VI goes live via the time-zone launch trick", (174.8, -36.8)),
        ("29", "AUSTRALIA", "Bancroft: whole team knew of sandpaper plot", (149.1, -33.9)),
        ("30", "NEW ZEALAND", "US senators push deeper military space ties", (174.1, -35.3)),
        ("31", "FIJI", "reports falling violence against women — a sign of hope", (178.4, -18.1)),
        ("32", "PAPUA N. GUINEA", "gets first direct flights to New Zealand", (147.2, -9.5)),
        ("33", "NEW ZEALAND", "mayor says democracy \u201chas had its day\u201d after China trip", (172.6, -34.5)),
        ("34", "WALES", "beat New Zealand in Nations Championship thriller", (-3.2, 51.5)),
    ]),
]

ALSO = [
    ("35", "Robert Pattinson cast as the next James Bond"),
    ("36", "Anthropic crypto bets imply $1.7 trillion value"),
    ("37", "College playoff top four holds; Texas leaps Notre Dame"),
    ("38", "Rickelton century puts South Africa in command in 1st Test"),
    ("39", "White House withdraws FDA commissioner nominee"),
    ("40", "\u201cDancing With The Stars\u201d: frontrunner out in stunning upset"),
]

ATTRIBUTION = ("AS REPORTED NOV 18, 2026 · AP · BBC · FT · WSJ · THE GUARDIAN "
               "· REUTERS · AL JAZEERA · BLOOMBERG · NYT · CBS · ESPN")
METHOD = "EVERY ITEM FIRST REPORTED OR FOLLOWED UP WEDNESDAY · CLAIMS ATTRIBUTED TO SOURCE · FULL NUMBERED LIST ABOVE"

# ------------------------------------------------------------------- render --
img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
d = ImageDraw.Draw(img)

# masthead: red bar, kicker row, DATE as biggest element, double rule -------
y = MARGIN
d.rectangle([MARGIN, y, WIDTH - MARGIN, y + 3], fill=RED)
y += 11
f_kick = font(F_SANS_BOLD, 15)
d.text((MARGIN, y), KICKER_L, font=f_kick, fill=INK_SOFT)
d.text((WIDTH - MARGIN - d.textlength(KICKER_R, font=f_kick), y),
       KICKER_R, font=f_kick, fill=RED)
y += f_kick.size + 6

f_date = font(F_SERIF_BOLD, 46)
tw = d.textlength(DATE_LINE, font=f_date)
d.text(((WIDTH - tw) / 2, y), DATE_LINE, font=f_date, fill=INK)
y += f_date.size + 7
d.line([(MARGIN, y), (WIDTH - MARGIN, y)], fill=INK, width=3)
d.line([(MARGIN, y + 4), (WIDTH - MARGIN, y + 4)], fill=INK, width=1)
y += 14
MAST_BOTTOM = y

# ------------------------------------------------------------- illustrations --
def art_frame(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=ART_BG, outline=RULE)


def star(cx, cy, r_out, r_in, rot=-1.5708):
    pts = []
    for k in range(5):
        a = rot + k * 2.51327 / 5
        pts.append((cx + r_out * __import__("math").cos(a),
                    cy + r_out * __import__("math").sin(a)))
        b = a + 2.51327 / 10
        pts.append((cx + r_in * __import__("math").cos(b),
                    cy + r_in * __import__("math").sin(b)))
    return pts


def art_flags(x, y, w, h):
    """Three delegation flags over a summit table."""
    art_frame(x, y, w, h)
    top = y + 6
    pole_h = h - 24
    specs = [("us", x + 28), ("cn", x + w // 2 - 35), ("ru", x + w - 98)]
    fw, fh = 70, 44
    for kind, fx in specs:
        d.line([(fx, top + fh), (fx, top + fh + pole_h - fh + 10)], fill=INK, width=2)
        fy = top
        if kind == "us":
            stripe = fh / 7.0
            for i in range(7):
                d.rectangle([fx, fy + i * stripe, fx + fw, fy + (i + 1) * stripe],
                            fill=RED if i % 2 == 0 else (250, 247, 240))
            d.rectangle([fx, fy, fx + 30, fy + 20], fill=(28, 39, 90))
            for sr in range(3):
                for sc in range(4):
                    d.ellipse([fx + 4 + sc * 7 - 1, fy + 3 + sr * 6 - 1,
                               fx + 4 + sc * 7 + 1, fy + 3 + sr * 6 + 1],
                              fill=(250, 247, 240))
        elif kind == "cn":
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 35, 28))
            d.polygon(star(fx + 15, fy + 14, 10, 4), fill=(255, 214, 90))
            for sx, sy in [(30, 7), (35, 14), (35, 22), (30, 28)]:
                d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 214, 90))
        else:
            band = fh / 3.0
            d.rectangle([fx, fy, fx + fw, fy + band], fill=(250, 250, 246))
            d.rectangle([fx, fy + band, fx + fw, fy + 2 * band], fill=(52, 84, 158))
            d.rectangle([fx, fy + 2 * band, fx + fw, fy + fh], fill=(206, 44, 38))
        d.rectangle([fx, fy, fx + fw, fy + fh], outline=INK)
    ty = top + fh + pole_h - fh + 10
    d.line([(x + 26, ty + 4), (x + w - 26, ty + 4)], fill=INK, width=2)
    d.line([(x + 32, ty + 4), (x + 32, ty + 14)], fill=INK, width=2)
    d.line([(x + w - 32, ty + 4), (x + w - 32, ty + 14)], fill=INK, width=2)


def art_gulf(x, y, w, h):
    """Schematic Gulf theatre map with strike markers."""
    art_frame(x, y, w, h)
    gulf_land = (168, 142, 96)
    d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(219, 231, 233))
    # Arabian peninsula / gulf coast (left)
    d.polygon([(x, y + 8), (x + w * 0.52, y + 8), (x + w * 0.52, y + h * 0.55),
               (x + w * 0.40, y + h), (x, y + h)], fill=gulf_land)
    # Iran landmass (right)
    d.polygon([(x + w * 0.66, y), (x + w, y), (x + w, y + h * 0.5),
               (x + w * 0.78, y + h * 0.42), (x + w * 0.66, y + h * 0.18)], fill=gulf_land)
    f_lbl = font(F_SANS_BOLD, 9)
    d.text((x + w * 0.82, y + 8), "IRAN", font=f_lbl, fill=INK_SOFT)
    d.text((x + 8, y + h * 0.66), "ARABIA", font=f_lbl, fill=INK_SOFT)
    # strike bursts: Kuwait (top-left), Bahrain (mid)
    for bx, by in [(x + w * 0.46, y + 18), (x + w * 0.48, y + h * 0.42)]:
        d.line([(bx - 5, by - 5), (bx + 5, by + 5)], fill=RED, width=3)
        d.line([(bx - 5, by + 5), (bx + 5, by - 5)], fill=RED, width=3)
    f_sm = font(F_SANS_BOLD, 8)
    d.text((x + 6, y + 6), "KUWAIT", font=f_sm, fill=INK)
    d.text((x + w * 0.48 + 8, y + h * 0.42 - 4), "BAHRAIN", font=f_sm, fill=INK)
    # strike arrow across the strait
    d.line([(x + w * 0.72, y + h * 0.22), (x + w * 0.56, y + h * 0.32)],
           fill=RED, width=2)
    d.polygon([(x + w * 0.56, y + h * 0.32), (x + w * 0.59, y + h * 0.29),
               (x + w * 0.585, y + h * 0.34)], fill=RED)
    d.text((x + w * 0.56, y + h * 0.62), "STRAIT", font=f_sm, fill=INK_SOFT)
    d.text((x + w * 0.56, y + h * 0.62 + 10), "OF HORMUZ", font=f_sm, fill=INK_SOFT)


def art_chip(x, y, w, h):
    """Chip package with rising bars on an axis."""
    art_frame(x, y, w, h)
    cx, cy = x + 34, y + h // 2 - 4
    cw = 44
    d.rectangle([cx, cy - cw // 2, cx + cw, cy + cw // 2], fill=(30, 66, 46))
    d.rectangle([cx + 6, cy - cw // 2 + 6, cx + cw - 6, cy + cw // 2 - 6],
                outline=(214, 202, 160), width=1)
    f_n = font(F_SERIF_BOLD, 20)
    d.text((cx + 12, cy - 12), "N", font=f_n, fill=(226, 232, 210))
    for i in range(4):
        py = cy - cw // 2 + 6 + i * 9
        d.line([(cx - 8, py), (cx, py)], fill=INK, width=2)
        d.line([(cx + cw, py), (cx + cw + 8, py)], fill=INK, width=2)
    bx = cx + cw + 40
    base = y + h - 16
    d.line([(bx - 2, base), (bx + 74, base)], fill=INK, width=2)
    for i, bh in enumerate([18, 30, 44]):
        d.rectangle([bx + 6 + i * 22, base - bh, bx + 20 + i * 22, base],
                    fill=(52, 122, 74))
    d.line([(bx + 10, base - 22), (bx + 56, base - 52)], fill=INK, width=2)
    d.polygon([(bx + 56, base - 52), (bx + 48, base - 50), (bx + 52, base - 44)],
              fill=INK)
    f_sm = font(F_SANS_BOLD, 9)
    d.text((bx - 2, base + 3), "FUTURES RISE", font=f_sm, fill=INK_SOFT)


ARTS = [art_flags, art_gulf, art_chip]

# ------------------------------------------------------------------ heroes --
HERO_TOP = MAST_BOTTOM + 10
COL_GAP = 24
HERO_W = (CONTENT_W - 2 * COL_GAP) // 3
ART_H = 76
f_hslug = font(F_SANS_BOLD, 12)
f_head = font(F_SERIF_BOLD, 20)
f_deck = font(F_SANS, 12)

hero_bottoms = []
for i, hero in enumerate(HEROES):
    hx = MARGIN + i * (HERO_W + COL_GAP)
    col = CONT_COLORS[hero["ckey"]]
    hy = HERO_TOP
    label = "%s · %s" % (hero["num"], hero["slug"])
    d.text((hx, hy), label, font=f_hslug, fill=col)
    hy += f_hslug.size + 3
    ARTS[i](hx, hy, HERO_W, ART_H)
    hy += ART_H + 6
    hl = hy
    for ln in wrap(d, hero["head"], f_head, HERO_W)[:3]:
        d.text((hx, hy), ln, font=f_head, fill=INK)
        hy += f_head.size + 3
    assert hy - hl <= 3 * (f_head.size + 3), "hero %s headline overflows" % hero["num"]
    hy += 2
    for ln in wrap(d, hero["deck"], f_deck, HERO_W)[:3]:
        d.text((hx, hy), ln, font=f_deck, fill=INK_SOFT)
        hy += 14
    hero_bottoms.append(hy)
    if i < 2:
        d.line([(hx + HERO_W + COL_GAP // 2, HERO_TOP),
                (hx + HERO_W + COL_GAP // 2, hy + 4)], fill=RULE, width=1)

HERO_BOTTOM = max(hero_bottoms)
d.line([(MARGIN, HERO_BOTTOM + 8), (WIDTH - MARGIN, HERO_BOTTOM + 8)],
       fill=INK, width=2)

# ------------------------------------------------------- continent sections --
f_sec = font(F_SANS_BOLD, 14)
f_num = font(F_SANS_BOLD, 11)
f_place = font(F_SANS_BOLD, 12)
f_item = font(F_SANS, 12)
LINE_H = 15

GRID_TOP = HERO_BOTTOM + 20
GRID_COLS = 2
COL_W = (CONTENT_W - COL_GAP) // 2

# pair sections into rows so tall/short sections balance
ROWS = [
    (SECTIONS[0], SECTIONS[4]),   # AMERICAS | AFRICA
    (SECTIONS[1], SECTIONS[2]),   # EUROPE & RUSSIA | MIDDLE EAST
    (SECTIONS[3], SECTIONS[5]),   # ASIA | OCEANIA
]


def draw_section(x, ytop, name, items):
    col = CONT_COLORS[name]
    d.rectangle([x, ytop, x + 42, ytop + 12], fill=col)
    d.text((x + 48, ytop), name, font=f_sec, fill=col)
    yy = ytop + f_sec.size + 4
    for num, place, text, _pin in items:
        d.text((x, yy), num, font=f_num, fill=col)
        nx = x + d.textlength(num, font=f_num) + 5
        head = place + " — "
        d.text((nx, yy), head, font=f_place, fill=INK)
        cx = nx + d.textlength(head, font=f_place)
        words = text.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if cx + d.textlength(trial, font=f_item) <= x + COL_W or not cur:
                cur = trial
            else:
                d.text((cx, yy), cur, font=f_item, fill=INK_SOFT)
                yy += LINE_H
                cx = x
                cur = word
        if cur:
            d.text((cx, yy), cur, font=f_item, fill=INK_SOFT)
            yy += LINE_H
    return yy


row_cursor = GRID_TOP
for r, (left, right) in enumerate(ROWS):
    row_top = row_cursor
    b1 = draw_section(MARGIN, row_top, left[0], left[1])
    b2 = draw_section(MARGIN + COL_W + COL_GAP, row_top, right[0], right[1])
    bottom = max(b1, b2)
    if r < 2:
        ry = bottom + 5
        d.line([(MARGIN, ry), (WIDTH - MARGIN, ry)], fill=RULE, width=1)
    row_cursor = bottom + 10

GRID_BOTTOM = row_cursor
d.line([(MARGIN + COL_W + COL_GAP // 2, GRID_TOP),
        (MARGIN + COL_W + COL_GAP // 2, GRID_BOTTOM - 12)], fill=RULE, width=1)

# ---------------------------------------------------------- map + also-on --
BAND_TOP = GRID_BOTTOM + 12
MAP_W = 330
MAP_H = 190

f_band = font(F_SANS_BOLD, 14)
d.text((MARGIN, BAND_TOP), "WHERE IT HAPPENED", font=f_band, fill=INK)
d.text((MARGIN + MAP_W + COL_GAP, BAND_TOP), "ALSO ON WEDNESDAY", font=f_band,
       fill=INK)
band_y = BAND_TOP + f_band.size + 6

# --- world map (equirectangular, simplified) ---
mx, my = MARGIN, band_y
mw, mh = MAP_W, MAP_H


def proj(lon, lat):
    px = (lon + 170.0) / 350.0 * mw
    py = (78.0 - lat) / 133.0 * mh
    return mx + px, my + py


d.rectangle([mx, my, mx + mw, my + mh], fill=SEA, outline=RULE)


def poly(coords):
    d.polygon([proj(lo, la) for lo, la in coords], fill=LAND)


poly([(-166, 66), (-155, 71), (-135, 69), (-120, 72), (-100, 73), (-85, 68),
      (-78, 58), (-60, 58), (-65, 48), (-75, 44), (-70, 42), (-76, 36),
      (-81, 30), (-80, 26), (-90, 29), (-97, 26), (-97, 20), (-105, 20),
      (-110, 24), (-117, 33), (-125, 40), (-125, 49), (-135, 58), (-150, 60),
      (-166, 60)])
poly([(-45, 60), (-30, 68), (-20, 70), (-25, 78), (-40, 80), (-55, 76),
      (-58, 68), (-50, 62)])
poly([(-78, 8), (-70, 11), (-60, 9), (-52, 4), (-42, -3), (-35, -8),
      (-38, -15), (-48, -25), (-53, -33), (-58, -38), (-65, -45), (-70, -52),
      (-73, -46), (-72, -35), (-70, -20), (-76, -14), (-81, -5)])
poly([(-9, 37), (-2, 36), (3, 42), (8, 44), (12, 42), (16, 41), (20, 40),
      (23, 37), (27, 38), (36, 36), (40, 42), (48, 46), (8, 55), (5, 58),
      (5, 62), (12, 66), (18, 70), (28, 71), (33, 69), (40, 68), (60, 70),
      (75, 73), (95, 76), (110, 74), (130, 72), (150, 70), (162, 69),
      (170, 66), (172, 60), (162, 58), (156, 52), (142, 54), (131, 43),
      (127, 34), (121, 31), (121, 25), (110, 20), (108, 15), (105, 9),
      (103, 1), (98, 8), (94, 16), (88, 21), (85, 19), (80, 15), (77, 7),
      (72, 19), (66, 24), (61, 25), (57, 27), (48, 30), (44, 36), (40, 42)])
poly([(48, 30), (57, 26), (58, 22), (54, 16), (48, 13), (43, 12), (39, 17),
      (35, 27), (39, 31), (44, 29)])
poly([(-6, 35), (-2, 35), (3, 37), (10, 37), (11, 33), (20, 32), (25, 32),
      (32, 31), (34, 28), (37, 22), (40, 15), (43, 11), (48, 11), (51, 12),
      (45, 2), (42, -3), (40, -10), (36, -18), (33, -26), (28, -33),
      (20, -35), (17, -30), (12, -18), (9, -2), (9, 4), (6, 4), (-4, 5),
      (-8, 4), (-13, 9), (-17, 15), (-16, 20), (-13, 27), (-10, 31)])
poly([(114, -22), (114, -34), (118, -35), (124, -33), (130, -32), (136, -35),
      (140, -38), (146, -39), (150, -37), (153, -30), (153, -25), (147, -19),
      (142, -11), (137, -12), (132, -11), (129, -14), (125, -14), (122, -18)])
poly([(173, -35), (175, -37), (178, -38), (176, -40), (174, -39)])
poly([(168, -44), (172, -41), (174, -41), (171, -45), (167, -46)])
poly([(130, 31), (132, 34), (136, 35), (140, 36), (141, 40), (142, 43),
      (145, 44), (143, 42), (140, 38), (137, 35), (133, 33)])
poly([(95, 6), (99, 3), (104, -2), (106, -6), (102, -5), (96, 2)])
poly([(109, 1), (113, 4), (117, 6), (119, 1), (116, -3), (110, -2)])
poly([(131, -1), (136, -2), (141, -3), (147, -6), (150, -9), (145, -8),
      (138, -7), (133, -4)])
poly([(44, -12), (48, -15), (50, -16), (48, -22), (45, -25), (43, -22)])

# pins: story num -> (lon, lat, continent key, label side, dx, dy)
PINS = {
    "01": (114, 22.5, "ASIA", "r", 0, 0),
    "04": (-77, 38.9, "AMERICAS", "r", 0, 0),
    "07": (-134.5, 58.3, "AMERICAS", "r", 0, 0),
    "08": (-118.3, 34, "AMERICAS", "r", 0, 0),
    "11": (90, 61, "EUROPE & RUSSIA", "r", 0, 0),
    "13": (36.5, 45.3, "EUROPE & RUSSIA", "t", 0, 0),
    "14": (-0.1, 51.0, "EUROPE & RUSSIA", "r", 0, 0),
    "15": (50.5, 26.2, "MIDDLE EAST", "r", 0, 0),
    "16": (35.2, 31.8, "MIDDLE EAST", "l", 0, 4),
    "17": (44.4, 33.3, "MIDDLE EAST", "t", 0, 0),
    "18": (127, 37.5, "ASIA", "r", 0, 0),
    "19": (77.2, 28.6, "ASIA", "r", 0, 0),
    "21": (28, -26.2, "AFRICA", "r", 0, 0),
    "25": (7.5, 9.1, "AFRICA", "r", 0, 0),
    "28": (174.8, -36.8, "OCEANIA", "l", 0, 0),
    "31": (178.4, -18.1, "OCEANIA", "l", 0, 0),
    "34": (-3.2, 51.5, "EUROPE & RUSSIA", "b", -4, 6),
}
f_pin = font(F_SANS_BOLD, 11)
for num, (lo, la, key, side, dx, dy) in PINS.items():
    px, py = proj(lo, la)
    px += dx
    py += dy
    col = CONT_COLORS[key]
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=col,
              outline=PAPER)
    tw_ = d.textlength(num, font=f_pin)
    if side == "r":
        tx, ty = px + 6, py - 6
    elif side == "l":
        tx, ty = px - 6 - tw_, py - 6
    elif side == "t":
        tx, ty = px - tw_ / 2, py - 17
    else:
        tx, ty = px - tw_ / 2, py + 5
    d.text((tx, ty), num, font=f_pin, fill=col)

# legend row under the map
LEGEND = [("AMERICAS", "AMER"), ("EUROPE & RUSSIA", "EUR"),
          ("MIDDLE EAST", "M.EAST"), ("ASIA", "ASIA"),
          ("AFRICA", "AFR"), ("OCEANIA", "OCEAN")]
f_leg = font(F_SANS_BOLD, 10)
lx = mx
for key, short in LEGEND:
    d.rectangle([lx, my + mh + 6, lx + 10, my + mh + 16], fill=CONT_COLORS[key])
    d.text((lx + 13, my + mh + 6), short, font=f_leg, fill=INK_SOFT)
    lx += 16 + d.textlength(short, font=f_leg) + 6
assert lx < mx + mw + 6, "map legend overflows map width"
d.text((mx, my + mh + 18), "PIN = LEAD STORY PER LOCATION · ALL 40 STORIES NUMBERED ABOVE",
       font=f_leg, fill=RULE)

# --- also-on briefs (right of map, 2 cols x 3 rows) ---
ax = MARGIN + MAP_W + COL_GAP
f_also = font(F_SANS_BOLD, 12)
f_aitem = font(F_SANS, 12)
acol_w = (CONTENT_W - MAP_W - COL_GAP - 18) // 2
assert ax + acol_w * 2 + 18 <= MARGIN + CONTENT_W, "also band overflows right margin"
also_bottom = band_y
for i, (num, text) in enumerate(ALSO):
    r, col_i = divmod(i, 2)
    ix = ax + col_i * (acol_w + 18)
    iy = band_y + r * 44
    d.text((ix, iy), num, font=f_also, fill=RED)
    nx = ix + d.textlength(num, font=f_also) + 5
    yy = iy
    cur = ""
    cx = nx
    for word in text.split():
        trial = (cur + " " + word).strip()
        if cx + d.textlength(trial, font=f_aitem) <= ix + acol_w or not cur:
            cur = trial
        else:
            d.text((cx, yy), cur, font=f_aitem, fill=INK_SOFT)
            yy += LINE_H
            cx = ix
            cur = word
    if cur:
        d.text((cx, yy), cur, font=f_aitem, fill=INK_SOFT)
        yy += LINE_H
    also_bottom = max(also_bottom, yy + 8)

BAND_BOTTOM = max(my + mh + 30, also_bottom)

# ------------------------------------------------------------- attribution --
attr_y = BAND_BOTTOM + 8
f_attr = font(F_SANS, 10)
f_meth = font(F_SANS, 9)
tw = d.textlength(ATTRIBUTION, font=f_attr)
d.text(((WIDTH - tw) / 2, attr_y), ATTRIBUTION, font=f_attr, fill=INK_SOFT)
tw2 = d.textlength(METHOD, font=f_meth)
d.text(((WIDTH - tw2) / 2, attr_y + 14), METHOD, font=f_meth, fill=RULE)
assert attr_y + 14 + f_meth.size <= HEIGHT - 10, \
    "page overflows: attribution at %d" % (attr_y + 14)

# ------------------------------------------------------------------- save --
print("mast=%d hero_bottom=%d grid=%d..%d band=%d..%d attr=%d" %
      (MAST_BOTTOM, HERO_BOTTOM, GRID_TOP, GRID_BOTTOM, BAND_TOP, BAND_BOTTOM,
       attr_y))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG")
print("saved", out, os.path.getsize(out), "bytes")
