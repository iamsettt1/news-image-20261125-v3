#!/usr/bin/env python3
"""THE WORLD TODAY - Wednesday 25 November 2026.

Renders a one-page newspaper front page (1024x1024 PNG) carrying 47
numbered stories from a single news day: three large drawn scenes,
eight pictogram scenes, a dotted world map with numbered pins, a stat
strip, a region tally bar, 36 numbered briefs, a date-check box and a
sources footer.  Fully deterministic: running this file always
produces the same entry.png byte for byte.

    python3 main.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- setup

W = H = 1024
MARGIN = 24
RIGHT = W - MARGIN
CONTENT_W = RIGHT - MARGIN

PAPER = (247, 242, 231)
INK = (26, 24, 20)
FAINT = (112, 102, 88)
RULE = (58, 53, 46)
RED = (164, 32, 28)
SEA = (203, 219, 231)
LAND_DOT = (96, 118, 92)
SKY = (214, 228, 240)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def tw(d, s, f):
    """Text width in pixels."""
    return d.textlength(s, font=f)


def wrap(d, s, f, maxw, first_maxw=None):
    """Greedy word wrap. Returns a list of lines."""
    words = s.split()
    lines = []
    limit = first_maxw if first_maxw is not None else maxw
    cur = ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(d, trial, f) <= limit or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
            limit = maxw
    if cur:
        lines.append(cur)
    return lines


def badge(d, x, y, n, r=11):
    """Red disc with a white story number."""
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    f = font(SANS_B, r + 1)
    s = str(n)
    w_ = tw(d, s, f)
    d.text((x - w_ / 2, y - (r + 1) / 2 - 1), s, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- stories
# (number, region, dateline, text) - text ends with the outlet in parens.

STORIES = [
    (1, "EUROPE", "KYIV",
     "Ukraine's sea drones strike Russian warships in two seas (Reuters)"),
    (2, "AFRICA", "GOMA",
     "WHO pulls Ebola teams out of Congo hospital after attack (AP)"),
    (3, "ASIA", "JIUQUAN",
     "Shenzhou-24 lifts off with Pakistan's first astronaut (Xinhua)"),
    (4, "MIDEAST", "HORMUZ",
     "Iran seeds mines off Hormuz as tankers mass (Reuters)"),
    (5, "MIDEAST", "GAZA",
     "Israeli strikes kill seven across Gaza (AJ)"),
    (6, "SPORT", "CRICKET",
     "Sooryavanshi, 15, smashes 204 off 53 balls (AFP)"),
    (7, "BUSINESS", "SEATTLE",
     "Boeing lands $7.4bn order for 737 jets (Reuters)"),
    (8, "ASIA", "JAVA",
     "Rescue race at flooded mine; fire at candy factory (AP)"),
    (9, "BUSINESS", "NEW YORK",
     "Huawei convicted in US trade-secrets case (BBC)"),
    (10, "BUSINESS", "MARKETS",
     "Asia markets slide; Brent crude at $87.49 (Reuters)"),
    (11, "ASIA", "DHAKA",
     "Bangladesh garment wages rise 36% (AFP)"),
    (12, "AFRICA", "KHARTOUM",
     "Drones strike Khartoum as Sudan's war grinds on (AJ)"),
    (13, "MIDEAST", "TEHRAN",
     "Singer flogged over hijab protest song (BBC)"),
    (14, "AFRICA", "KINSHASA",
     "Plane with 19 aboard missing over rainforest (AP)"),
    (15, "PACIFIC", "HONIARA",
     "Solomon Islands signs new treaty with China (AFP)"),
    (16, "ASIA", "BEIJING",
     "Chen Jining tipped for promotion in party shuffle (Reuters)"),
    (17, "ASIA", "HONG KONG",
     "Tai Po tower fire: search goes on (AFP)"),
    (18, "ASIA", "SEOUL",
     "Jets scrambled as Russian bombers near airspace (AP)"),
    (19, "ASIA", "PYONGYANG",
     "North Korea expels head of Swiss aid agency (Reuters)"),
    (20, "ASIA", "HANOI",
     "Deadly blast at chemicals factory (AFP)"),
    (21, "ASIA", "KUALA LUMPUR",
     "Rohingya boat people found adrift, taken ashore (AP)"),
    (22, "AMERICAS", "MADRID",
     "Abrego Garcia flown to Spain in deal (CNN)"),
    (23, "AMERICAS", "CARTAGENA",
     "Hostages freed after port warehouse siege (AP)"),
    (24, "AMERICAS", "GULF OF MEXICO",
     "Plane crashes into the Gulf of Mexico (AP)"),
    (25, "AMERICAS", "NEW YORK",
     "Thanksgiving storms threaten 17.6m flyers (CNN)"),
    (26, "AMERICAS", "WASHINGTON",
     "Trump gives Giuliani the Medal of Freedom (AP)"),
    (27, "AMERICAS", "OTTAWA",
     "Pentagon criticises Canada's defence plan (Reuters)"),
    (28, "AMERICAS", "GENEVA",
     "WHO chief: Cuba blockade is harming patients (AP)"),
    (29, "EUROPE", "MADRID",
     "Spain's PM calls snap election for spring (Reuters)"),
    (30, "EUROPE", "LONDON",
     "Break-in at royal residence: two arrested (BBC)"),
    (31, "AFRICA", "LUSAKA",
     "Ex-minister indicted for treason in Zambia (AFP)"),
    (32, "ASIA", "THE HAGUE",
     "World court rules Myanmar committed genocide (Reuters)"),
    (33, "EUROPE", "LONDON",
     "England counts 5,200 heat-linked deaths this year (BBC)"),
    (34, "ASIA", "MANILA",
     "Magnitude 5.3 quake rattles Panay island (AFP)"),
    (35, "AMERICAS", "DES MOINES",
     "Army to blow up 5 tonnes of old explosives in Iowa (AP)"),
    (36, "BUSINESS", "NEW YORK",
     "Nvidia falls 7% as chip rally cools (Reuters)"),
    (37, "BUSINESS", "PARIS",
     "Sanofi to buy Insmed in $41bn deal (Reuters)"),
    (38, "BUSINESS", "CARACAS",
     "Venezuela unveils plan for $237.5bn debt pile (Reuters)"),
    (39, "BUSINESS", "WASHINGTON",
     "Trump tariffs land on 16 trading partners (AP)"),
    (40, "BUSINESS", "NEW YORK",
     "US consumer confidence reads 103.3 (AP)"),
    (41, "AMERICAS", "WASHINGTON",
     "CIA probes cyber breach at contractor (CNN)"),
    (42, "BUSINESS", "LONDON",
     "Gold at $3,545 an ounce before US inflation data (Reuters)"),
    (43, "BUSINESS", "DATA WATCH",
     "US PCE due today; German GDP +0.1% (Reuters)"),
    (44, "BUSINESS", "TECH BRIEFS",
     "Tidal bans AI acts; Broadcom patches VMware (BBC)"),
    (45, "SPORT", "FOOTBALL",
     "Midweek results, weekend fixtures (BBC)"),
    (46, "LIFE", "SHOWBIZ",
     "New Miss Universe crowned in glittering final (AFP)"),
    (47, "BUSINESS", "NEW YORK",
     "REPORTED: SpaceX and Tesla in merger talks (Reuters)"),
]

N_STORIES = len(STORIES)

REGION_ORDER = ["EUROPE", "ASIA", "MIDEAST", "AFRICA", "AMERICAS",
                "PACIFIC", "BUSINESS", "SPORT & LIFE"]
REGION_COLORS = {
    "EUROPE": (52, 90, 160),
    "ASIA": (196, 60, 44),
    "MIDEAST": (222, 150, 40),
    "AFRICA": (90, 140, 60),
    "AMERICAS": (120, 70, 150),
    "PACIFIC": (40, 150, 170),
    "BUSINESS": (92, 92, 98),
    "SPORT & LIFE": (30, 140, 110),
}


def region_counts():
    counts = {r: 0 for r in REGION_ORDER}
    for _, region, _, _ in STORIES:
        key = "SPORT & LIFE" if region in ("SPORT", "LIFE") else region
        counts[key] += 1
    return counts


# ---------------------------------------------------------------- scenes

def scene_ships(d, x, y, w, h):
    """Story 1: sea drones strike warships in two seas."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    sea_y = y + int(h * 0.52)
    d.rectangle([x, sea_y, x + w, y + h], fill=(70, 110, 150))
    for i in range(5):  # wave lines
        wy = sea_y + 8 + i * 9
        d.line([x + 6, wy, x + w - 6, wy], fill=(120, 160, 195), width=1)
    # far ship (left)
    sx, sy = x + 26, sea_y - 12
    d.polygon([(sx, sy), (sx + 74, sy), (sx + 64, sy + 10), (sx + 8, sy + 10)],
              fill=(52, 56, 62))
    d.rectangle([sx + 26, sy - 10, sx + 46, sy], fill=(52, 56, 62))
    d.line([sx + 56, sy - 16, sx + 56, sy], fill=(52, 56, 62), width=2)
    # near ship (right), listing, with burst
    sx2, sy2 = x + w - 118, sea_y - 6
    d.polygon([(sx2, sy2), (sx2 + 92, sy2), (sx2 + 80, sy2 + 12),
               (sx2 + 10, sy2 + 12)], fill=(38, 42, 48))
    d.rectangle([sx2 + 34, sy2 - 12, sx2 + 58, sy2], fill=(38, 42, 48))
    d.line([sx2 + 24, sy2 - 20, sx2 + 24, sy2], fill=(38, 42, 48), width=2)
    cx, cy = sx2 + 84, sy2 - 8  # starburst
    for dx, dy in [(0, -13), (9, -9), (13, 0), (9, 9), (0, 13), (-9, 9),
                   (-13, 0), (-9, -9)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=(232, 120, 30), width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(245, 180, 60))
    # two drones in the sky
    for dx, dy in [(70, 18), (180, 10)]:
        px, py = x + dx, y + dy
        d.line([px - 9, py - 6, px + 9, py + 6], fill=INK, width=2)
        d.line([px - 9, py + 6, px + 9, py - 6], fill=INK, width=2)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=INK)
    d.rectangle([x, y + h - 14, x + 118, y + h], fill=(38, 42, 48))
    f = font(SANS_B, 9)
    d.text((x + 6, y + h - 12), "BLACK SEA + BALTIC", font=f, fill=(255, 255, 255))


