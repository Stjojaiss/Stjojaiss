"""Render data/contributions.json as an animated heatmap (contrib-heatmap.svg)."""
import json
import os
from datetime import date
from pathlib import Path

from theme import ACCENT, MUTED, PROMPT, TEXT, window

ROOT = Path(__file__).resolve().parent.parent
STATIC = os.environ.get("STATIC") == "1"
LEVELS = ["#161b22", "#3d2e0a", "#6b4f10", "#a87a16", "#e0a21f", "#ffd166"]

data = json.loads((ROOT / "data/contributions.json").read_text())
days, stats = data["days"], data["stats"]

CELL, GAP = 12, 3
STEP = CELL + GAP
LEFT, TOP = 46, 86
W = LEFT + 53 * STEP + 24

first = date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday

cells, months, seen = [], [], set()
for i, d in enumerate(days):
    pos = i + offset
    col, row = divmod(pos, 7)
    x, y = LEFT + col * STEP, TOP + row * STEP
    count = d["count"]
    level = d["level"]
    if count and level == 0:
        level = 1
    if count >= 15:
        level = 5
    fill = LEVELS[min(level, 5)]
    delay = f' style="animation-delay:{(col + row) * 0.012:.3f}s"' if not STATIC else ""
    cells.append(f'<rect class="c"{delay} x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{fill}">'
                 f'<title>{d["date"]}: {count}</title></rect>')
    dt = date.fromisoformat(d["date"])
    key = (dt.year, dt.month)
    if dt.day <= 7 and key not in seen and col < 52:
        seen.add(key)
        months.append(f'<text x="{x}" y="{TOP - 8}" fill="{MUTED}" font-size="10.5">{dt.strftime("%b")}</text>')

wd = "".join(f'<text x="{LEFT - 8}" y="{TOP + r * STEP + 10}" fill="{MUTED}" font-size="10" text-anchor="end">{n}</text>'
             for r, n in [(1, "Mon"), (3, "Wed"), (5, "Fri")])

grid_bottom = TOP + 7 * STEP
s = stats
stat_items = [
    (f'{s["total"]:,}', "contributions"),
    (str(s["active_days"]), "active days"),
    (f'{s["current_streak"]}d', "current streak"),
    (f'{s["longest_streak"]}d', "longest streak"),
    (str(s["best_day"]["count"]), f'best day ({date.fromisoformat(s["best_day"]["date"]).strftime("%d %b")})'),
]
col_w = (W - 2 * 22) / len(stat_items)
stats_svg = "".join(
    f'<text class="s" x="{22 + i * col_w + col_w / 2:.0f}" y="{grid_bottom + 34}" text-anchor="middle">'
    f'<tspan fill="{ACCENT}" font-size="17" font-weight="700">{v}</tspan>'
    f'<tspan x="{22 + i * col_w + col_w / 2:.0f}" dy="17" fill="{MUTED}" font-size="11">{label}</tspan></text>'
    for i, (v, label) in enumerate(stat_items))

legend_x = W - 22 - 6 * STEP - 70
legend = (f'<text x="{legend_x}" y="{TOP - 30}" fill="{MUTED}" font-size="10.5">less</text>'
          + "".join(f'<rect x="{legend_x + 28 + i * STEP}" y="{TOP - 40}" width="{CELL}" height="{CELL}" rx="2.5" fill="{c}"/>'
                    for i, c in enumerate(LEVELS))
          + f'<text x="{legend_x + 32 + 6 * STEP}" y="{TOP - 30}" fill="{MUTED}" font-size="10.5">more</text>')
title = (f'<text x="22" y="{TOP - 30}" font-size="13.5"><tspan fill="{PROMPT}">❯</tspan>'
         f'<tspan fill="{TEXT}"> ./contributions.sh</tspan>'
         f'<tspan fill="{MUTED}" font-size="12">  # last 12 months, updated {date.today().isoformat()}</tspan></text>')

style = "" if STATIC else """
.c { opacity: 0; animation: drop .5s cubic-bezier(.2,.8,.3,1) forwards; }
@keyframes drop { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: none; } }
.s { opacity: 0; animation: fade .6s ease-out 1.1s forwards; }
@keyframes fade { to { opacity: 1; } }
"""
H = grid_bottom + 66
body = title + legend + "".join(months) + wd + "".join(cells) + stats_svg
(ROOT / "contrib-heatmap.svg").write_text(window(W, H, "johannes@github: ~", body, style=style))
print(f"wrote contrib-heatmap.svg ({W}x{H}px, {len(cells)} cells)")
