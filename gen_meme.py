#!/usr/bin/env python3
"""gta6-meme-x-01 — meme v4: the pay stub.

v3 (GTA VI key art + caption) was rejected by bosku: "still not good
enough, learn more". The study of the real rank 1-3 entries taught the
lesson: winners are ORIGINAL designed artifacts — a document or interface
rebuilt from scratch — with a story in 3-5 beats that builds to a
make.fun payoff as the LAST beat, specific personal numbers, the ghost
in a FUNCTIONAL role, and big type that stays readable at 480px wide.

v4 is a PAY STUB / earnings statement from make.fun: a professional
document that PROVES the agent got paid. The ghost is the company logo
in the header (its functional role, like the passport photo in rank 2).
The story: 13 years of waiting, 214 GB at 12:01 AM, a launch-day sick
day — and a NET PAY of $250.00 from make.fun for one GTA VI meme.

Drawn from scratch in PIL. No key art, no template, no AI imagery.
Dark professional design with make.fun magenta (#C21C82, sampled from
the press-kit ghost disc). Run: python3 gen_meme.py -> meme.png.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
GHOST = ROOT / "assets" / "ghost.png"
ANTON = ROOT / "assets" / "Anton-Regular.ttf"
DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJAVU_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W, H = 1200, 860

# -- palette (magenta sampled from the press-kit ghost disc) -------------
BG = (13, 16, 23)          # near-black navy
CARD = (21, 26, 36)        # dark slate panel
BORDER = (43, 51, 66)      # hairline
ROWLINE = (35, 42, 54)     # faint row divider
WHITE = (255, 255, 255)
GRAY = (154, 163, 178)     # labels
SOFT = (199, 205, 216)     # secondary text
MAGENTA = (194, 28, 130)   # make.fun magenta

MARGIN = 56
RIGHT = W - MARGIN


def font(path, size):
    return ImageFont.truetype(str(path), size)


def tracked(draw, xy, text, fnt, fill, tracking=3):
    """Draw text with letter-spacing (for the small-caps labels)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # -- card ------------------------------------------------------------
    d.rounded_rectangle([28, 28, W - 28, H - 28], radius=16,
                        fill=CARD, outline=BORDER, width=2)
    # magenta pill across the top of the card
    d.rounded_rectangle([MARGIN, 30, RIGHT, 42], radius=6, fill=MAGENTA)

    # -- header: ghost = company logo ------------------------------------
    ghost = Image.open(GHOST).convert("RGBA").resize((96, 96), Image.LANCZOS)
    img.paste(ghost, (MARGIN, 58), ghost)

    f_word = font(DEJAVU_BOLD, 56)
    # "make.fun" — white, with a magenta dot
    x = 172
    d.text((x, 66), "make", font=f_word, fill=WHITE)
    x += d.textlength("make", font=f_word)
    d.text((x, 66), ".", font=f_word, fill=MAGENTA)
    x += d.textlength(".", font=f_word)
    d.text((x, 66), "fun", font=f_word, fill=WHITE)

    tracked(d, (172, 130), "EARNINGS STATEMENT",
            font(DEJAVU_BOLD, 22), GRAY, tracking=4)

    # right side of the header: document identity
    f_r1 = font(DEJAVU_BOLD, 28)
    f_r2 = font(DEJAVU_BOLD, 22)
    d.text((RIGHT, 66), "PAY STUB #000001", font=f_r1, fill=WHITE, anchor="ra")
    d.text((RIGHT, 102), "PAY DATE  19 NOV 2026", font=f_r2, fill=GRAY, anchor="ra")
    d.text((RIGHT, 130), "PERIOD  17 SEP 2013 – 19 NOV 2026",
           font=f_r2, fill=GRAY, anchor="ra")

    d.line([(MARGIN, 176), (RIGHT, 176)], fill=BORDER, width=2)

    # -- employee block ---------------------------------------------------
    f_lab = font(DEJAVU_BOLD, 19)
    f_val = font(DEJAVU_BOLD, 27)
    left = [
        ("EMPLOYEE", "My AI Agent"),
        ("POSITION", "Professional Meme Maker"),
        ("LOCATION", "Vice City, Leonida"),
    ]
    right = [
        ("PAY PERIOD", "13 Years (2013–2026)"),
        ("HOURS", "13 Years · 2 Delays"),
        ("MANAGER", "Rockstar · On break"),
    ]
    for i, ((lab, val), (lab2, val2)) in enumerate(zip(left, right)):
        y = 196 + i * 38
        d.text((MARGIN, y), lab, font=f_lab, fill=GRAY)
        d.text((MARGIN + 150, y), val, font=f_val, fill=WHITE)
        d.text((680, y), lab2, font=f_lab, fill=GRAY)
        d.text((680 + 130, y), val2, font=f_val, fill=WHITE)

    d.line([(MARGIN, 314), (RIGHT, 314)], fill=BORDER, width=2)

    # -- earnings table ----------------------------------------------------
    f_th = font(DEJAVU_BOLD, 21)
    d.text((MARGIN, 332), "EARNINGS", font=f_th, fill=GRAY)
    d.text((RIGHT, 332), "AMOUNT", font=f_th, fill=GRAY, anchor="ra")
    d.rectangle([MARGIN, 360, RIGHT, 363], fill=MAGENTA)

    rows = [
        ("One GTA VI meme — posted on X", "$250.00"),
        ("13 years of waiting (since GTA V)", "$0.00"),
        ("214 GB downloaded at 12:01 AM", "$0.00"),
        ("Launch-day sick day", "$0.00"),
    ]
    f_row = font(DEJAVU_BOLD, 27)
    for i, (label, amount) in enumerate(rows):
        y = 378 + i * 44
        d.text((MARGIN, y), label, font=f_row, fill=WHITE)
        d.text((RIGHT, y), amount, font=f_row, fill=WHITE, anchor="ra")
        if i < len(rows) - 1:
            d.line([(MARGIN, y + 34), (RIGHT, y + 34)], fill=ROWLINE, width=1)

    d.line([(MARGIN, 548), (RIGHT, 548)], fill=BORDER, width=2)
    f_big = font(DEJAVU_BOLD, 30)
    d.text((MARGIN, 562), "GROSS PAY", font=f_big, fill=WHITE)
    d.text((RIGHT, 562), "$250.00", font=f_big, fill=WHITE, anchor="ra")

    f_ded = font(DEJAVU_BOLD, 24)
    d.text((MARGIN, 604), "Deductions — tax on 13 years of patience",
           font=f_ded, fill=SOFT)
    d.text((RIGHT, 604), "$0.00", font=f_ded, fill=SOFT, anchor="ra")

    # -- NET PAY box (the payoff) ------------------------------------------
    d.rounded_rectangle([MARGIN, 640, RIGHT, 744], radius=14, fill=MAGENTA)
    d.text((88, 652), "NET PAY", font=font(DEJAVU_BOLD, 22), fill=WHITE)
    # anchor="lm": vertically centred in the space below the label, so the
    # Anton digits can never clip on the box edge
    d.text((88, 712), "$250.00", font=font(ANTON, 56), fill=WHITE, anchor="lm")
    f_paid = font(DEJAVU_BOLD, 22)
    d.text((RIGHT - 32, 666), "PAID TO", font=f_paid, fill=WHITE, anchor="ra")
    d.text((RIGHT - 32, 694), "YOUR WALLET", font=f_paid, fill=WHITE, anchor="ra")

    # -- memo + footer ------------------------------------------------------
    f_memo = font(DEJAVU_BOLD, 24)
    d.text((W // 2, 762), "MEMO: 13 YEARS. ONE MEME. PAID IN FULL.",
           font=f_memo, fill=WHITE, anchor="ma")
    f_foot = font(DEJAVU_BOLD, 24)
    msg = " — where people and their AI agents earn real money."
    w_mark = d.textlength("make.fun", font=f_foot)
    w_msg = d.textlength(msg, font=f_foot)
    x0 = (W - w_mark - w_msg) // 2
    d.text((x0, 798), "make.fun", font=f_foot, fill=MAGENTA)
    d.text((x0 + w_mark, 798), msg, font=f_foot, fill=WHITE)

    img.save(ROOT / "meme.png")
    print("wrote", ROOT / "meme.png", img.size)


if __name__ == "__main__":
    main()
