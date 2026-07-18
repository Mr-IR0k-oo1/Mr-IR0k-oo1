#!/usr/bin/env python3
"""Render contributions.json into an animated heatmap SVG."""

import json
import os
from datetime import date, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# GitHub-ish green ramp: level 0-5
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0ae"]

CELL   = 13       # cell size
GAP    = 3        # gap between cells
RADIUS = 2.5      # rounded corners
PAD_L  = 36       # left padding (day labels)
PAD_T  = 30       # top padding (month labels)
MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS_LABELS = ["", "Mon", "", "Wed", "", "Fri", ""]


def load_data() -> dict:
    path = os.path.join(DATA_DIR, "contributions.json")
    with open(path) as f:
        return json.load(f)


def build_grid(days: list[dict]) -> list[list[dict | None]]:
    """Organise days into a 7-row × N-column grid (Mon=0 … Sun=6)."""
    if not days:
        return []

    by_date = {d["date"]: d for d in days}
    start = date.fromisoformat(days[0]["date"])
    end = date.fromisoformat(days[-1]["date"])

    # Align start to Monday
    start -= timedelta(days=start.weekday())

    grid: list[list[dict | None]] = [[] for _ in range(7)]
    d = start
    while d <= end:
        col_idx = (d - start).days // 7
        row = d.weekday()  # Mon=0 … Sun=6
        iso = d.isoformat()
        cell = by_date.get(iso)
        grid[row].append(cell)
        d += timedelta(days=1)

    return grid


def render_svg(data: dict) -> str:
    days = data.get("days", [])
    stats = data.get("stats", {})
    grid = build_grid(days)
    if not grid:
        return "<svg></svg>"

    num_cols = max(len(row) for row in grid)
    W = PAD_L + num_cols * (CELL + GAP) + 10
    H = PAD_T + 7 * (CELL + GAP) + 50  # extra for legend + footer

    # --- Day labels ---
    day_labels = ""
    for i, label in enumerate(DAYS_LABELS):
        if label:
            y = PAD_T + i * (CELL + GAP) + CELL - 2
            day_labels += (
                f'<text x="0" y="{y}" '
                f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="10" fill="#8b949e" text-anchor="start">{label}</text>\n'
            )

    # --- Cells ---
    cells_svg = ""
    cell_idx = 0
    for col in range(num_cols):
        for row in range(7):
            cell = grid[row][col] if col < len(grid[row]) else None
            level = cell["level"] if cell else 0
            fill = PALETTE[min(level, 5)]

            x = PAD_L + col * (CELL + GAP)
            y = PAD_T + row * (CELL + GAP)
            delay = 0.05 + cell_idx * 0.003  # diagonal stagger

            cells_svg += (
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                f'rx="{RADIUS}" fill="{fill}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{delay:.3f}s" dur="0.3s" fill="freeze"/>'
                f'</rect>\n'
            )
            cell_idx += 1

    # --- Month labels ---
    month_labels = ""
    if grid and grid[0]:
        seen_months = {}
        for col in range(num_cols):
            # find the date for the first row of this column
            cell = grid[0][col] if col < len(grid[0]) else None
            if cell and cell["date"]:
                m = int(cell["date"][5:7])
                if m not in seen_months:
                    seen_months[m] = col
        for m, col in seen_months.items():
            x = PAD_L + col * (CELL + GAP)
            month_labels += (
                f'<text x="{x}" y="{PAD_T - 8}" '
                f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="10" fill="#8b949e">{MONTHS[m]}</text>\n'
            )

    # --- Legend ---
    legend_y = PAD_T + 7 * (CELL + GAP) + 18
    legend_x = PAD_L
    legend = (
        f'<text x="{legend_x}" y="{legend_y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="10" fill="#8b949e">Less</text>\n'
    )
    for i, color in enumerate(PALETTE):
        lx = legend_x + 38 + i * (CELL + GAP)
        legend += (
            f'<rect x="{lx}" y="{legend_y - 10}" width="{CELL}" height="{CELL}" '
            f'rx="{RADIUS}" fill="{color}"/>\n'
        )
    legend += (
        f'<text x="{legend_x + 38 + len(PALETTE) * (CELL + GAP) + 6}" y="{legend_y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="10" fill="#8b949e">More</text>\n'
    )

    # --- Footer ---
    total = stats.get("total", 0)
    footer_y = legend_y + 24
    footer = (
        f'<text x="{PAD_L}" y="{footer_y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="12" fill="#8b949e">'
        f'{total:,} contributions in the last year</text>\n'
    )

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  </style>
  <rect width="{W}" height="{H}" fill="transparent"/>
  {day_labels}
  {month_labels}
  {cells_svg}
  {legend}
  {footer}
</svg>'''


def main():
    data = load_data()
    svg = render_svg(data)
    out = os.path.join(DATA_DIR, "..", "contrib-heatmap.svg")
    with open(out, "w") as f:
        f.write(svg)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