def scene_hospital(d, x, y, w, h):
    """Story 2: WHO pulls Ebola teams out of a Congo hospital."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 226))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(150, 146, 130))
    # hospital block
    bx, by, bw, bh = x + 26, y + 16, 128, h - 32
    d.rectangle([bx, by, bx + bw, by + bh], fill=(238, 238, 234),
                outline=INK, width=2)
    for r_ in range(3):
        for c_ in range(4):
            wx = bx + 12 + c_ * 29
            wy = by + 12 + r_ * 24
            d.rectangle([wx, wy, wx + 17, wy + 13], outline=FAINT, width=1)
    # red cross on the roof
    cx, cy = bx + bw // 2, by + 20
    d.rectangle([cx - 4, cy - 13, cx + 4, cy + 13], fill=RED)
    d.rectangle([cx - 13, cy - 4, cx + 13, cy + 4], fill=RED)
    # ambulance driving away (right)
    ax, ay = x + w - 128, y + h - 52
    d.rectangle([ax, ay, ax + 74, ay + 26], fill=(250, 250, 248),
                outline=INK, width=2)
    d.polygon([(ax + 74, ay + 6), (ax + 94, ay + 12), (ax + 94, ay + 26),
               (ax + 74, ay + 26)], fill=(250, 250, 248), outline=INK)
    d.rectangle([ax + 78, ay + 12, ax + 90, ay + 20], fill=SEA)
    d.rectangle([ax + 30, ay + 6, ax + 37, ay + 20], fill=RED)
    d.rectangle([ax + 25, ay + 10, ax + 42, ay + 16], fill=RED)
    for wx in (ax + 16, ax + 80):
        d.ellipse([wx - 7, ay + 22, wx + 7, ay + 36], fill=INK)
    for i in range(3):  # motion lines
        d.line([ax - 22 + i * 3, ay + 8 + i * 7, ax - 8 + i * 3,
                ay + 8 + i * 7], fill=FAINT, width=2)
    # warning sign
    tx, ty = x + w - 52, y + 16
    d.polygon([(tx, ty + 26), (tx + 15, ty), (tx + 30, ty + 26)], outline=RED)
    f = font(SANS_B, 15)
    d.text((tx + 11, ty + 9), "!", font=f, fill=RED)


def scene_rocket(d, x, y, w, h):
    """Story 3: Shenzhou-24 lifts off from Jiuquan."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 34, 64))
    # deterministic star field
    for i in range(46):
        sx = x + (i * 67) % max(w - 8, 1) + 4
        sy = y + (i * 41) % max(int(h * 0.6), 1) + 4
        d.point((sx, sy), fill=(230, 235, 245))
        if i % 7 == 0:
            d.point((sx + 1, sy), fill=(200, 210, 225))
    gx = x + w // 2  # rocket centre line
    top = y + 4
    d.polygon([(gx - 10, top + 22), (gx, top), (gx + 10, top + 22)],
              fill=(235, 235, 238))
    d.rectangle([gx - 10, top + 22, gx + 10, top + 56], fill=(245, 245, 248))
    d.ellipse([gx - 4, top + 28, gx + 4, top + 38], fill=SEA, outline=INK)
    d.rectangle([gx - 10, top + 46, gx + 10, top + 49], fill=RED)
    d.polygon([(gx - 10, top + 56), (gx - 19, top + 66), (gx - 10, top + 66)],
              fill=(200, 60, 44))
    d.polygon([(gx + 10, top + 56), (gx + 19, top + 66), (gx + 10, top + 66)],
              fill=(200, 60, 44))
    # flame, kept inside the art box
    d.polygon([(gx - 7, top + 66), (gx, top + 78), (gx + 7, top + 66)],
              fill=(245, 170, 50))
    d.polygon([(gx - 3, top + 66), (gx, top + 73), (gx + 3, top + 66)],
              fill=(250, 220, 130))
    for dx, r_ in [(-26, 8), (-13, 6), (14, 7), (27, 9)]:
        cy = y + h - 5
        d.ellipse([gx + dx - r_, cy - r_ // 2, gx + dx + r_, cy + r_ // 2],
                  fill=(198, 200, 205))
    # gantry tower
    tx = x + 26
    d.rectangle([tx, y + 18, tx + 9, y + h - 6], fill=(120, 124, 132))
    for i in range(4):
        ly = y + 24 + i * 12
        d.line([tx, ly, tx + 9, ly + 8], fill=(120, 124, 132), width=1)
    # Pakistan flag patch (green field, white stripe, crescent)
    fx, fy = x + w - 56, y + 14
    d.rectangle([fx, fy, fx + 34, fy + 22], fill=(20, 110, 55))
    d.rectangle([fx, fy, fx + 8, fy + 22], fill=(245, 245, 245))
    d.ellipse([fx + 16, fy + 5, fx + 28, fy + 17], fill=(245, 245, 245))
    d.ellipse([fx + 19, fy + 4, fx + 30, fy + 15], fill=(20, 110, 55))


SCENES = [
    (1, scene_ships,
     "Kyiv's drones strike Russian warships in two seas",
     "Ukraine says sea drones hit a frigate in the Black Sea and a "
     "shadow-fleet tanker in the Baltic. (Reuters)"),
    (2, scene_hospital,
     "WHO pulls Ebola teams out of Congo hospital",
     "Staff were evacuated after gunmen stormed the wards; the "
     "outbreak's death toll has reached 5,775. (AP)"),
    (3, scene_rocket,
     "Shenzhou-24 lifts off, Pakistan's first astronaut aboard",
     "The Long March crew reached orbit from Jiuquan, bound for the "
     "Tiangong station. (Xinhua)"),
]

# ---------------------------------------------------------------- pictograms

def picto_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(215, 228, 238))
    wy = y + h - 12
    d.rectangle([x, wy, x + w, y + h], fill=(70, 110, 150))
    hx, hy = x + 14, wy - 10
    d.polygon([(hx, hy), (hx + w - 34, hy), (hx + w - 44, hy + 8),
               (hx + 8, hy + 8)], fill=(52, 56, 62))
    d.rectangle([hx + 16, hy - 8, hx + 30, hy], fill=(52, 56, 62))
    for i in range(3):  # mines: spiked circles in the water
        mx = x + 30 + i * 36
        my = wy + 5
        d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=INK)
        for dx, dy in [(0, -8), (6, -5), (8, 2), (-6, -5), (-8, 2),
                       (4, 6), (-4, 6)]:
            d.line([mx, my, mx + dx, my + dy], fill=INK, width=1)


