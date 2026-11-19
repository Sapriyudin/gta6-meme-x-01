#!/usr/bin/env python3
"""Build the GTA 6 meme for the make.fun bounty gta6-meme-x-01.

Classic Drake format, captioned the way a human would caption it:
white Anton caps with a black outline, no AI-generated imagery.
The joke is in Indonesian, the way bosku talks:

  top panel (Drake waving it away):  NUNGGU GTA VI / 13 TAHUN
  bottom panel (Drake pointing, approving): DIBAYAR BUAT / NGE-MEME GTA VI / DI MAKE.FUN

make.fun's ghost is worked into the bottom panel scene itself: it
stands right beside Drake, where Drake is pointing, big enough to
recognise when the picture is shrunk to 480x480.

Inputs live in assets/ next to this script. Run it from the repo root:
    python3 gen_meme.py
It writes meme.png (1200x1200) in the repo root.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

DRAKE = ASSETS / "drake.jpg"
GHOST = ASSETS / "ghost.png"
FONT = ASSETS / "Anton-Regular.ttf"

OUT = HERE / "meme.png"

# The Drake template is 1200x1200: Drake on the left half, blank white
# on the right half. Top panel 0..600 (rejecting), bottom 600..1200
# (approving, pointing right).
TOP_LINES = ["NUNGGU GTA VI", "13 TAHUN"]
BOTTOM_LINES = ["DIBAYAR BUAT", "NGE-MEME GTA VI", "DI MAKE.FUN"]

TOP_BOX = (620, 1180)      # x range for the top caption
BOTTOM_BOX = (860, 1185)   # x range for the bottom caption
GHOST_BOX = (615, 790, 220)  # x, y, size of the ghost in the bottom panel


def fit_font(draw, lines, box_width, max_size):
    """Biggest Anton size whose longest line still fits the box."""
    size = max_size
    while size > 10:
        font = ImageFont.truetype(str(FONT), size)
        stroke = max(3, size // 12)
        widths = [draw.textlength(line, font=font) + 2 * stroke for line in lines]
        if max(widths) <= box_width:
            return font, stroke
        size -= 2
    font = ImageFont.truetype(str(FONT), 10)
    return font, 3


def draw_caption(draw, lines, box, centre_y, max_size):
    """Draw centred white-on-black-outline caption lines in the box."""
    x0, x1 = box
    box_width = x1 - x0
    centre_x = (x0 + x1) // 2
    font, stroke = fit_font(draw, lines, box_width, max_size)
    line_height = int(font.size * 1.15)
    total = line_height * len(lines)
    y = centre_y - total // 2
    for line in lines:
        draw.text(
            (centre_x, y + line_height // 2),
            line,
            font=font,
            fill="white",
            stroke_width=stroke,
            stroke_fill="black",
            anchor="mm",
        )
        y += line_height
    return font.size


def main():
    base = Image.open(DRAKE).convert("RGB")
    draw = ImageDraw.Draw(base)

    top_size = draw_caption(draw, TOP_LINES, TOP_BOX, 300, 84)
    bottom_size = draw_caption(draw, BOTTOM_LINES, BOTTOM_BOX, 900, 56)

    ghost = Image.open(GHOST).convert("RGBA")
    gx, gy, gsize = GHOST_BOX
    ghost = ghost.resize((gsize, gsize), Image.LANCZOS)
    base.paste(ghost, (gx, gy), ghost)

    base.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({base.size[0]}x{base.size[1]})")
    print(f"top font {top_size}px, bottom font {bottom_size}px, ghost {gsize}px")


if __name__ == "__main__":
    main()
