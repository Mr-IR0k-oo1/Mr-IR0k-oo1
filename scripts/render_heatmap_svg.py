#!/usr/bin/env python3
"""Render contributions.json into an animated heatmap SVG wrapped in a terminal window."""

import json
import os
from datetime import date, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# --- Catppuccin Mocha palette ---
BG      = "#1e1e2e"
SURFACE = "#313244"
DIM     = "#6c7086"
TEXT    = "#cdd6f4"
RED     = "#f38ba8"
YELLOW  = "#f9e2af"
GREEN   = "#a6e3a1"
BLUE    = "#89b4fa"
TEAL    = "#94e2d5"

# GitHub-ish green ramp: level 0-5
HEAT_PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0ae"]

CELL   = 13
GAP    = 3
RADIUS = 2.5
PAD_L  = 36
PAD_T  = 30
MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS_LABELS = ["", "Mon", "", "Wed", "", "Fri", ""]

# Terminal chrome
BAR_H  = 34
WIN_PAD = 16  # padding inside the terminal window


def load_data() -> dict:
    path = os.path.join(DATA_DIR, "contributions.json")
    with open(path) as f:
        return json.load(f)


def build_grid(days: list[dict]) -> list[list[dict | None]]:
    if not days:
        return []

    by_date = {d["date"]: d for d in days}
    start = date.fromisoformat(days[0]["date"])
    end = date.fromisoformat(days[-1]["date"])
    start -= timedelta(days=start.weekday())

    grid: list[list[dict | None]] = [[] for _ in range(7)]
    d = start
    while d <= end:
        row = d.weekday()
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

    # Inner heatmap dimensions
    heat_w = PAD_L + num_cols * (CELL + GAP) + 10
    heat_h = PAD_T + 7 * (CELL + GAP) + 50

    # Total SVG dimensions (terminal window)
    inner_w = heat_w + WIN_PAD * 2
    inner_h = BAR_H + heat_h + WIN_PAD * 2
    W = inner_w + 4  # outer stroke
    H = inner_h + 4

    # Offsets for content inside the terminal
    ox = 2 + WIN_PAD
    oy = 2 + BAR_H + WIN_PAD

    parts = []

    # --- Terminal window ---
    parts.append(f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{SURFACE}" stroke-width="1"/>')
    parts.append(f'<rect width="{W}" height="{BAR_H}" rx="10" fill="{SURFACE}"/>')
    parts.append(f'<rect y="24" width="{W}" height="10" fill="{SURFACE}"/>')
    parts.append(f'<circle cx="18" cy="{BAR_H//2}" r="5" fill="{RED}"/>')
    parts.append(f'<circle cx="36" cy="{BAR_H//2}" r="5" fill="{YELLOW}"/>')
    parts.append(f'<circle cx="54" cy="{BAR_H//2}" r="5" fill="{GREEN}"/>')
    parts.append(
        f'<text x="{W//2}" y="{BAR_H//2 + 5}" text-anchor="middle" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="12" fill="{DIM}">contributions — 52 weeks</text>'
    )

    # --- Shell prompt ---
    prompt_y = oy + 12
    parts.append(
        f'<text x="{ox}" y="{prompt_y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="11" fill="{GREEN}">'
        f'$ git log --oneline --since="52 weeks ago" | wc -l</text>'
    )
    prompt_y += 18
    total = stats.get("total", 0)
    parts.append(
        f'<text x="{ox}" y="{prompt_y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="12" fill="{TEXT}" opacity="0">'
        f'{total:,}'
        f'<animate attributeName="opacity" from="0" to="1" begin="0.3s" dur="0.3s" fill="freeze"/>'
        f'</text>'
    )

    # Offset heatmap below the prompt
    grid_oy = oy + 44

    # --- Day labels ---
    for i, label in enumerate(DAYS_LABELS):
        if label:
            y = grid_oy + PAD_T + i * (CELL + GAP) + CELL - 2
            parts.append(
                f'<text x="{ox}" y="{y}" '
                f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="10" fill="{DIM}" text-anchor="start">{label}</text>'
            )

    # --- Month labels ---
    if grid and grid[0]:
        seen_months = {}
        for col in range(num_cols):
            cell = grid[0][col] if col < len(grid[0]) else None
            if cell and cell["date"]:
                m = int(cell["date"][5:7])
                if m not in seen_months:
                    seen_months[m] = col
        for m, col in seen_months.items():
            x = ox + PAD_L + col * (CELL + GAP)
            y = grid_oy + PAD_T - 8
            parts.append(
                f'<text x="{x}" y="{y}" '
                f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="10" fill="{DIM}">{MONTHS[m]}</text>'
            )

    # --- Cells ---
    cell_idx = 0
    for col in range(num_cols):
        for row in range(7):
            cell = grid[row][col] if col < len(grid[row]) else None
            level = cell["level"] if cell else 0
            fill = HEAT_PALETTE[min(level, 5)]

            x = ox + PAD_L + col * (CELL + GAP)
            y = grid_oy + PAD_T + row * (CELL + GAP)
            delay = 0.1 + cell_idx * 0.003

            parts.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                f'rx="{RADIUS}" fill="{fill}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{delay:.3f}s" dur="0.3s" fill="freeze"/>'
                f'</rect>'
            )
            cell_idx += 1

    # --- Legend ---
    legend_y = grid_oy + PAD_T + 7 * (CELL + GAP) + 18
    legend_x = ox + PAD_L
    parts.append(
        f'<text x="{legend_x}" y="{legend_y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="10" fill="{DIM}">Less</text>'
    )
    for i, color in enumerate(HEAT_PALETTE):
        lx = legend_x + 38 + i * (CELL + GAP)
        parts.append(
            f'<rect x="{lx}" y="{legend_y - 10}" width="{CELL}" height="{CELL}" '
            f'rx="{RADIUS}" fill="{color}"/>'
        )
    parts.append(
        f'<text x="{legend_x + 38 + len(HEAT_PALETTE) * (CELL + GAP) + 6}" y="{legend_y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="10" fill="{DIM}">More</text>'
    )

    # --- Streak stats ---
    streak_y = legend_y + 20
    streak = stats.get("current_streak", 0)
    longest = stats.get("longest_streak", 0)
    parts.append(
        f'<text x="{ox + PAD_L}" y="{streak_y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="10" fill="{DIM}" opacity="0">'
        f'current streak: {streak}d  ·  longest: {longest}d'
        f'<animate attributeName="opacity" from="0" to="1" begin="2.5s" dur="0.4s" fill="freeze"/>'
        f'</text>'
    )

    svg_body = "\n  ".join(parts)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  </style>
  {svg_body}
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