def picto_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 205))
    d.ellipse([x + w - 30, y + 6, x + w - 12, y + 24], fill=(240, 190, 80))
    base = y + h - 6
    heights = [22, 34, 16, 28, 12]
    for i, bh in enumerate(heights):
        bx = x + 8 + i * 19
        d.rectangle([bx, base - bh, bx + 14, base], fill=(120, 110, 100))
    # broken tower + smoke
    bx = x + 46
    d.polygon([(bx, base), (bx, base - 30), (bx + 7, base - 22),
               (bx + 14, base - 27), (bx + 14, base)], fill=(90, 84, 78))
    for i, r_ in enumerate([5, 8, 11]):
        cx = bx + 16 + i * 7
        cy = base - 36 - i * 6
        d.ellipse([cx - r_, cy - r_ // 2, cx + r_, cy + r_ // 2],
                  fill=(150, 148, 144))


def picto_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 232, 200))
    cx, cy = x + w // 2, y + h // 2
    for sx in (-16, 0, 16):  # stumps
        d.rectangle([cx + sx - 2, cy - 16, cx + sx + 2, cy + 16],
                    fill=(214, 178, 94), outline=INK)
    d.line([cx - 19, cy - 16, cx - 13, cy - 16], fill=INK, width=2)
    d.line([cx + 13, cy - 16, cx + 19, cy - 16], fill=INK, width=2)
    # bat leaning in
    d.polygon([(cx - 44, cy + 18), (cx - 30, cy - 14), (cx - 24, cy - 11),
               (cx - 36, cy + 20)], fill=(196, 158, 96), outline=INK)
    d.line([cx - 29, cy - 13, cx - 24, cy - 22], fill=INK, width=3)
    # ball flying out with motion arc
    d.ellipse([cx + 26, cy - 22, cx + 36, cy - 12], fill=RED)
    d.arc([cx + 6, cy - 26, cx + 34, cy + 2], 300, 60, fill=FAINT, width=1)


