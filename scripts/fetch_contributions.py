"""Scrape the public contribution calendar (no token) into data/contributions.json."""
import json
import re
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
USER = "Stjojaiss"

html = requests.get(f"https://github.com/users/{USER}/contributions",
                    headers={"User-Agent": "profile-readme-bot"}, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

counts = {}
for tip in soup.find_all("tool-tip"):
    m = re.match(r"(\d+|No) contributions?", tip.get_text(strip=True))
    if m:
        counts[tip.get("for")] = 0 if m.group(1) == "No" else int(m.group(1))

days = []
for td in soup.select("td.ContributionCalendar-day[data-date]"):
    days.append({"date": td["data-date"], "level": int(td.get("data-level", 0)),
                 "count": counts.get(td.get("id"), 0)})
days.sort(key=lambda d: d["date"])
if len(days) < 300:
    raise SystemExit(f"only {len(days)} days parsed, GitHub markup changed?")

today = date.today().isoformat()
past = [d for d in days if d["date"] <= today]

longest = run = 0
for d in past:
    run = run + 1 if d["count"] else 0
    longest = max(longest, run)
current = 0
for i, d in enumerate(reversed(past)):
    if d["count"]:
        current += 1
    elif i > 0:  # an empty today doesn't break the streak yet
        break
best = max(past, key=lambda d: d["count"])

data = {
    "user": USER,
    "days": days,
    "stats": {
        "total": sum(d["count"] for d in past),
        "active_days": sum(1 for d in past if d["count"]),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
    },
}
(ROOT / "data/contributions.json").write_text(json.dumps(data, indent=1))
print(f"{len(days)} days, stats: {data['stats']}")
