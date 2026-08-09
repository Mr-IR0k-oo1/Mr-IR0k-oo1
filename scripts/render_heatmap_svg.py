#!/usr/bin/env python3
"""Render contributions.json into the industrial-brutalist animated heatmap SVG.

Theme-aware: palette comes from theme.py CSS custom properties so the card
adapts to GitHub's light/dark mode while keeping the tactical telemetry
aesthetic in dark mode. Motion honours REDUCE_MOTION=1 (no SMIL emitted).
"""

import json
import os
from datetime import date, timedelta

import theme

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# --- Geometry ---
CELL   = 13
GAP    = 3
RADIUS = 1.0  # Ultra-sharp modular corners
PAD_L  = 36
PAD_T  = 20
MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS_LABELS = ["", "Mon", "", "Wed", "", "Fri", ""]

# Terminal dimensions & layout
BAR_H   = 26
WIN_PAD = 20


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

    heat_w = PAD_L + num_cols * (CELL + GAP) + 10
    W = heat_w + WIN_PAD * 2
    H = 295  # Standardized stable height for 52-week matrix console

    ox = WIN_PAD
    oy = BAR_H + WIN_PAD

    parts = []

    # --- Container and main grid ---
    parts.append(f'<rect width="{W}" height="{H}" fill="var(--bg)" stroke="var(--border)" stroke-width="1.5"/>')

    # Blueprint Grid Lines
    parts.append(f'<line x1="0" y1="26" x2="{W}" y2="26" stroke="var(--border)" stroke-width="1"/>')
    parts.append(f'<line x1="0" y1="{H - 26}" x2="{W}" y2="{H - 26}" stroke="var(--border)" stroke-width="1"/>')

    # Corner registration crosshairs (+)
    parts.append(f'<text x="6" y="12" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')
    parts.append(f'<text x="{W - 13}" y="12" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')
    parts.append(f'<text x="6" y="{H - 6}" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')
    parts.append(f'<text x="{W - 13}" y="{H - 6}" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')

    # --- Header bar contents ---
    # Flashing system status square
    parts.append(
        f'<rect x="20" y="10" width="6" height="6" fill="var(--green)">'
        f'{theme.smil("opacity", "1;0.3;1", "1.5s", repeat="indefinite")}'
        f'</rect>'
    )
    parts.append(f'<text x="32" y="16" font-size="9" font-weight="bold" fill="var(--green)">[ CONSOLE: BASHLOG ]</text>')

    parts.append(
        f'<text x="{W//2}" y="16" text-anchor="middle" font-size="9" fill="var(--dim)" font-weight="bold">'
        f'STREAM: SYSTEM_ACTIVITY_INDEX // 52_WEEK_MATRIX'
        f'</text>'
    )

    parts.append(f'<text x="{W - 20}" y="16" text-anchor="end" font-size="9" fill="var(--red)" font-weight="bold">INGEST_STATE: ONLINE</text>')

    # --- Shell prompt ---
    prompt_y = oy + 12
    parts.append(
        f'<text x="{ox}" y="{prompt_y}" '
        f'font-size="11" fill="var(--blue)">'
        f'mr-ir0k-oo1@mainframe:~$ git log --since="52 weeks ago" | wc -l</text>'
    )

    prompt_y += 16
    total = stats.get("total", 0)
    op, anim = theme.fade("0.2s", "0.2s")
    parts.append(
        f'<text x="{ox}" y="{prompt_y}" '
        f'font-size="12" fill="var(--green)" font-weight="bold" {op}>'
        f'[+] {total:,} INGESTED LOGS DETECTED'
        f'{anim}'
        f'</text>'
    )

    grid_oy = oy + 36

    # --- Day labels ---
    for i, label in enumerate(DAYS_LABELS):
        if label:
            y = grid_oy + PAD_T + i * (CELL + GAP) + CELL - 2
            parts.append(
                f'<text x="{ox}" y="{y}" '
                f'font-size="9.5" fill="var(--dim)" text-anchor="start" font-weight="bold">{label}</text>'
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
                f'font-size="9.5" fill="var(--dim)" font-weight="bold">{MONTHS[m].upper()}</text>'
            )

    # --- Heatmap Cells ---
    cell_idx = 0
    for col in range(num_cols):
        for row in range(7):
            cell = grid[row][col] if col < len(grid[row]) else None
            level = cell["level"] if cell else 0
            fill = f"var(--cell-{min(level, 5)})"

            x = ox + PAD_L + col * (CELL + GAP)
            y = grid_oy + PAD_T + row * (CELL + GAP)

            delay = 0.05 + cell_idx * 0.002
            op, anim = theme.fade(f"{delay:.3f}s")

            parts.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                f'rx="{RADIUS}" fill="{fill}" {op}>'
                f'{anim}'
                f'</rect>'
            )
            cell_idx += 1

    # --- Legend ---
    legend_y = grid_oy + PAD_T + 7 * (CELL + GAP) + 18
    legend_x = ox + PAD_L
    parts.append(
        f'<text x="{legend_x}" y="{legend_y}" '
        f'font-size="9.5" fill="var(--dim)" font-weight="bold">LESS</text>'
    )
    for i in range(6):
        lx = legend_x + 38 + i * (CELL + GAP)
        parts.append(
            f'<rect x="{lx}" y="{legend_y - 10}" width="{CELL}" height="{CELL}" '
            f'rx="{RADIUS}" fill="var(--cell-{i})"/>'
        )
    parts.append(
        f'<text x="{legend_x + 38 + 6 * (CELL + GAP) + 6}" y="{legend_y}" '
        f'font-size="9.5" fill="var(--dim)" font-weight="bold">MORE</text>'
    )

    # --- Tactical Stats Panel ---
    stats_divider_y = legend_y + 14
    op, anim = theme.fade("1.2s", "0.3s")
    parts.append(
        f'<text x="{ox}" y="{stats_divider_y}" font-size="10" fill="var(--dim)" {op}>'
        f'[ STATS_METRICS ] ───────────────────────────────────────────────────────────────────────────────────'
        f'{anim}'
        f'</text>'
    )

    stats_y = stats_divider_y + 16
    streak = stats.get("current_streak", 0)
    longest = stats.get("longest_streak", 0)
    op, anim = theme.fade("1.4s", "0.3s")
    parts.append(
        f'<text x="{ox + PAD_L}" y="{stats_y}" font-size="11" {op}>'
        f'<tspan font-weight="bold" fill="var(--red)">[ CURRENT_STREAK ]</tspan> '
        f'<tspan fill="var(--text)">{streak} DAYS</tspan>  ·  '
        f'<tspan font-weight="bold" fill="var(--amber)">[ LONGEST_STREAK ]</tspan> '
        f'<tspan fill="var(--text)">{longest} DAYS</tspan>  ·  '
        f'<tspan font-weight="bold" fill="var(--blue)">[ COMPILATION ]</tspan> '
        f'<tspan fill="var(--text)">NOMINAL</tspan>'
        f'{anim}'
        f'</text>'
    )

    # --- Bottom bar content ---
    parts.append(
        f'<text x="20" y="{H - 11}" font-size="9" fill="var(--dim)" font-weight="bold">'
        f'DATABASE // INDEXING : OK'
        f'</text>'
    )
    parts.append(
        f'<text x="{W - 20}" y="{H - 11}" font-size="9" fill="var(--dim)" font-weight="bold" text-anchor="end">'
        f'STORAGE_NODE: LOCAL_SHARD_01 // SECURE_FLOW'
        f'</text>'
    )

    svg_body = "\n  ".join(parts)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Hallmark · system: industrial-brutalist (DESIGN.md) · card: contribution-heatmap · motion: SMIL cascade · reduced-motion: {"yes" if theme.REDUCE_MOTION else "no"} -->
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="hm-title hm-desc">
  <title id="hm-title">Contribution heatmap</title>
  <desc id="hm-desc">{total:,} contributions over the past 52 weeks; current streak {streak} days.</desc>
  {theme.css()}
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