def picto_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 224, 240))
    cy = y + h // 2
    d.polygon([(x + 10, cy + 2), (x + 30, cy - 8), (x + w - 26, cy - 8),
               (x + w - 12, cy + 2), (x + w - 26, cy + 8), (x + 30, cy + 8)],
              fill=(245, 245, 248), outline=INK)
    d.polygon([(x + 16, cy - 7), (x + 26, cy - 20), (x + 36, cy - 20),
               (x + 34, cy - 7)], fill=(200, 60, 44))
    d.polygon([(x + 52, cy + 6), (x + 66, cy + 18), (x + 76, cy + 18),
               (x + 70, cy + 6)], fill=(200, 60, 44))
    for i in range(6):
        wx = x + 44 + i * 11
        d.ellipse([wx, cy - 5, wx + 6, cy - 1], fill=SEA)


def picto_mine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.polygon([(x + 6, y + h - 14), (x + w // 2, y + 6),
               (x + w - 6, y + h - 14)], fill=(140, 124, 100))
    ax, ay = x + w // 2, y + h - 14  # tunnel mouth
    d.pieslice([ax - 13, ay - 24, ax + 13, ay + 2], 180, 360, fill=(30, 28, 26))
    d.rectangle([ax - 13, ay - 12, ax + 13, ay], fill=(30, 28, 26))
    wy = y + h - 10  # flood water
    d.rectangle([x, wy, x + w, y + h], fill=(70, 110, 150))
    for i in range(4):
        d.arc([x + 8 + i * 24, wy - 3, x + 26 + i * 24, wy + 5], 0, 180,
              fill=(170, 200, 225), width=1)
    d.ellipse([ax - 4, ay - 34, ax + 4, ay - 26], fill=(245, 190, 60))


def picto_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 228, 220))
    cx = x + w // 2
    d.polygon([(x + 10, y + 14), (cx, y + 4), (x + w - 10, y + 14)],
              fill=(110, 104, 96))
    d.rectangle([x + 10, y + 16, x + w - 10, y + 19], fill=(110, 104, 96))
    for i in range(5):
        cxx = x + 18 + i * ((w - 36) // 4)
        d.rectangle([cxx - 3, y + 21, cxx + 3, y + h - 16],
                    fill=(248, 248, 244), outline=FAINT)
    d.rectangle([x + 12, y + h - 14, x + w - 12, y + h - 11],
                fill=(110, 104, 96))
    d.rectangle([x + 8, y + h - 10, x + w - 8, y + h - 7],
                fill=(110, 104, 96))
    d.ellipse([cx - 3, y + 8, cx + 3, y + 14], outline=INK, width=1)


def picto_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 240, 238))
    ox, oy = x + 12, y + h - 10
    d.line([ox, y + 6, ox, oy], fill=INK, width=1)
    d.line([ox, oy, x + w - 8, oy], fill=INK, width=1)
    pts = [(0, 8), (16, 12), (30, 10), (44, 20), (58, 18), (72, 30),
           (86, 34)]
    pts = [(ox + 6 + px, oy - 26 + py) for px, py in pts]
    d.line(pts, fill=RED, width=2)
    for px, py in pts:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    d.polygon([(pts[-1][0], pts[-1][1] - 4), (pts[-1][0] + 8, pts[-1][1] + 2),
               (pts[-1][0] + 1, pts[-1][1] + 3)], fill=RED)
    for i, bh in enumerate([10, 14, 8]):  # volume bars
        bx = ox + 12 + i * 18
        d.rectangle([bx, oy - bh, bx + 9, oy], fill=(150, 150, 155))


