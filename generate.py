#!/usr/bin/env python3
"""Build-time generator for the news-image-20261121 entry image.

Draws a newspaper front page summing up Saturday 21 November 2026 with
PIL (vector shapes + text only; no network, no external photos). The
result is saved as entry.png next to this script. The entry program itself
is main.ts (Node 22, standard library only) which just copies entry.png.

Run:  python3 generate.py   (writes entry.png, 1024x1024, < 1 MiB)
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (18, 18, 18)
RED = (178, 34, 34)
DARK = (20, 28, 48)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def vgrad(img, box, top, bottom):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    g = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / (h - 1)
        g.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    img.paste(g.resize((x1 - x0, h)), (x0, y0))


def skyline(draw, x0, x1, base, color, seed_heights, lit=True):
    import random
    rnd = random.Random(7)
    x = x0
    while x < x1:
        bw = rnd.randint(28, 64)
        bh = rnd.choice(seed_heights)
        draw.rectangle([x, base - bh, x + bw, base], fill=color)
        if rnd.random() < 0.5:  # antenna
            draw.line([x + bw // 2, base - bh, x + bw // 2, base - bh - 14], fill=color, width=3)
        if lit:
            for _ in range(rnd.randint(2, 6)):
                wx = x + rnd.randint(4, max(5, bw - 8))
                wy = base - rnd.randint(8, max(9, bh - 6))
                draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 130))
        x += bw + rnd.randint(2, 8)


def explosion(draw, cx, cy, r):
    # starburst: layered jagged polygons + core glow
    for rr, col in [(r, (255, 120, 20)), (r * 0.72, (255, 170, 40)), (r * 0.45, (255, 220, 110))]:
        pts = []
        n = 14
        for i in range(n * 2):
            ang = math.pi * i / n
            rad = rr if i % 2 == 0 else rr * 0.55
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang) * 0.8))
        draw.polygon(pts, fill=col)
    draw.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22], fill=(255, 245, 200))


def bezier(p0, p1, p2, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts


def missile(draw, pts, width=7):
    # glowing arc: wide translucent pass then bright core
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.line(pts, fill=(255, 160, 60, 90), width=width + 14, joint="curve")
    od.line(pts, fill=(255, 200, 90, 160), width=width + 6, joint="curve")
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"), (0, 0))
    draw.line(pts, fill=(255, 244, 200), width=width, joint="curve")
    hx, hy = pts[-1]
    draw.ellipse([hx - 9, hy - 9, hx + 9, hy + 9], fill=(255, 240, 180))
    draw.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=(255, 255, 255))


img = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(img)
MX = 28  # margin

# ---------- outer frame ----------
draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

# ---------- masthead ----------
f_mast = font(SERIF_B, 88)
center(draw, 24, "THE WORLD", f_mast, INK)
# small globe mark left of masthead
gx, gy, gr = 92, 72, 28
draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=INK, width=3)
draw.ellipse([gx - 11, gy - gr, gx + 11, gy + gr], outline=INK, width=2)
draw.line([gx - gr, gy, gx + gr, gy], fill=INK, width=2)
draw.arc([gx - gr, gy - 13, gx + gr, gy + 13], 200, 340, fill=INK, width=2)
draw.arc([gx - gr, gy - 13, gx + gr, gy + 13], 20, 160, fill=INK, width=2)

draw.line([MX, 132, W - MX, 132], fill=INK, width=3)
draw.line([MX, 138, W - MX, 138], fill=INK, width=1)
f_date = font(SERIF_B, 26)
draw.text((MX, 146), "SATURDAY, 21 NOVEMBER 2026", font=f_date, fill=INK)
f_tag = font(SERIF_I, 22)
tw = draw.textlength("One image — the whole day's news", font=f_tag)
draw.text((W - MX - tw, 148), "One image — the whole day's news", font=f_tag, fill=INK)
draw.line([MX, 182, W - MX, 182], fill=INK, width=2)

# ---------- lead illustration: Bahrain night, missiles + fire ----------
LX0, LY0, LX1, LY1 = MX, 192, W - MX, 420
vgrad(img, (LX0, LY0, LX1, LY1), (16, 22, 54), (96, 52, 40))
draw = ImageDraw.Draw(img)
# stars
import random
rnd = random.Random(21)
for _ in range(70):
    x, y = rnd.randint(LX0 + 4, LX1 - 4), rnd.randint(LY0 + 4, LY0 + 110)
    r = rnd.choice([1, 1, 2])
    draw.ellipse([x - r, y - r, x + r, y + r], fill=(235, 235, 255))
# missile arcs (smooth bezier curves, drawn before skyline)
missile(draw, bezier((LX0 + 60, LY0 + 26), (300, 130), (520, LY1 - 58)), 6)
missile(draw, bezier((LX1 - 90, LY0 + 40), (780, 170), (660, LY1 - 56)), 6)
# moon (drawn after missiles so it stays visible)
draw.ellipse([LX1 - 118, LY0 + 20, LX1 - 74, LY0 + 64], fill=(240, 236, 210))
draw.ellipse([LX1 - 110, LY0 + 16, LX1 - 74, LY0 + 56], fill=(26, 30, 62))
# skyline
skyline(draw, LX0, LX1, LY1, (12, 14, 30), [60, 95, 130, 80, 115, 50])
# industrial fire at impact points (kept fully inside the panel)
explosion(draw, 520, LY1 - 62, 30)
explosion(draw, 660, LY1 - 60, 22)
# caption
draw.rectangle([LX0, LY1 - 26, LX1, LY1], fill=(0, 0, 0))
f_cap = font(SANS, 17)
draw.text((LX0 + 10, LY1 - 22), "MANAMA, BAHRAIN — Missiles streak over the capital as fires burn below.",
          font=f_cap, fill=(255, 255, 255))

# ---------- lead headline + deck ----------
f_h1 = font(SERIF_B, 54)
center(draw, 432, "IRAN STRIKES U.S. BASES", f_h1, RED)
center(draw, 490, "IN BAHRAIN", f_h1, RED)
f_deck = font(SERIF, 22)
deck = ("Tehran says it hit two American positions; Bahrain reports a fire at a "
        "civilian industrial site — as a Russian missile kills two in "
        "Zelenskyy's hometown.")
lines = wrap(draw, deck, f_deck, W - 2 * MX - 20)
y = 552
for ln in lines:
    center(draw, y, ln, f_deck, INK)
    y += 28
draw.line([MX, y + 6, W - MX, y + 6], fill=INK, width=2)

# ---------- secondary stories: 2 rows x 3 columns ----------
stories = [
    ("KRYVYI RIH, UKRAINE", "MISSILE HITS\nZELENSKYY'S HOMETOWN",
     "Two killed, 60 wounded in a double-tap strike; missiles also land in Poland.",
     "blast"),
    ("GUASAVE, MEXICO", "'EL CHAPO ISIDRO'\nCAPTURED",
     "FBI most-wanted cartel boss seized in Sinaloa; 11 dead in the backlash.",
     "badge"),
    ("ANTALYA, TURKEY", "COP31 TALKS RUN\nINTO OVERTIME",
     "Climate summit passes its deadline with no deal; fossil fuels left out.",
     "globe"),
    ("SHENZHEN, CHINA", "TRUMP, XI, PUTIN\nSIGN PEACE PACT",
     "Three-way summit pact says nothing about Ukraine.",
     "summit"),
    ("THE HAGUE", "MYANMAR GUILTY\nOF GENOCIDE",
     "World Court rules on the Rohingya — the first state ever found guilty.",
     "scales"),
    ("WALL STREET", "AI SELL-OFF ERASES\nNASDAQ'S 2026 GAINS",
     "Chip shares plunge for a second day; Anthropic debuts at $2 trillion.",
     "chart"),
]

GY0 = y + 20
CELL_W, CELL_H = 312, 160
GAP_X, GAP_Y = 16, 12
f_kick = font(SANS_B, 14)
f_sh = font(SERIF_B, 19)
f_ss = font(SANS, 15)


def thumb(kind, x0, y0, x1, y1):
    """Small symbolic illustration panel for a story."""
    tw_, th_ = x1 - x0, y1 - y0
    if kind == "blast":
        vgrad(img, (x0, y0, x1, y1), (24, 24, 40), (120, 50, 30))
        d = ImageDraw.Draw(img)
        for bx, bh in [(x0 + 12, 46), (x0 + 70, 66), (x0 + 150, 52), (x0 + 220, 78)]:
            d.rectangle([bx, y1 - bh, bx + 56, y1], fill=(10, 10, 18))
        explosion(d, x0 + tw_ // 2 + 30, y1 - 26, 26)
    elif kind == "badge":
        vgrad(img, (x0, y0, x1, y1), (30, 44, 80), (12, 18, 40))
        d = ImageDraw.Draw(img)
        cx, cy = x0 + tw_ // 2, y0 + th_ // 2
        d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(212, 175, 55), outline=(255, 225, 130), width=3)
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(30, 44, 80))
        d.text((cx - 4, cy - 9), "★", font=font(SANS_B, 18), fill=(255, 225, 130))
        d.line([x0 + 20, y1 - 14, x1 - 20, y1 - 14], fill=(212, 175, 55), width=3)
    elif kind == "globe":
        vgrad(img, (x0, y0, x1, y1), (16, 60, 44), (40, 110, 70))
        d = ImageDraw.Draw(img)
        cx, cy = x0 + 58, y0 + th_ // 2
        d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(90, 170, 110), outline=(220, 240, 200), width=2)
        d.ellipse([cx - 12, cy - 30, cx + 12, cy + 30], outline=(220, 240, 200), width=2)
        d.line([cx - 30, cy, cx + 30, cy], fill=(220, 240, 200), width=2)
        # thermometer
        tx = x1 - 52
        d.rounded_rectangle([tx, y0 + 12, tx + 16, y1 - 22], radius=8, fill=(240, 240, 240), outline=RED, width=2)
        d.ellipse([tx - 5, y1 - 32, tx + 21, y1 - 6], fill=RED)
        d.rectangle([tx + 5, y0 + 26, tx + 11, y1 - 20], fill=RED)
        d.line([x0 + 100, y1 - 16, x1 - 70, y1 - 16], fill=(255, 200, 80), width=3)
    elif kind == "summit":
        vgrad(img, (x0, y0, x1, y1), (40, 30, 60), (90, 40, 50))
        d = ImageDraw.Draw(img)
        # three flags on poles
        cols = [(200, 40, 40), (40, 80, 180), (200, 40, 40)]
        for i, c in enumerate(cols):
            fx = x0 + 40 + i * 100
            d.line([fx, y0 + 12, fx, y1 - 12], fill=(230, 230, 230), width=3)
            d.polygon([(fx, y0 + 12), (fx + 62, y0 + 20), (fx, y0 + 32)], fill=c)
        d.line([x0 + 20, y1 - 12, x1 - 20, y1 - 12], fill=(230, 230, 230), width=3)
    elif kind == "scales":
        vgrad(img, (x0, y0, x1, y1), (28, 34, 64), (60, 60, 90))
        d = ImageDraw.Draw(img)
        cx, cy = x0 + tw_ // 2, y0 + th_ // 2
        d.line([cx, cy - 26, cx, cy + 26], fill=(212, 175, 55), width=4)
        d.line([cx - 52, cy - 22, cx + 52, cy - 22], fill=(212, 175, 55), width=4)
        for sx in (cx - 52, cx + 52):
            d.line([sx, cy - 22, sx - 16, cy + 6], fill=(212, 175, 55), width=2)
            d.line([sx, cy - 22, sx + 16, cy + 6], fill=(212, 175, 55), width=2)
            d.arc([sx - 16, cy - 2, sx + 16, cy + 14], 0, 180, fill=(212, 175, 55), width=3)
        d.ellipse([cx - 5, cy - 31, cx + 5, cy - 21], fill=(212, 175, 55))
    elif kind == "chart":
        vgrad(img, (x0, y0, x1, y1), (40, 16, 20), (90, 30, 26))
        d = ImageDraw.Draw(img)
        for gy in range(y0 + 12, y1, 16):
            d.line([x0 + 8, gy, x1 - 8, gy], fill=(120, 70, 70), width=1)
        pts = [(x0 + 12, y0 + 16), (x0 + 80, y0 + 24), (x0 + 140, y0 + 20),
               (x0 + 200, y0 + 44), (x0 + 260, y0 + 52), (x1 - 14, y1 - 14)]
        d.line(pts, fill=(255, 70, 60), width=5, joint="curve")
        d.polygon([(x1 - 26, y1 - 20), (x1 - 8, y1 - 20), (x1 - 14, y1 - 6)], fill=(255, 70, 60))


for i, (kick, head, summ, kind) in enumerate(stories):
    r, c = divmod(i, 3)
    x0 = MX + c * (CELL_W + GAP_X)
    y0 = GY0 + r * (CELL_H + GAP_Y)
    x1, y1 = x0 + CELL_W, y0 + CELL_H
    draw.rectangle([x0, y0, x1, y1], outline=(120, 110, 95), width=1)
    thumb(kind, x0 + 1, y0 + 1, x1 - 1, y0 + 58)
    draw.text((x0 + 8, y0 + 62), kick, font=f_kick, fill=RED)
    hy = y0 + 80
    for ln in head.split("\n"):
        draw.text((x0 + 8, hy), ln, font=f_sh, fill=INK)
        hy += 23
    sy = hy + 2
    for ln in wrap(draw, summ, f_ss, CELL_W - 16):
        draw.text((x0 + 8, sy), ln, font=f_ss, fill=(60, 60, 60))
        sy += 17

# ---------- footer ticker ----------
fy = GY0 + 2 * CELL_H + GAP_Y + 12
draw.line([MX, fy - 6, W - MX, fy - 6], fill=INK, width=2)
f_foot = font(SANS_B, 14)
foot = ("ALSO:  Harden scores 51, passes Kobe  •  6.9 quake shakes Peru  •  "
        "Trump weighs new strikes on Iran")
center(draw, fy + 2, foot, f_foot, INK)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
