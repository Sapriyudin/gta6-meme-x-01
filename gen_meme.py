#!/usr/bin/env python3
"""Regenerate meme.png (v2) for the make.fun bounty gta6-meme-x-01.

"PAID" — a parody of GTA's iconic WASTED death screen, drawn from
scratch. No recycled template, no AI imagery. Black and moody: the
make.fun ghost stands large above the word PAID, holding its magenta
star coin — it is the one paying. First person, professional voice:

    My AI agent memed GTA VI. make.fun paid for it.

Run:  python3 gen_meme.py   ->  writes meme.png (1200x1200) here.
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = 1200
ANTON = "assets/Anton-Regular.ttf"
GHOST = "assets/ghost.png"
DEJAVU_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
LIBERATION_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

MAGENTA = (233, 30, 99)          # make.fun magenta, for the rule + dot
PAID_FILL = (217, 217, 217)      # WASTED-style light grey
WHITE = (242, 242, 242)


def load_bold(size):
    """A clean sans bold for the sub-line and the wordmark."""
    for path in (DEJAVU_BOLD, LIBERATION_BOLD):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def fit_anton(draw, text, target_width, start=200, ceiling=420):
    """Grow Anton until the text spans about target_width pixels."""
    size = start
    while size < ceiling:
        font = ImageFont.truetype(ANTON, size)
        if draw.textlength(text, font=font) >= target_width:
            return font
        size += 5
    return ImageFont.truetype(ANTON, ceiling)


def vertical_gradient(size, top, bottom):
    """A top-to-bottom gradient image, built one row at a time."""
    base = Image.new("RGB", (1, size))
    px = base.load()
    for y in range(size):
        t = y / max(size - 1, 1)
        px[0, y] = tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return base.resize((size, size))


def soft_glow(size, centre, radius, colour, blur):
    """A blurred disc of light on black, returned as an RGB image."""
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    cx, cy = centre
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=70)
    mask = mask.filter(ImageFilter.GaussianBlur(blur))
    solid = Image.new("RGB", (size, size), colour)
    out = Image.new("RGB", (size, size), (0, 0, 0))
    out.paste(solid, (0, 0), mask)
    return out


def main():
    # 1. Moody black background: near-black gradient + a soft glow
    #    behind the ghost and the headline, WASTED-screen style.
    img = vertical_gradient(SIZE, (14, 14, 14), (0, 0, 0))
    glow = soft_glow(SIZE, (SIZE // 2, 480), 520, (38, 38, 38), 180)
    img = Image.blend(img, glow, 0.85)
    draw = ImageDraw.Draw(img)

    # 2. The ghost, large and central: it is the one paying.
    ghost = Image.open(GHOST).convert("RGBA")
    ghost = ghost.resize((380, 380), Image.LANCZOS)
    img.paste(ghost, (SIZE // 2 - 190, 85), ghost)
    draw = ImageDraw.Draw(img)

    # 3. PAID, huge, WASTED style: light grey Anton, dark outline.
    #    Anton at this size is ~355px tall, so it must start high
    #    enough to clear the sub-line below it.
    paid_font = fit_anton(draw, "PAID", 1020)
    # A faint dark-grey offset copy first, so the letters lift off black.
    draw.text((SIZE // 2 + 5, 500), "PAID", font=paid_font,
              fill=(48, 48, 48), anchor="mt")
    draw.text((SIZE // 2, 495), "PAID", font=paid_font, fill=PAID_FILL,
              stroke_width=9, stroke_fill=(0, 0, 0), anchor="mt")

    # 4. A short magenta rule under the headline.
    draw.rectangle([SIZE // 2 - 65, 890, SIZE // 2 + 65, 895], fill=MAGENTA)

    # 5. The sub-line, clean type, two lines, centred.
    sub_font = load_bold(54)
    for i, line in enumerate(("My AI agent memed GTA VI.",
                             "make.fun paid for it.")):
        while draw.textlength(line, font=sub_font) > 1060 and sub_font.size > 30:
            sub_font = load_bold(sub_font.size - 2)
        draw.text((SIZE // 2, 920 + i * 68), line, font=sub_font,
                  fill=WHITE, anchor="mt")

    # 6. The wordmark at the bottom: make.fun, dot in magenta.
    mark_font = load_bold(46)
    w_make = draw.textlength("make", font=mark_font)
    w_dot = draw.textlength(".", font=mark_font)
    w_fun = draw.textlength("fun", font=mark_font)
    x = SIZE // 2 - (w_make + w_dot + w_fun) / 2
    y = 1115
    draw.text((x, y), "make", font=mark_font, fill=WHITE)
    draw.text((x + w_make, y), ".", font=mark_font, fill=MAGENTA)
    draw.text((x + w_make + w_dot, y), "fun", font=mark_font, fill=WHITE)

    img.save("meme.png")
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()
