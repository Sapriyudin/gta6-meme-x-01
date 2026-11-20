"""gta6-meme-x-01 — meme v8 generator (written fresh for the resubmit).

Design: the pay stub is TRANSPARENT. There is no black box anywhere:
the GTA VI key art fills the whole canvas, the stub text sits straight
on the art, and a dark gradient overlay keeps the words readable while
the sunset shows through faintly behind them.

Build order:
  1. Backdrop — keyart.jpg cover-scaled to 1200x1390, blurred.
  2. Dark gradient overlay — clear at the top, ~84% black where the
     text lives, so the art stays visible but never fights the words.
  3. Crisp banner — the same key art, sharp, on top; it fades into
     the darkened backdrop so the sunset melts into the document.
  4. Pay stub — ghost logo, make.fun header, employee block, earnings
     rows, magenta NET PAY box, and the PURCHASED WITH THIS PAYCHECK
     box (GTA VI Standard Edition $69.99, cash left $180.01).

The posted image this rebuilds is at
https://x.com/SAPRIYUDIN18/status/2123614264019779916
(the earlier v4 post was status 2123486376943644985).

Run: python3 gen_meme_v8.py  ->  meme.png (1200x1390) in this dir.

Calibration note: every text size and position below was measured
against the posted image (status 2123614264019779916), not guessed.
The differences from a first draft: the "make.fun" title is a wide
rounded bold (DejaVu Bold 54), not condensed Anton; the employee
values are 27px and the right column sits at x=812; the earnings
rows start at y=712; the NET box sits 12px higher (972-1076) with a
smaller $250.00 (Anton 56); the purchase block carries a $69.99
amount line above a green ✓ PAID on the Bought row; MEMO and the
footer are 24px.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
KEYART = ROOT / "keyart.jpg"
GHOST = ROOT / "assets" / "ghost.png"
ANTON = ROOT / "assets" / "Anton-Regular.ttf"
DEJAVU = Path("/usr/share/fonts/truetype/dejavu")
OUT = ROOT / "meme.png"

W, H = 1200, 1390

MAGENTA = (194, 28, 130)   # #C21C82
WHITE = (255, 255, 255)
SOFT = (139, 148, 167)     # #8B94A7 — labels
LIGHT = (203, 205, 214)    # secondary body text (deductions, Bought
                           # line): measured from the posted image, this
                           # text is a light gray, nearly white — much
                           # brighter than the SOFT label gray.
GREEN = (46, 204, 113)     # #2ECC71
LINE = (45, 53, 68)        # thin divider lines

LEFT = 56
RIGHT = 1144


def anton(size):
    return ImageFont.truetype(str(ANTON), size)


def bold(size):
    return ImageFont.truetype(str(DEJAVU / "DejaVuSans-Bold.ttf"), size)


def regular(size):
    return ImageFont.truetype(str(DEJAVU / "DejaVuSans.ttf"), size)


def draw_right(d, x, y, text, font, fill):
    """Draw text right-aligned so its right edge is at x."""
    w = d.textlength(text, font=font)
    d.text((x - w, y), text, font=font, fill=fill)


def draw_center(d, cx, y, text, font, fill):
    """Draw text centered on cx."""
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)


def draw_spaced(d, x, y, text, font, fill, spacing=4):
    """Draw text left-aligned with extra tracking between letters."""
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + spacing


def divider(d, y, fill=LINE, width=2):
    d.line([(LEFT, y), (RIGHT, y)], fill=fill, width=width)


def main():
    # -- 1. Backdrop: key art, full-bleed + blurred ---------------------
    # keyart.jpg is 650x366. Cover-scale to the whole 1200x1390 canvas
    # (center crop), then blur so the art becomes soft colour behind
    # the text instead of readable shapes.
    key = Image.open(KEYART).convert("RGB")
    scale = max(W / key.width, H / key.height)
    bw, bh = int(key.width * scale + 0.5), int(key.height * scale + 0.5)
    backdrop = key.resize((bw, bh), Image.LANCZOS)
    left = (bw - W) // 2
    top = (bh - H) // 2
    backdrop = backdrop.crop((left, top, left + W, top + H))
    backdrop = backdrop.filter(ImageFilter.GaussianBlur(10))
    img = backdrop.copy()

    # -- 2. Dark gradient overlay ---------------------------------------
    # Black, transparent above y=240, ramping to alpha 215 at y=400 and
    # constant below. The art shows through faintly behind the words —
    # that is the transparent look.
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(H):
        if y < 240:
            a = 0
        elif y < 400:
            a = int(215 * (y - 240) / 160)
        else:
            a = 215
        od.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    # -- 3. Crisp banner on top, fading into the backdrop ---------------
    # Same key art, sharp: resize to 1200 wide (676 tall), take the band
    # y=25..385 — the "grand theft auto" logo plus Jason & Lucia's
    # faces. The outdated "VI COMING 2025" at the bottom is cropped
    # out. Gradient alpha (opaque to y=240, transparent at y=360) melts
    # the sunset into the darkened backdrop.
    banner = key.resize((1200, 676), Image.LANCZOS).crop((0, 25, 1200, 385))
    mask = Image.new("L", (1200, 360), 0)
    md = ImageDraw.Draw(mask)
    for y in range(360):
        a = 255 if y < 240 else int(255 * (360 - y) / 120)
        md.line([(0, y), (1200, y)], fill=a)
    img.paste(banner, (0, 0), mask)
    d = ImageDraw.Draw(img)

    # -- 4. Header ------------------------------------------------------
    # Ghost logo: magenta disc (diameter 110) with the white ghost on it.
    d.ellipse([(56, 390), (166, 500)], fill=MAGENTA)
    ghost = Image.open(GHOST).convert("RGBA").resize((84, 84), Image.LANCZOS)
    img.paste(ghost, (69, 403), ghost)
    d = ImageDraw.Draw(img)

    # "make.fun" — DejaVu Bold 54px, white, with a magenta dot.
    # Measured from the posted image: the title is a wide rounded
    # bold, not condensed Anton (Anton 62 renders 231px wide; the
    # posted title is 284px wide and 43px tall, which is DejaVu
    # Bold 54). Anton would also collide with EARNINGS STATEMENT.
    f_title = bold(54)
    x = 180
    for part, color in (("make", WHITE), (".", MAGENTA), ("fun", WHITE)):
        d.text((x, 398), part, font=f_title, fill=color)
        x += d.textlength(part, font=f_title)
    draw_spaced(d, 180, 452, "EARNINGS STATEMENT", bold(26), SOFT, spacing=5)

    # Right side, right-aligned at x=1144. PAY STUB is DejaVu Bold 28
    # in the posted image (294px wide), not Anton 34 (238px).
    draw_right(d, RIGHT, 398, "PAY STUB #000001", bold(28), WHITE)
    draw_right(d, RIGHT, 438, "PAY DATE  19 NOV 2026", bold(26), SOFT)
    draw_right(d, RIGHT, 468, "PERIOD  17 SEP 2013 - 19 NOV 2026",
               bold(26), SOFT)

    divider(d, 500)

    # -- 5. Employee block ----------------------------------------------
    # Measured from the posted image: the values are 27px (not 30 —
    # "Professional Meme Maker" is 388px wide, which is Bold 27),
    # the right column sits at x=812 (not 855 — Bold 30 at 855 runs
    # off the right edge), and the right labels are 19px so the long
    # "PAY PERIOD" clears the values.
    f_label = bold(24)
    f_rlabel = bold(19)
    f_value = bold(27)
    d.text((LEFT, 530), "EMPLOYEE", font=f_label, fill=SOFT)
    d.text((LEFT, 566), "POSITION", font=f_label, fill=SOFT)
    d.text((LEFT, 602), "LOCATION", font=f_label, fill=SOFT)
    d.text((210, 530), "My AI Agent", font=f_value, fill=WHITE)
    d.text((210, 566), "Professional Meme Maker", font=f_value, fill=WHITE)
    d.text((210, 602), "Vice City, Leonida", font=f_value, fill=WHITE)

    d.text((685, 530), "PAY PERIOD", font=f_rlabel, fill=SOFT)
    d.text((685, 566), "HOURS", font=f_rlabel, fill=SOFT)
    d.text((685, 602), "MANAGER", font=f_rlabel, fill=SOFT)
    d.text((812, 530), "13 Years (2013-2026)", font=f_value, fill=WHITE)
    d.text((812, 566), "13 Years · 2 Delays", font=f_value, fill=WHITE)
    d.text((812, 602), "Rockstar · On break", font=f_value, fill=WHITE)

    divider(d, 646)

    # -- 6. Earnings ----------------------------------------------------
    # Header is 20px in the posted image (ink 14px tall), and the
    # magenta underline sits at y=693, not 706.
    d.text((LEFT, 664), "EARNINGS", font=bold(20), fill=SOFT)
    draw_right(d, RIGHT, 664, "AMOUNT", bold(20), SOFT)
    d.line([(LEFT, 693), (RIGHT, 693)], fill=MAGENTA, width=4)

    f_row = bold(34)
    rows = [
        (712, "One GTA VI meme — posted on X", "$250.00"),
        (756, "13 years of waiting (since GTA V)", "$0.00"),
        (800, "214 GB downloaded at 12:01 AM", "$0.00"),
        (844, "Launch-day sick day", "$0.00"),
    ]
    for y, label, amount in rows:
        d.text((LEFT, y), label, font=f_row, fill=WHITE)
        draw_right(d, RIGHT, y, amount, f_row, WHITE)

    divider(d, 896)

    # -- 7. Gross pay + deductions --------------------------------------
    # Measured: GROSS PAY is DejaVu Bold 30 (183px wide, 21px tall),
    # not Anton 38 (151px wide, 33px tall) — and so is its $250.00.
    # The deductions line and its $0.00 are LIGHT gray, not SOFT.
    d.text((LEFT, 894), "GROSS PAY", font=bold(30), fill=WHITE)
    draw_right(d, RIGHT, 894, "$250.00", bold(30), WHITE)
    d.text((LEFT, 935), "Deductions — tax on 13 years of patience",
           font=regular(28), fill=LIGHT)
    draw_right(d, RIGHT, 935, "$0.00", regular(28), LIGHT)

    # -- 8. NET PAY box -------------------------------------------------
    # Measured: the box spans y=972-1076 (12px higher than a first
    # draft), NET PAY is 24px, and the big amount is Anton 56
    # (173px wide), not Anton 68 (215px).
    d.rounded_rectangle([(56, 972), (1144, 1076)], radius=16, fill=MAGENTA)
    d.text((86, 984), "NET PAY", font=bold(24), fill=WHITE)
    d.text((86, 1002), "$250.00", font=anton(56), fill=WHITE)
    draw_right(d, 1114, 998, "PAID TO", bold(24), WHITE)
    draw_right(d, 1114, 1026, "YOUR WALLET", bold(24), WHITE)

    # -- 9. Purchased with this paycheck --------------------------------
    # Measured: the label is Bold 24 with 2px tracking (514px wide);
    # the right column is $69.99 on the title row and ✓ PAID on the
    # Bought row — a first draft put ✓ PAID on the title row and
    # forgot the $69.99 entirely.
    draw_spaced(d, LEFT, 1122, "PURCHASED WITH THIS PAYCHECK",
                bold(24), MAGENTA, spacing=2)
    d.text((LEFT, 1152), "GTA VI — Standard Edition", font=bold(34),
           fill=WHITE)
    draw_right(d, RIGHT, 1150, "$69.99", bold(34), WHITE)
    d.text((LEFT, 1188), "Bought with this paycheck · 19 Nov 2026",
           font=regular(26), fill=LIGHT)
    draw_right(d, RIGHT, 1188, "✓ PAID", bold(30), GREEN)
    d.text((LEFT, 1227), "Cash left from this paycheck", font=bold(30),
           fill=WHITE)
    draw_right(d, RIGHT, 1227, "$180.01", bold(34), WHITE)

    divider(d, 1272)

    # -- 10. Memo + footer ----------------------------------------------
    # Measured: MEMO is Bold 24 (592px wide) at y=1272, right under
    # the divider; the footer is Bold 24 at y=1312.
    draw_center(d, W // 2, 1272, "MEMO: 13 YEARS. ONE MEME. PAID IN FULL.",
                bold(24), WHITE)
    f_foot = bold(24)
    tail = " — where people and their AI agents earn real money."
    total_w = (d.textlength("make.fun", font=f_foot)
               + d.textlength(tail, font=f_foot))
    x = (W - total_w) / 2
    d.text((x, 1312), "make.fun", font=f_foot, fill=MAGENTA)
    d.text((x + d.textlength("make.fun", font=f_foot), 1312), tail,
           font=f_foot, fill=WHITE)

    img.save(OUT)
    print(f"wrote {OUT} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
