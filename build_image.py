#!/usr/bin/env python3
"""Draw the front page for Sunday 22 November 2026.

A newspaper front page, drawn entirely with Pillow: masthead, one lead
story and five smaller stories, each with a flat vector-style
illustration, plus a ticker of the day's other news. Output is a
1024x1024 PNG, deterministic: same input, same bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (178, 34, 27)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GREY = (90, 86, 76)
LIGHT = (232, 226, 210)
SEA = (46, 110, 138)
SAND = (214, 196, 150)
DARKPANEL = (24, 42, 60)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(draw, cx, cy, r):
    """A cracked globe: blue disc, meridian lines, red crack."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 124, 165),
                 outline=INK, width=3)
    for k in (-0.55, 0.0, 0.55):
        x0 = cx + int(r * k)
        draw.arc([x0 - int(r * 0.45), cy - r, x0 + int(r * 0.45), cy + r],
                 start=270, end=90, fill=(210, 230, 240), width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(210, 230, 240), width=2)
    # land blobs
    draw.ellipse([cx - r + 12, cy - r + 18, cx - 8, cy - 6], fill=(74, 140, 90))
    draw.ellipse([cx + 2, cy + 4, cx + r - 14, cy + r - 16], fill=(74, 140, 90))
    # crack
    pts = [(cx + 6, cy - r + 4), (cx - 12, cy - r // 2), (cx + 10, cy - 4),
           (cx - 8, cy + r // 3), (cx + 4, cy + r - 8)]
    draw.line(pts, fill=RED, width=5, joint="curve")


def draw_flats(draw, x, y, w, h):
    """Apartment block with a smoke column, contained in its box."""
    top = y + 34
    draw.rectangle([x, top, x + w, y + h], fill=(120, 116, 104))
    draw.rectangle([x, top, x + w, top + 12], fill=(84, 80, 70))
    for r in range(2):
        for c in range(4):
            wx = x + 12 + c * (w // 4)
            wy = top + 22 + r * 26
            lit = (r + c) % 3 == 0
            draw.rectangle([wx, wy, wx + w // 6, wy + 16],
                           fill=(255, 214, 130) if lit else (52, 52, 52))
    # broken corner + smoke, inside the box
    draw.polygon([(x + w - 26, top), (x + w, top), (x + w, top + 26),
                  (x + w - 40, top + 16)], fill=(40, 38, 34))
    sx = x + w - 14
    for i, rr in enumerate((9, 12, 14)):
        cy = y + 26 - i * 9
        draw.ellipse([sx - rr, cy - rr, sx + rr, cy + rr],
                     fill=(150, 148, 140))


def draw_tanker(draw, x, y, w, h):
    """Tanker on the sea under two missile arcs."""
    sea_y = y + h - 26
    draw.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    for i in range(4):
        draw.arc([x + i * 40, sea_y + 4, x + i * 40 + 46, sea_y + 18],
                 start=180, end=360, fill=(210, 230, 240), width=2)
    draw.rectangle([x + 8, sea_y - 34, x + w - 8, sea_y], fill=(150, 52, 40))
    draw.rectangle([x + w - 34, sea_y - 52, x + w - 14, sea_y - 34],
                   fill=(220, 220, 210))
    draw.line([(x + w - 24, sea_y - 52), (x + w - 24, sea_y - 64)],
              fill=INK, width=3)
    # missile arcs, inside the box
    draw.arc([x + 6, y + 2, x + w // 2, y + 40], start=200, end=330,
             fill=RED, width=3)
    draw.arc([x + w // 2, y + 2, x + w - 6, y + 40], start=210, end=340,
             fill=RED, width=3)
    draw.ellipse([x + 10, y + 6, x + 18, y + 14], fill=RED)
    draw.ellipse([x + w - 18, y + 6, x + w - 10, y + 14], fill=RED)


def draw_ship_fire(draw, x, y, w, h):
    """Cargo ship burning on the sea, contained in its box."""
    sea_y = y + h - 24
    draw.rectangle([x, sea_y, x + w, y + h], fill=(38, 90, 120))
    draw.rectangle([x + 10, sea_y - 26, x + w - 10, sea_y], fill=(60, 60, 62))
    draw.rectangle([x + w // 2 - 8, sea_y - 44, x + w // 2 + 22, sea_y - 26],
                   fill=(200, 200, 190))
    draw.rectangle([x + 16, sea_y - 38, x + 44, sea_y - 26], fill=(140, 140, 130))
    # flames, kept inside the box
    fx = x + w // 2 + 4
    for dx, fh, col in ((-16, 26, (255, 140, 0)), (0, 36, (255, 90, 0)),
                        (16, 24, (255, 170, 40))):
        draw.polygon([(fx + dx - 10, sea_y - 38), (fx + dx, sea_y - 38 - fh),
                      (fx + dx + 10, sea_y - 38)], fill=col)
    # two small smoke puffs above the flames, inside the box
    for i, rr in enumerate((9, 12)):
        cy = y + 22 - i * 10
        draw.ellipse([fx - rr + 8, cy - rr, fx + rr + 8, cy + rr],
                     fill=(120, 118, 110))


def draw_mercury(draw, cx, cy, r):
    """Small cratered planet with a probe."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(176, 164, 148),
                 outline=INK, width=2)
    for dx, dy, cr in ((-14, -10, 7), (10, 6, 9), (-4, 14, 5), (16, -14, 4)):
        draw.ellipse([cx + dx - cr, cy + dy - cr, cx + dx + cr, cy + dy + cr],
                     fill=(140, 128, 112), outline=(110, 100, 86))
    # probe: small body + panels
    px, py = cx + r + 26, cy - r - 6
    draw.rectangle([px - 14, py - 3, px + 14, py + 3], fill=BLUE)
    draw.rectangle([px - 4, py - 8, px + 4, py + 8], fill=(220, 220, 210),
                   outline=INK)
    draw.line([(px - 4, py), (cx + r + 2, cy - r + 8)], fill=GREY, width=2)


def panel_head(draw, x, y, w, kicker, title, tsize=27):
    draw.text((x, y), kicker, font=F_SANS_B(15), fill=RED)
    y = para(draw, x, y + 22, title, F_SANS_B(tsize), w, leading=tsize + 4)
    return y + 4


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---------- masthead ----------
    rule(d, M, 30, W - M, 3)
    d.text((W // 2, 44), "THE WORLD IN ONE PAGE",
           font=F_SERIF_B(56), fill=INK, anchor="mt")
    rule(d, M, 116, W - M, 2)
    d.text((M, 126), "SUNDAY, 22 NOVEMBER 2026", font=F_SANS_B(19), fill=INK)
    d.text((W - M, 126), "ONE DAY  ·  ONE PAGE", font=F_SANS_B(19),
           fill=INK, anchor="rt")
    rule(d, M, 154, W - M, 3)

    # ---------- lead: COP31 ----------
    ly = 168
    d.text((M, ly), "CLIMATE  ·  ANTALYA, TURKEY", font=F_SANS_B(16), fill=RED)
    d.text((M, ly + 26), "COP31 COLLAPSES", font=F_SERIF_B(66), fill=INK)
    d.text((M, ly + 100),
           "Climate talks end with no deal at all",
           font=F_SERIF(26), fill=INK)
    body = ("Nearly 200 countries leave Antalya without an agreement after "
            "the EU and its allies reject a final draft that never mentions "
            "fossil fuels. The summit closes two days late, empty-handed.")
    para(d, M, ly + 140, body, F_SANS(19), 560, leading=25)
    draw_globe(d, 862, ly + 122, 78)
    d.text((862, ly + 216), "No deal on fossil fuels,",
           font=F_SANS(15), fill=GREY, anchor="mt")
    d.text((862, ly + 236), "no deal on climate finance.",
           font=F_SANS(15), fill=GREY, anchor="mt")
    rule(d, M, 452, W - M, 2)

    # ---------- row 2: three stories ----------
    ry = 470
    cols = [(M, 300), (M + 312, 300), (M + 624, 300)]
    # A: Dymer
    x, w = cols[0]
    y = panel_head(d, x, ry, w, "UKRAINE  ·  DYMER, NEAR KYIV",
                   "Drone hits flats; 14 missing")
    draw_flats(d, x, y + 8, w, 108)
    para(d, x, y + 128,
         "A Russian drone strikes a five-storey apartment block. Two killed, "
         "four hurt, 14 feared under the rubble.",
         F_SANS(16), w, leading=21)
    # B: Gulf
    x, w = cols[1]
    y = panel_head(d, x, ry, w, "THE GULF  ·  BAHRAIN",
                   "Iran strikes Bahrain site")
    draw_tanker(d, x, y + 8, w, 108)
    para(d, x, y + 128,
         "Projectiles hit a civilian industrial site in Sitra; two hurt. "
         "Gulf states condemn the attack.",
         F_SANS(16), w, leading=21)
    # C: Baltic
    x, w = cols[2]
    y = panel_head(d, x, ry, w, "THE BALTIC  ·  GULF OF FINLAND",
                   "Russian ship still burning")
    draw_ship_fire(d, x, y + 8, w, 108)
    para(d, x, y + 128,
         "The cargo ship Sparta II burns a day after a drone strike Finland "
         "says was likely Ukraine's.",
         F_SANS(16), w, leading=21)
    rule(d, M, 752, W - M, 2)

    # ---------- row 3: three short stories ----------
    ry = 770
    x, w = cols[0]
    y = panel_head(d, x, ry, w, "MEXICO  ·  SINALOA",
                   "\u2018El Chapo Isidro\u2019 captured", 24)
    para(d, x, y, "Troops seize cartel boss Fausto Isidro Meza Flores; "
         "11 killed in the raid.",
         F_SANS(16), w, leading=21)
    x, w = cols[1]
    y = panel_head(d, x, ry, w, "INDONESIA  ·  CIKANDE, BANTEN",
                   "Factory fire: 3 dead, 36 missing", 24)
    para(d, x, y, "A blaze at a candy factory leaves three dead and "
         "dozens missing.",
         F_SANS(16), w, leading=21)
    x, w = cols[2]
    y = panel_head(d, x, ry, w, "SPACE  ·  MERCURY",
                   "BepiColombo arrives", 24)
    draw_mercury(d, x + 48, y + 46, 30)
    d.text((x + 100, y + 18), "Two probes enter orbit",
           font=F_SANS(16), fill=INK)
    d.text((x + 100, y + 40), "around Mercury after",
           font=F_SANS(16), fill=INK)
    d.text((x + 100, y + 62), "an eight-year journey.",
           font=F_SANS(16), fill=INK)
    rule(d, M, 906, W - M, 2)

    # ---------- ticker ----------
    ty = 920
    d.text((M, ty), "ALSO ON 22 NOVEMBER", font=F_SANS_B(15), fill=RED)
    ticker = ("Markets slide into correction  ·  World Court: Myanmar guilty "
              "of Rohingya genocide  ·  EU–Indonesia sign trade deal  ·  "
              "Settlers torch cars in West Bank  ·  24 dead as a boat capsizes "
              "in Nigeria  ·  FBI probes crime-database breach")
    para(d, M, ty + 24, ticker, F_SANS(15), W - 2 * M, leading=20)
    rule(d, M, 992, W - M, 2)
    d.text((W // 2, 1000),
           "All stories as reported on Sunday 22 November 2026",
           font=F_SANS(13), fill=GREY, anchor="mt")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