def picto_garment(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 214))
    cx = x + w // 2 - 12
    # factory block behind, left
    d.rectangle([x + 6, y + h - 20, x + 38, y + h - 6], fill=(170, 160, 145))
    d.rectangle([x + 12, y + h - 30, x + 18, y + h - 20], fill=(120, 112, 100))
    d.rectangle([x + 24, y + h - 27, x + 29, y + h - 20], fill=(120, 112, 100))
    # t-shirt, large and centred
    d.polygon([(cx - 10, y + 5), (cx - 27, y + 12), (cx - 21, y + 23),
               (cx - 11, y + 20), (cx - 11, y + h - 6), (cx + 21, y + h - 6),
               (cx + 21, y + 20), (cx + 31, y + 23), (cx + 37, y + 12),
               (cx + 20, y + 5), (cx + 10, y + 7), (cx, y + 11),
               (cx - 10, y + 7)], fill=(250, 250, 248), outline=INK)
    f = font(SANS_B, 13)
    s = "+36%"
    d.text((x + w - tw(d, s, f) - 8, y + h - 22), s, font=f, fill=RED)


PICTOS = [
    (4, picto_tanker, "Iran seeds mines off Hormuz as tankers mass (Reuters)"),
    (5, picto_gaza, "Israeli strikes kill seven across Gaza (AJ)"),
    (6, picto_cricket, "Sooryavanshi, 15, smashes 204 off 53 balls (AFP)"),
    (7, picto_plane, "Boeing lands $7.4bn order for 737 jets (Reuters)"),
    (8, picto_mine, "Rescue race at flooded mine in Indonesia (AP)"),
    (9, picto_court, "Huawei convicted in US trade-secrets case (BBC)"),
    (10, picto_chart, "Asia markets slide; Brent crude at $87.49 (Reuters)"),
    (11, picto_garment, "Bangladesh garment wages rise 36% (AFP)"),
]

