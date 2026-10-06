"""Neofetch-style info card (info-card.svg). Edit INFO to change the content."""
import os
from pathlib import Path

from theme import ACCENT, MUTED, PROMPT, TEXT, esc, window

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

W = 470
PAD = 22
LINE_H = 21
TOP = 62
KEY_W = 74

rows = []
y = TOP
rows.append((y, f'<tspan fill="{ACCENT}" font-weight="700">{USER}</tspan>'))
y += LINE_H
rows.append((y, f'<tspan fill="{MUTED}">{"─" * len(USER)}</tspan>'))
for key, val in INFO:
    y += LINE_H if key is not None else LINE_H * 0.6
    if key is None:
        continue
    k = f'<tspan fill="{ACCENT}" font-weight="700">{esc(key)}</tspan>' if key else ""
    rows.append((y, f'{k}<tspan x="{PAD + KEY_W}" fill="{TEXT}">{esc(val)}</tspan>'))
y += LINE_H * 1.1
palette = "".join(
    f'<rect x="{PAD + i * 26}" y="{y - 12}" width="22" height="12" rx="2" fill="{c}"/>'
    for i, c in enumerate(["#3d2e0a", "#6b4f10", "#a87a16", "#e0a21f", "#f2b632", "#ffd166", "#c9d1d9"]))
y += LINE_H
cursor_y = y

style = "" if STATIC else """
.l { opacity: 0; animation: in .45s ease-out forwards; }
@keyframes in { from { opacity: 0; transform: translateX(-8px); } to { opacity: 1; transform: none; } }
.cur { animation: blink 1s steps(1) infinite; }
@keyframes blink { 50% { opacity: 0; } }
"""

body = []
for i, (ry, content) in enumerate(rows):
    delay = f' style="animation-delay:{0.25 + i * 0.12:.2f}s"' if not STATIC else ""
    body.append(f'<text class="l"{delay} x="{PAD}" y="{ry:.1f}" font-size="13.5">{content}</text>')
pal_delay = f' style="animation-delay:{0.25 + len(rows) * 0.12:.2f}s"' if not STATIC else ""
body.append(f'<g class="l"{pal_delay}>{palette}</g>')
body.append(f'<text x="{PAD}" y="{cursor_y:.1f}" font-size="13.5"><tspan fill="{PROMPT}">❯</tspan>'
            f'<tspan class="cur" fill="{TEXT}"> █</tspan></text>')

H = round(cursor_y + PAD)
(ROOT / "info-card.svg").write_text(window(W, H, "~ neofetch", "\n".join(body), style=style))
print(f"wrote info-card.svg ({W}x{H}px)")
