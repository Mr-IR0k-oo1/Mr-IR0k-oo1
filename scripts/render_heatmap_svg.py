#!/usr/bin/env python3
"""Render data/contributions.json into a clean, theme-aware heatmap SVG."""

import json
import os
from datetime import date, timedelta

import theme

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA_PATH = os.path.join(ROOT, "data", "contributions.json")
OUT_PATH = os.path.join(ROOT, "contrib-heatmap.svg")

W = 880
PAD = 24
CELL = 12
GAP = 3
STEP = CELL + GAP
LABEL_W = 30          # room for weekday labels
MAX_LEVEL = 4
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WEEKDAYS = {0: "Mon", 2: "Wed", 4: "Fri"}


def build_grid(days: list[dict]) -> list[list[dict | None]]:
    """Return columns (weeks) of 7 cells, Monday first."""
    if not days:
        return []
    by_date = {d["date"]: d for d in days}
    start = date.fromisoformat(days[0]["date"])
    end = date.fromisoformat(days[-1]["date"])
    start -= timedelta(days=start.weekday())

    weeks: list[list[dict | None]] = []
    d = start
    while d <= end:
        if d.weekday() == 0:
            weeks.append([None] * 7)
        weeks[-1][d.weekday()] = by_date.get(d.isoformat())
        d += timedelta(days=1)
    return weeks


def busiest_month(monthly: dict[str, int]) -> str | None:
    if not monthly:
        return None
    key, count = max(monthly.items(), key=lambda kv: kv[1])
    year, month = key.split("-")
    return f"{MONTHS[int(month) - 1]} {year} ({count:,})"


def render_svg(data: dict) -> str:
    stats = data.get("stats", {})
    weeks = build_grid(data.get("days", []))
    total = stats.get("total", 0)
    streak = stats.get("current_streak", 0)
    longest = stats.get("longest_streak", 0)

    grid_w = LABEL_W + len(weeks) * STEP - GAP
    gx = (W - grid_w) // 2 + LABEL_W   # center the grid horizontally
    title_y = PAD + 14
    month_y = title_y + 30
    gy = month_y + 8
    grid_bottom = gy + 7 * STEP - GAP
    divider_y = grid_bottom + 20
    footer_y = divider_y + 26
    H = footer_y + PAD - 4

    p: list[str] = []
    p.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6" '
             f'fill="var(--bg)" stroke="var(--border)"/>')

    # Header
    p.append(f'<text x="{PAD}" y="{title_y}" font-size="15" font-weight="600" '
             f'fill="var(--text)">Contribution activity</text>')
    p.append(f'<text x="{W - PAD}" y="{title_y}" font-size="13" fill="var(--muted)" '
             f'text-anchor="end"><tspan font-weight="600" fill="var(--text)">'
             f'{total:,}</tspan> contributions in the last year</text>')

    # Month labels: first week whose Monday-column cell starts a new month
    last_month = None
    last_x = -100
    for i, week in enumerate(weeks):
        first = next((c for c in week if c), None)
        if not first:
            continue
        m = int(first["date"][5:7])
        x = gx + i * STEP
        if m != last_month and x - last_x >= 3 * STEP:
            p.append(f'<text x="{x}" y="{month_y}" font-size="11" '
                     f'fill="var(--muted)">{MONTHS[m - 1]}</text>')
            last_x = x
        last_month = m

    # Weekday labels
    for row, label in WEEKDAYS.items():
        y = gy + row * STEP + CELL - 2
        p.append(f'<text x="{gx - 8}" y="{y}" font-size="10" fill="var(--muted)" '
                 f'text-anchor="end">{label}</text>')

    # Cells
    for i, week in enumerate(weeks):
        for row, cell in enumerate(week):
            if cell is None:
                continue
            level = min(cell.get("level", 0), MAX_LEVEL)
            x = gx + i * STEP
            y = gy + row * STEP
            p.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
                     f'fill="var(--cell-{level})"><title>{cell["date"]}: '
                     f'{cell.get("count", 0)} contributions</title></rect>')

    # Divider + footer
    p.append(f'<line x1="{PAD}" y1="{divider_y}" x2="{W - PAD}" y2="{divider_y}" '
             f'stroke="var(--border)"/>')

    metrics = [("Current streak", f"{streak} days"),
               ("Longest streak", f"{longest} days")]
    best = busiest_month(stats.get("monthly", {}))
    if best:
        metrics.append(("Busiest month", best))
    x = PAD
    for label, value in metrics:
        p.append(f'<text x="{x}" y="{footer_y}" font-size="12" fill="var(--muted)">'
                 f'{label} <tspan font-weight="600" fill="var(--text)">{value}</tspan></text>')
        x += 190

    # Legend (right-aligned)
    lx = W - PAD - 30 - (MAX_LEVEL + 1) * STEP
    p.append(f'<text x="{lx - 8}" y="{footer_y}" font-size="11" fill="var(--muted)" '
             f'text-anchor="end">Less</text>')
    for lvl in range(MAX_LEVEL + 1):
        p.append(f'<rect x="{lx + lvl * STEP}" y="{footer_y - 10}" width="{CELL}" '
                 f'height="{CELL}" rx="2" fill="var(--cell-{lvl})"/>')
    p.append(f'<text x="{lx + (MAX_LEVEL + 1) * STEP + 5}" y="{footer_y}" '
             f'font-size="11" fill="var(--muted)">More</text>')

    body = "\n  ".join(p)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="hm-title hm-desc">
  <title id="hm-title">Contribution activity</title>
  <desc id="hm-desc">{total:,} contributions in the last year; current streak {streak} days, longest streak {longest} days.</desc>
  {theme.css()}
  {body}
</svg>
'''


def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(render_svg(data))
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
