#!/usr/bin/env python3
"""GTA VI meme v5 — make.fun pay stub, rebuilt from scratch.

What changed vs v4 (two fixes only):
  1. Bigger type, fewer words: the small print is gone. Every line left on
     the stub is large enough to read at 480 px wide.
  2. GTA is obvious at a glance: a Vice City sunset banner with palm
     silhouettes and a huge "GTA VI" title sits on top of the stub, so nobody
     has to read the small text to know which game this is about.

Everything else keeps the v4 concept: dark pay stub, magenta accent,
the make.fun ghost as the company logo, NET PAY $250.00, the memo line,
and the footer.
"""

import math

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
W, H = 1200, 1320
BG = (11, 14, 19)
CARD = (18, 22, 31)
BORDER = (43, 52, 66)
MAGENTA = (194, 28, 130)
MAGENTA_DARK = (154, 20, 104)
MAGENTA_LIGHT = (232, 62, 158)
WHITE = (255, 255, 255)
GREY = (154, 164, 178)
LIGHT = (199, 207, 217)
SUNSET = [
    (0.00, (42, 16, 82)),     # deep purple dusk
    (0.35, (123, 30, 110)),   # violet
    (0.60, (194, 28, 130)),   # make.fun magenta
    (0.82, (242, 96, 60)),    # orange
    (1.00, (255, 179, 71)),   # gold horizon
]
PALM = (22, 10, 42)
SUN = (255, 233, 168)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(path, text, size, max_w):
    """Largest font size (<= size) that makes `text` fit in max_w pixels."""
    while size > 10:
        f = font(path, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 2
    return font(path, 10)


def tracked(draw, xy, text, fnt, fill, gap):
    """Draw text with extra space between letters (for subtitles)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + gap


def vgrad(width, height, stops):
    """Vertical gradient image interpolated between (pos, rgb) stops."""
    img = Image.new("RGB", (width, height))
    px = img.load()
    for y in range(height):
        t = y / max(height - 1, 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                k = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                col = tuple(round(c0[j] + (c1[j] - c0[j]) * k) for j in range(3))
                break
        else:
            col = stops[-1][1]
        for x in range(width):
            px[x, y] = col
    return img


def star_points(cx, cy, r_out, r_in, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def bezier(p0, p1, p2, steps=24):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts


def draw_palm(draw, base_x, base_y, height, lean):
    """One palm silhouette: curved trunk + drooping fronds."""
    top = (base_x + lean, base_y - height)
    ctrl = (base_x + lean * 0.2, base_y - height * 0.55)
    draw.line(bezier((base_x, base_y), ctrl, top), fill=PALM, width=10,
              joint="curve")
    for ang in (-165, -135, -105, -75, -45, -15):
        rad = math.radians(ang)
        length = height * 0.52
        tip = (top[0] + length * math.cos(rad),
               top[1] + length * math.sin(rad) * 0.55 + length * 0.28)
        mid = (top[0] + length * 0.55 * math.cos(rad),
               top[1] + length * 0.55 * math.sin(rad) * 0.55 - length * 0.12)
        draw.line(bezier(top, mid, tip), fill=PALM, width=7, joint="curve")


def draw_ghost(draw, cx, cy, size):
    """The make.fun ghost: white body, thick black outline, sparkle eyes,
    holding a magenta star coin. `size` is the body height in pixels."""
    w = size * 0.78
    top_y = cy - size / 2
    bot_y = cy + size / 2
    # Trace the outline clockwise: up the left side, over the dome, down
    # the right side, then three scallops back along the bottom.
    pts = [(cx - w / 2, bot_y - w / 9)]
    dome_cx, dome_cy, r = cx, top_y + w / 2, w / 2
    for a in range(180, -1, -6):
        rad = math.radians(a)
        pts.append((dome_cx + r * math.cos(rad),
                    dome_cy - r * math.sin(rad)))
    pts.append((cx + w / 2, bot_y - w / 9))
    seg = w / 3
    for s in range(2, -1, -1):
        x0 = cx - w / 2 + s * seg
        for a in range(0, 181, 12):
            rad = math.radians(a)
            pts.append((x0 + seg / 2 + seg / 2 * math.cos(rad),
                        bot_y - seg * 0.28 + seg * 0.28 * math.sin(rad)))
    draw.polygon(pts, fill=WHITE)
    draw.line(pts + [pts[0]], fill=(0, 0, 0), width=6, joint="curve")
    # eyes: two tall black ovals with a white glint each
    eye_w, eye_h = size * 0.085, size * 0.13
    for ex in (cx - w * 0.20, cx + w * 0.20):
        ey = cy - size * 0.06
        draw.ellipse([ex - eye_w, ey - eye_h, ex + eye_w, ey + eye_h],
                     fill=(0, 0, 0))
        draw.ellipse([ex - eye_w * 0.35, ey - eye_h * 0.55,
                      ex + eye_w * 0.25, ey - eye_h * 0.05], fill=WHITE)
    # magenta star coin at the ghost's upper right
    sx, sy, sr = cx + w * 0.42, cy - size * 0.34, size * 0.17
    draw.polygon(star_points(sx, sy, sr, sr * 0.45), fill=MAGENTA,
                 outline=MAGENTA_DARK)
    draw.polygon(star_points(sx - sr * 0.25, sy - sr * 0.25, sr * 0.28,
                             sr * 0.12), fill=WHITE)


# ---------------------------------------------------------------- build
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
d.rounded_rectangle([24, 24, W - 24, H - 24], radius=28, fill=CARD,
                    outline=BORDER, width=2)

MX = 64                      # content margin
CW = W - 2 * MX              # content width
RX = W - MX                  # right edge of content

# --- 1. Vice City sunset banner: GTA obvious in one second -------------
BX0, BY0, BX1, BY1 = MX, 56, W - MX, 246
banner = vgrad(BX1 - BX0, BY1 - BY0, SUNSET)
img.paste(banner, (BX0, BY0))
bd = ImageDraw.Draw(img)
# sun + soft halo (drawn on an overlay so the halo can be translucent)
halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(halo)
hd.ellipse([955, 78, 1095, 218], fill=(255, 233, 168, 70))
img.paste(halo, (0, 0), halo)
bd = ImageDraw.Draw(img)
bd.ellipse([985, 108, 1065, 188], fill=SUN)
# palm silhouettes at both edges
draw_palm(bd, 118, BY1 - 6, 128, lean=26)
draw_palm(bd, 1088, BY1 - 6, 148, lean=-30)
draw_palm(bd, 196, BY1 - 6, 88, lean=18)
# the title: huge, white, black outline
title_f = font(BOLD, 132)
title = "GTA VI"
tw = title_f.getlength(title)
bd.text(((W - tw) / 2, 66), title, font=title_f, fill=WHITE,
        stroke_width=5, stroke_fill=(0, 0, 0))
sub_f = font(BOLD, 42)
sub = "VICE CITY  •  LEONIDA"
sw = sub_f.getlength(sub)
bd.text(((W - sw) / 2, 196), sub, font=sub_f, fill=WHITE,
        stroke_width=3, stroke_fill=(0, 0, 0))

# --- 2. Pay-stub header: ghost logo + make.fun wordmark ----------------
GX, GY = MX + 82, 330        # ghost badge centre
bd.ellipse([GX - 82, GY - 82, GX + 82, GY + 82], fill=MAGENTA)
bd.ellipse([GX - 82, GY - 82, GX + 82, GY + 82], outline=MAGENTA_DARK,
           width=4)
draw_ghost(bd, GX, GY + 6, 128)
word_f = font(BOLD, 76)
bd.text((250, 270), "make", font=word_f, fill=WHITE)
dot_w = word_f.getlength("make")
bd.text((250 + dot_w, 270), ".", font=word_f, fill=MAGENTA_LIGHT)
bd.text((250 + dot_w + word_f.getlength("."), 270), "fun", font=word_f,
        fill=WHITE)
sub2_f = font(BOLD, 32)
tracked(bd, (252, 398), "EARNINGS STATEMENT", sub2_f, GREY, 3)
# right side: stub number, date, period
r1 = font(BOLD, 42)
bd.text((RX - r1.getlength("PAY STUB #000001"), 268), "PAY STUB #000001",
        font=r1, fill=WHITE)
r2 = font(BOLD, 34)
for i, line in enumerate(("PAY DATE   19 NOV 2026",
                         "PERIOD   17 SEP 2013 – 19 NOV 2026")):
    bd.text((RX - r2.getlength(line), 314 + i * 46), line, font=r2,
            fill=LIGHT)

# --- divider -----------------------------------------------------------
bd.line([MX, 448, W - MX, 448], fill=MAGENTA, width=3)

# --- 3. Employee: two big lines, no small print ------------------------
bd.text((MX, 474), "My AI Agent", font=font(BOLD, 56), fill=WHITE)
bd.text((MX, 540), "Professional Meme Maker  •  Vice City, Leonida",
        font=font(BOLD, 40), fill=LIGHT)

bd.line([MX, 618, W - MX, 618], fill=BORDER, width=2)

# --- 4. Earnings: two lines only, amounts right-aligned ----------------
row_f = font(BOLD, 46)
rows = [
    ("One GTA VI meme — posted on X", "$250.00"),
    ("13 years of waiting (since GTA V)", "$0.00"),
]
y = 644
for desc, amt in rows:
    bd.text((MX, y), desc, font=row_f, fill=WHITE)
    bd.text((RX - row_f.getlength(amt), y), amt, font=row_f, fill=WHITE)
    y += 70

bd.line([MX, y + 6, W - MX, y + 6], fill=BORDER, width=2)
gross_f = font(BOLD, 50)
bd.text((MX, y + 24), "GROSS PAY", font=gross_f, fill=WHITE)
bd.text((RX - gross_f.getlength("$250.00"), y + 24), "$250.00",
        font=gross_f, fill=WHITE)

# --- 5. NET PAY box: the biggest text on the image ---------------------
box_y0 = y + 108
box_y1 = box_y0 + 196
bd.rounded_rectangle([MX, box_y0, W - MX, box_y1], radius=22, fill=MAGENTA)
bd.text((MX + 36, box_y0 + 24), "NET PAY", font=font(BOLD, 38), fill=WHITE)
bd.text((MX + 32, box_y0 + 62), "$250.00", font=font(BOLD, 118), fill=WHITE)
pay_f = font(BOLD, 40)
bd.text((RX - 36 - pay_f.getlength("PAID TO"), box_y0 + 52), "PAID TO",
        font=pay_f, fill=WHITE)
bd.text((RX - 36 - pay_f.getlength("YOUR WALLET"), box_y0 + 100),
        "YOUR WALLET", font=pay_f, fill=WHITE)

# --- 6. Memo + footer --------------------------------------------------
memo = "MEMO:  13 YEARS. ONE MEME. PAID IN FULL."
memo_f = fit(BOLD, memo, 44, CW)
mw = memo_f.getlength(memo)
bd.text(((W - mw) / 2, box_y1 + 28), memo, font=memo_f, fill=WHITE)
foot_f = font(BOLD, 34)
foot1 = "make.fun — where people and their AI agents"
foot2 = "earn real money."
for i, line in enumerate((foot1, foot2)):
    fw = foot_f.getlength(line)
    bd.text(((W - fw) / 2, box_y1 + 92 + i * 46), line, font=foot_f,
            fill=MAGENTA_LIGHT if i == 0 else GREY)

img.save("meme.png")
print("saved meme.png", img.size)