# ---------------------------------------------------------------- world map
# Rough continent outlines as (lon, lat) polygons, drawn as dot grids.

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-76, 58), (-65, 50), (-70, 44), (-74, 40), (-76, 35),
     (-80, 32), (-81, 26), (-84, 30), (-89, 30), (-94, 29), (-97, 26),
     (-97, 22), (-94, 17), (-90, 14), (-83, 9), (-79, 9), (-86, 13),
     (-92, 15), (-97, 16), (-105, 20), (-110, 23), (-114, 29),
     (-117, 33), (-122, 37), (-124, 46), (-130, 54), (-140, 60),
     (-155, 60), (-165, 60)],
    # Greenland
    [(-45, 60), (-32, 68), (-22, 70), (-20, 76), (-30, 82), (-50, 80),
     (-58, 72), (-55, 64)],
    # South America
    [(-79, 9), (-75, 11), (-72, 12), (-64, 10), (-55, 6), (-50, 0),
     (-44, -3), (-35, -8), (-39, -13), (-40, -20), (-48, -26), (-52, -32),
     (-58, -38), (-62, -41), (-65, -45), (-67, -50), (-68, -54),
     (-71, -54), (-73, -46), (-73, -37), (-71, -30), (-70, -20),
     (-75, -15), (-79, -8), (-81, -4), (-80, 1), (-77, 4), (-79, 7)],
    # Europe
    [(-9, 43), (-2, 44), (-1, 46), (-5, 48), (0, 50), (3, 53), (8, 55),
     (7, 57), (5, 59), (6, 62), (11, 65), (14, 67), (18, 69), (25, 71),
     (35, 68), (45, 68), (55, 68), (66, 65), (60, 58), (50, 55),
     (42, 50), (35, 47), (30, 46), (28, 41), (23, 40), (19, 40),
     (15, 38), (16, 42), (12, 44), (8, 44), (3, 43), (0, 39), (-2, 37),
     (-6, 36), (-9, 37)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 55), (-3, 57), (-5, 58), (-7, 55),
     (-8, 52), (-6, 50)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
     (35, 28), (38, 22), (40, 15), (43, 12), (48, 11), (51, 12), (48, 5),
     (42, -5), (40, -12), (38, -20), (35, -27), (32, -29), (25, -34),
     (19, -35), (17, -32), (15, -27), (13, -18), (12, -10), (9, -2),
     (9, 4), (4, 6), (-2, 5), (-8, 5), (-13, 8), (-17, 12), (-17, 15),
     (-16, 20), (-15, 25), (-13, 28), (-9, 31)],
    # Madagascar
    [(44, -16), (47, -15), (50, -18), (48, -22), (46, -25), (45, -22),
     (44, -18)],
    # Russia / Central Asia
    [(30, 46), (40, 48), (55, 51), (70, 54), (90, 55), (110, 55),
     (130, 55), (150, 55), (165, 58), (175, 64), (170, 69), (150, 71),
     (130, 72), (110, 74), (95, 76), (80, 73), (68, 69), (58, 68),
     (48, 66), (40, 60), (35, 52)],
    # Arabia
    [(35, 31), (42, 37), (48, 39), (50, 36), (54, 31), (56, 27),
     (59, 23), (58, 20), (55, 17), (52, 15), (48, 14), (44, 12),
     (42, 14), (39, 20), (36, 24), (35, 28)],
    # Persia to Central Asia south
    [(44, 38), (54, 39), (62, 38), (68, 37), (72, 36), (70, 33),
     (66, 30), (61, 25), (57, 26), (54, 30), (50, 29), (48, 33),
     (44, 36)],
    # India
    [(68, 32), (72, 34), (78, 34), (84, 33), (88, 30), (92, 28),
     (95, 29), (97, 28), (95, 24), (92, 21), (89, 22), (86, 20),
     (84, 18), (80, 15), (77, 8), (74, 12), (72, 19), (70, 22),
     (68, 25)],
    # China / East Asia
    [(75, 39), (82, 42), (90, 42), (98, 42), (105, 41), (112, 41),
     (118, 41), (122, 39), (121, 35), (122, 31), (120, 27), (117, 24),
     (113, 22), (109, 20), (108, 17), (106, 20), (103, 22), (99, 22),
     (97, 25), (94, 28), (89, 29), (84, 31), (79, 34), (75, 37)],
    # Korea
    [(126, 35), (128, 36), (129, 38), (128, 40), (126, 40), (125, 38)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44),
     (143, 44), (141, 39), (139, 35), (135, 34), (132, 33)],
    # South-East Asia
    [(94, 17), (95, 24), (98, 24), (100, 20), (100, 16), (101, 13),
     (100, 8), (101, 5), (103, 2), (104, 4), (102, 7), (104, 9),
     (106, 9), (107, 11), (109, 13), (109, 16), (106, 20), (103, 22),
     (99, 22), (96, 20)],
    # Indonesia - Sumatra / Java / Borneo / New Guinea blobs
    [(95, 5), (100, 1), (104, -3), (106, -6), (104, -5), (99, 0),
     (96, 3)],
    [(106, -6), (114, -7), (114, -9), (106, -8)],
    [(109, 1), (113, 4), (117, 5), (119, 1), (117, -2), (113, -3),
     (110, -2)],
    [(131, -1), (138, -2), (145, -4), (147, -7), (142, -8), (136, -4),
     (131, -3)],
    # Philippines
    [(120, 18), (122, 16), (122, 13), (121, 11), (123, 10), (124, 8),
     (122, 9), (120, 12), (120, 16)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -36), (140, -38),
     (145, -38), (147, -38), (150, -37), (153, -32), (153, -27),
     (151, -24), (146, -19), (142, -15), (142, -11), (140, -17),
     (136, -15), (135, -12), (132, -11), (130, -13), (126, -14),
     (122, -17), (118, -20)],
    # New Zealand
    [(167, -45), (170, -43), (173, -41), (174, -39), (176, -38),
     (174, -41), (172, -43), (169, -46)],
]

