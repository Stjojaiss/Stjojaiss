"""Render assets/source.png as a self-typing ASCII-art SVG (ascii-art.svg)."""
import os
from pathlib import Path

import numpy as np
from PIL import Image

from theme import ACCENT, esc, window

BODY = "#6e7681"  # dim grey body so the yellow spots carry the image
EDGE = "#484f58"

ROOT = Path(__file__).resolve().parent.parent
COLS = 58
RAMP = " .`:-=+*cs#%@"
FONT_SIZE = 10
CHAR_W = 6.02  # monospace advance at 10px
LINE_H = 10.6
PAD = 0
TOP = 0
ROW_DELAY = 0.045  # seconds between rows
ROW_DUR = 0.35

STATIC = os.environ.get("STATIC") == "1"
BEGIN = 0.6

img = Image.open(ROOT / "assets/source.png").convert("RGB")
arr = np.asarray(img).astype(int)
ink = (arr.min(axis=2) < 235)
ys, xs = np.where(ink)
img = img.crop((xs.min() - 4, ys.min() - 4, xs.max() + 5, ys.max() + 5))

# Monospace cells are ~twice as tall as wide.
rows = round(COLS * img.height / img.width * CHAR_W / LINE_H)
small = np.asarray(img.resize((COLS, rows), Image.LANCZOS)).astype(int)

lines = []  # list of rows, each a list of (char, colour)
for y in range(rows):
    row = []
    for x in range(COLS):
        r, g, b = small[y, x]
        lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
        is_yellow = r > 150 and g > 100 and b < 120 and r - b > 80
        if is_yellow:
            row.append(("#" if lum < 170 else "@", ACCENT))
        else:
            dark = 1 - lum / 255
            idx = min(len(RAMP) - 1, int(dark * len(RAMP)))
            row.append((RAMP[idx], BODY if idx > 7 else EDGE))
    lines.append(row)

width = round(COLS * CHAR_W)
height = round(rows * LINE_H)

defs, body = [], []
for y, row in enumerate(lines):
    ty = TOP + (y + 1) * LINE_H - 2
    spans, run_c, run_s = [], None, ""
    for ch, c in row + [(None, None)]:
        if c != run_c and run_s:
            spans.append(f'<tspan fill="{run_c}">{esc(run_s)}</tspan>')
            run_s = ""
        if ch is not None:
            run_c, run_s = c, run_s + ch
    text = (f'<text x="{PAD}" y="{ty:.1f}" font-size="{FONT_SIZE}" xml:space="preserve" '
            f'textLength="{COLS * CHAR_W:.1f}" lengthAdjust="spacing">{"".join(spans)}</text>')
    if STATIC:
        body.append(text)
        continue
    begin = BEGIN + y * ROW_DELAY
    defs.append(
        f'<clipPath id="r{y}"><rect x="{PAD}" y="{ty - LINE_H + 2:.1f}" height="{LINE_H + 1:.1f}" width="0">'
        f'<animate attributeName="width" from="0" to="{COLS * CHAR_W + 2:.1f}" begin="{begin:.2f}s" '
        f'dur="{ROW_DUR}s" fill="freeze"/></rect></clipPath>')
    body.append(f'<g clip-path="url(#r{y})">{text}</g>')

DEFS, BODY, WIDTH, HEIGHT = "".join(defs), "\n".join(body), width, height

if __name__ == "__main__":
    svg = window(width + 32, height + 60, "~/salamander.txt",
                 f'<g transform="translate(16 44)">{BODY}</g>', DEFS)
    (ROOT / "ascii-art.svg").write_text(svg)
    print(f"wrote ascii-art.svg ({COLS}x{rows}, {len(svg) // 1024} KB)")
