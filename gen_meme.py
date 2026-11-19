"""gta6-meme-x-01 — meme v3.

Base: GTA VI key art (keyart.jpg, provided by bosku), 650x366.
v3 edits, all by this script (Python + PIL):
  1. Rockstar logo (yellow R* box, bottom-right) removed by diffusion
     inpainting from the surrounding building facade — no trace left.
  2. make.fun ghost pasted onto the car hood, in the scene, near the
     characters. Faces, title and the VI logo are untouched.
  3. Two-line English caption, bottom-left, white DejaVuSans-Bold
     with a black outline: "My AI agent got paid / to meme this."
Deterministic: same input files -> same output bytes (fixed RNG seed).
Run: python3 gen_meme.py   (writes meme.png in the repo root)
"""
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "keyart.jpg"
GHOST = ROOT / "assets" / "ghost.png"
OUT = ROOT / "meme.png"
INTERMEDIATE = Path("/tmp/v3-inpaint-only.png")
DEJAVU_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Rockstar logo: tight yellow bbox x608-641 y327-357, black border around
# it. Mask generously (a few px margin) so no border or yellow survives.
MASK = (602, 321, 647, 363)  # x0, y0, x1, y1 (exclusive)

GHOST_POS = (64, 232)  # top-left; sits on the car hood, near the characters
GHOST_SIZE = 88

CAPTION_LINES = ["My AI agent got paid", "to meme this."]
CAPTION_X = 16
CAPTION_MAX_RIGHT = 226  # keep clear of the VI logo (starts ~x230)
CAPTION_BOTTOM = 364     # bottom edge of the last line
CAPTION_GAP = 3


def inpaint_logo(img):
    """Fill the logo box by diffusion from the surrounding facade."""
    a = np.array(img).astype(np.float64)
    h, w, _ = a.shape
    x0, y0, x1, y1 = MASK
    mask = np.zeros((h, w), dtype=bool)
    mask[y0:y1, x0:x1] = True
    # Seed masked pixels with the mean colour of the fixed border ring
    # (top row + left column; the box touches the right/bottom edges).
    ring = [a[y0 - 1, x] for x in range(x0, x1)]
    ring += [a[y, x0 - 1] for y in range(y0, y1)]
    filled = a.copy()
    filled[mask] = np.mean(ring, axis=0)
    # Diffusion: each masked pixel becomes the mean of its 4 neighbours.
    # Edge-padded so the image border never wraps around.
    for _ in range(800):
        p = np.pad(filled, ((1, 1), (1, 1), (0, 0)), mode="edge")
        avg = (p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]) / 4.0
        filled[mask] = avg[mask]
    # Match the JPEG grain so the patch is not suspiciously smooth.
    rng = np.random.default_rng(7)
    filled[mask] = np.clip(
        filled[mask] + rng.normal(0, 2.0, size=filled[mask].shape), 0, 255
    )
    # Feather the mask edge so no hard seam shows.
    m = Image.fromarray((mask * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(1.2)
    )
    mf = np.array(m).astype(np.float64)[..., None] / 255.0
    out = a * (1.0 - mf) + filled * mf
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def add_ghost(img):
    ghost = Image.open(GHOST).convert("RGBA")
    ghost = ghost.resize((GHOST_SIZE, GHOST_SIZE), Image.LANCZOS)
    img.paste(ghost, GHOST_POS, ghost)
    return img


def add_caption(img):
    draw = ImageDraw.Draw(img)
    # Largest size whose longest line still clears the VI logo.
    size = 20
    while size > 15:
        font = ImageFont.truetype(DEJAVU_BOLD, size)
        widths = []
        for t in CAPTION_LINES:
            box = draw.textbbox((0, 0), t, font=font, stroke_width=2)
            widths.append(box[2] - box[0])
        if max(widths) <= CAPTION_MAX_RIGHT - CAPTION_X:
            break
        size -= 1
    font = ImageFont.truetype(DEJAVU_BOLD, size)
    heights = []
    for line in CAPTION_LINES:
        box = draw.textbbox((0, 0), line, font=font, stroke_width=2)
        heights.append(box[3] - box[1])
    # Anchor the block to the bottom edge, lines stacked upward.
    y = CAPTION_BOTTOM
    for line, hgt in reversed(list(zip(CAPTION_LINES, heights))):
        y -= hgt
        draw.text(
            (CAPTION_X, y), line, font=font,
            fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0),
        )
        y -= CAPTION_GAP
    print(f"caption font size: {size}")
    return img


def main():
    img = Image.open(BASE).convert("RGB")
    print(f"base: {img.size} {img.mode}")
    img = inpaint_logo(img)
    img.save(INTERMEDIATE)
    print(f"saved intermediate (logo removed only): {INTERMEDIATE}")
    img = add_ghost(img)
    img = add_caption(img)
    img.save(OUT)
    print(f"saved {OUT} {img.size}")


if __name__ == "__main__":
    main()