# (story number, lon, lat)
PINS = [
    (1, 31, 50), (2, 29, -1), (3, 100, 41), (4, 56, 26), (5, 34, 31),
    (6, 77, 20), (8, 107, -6), (11, 91, 25), (12, 32, 15), (14, 21, -4),
    (15, 160, -9), (17, 114, 22), (20, 106, 10), (23, -75, 10),
    (24, -90, 25), (25, -104, 36), (29, -4, 40), (30, 0, 51),
    (31, 29, -16), (32, 96, 21), (34, 122, 11), (35, -94, 44),
]


def _in_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)) and \
                (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=RULE, width=1)
    f = font(SANS_B, 10)
    d.text((x + 8, y + 5), "THE DAY ON THE MAP - pins match story numbers",
           font=f, fill=INK)
    top = y + 20
    mh = h - 24

    def px(lon):
        return x + (lon + 180) / 360.0 * w

    def py(lat):
        return top + (75 - lat) / 135.0 * mh

    step = 4
    lon_step = 360.0 / w * step
    lat_step = 135.0 / mh * step
    lat = 74.0
    while lat > -58:
        lon = -179.0
        while lon < 180:
            for poly in CONTINENTS:
                if _in_poly(lon, lat, poly):
                    cx, cy = px(lon), py(lat)
                    d.ellipse([cx - 1, cy - 1, cx + 1, cy + 1], fill=LAND_DOT)
                    break
            lon += lon_step
        lat -= lat_step
    for n, lon, lat_ in PINS:
        cx, cy = px(lon), py(lat_)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        f2 = font(SANS_B, 8)
        s = str(n)
        d.text((cx - tw(d, s, f2) / 2, cy - 4), s, font=f2,
               fill=(255, 255, 255))


# ---------------------------------------------------------------- sections

def masthead(d):
    f = font(SERIF_B, 52)
    s = "THE WORLD TODAY"
    d.text(((W - tw(d, s, f)) / 2, 12), s, font=f, fill=INK)
    f2 = font(SANS_B, 13)
    s2 = "Wednesday, 25 November 2026"
    d.text((MARGIN, 76), s2, font=f2, fill=INK)
    s3 = "%d STORIES - 9 REGIONS - ONE PAGE" % N_STORIES
    d.text((RIGHT - tw(d, s3, f2), 76), s3, font=f2, fill=RED)
    d.line([MARGIN, 98, RIGHT, 98], fill=INK, width=3)
    d.line([MARGIN, 102, RIGHT, 102], fill=INK, width=1)


def stat_strip(d, y):
    stats = [
        (str(N_STORIES), "STORIES TODAY"),
        ("204", "RUNS OFF 53 BALLS - 6"),
        ("5,200", "ENGLAND HEAT DEATHS - 33"),
        ("$3,545", "GOLD PER OUNCE - 42"),
        ("5.3", "PANAY QUAKE MAG. - 34"),
        ("36%", "BANGLADESH WAGES - 11"),
    ]
    cell = CONTENT_W / 6.0
    fnum = font(SANS_B, 23)
    flab = font(SANS, 9)
    for i, (num, lab) in enumerate(stats):
        cx = MARGIN + i * cell
        d.text((cx + (cell - tw(d, num, fnum)) / 2, y), num, font=fnum,
               fill=RED if i == 0 else INK)
        d.text((cx + (cell - tw(d, lab, flab)) / 2, y + 26), lab,
               font=flab, fill=FAINT)
        if i:
            d.line([cx, y + 2, cx, y + 34], fill=RULE, width=1)


def region_bar(d, y):
    counts = region_counts()
    total = float(N_STORIES)
    x = float(MARGIN)
    fnum = font(SANS_B, 10)
    flab = font(SANS_B, 9)
    for region in REGION_ORDER:
        w_ = CONTENT_W * counts[region] / total
        color = REGION_COLORS[region]
        d.rectangle([x, y, x + w_, y + 15], fill=color)
        s = str(counts[region])
        d.text((x + (w_ - tw(d, s, fnum)) / 2, y + 2), s, font=fnum,
               fill=(255, 255, 255))
        lab = region
        lx = x + (w_ - tw(d, lab, flab)) / 2
        lx = max(MARGIN, min(lx, RIGHT - tw(d, lab, flab)))
        d.text((lx, y + 18), lab, font=flab, fill=color)
        x += w_


