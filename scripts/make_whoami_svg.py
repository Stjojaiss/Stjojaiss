"""One terminal window: `❯ whoami` prompt, ASCII salamander left, neofetch info right (whoami.svg)."""
import os
from pathlib import Path

import make_ascii_svg as ascii_art
from theme import ACCENT, BORDER, MUTED, PROMPT, TEXT, esc, window

ROOT = Path(__file__).resolve().parent.parent
STATIC = os.environ.get("STATIC") == "1"

USER = "johannes@darmstadt"
INFO = [
    ("Now", "Founder @ Salamandra"),
    ("", "websites + AI tools for small businesses"),
    ("Study", "Hochschule Darmstadt (h_da)"),
    ("Teach", "AI workshops, h_da Trainerpool"),
    ("Build", "CHELIUS: iOS AR app for geology"),
    (None, None),
    ("Stack", "TypeScript, Next.js, Astro"),
    ("3D", "Three.js, R3F, GSAP, Blender"),
    ("Mobile", "Swift, ARKit, RealityKit"),
    ("AI", "Claude Code, MCP, local LLMs"),
    (None, None),
    ("Web", "johannesjaissle.de"),
    ("Langs", "Deutsch, English"),
]

W = 865
PAD = 22
PROMPT_Y = 60
CONTENT_TOP = 84
FS = 13.5
LINE_H = 21
KEY_W = 74

ART_X = PAD
INFO_X = ART_X + ascii_art.WIDTH + 44

# info column, vertically centred against the art
n_lines = 2 + sum(1 for k, _ in INFO if k is not None)
n_gaps = sum(1 for k, _ in INFO if k is None)
info_h = (n_lines - 1) * LINE_H + n_gaps * LINE_H * 0.6 + LINE_H * 1.1 + 12
y = CONTENT_TOP + max(0, (ascii_art.HEIGHT - info_h) / 2) + 12

rows = [(y, f'<tspan fill="{ACCENT}" font-weight="700">{USER}</tspan>')]
y += LINE_H
rows.append((y, f'<tspan fill="{MUTED}">{"─" * len(USER)}</tspan>'))
for key, val in INFO:
    y += LINE_H if key is not None else LINE_H * 0.6
    if key is None:
        continue
    k = f'<tspan fill="{ACCENT}" font-weight="700">{esc(key)}</tspan>' if key else ""
    rows.append((y, f'{k}<tspan x="{INFO_X + KEY_W}" fill="{TEXT}">{esc(val)}</tspan>'))
y += LINE_H * 1.1
palette = "".join(
    f'<rect x="{INFO_X + i * 26}" y="{y - 12:.1f}" width="22" height="12" rx="2" fill="{c}"/>'
    for i, c in enumerate(["#3d2e0a", "#6b4f10", "#a87a16", "#e0a21f", "#f2b632", "#ffd166", "#c9d1d9"]))

H = round(max(CONTENT_TOP + ascii_art.HEIGHT, y) + 26 + 30)
cursor_y = H - 22

style = "" if STATIC else """
.l { opacity: 0; animation: in .45s ease-out forwards; }
@keyframes in { from { opacity: 0; transform: translateX(-8px); } to { opacity: 1; transform: none; } }
.t { opacity: 0; animation: show .01s linear .15s forwards; }
@keyframes show { to { opacity: 1; } }
.cur { animation: blink 1s steps(1) infinite; }
@keyframes blink { 50% { opacity: 0; } }
"""

body = [
    f'<text x="{PAD}" y="{PROMPT_Y}" font-size="{FS}"><tspan fill="{PROMPT}">❯</tspan>'
    f'<tspan class="t" fill="{TEXT}"> whoami</tspan></text>',
    f'<line x1="{INFO_X - 22}" y1="{CONTENT_TOP}" x2="{INFO_X - 22}" y2="{CONTENT_TOP + ascii_art.HEIGHT}" stroke="{BORDER}"/>',
    f'<g transform="translate({ART_X} {CONTENT_TOP})">{ascii_art.BODY}</g>',
]
start = ascii_art.BEGIN + 0.2
for i, (ry, content) in enumerate(rows):
    delay = f' style="animation-delay:{start + i * 0.12:.2f}s"' if not STATIC else ""
    body.append(f'<text class="l"{delay} x="{INFO_X}" y="{ry:.1f}" font-size="{FS}">{content}</text>')
pal_delay = f' style="animation-delay:{start + len(rows) * 0.12:.2f}s"' if not STATIC else ""
body.append(f'<g class="l"{pal_delay}>{palette}</g>')
body.append(f'<text x="{PAD}" y="{cursor_y}" font-size="{FS}"><tspan fill="{PROMPT}">❯</tspan>'
            f'<tspan class="cur" fill="{TEXT}"> █</tspan></text>')

(ROOT / "whoami.svg").write_text(window(W, H, "johannes@github: ~", "\n".join(body), ascii_art.DEFS, style))
print(f"wrote whoami.svg ({W}x{H}px)")