def scene_row(d, y):
    w_ = 316
    gap = 14
    fh = font(SERIF_B, 16)
    fs = font(SANS, 11)
    for i, (n, draw_fn, head, stand) in enumerate(SCENES):
        x = MARGIN + i * (w_ + gap)
        d.rectangle([x, y, x + w_, y + 84], outline=RULE, width=1)
        draw_fn(d, x + 1, y + 1, w_ - 2, 82)
        badge(d, x + 16, y + 16, n, r=12)
        lines = wrap(d, head, fh, w_ - 4)
        ly = y + 89
        for ln in lines[:2]:
            d.text((x + 2, ly), ln, font=fh, fill=INK)
            ly += 18
        slines = wrap(d, stand, fs, w_ - 4)
        for ln in slines[:3]:
            d.text((x + 2, ly), ln, font=fs, fill=(70, 64, 56))
            ly += 13


def picto_grid(d, y):
    w_ = 238
    gap = 8
    row_h = 74
    fc = font(SANS, 10)
    for idx, (n, draw_fn, cap) in enumerate(PICTOS):
        r_, c_ = divmod(idx, 4)
        x = MARGIN + c_ * (w_ + gap)
        yy = y + r_ * (row_h + gap)
        d.rectangle([x, yy, x + w_, yy + row_h], outline=RULE, width=1)
        draw_fn(d, x + 1, yy + 1, w_ - 2, 42)
        badge(d, x + 12, yy + 12, n, r=10)
        lines = wrap(d, cap, fc, w_ - 8)
        ly = yy + 46
        for ln in lines[:2]:
            d.text((x + 4, ly), ln, font=fc, fill=INK)
            ly += 12


def date_check(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    f = font(SANS_B, 12)
    d.text((x + 10, y + 7), "DATE CHECK", font=f, fill=RED)
    body = ("Wires read on Wednesday 25 November 2026. Every story on "
            "this page was reported, or was still developing, on "
            "25 November in at least one time zone. Left out as other "
            "days' news: the Houthi strike on Riyadh's tower, Trump's "
            "turkey pardons and Senegal's AFCON ruling - all Tuesday "
            "24 November.")
    fb = font(SANS, 11)
    ly = y + 28
    for ln in wrap(d, body, fb, w - 20):
        d.text((x + 10, ly), ln, font=fb, fill=INK)
        ly += 14


def briefs(d, y):
    shown = {s[0] for s in SCENES} | {p[0] for p in PICTOS}
    items = [s for s in STORIES if s[0] not in shown]
    f = font(SANS_B, 12)
    d.text((MARGIN, y), "MORE OF THE DAY - %d NUMBERED BRIEFS" % len(items),
           font=f, fill=INK)
    d.line([MARGIN, y + 17, RIGHT, y + 17], fill=INK, width=1)
    top = y + 24
    col_w = 317
    gap = 12.5
    lh = 12
    fn = font(SANS_B, 10)
    fd = font(SANS_B, 11)
    ft = font(SANS, 11)

    def brief_lines(item):
        _n, _r, dateline, text = item
        head = dateline + " - "
        first_w = col_w - 23 - tw(d, head, fd)
        return wrap(d, text, ft, col_w - 23, first_maxw=first_w)

    # Balance the three columns by wrapped height, keeping the story
    # order ascending inside each column.
    columns = [[], [], []]
    heights = [0, 0, 0]
    for item in items:
        h_ = len(brief_lines(item)) * lh + 2
        ci = heights.index(min(heights))
        columns[ci].append(item)
        heights[ci] += h_

    for ci in range(3):
        x = MARGIN + ci * (col_w + gap)
        yy = top
        for item in columns[ci]:
            n, _region, dateline, text = item
            d.rectangle([x, yy + 1, x + 19, yy + 13], fill=RED)
            s = str(n)
            d.text((x + (19 - tw(d, s, fn)) / 2, yy + 2), s, font=fn,
                   fill=(255, 255, 255))
            tx = x + 23
            head = dateline + " - "
            lines = brief_lines(item)
            d.text((tx, yy), head, font=fd, fill=INK)
            if lines:
                d.text((tx + tw(d, head, fd), yy), lines[0], font=ft,
                       fill=INK)
                ly = yy + lh
                for ln in lines[1:3]:
                    d.text((tx, ly), ln, font=ft, fill=INK)
                    ly += lh
                yy = ly + 2
            else:
                yy += lh + 2


def footer(d, y):
    d.line([MARGIN, y, RIGHT, y], fill=INK, width=1)
    f = font(SANS, 10)
    s = ("Sources: Reuters - AP - AFP - BBC - CNN - Al Jazeera - Xinhua "
         "wire digests, read 25 Nov 2026  |  %d stories, one page  |  "
         "Set in code: python3 main.py regenerates this page" % N_STORIES)
    d.text(((W - tw(d, s, f)) / 2, y + 5), s, font=f, fill=FAINT)


# ---------------------------------------------------------------- main

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    stat_strip(d, 108)
    region_bar(d, 148)
    scene_row(d, 182)
    picto_grid(d, 352)
    draw_map(d, MARGIN, 516, 632, 124)
    date_check(d, 668, 516, RIGHT - 668, 124)
    briefs(d, 650)
    footer(d, 996)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()
