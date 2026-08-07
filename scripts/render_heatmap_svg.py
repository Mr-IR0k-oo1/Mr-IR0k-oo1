#!/usr/bin/env python3
"""Render contributions.json into a highly-engineered, industrial-brutalist animated heatmap SVG with tactical telemetry aesthetics."""

import json
import os
from datetime import date, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# --- Tactical Telemetry Palette (Consistent with other cards) ---
BG            = "#0B0C10"  # Deep space/charcoal technical background
BORDER        = "#1F2430"  # Dark steel grid line
BORDER_BRIGHT = "#3F4D66"  # Active frame highlight
TEXT          = "#E2E8F0"  # Crisp off-white phosphor text
DIM           = "#5A6578"  # Blueprint slate gray for metadata

# Accent Colors
RED           = "#FF3E3E"  # Aviation hazard / alarm red
GREEN         = "#00FF66"  # Matrix phosphor active green
BLUE          = "#00F0FF"  # Hyper-cyber blue/teal
AMBER         = "#FFB700"  # Tactical warning amber

# Tactical Monochromatic Green Heat Palette representing different contribution intensities
HEAT_PALETTE = [
    "#12151D",  # Level 0: Inactive deep charcoal
    "#0D3A1F",  # Level 1: Low-intensity phosphor
    "#145E32",  # Level 2: Medium-low intensity
    "#218C4A",  # Level 3: Medium-high intensity
    "#2DBC62",  # Level 4: High-intensity active
    "#00FF66"   # Level 5: Maximum activity glow
]

CELL   = 13
GAP    = 3
RADIUS = 1.0  # Ultra-sharp modular corners (rx=1.0)
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

    # Calculate inner dimensions dynamically but robustly
    heat_w = PAD_L + num_cols * (CELL + GAP) + 10
    W = heat_w + WIN_PAD * 2
    
    # Calculate height based on strict grid and telemetry blocks
    # Header space: BAR_H (26)
    # Inside margins: WIN_PAD (20)
    # Shell prompt space: 42
    # Grid offset padding: PAD_T (20)
    # Grid height: 7 * 16 = 112
    # Legend offset: 18
    # Legend height: 13
    # Stats block: 34
    # Footer space: BAR_H (26) + margins
    H = 295  # Standardized stable height for 52-week matrix console

    ox = WIN_PAD
    oy = BAR_H + WIN_PAD

    parts = []

    # --- Container and main grid ---
    # Draw solid 90-degree outer container with razor-sharp border
    parts.append(f'<rect width="{W}" height="{H}" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>')

    # Blueprint Grid Lines
    parts.append(f'<line x1="0" y1="26" x2="{W}" y2="26" stroke="{BORDER}" stroke-width="1"/>')
    parts.append(f'<line x1="0" y1="{H - 26}" x2="{W}" y2="{H - 26}" stroke="{BORDER}" stroke-width="1"/>')

    # Corner registration crosshairs (+)
    parts.append(f'<text x="6" y="12" font-size="9" fill="{DIM}" font-weight="bold">+</text>')
    parts.append(f'<text x="{W - 13}" y="12" font-size="9" fill="{DIM}" font-weight="bold">+</text>')
    parts.append(f'<text x="6" y="{H - 6}" font-size="9" fill="{DIM}" font-weight="bold">+</text>')
    parts.append(f'<text x="{W - 13}" y="{H - 6}" font-size="9" fill="{DIM}" font-weight="bold">+</text>')

    # --- Header bar contents ---
    # Flashing system status square
    parts.append(
        f'<rect x="20" y="10" width="6" height="6" fill="{GREEN}">'
        f'<animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    parts.append(f'<text x="32" y="16" font-size="9" font-weight="bold" fill="{GREEN}">[ CONSOLE: BASHLOG ]</text>')

    # Centered telemetry indicator
    parts.append(
        f'<text x="{W//2}" y="16" text-anchor="middle" font-size="9" fill="{DIM}" font-weight="bold">'
        f'STREAM: SYSTEM_ACTIVITY_INDEX // 52_WEEK_MATRIX'
        f'</text>'
    )

    # Right side security warning
    parts.append(f'<text x="{W - 20}" y="16" text-anchor="end" font-size="9" fill="{RED}" font-weight="bold">INGEST_STATE: ONLINE</text>')

    # --- Shell prompt ---
    prompt_y = oy + 12
    parts.append(
        f'<text x="{ox}" y="{prompt_y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="11" fill="{BLUE}">'
        f'mr-ir0k-oo1@mainframe:~$ git log --since="52 weeks ago" | wc -l</text>'
    )
    
    prompt_y += 16
    total = stats.get("total", 0)
    parts.append(
        f'<text x="{ox}" y="{prompt_y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="12" fill="{GREEN}" font-weight="bold" opacity="0">'
        f'[+] {total:,} INGESTED LOGS DETECTED'
        f'<animate attributeName="opacity" from="0" to="1" begin="0.2s" dur="0.2s" fill="freeze"/>'
        f'</text>'
    )

    # Offset heatmap below the prompt
    grid_oy = oy + 36

    # --- Day labels ---
    for i, label in enumerate(DAYS_LABELS):
        if label:
            y = grid_oy + PAD_T + i * (CELL + GAP) + CELL - 2
            parts.append(
                f'<text x="{ox}" y="{y}" '
                f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
                f'font-size="9.5" fill="{DIM}" text-anchor="start" font-weight="bold">{label}</text>'
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
                f'font-size="9.5" fill="{DIM}" font-weight="bold">{MONTHS[m].upper()}</text>'
            )

    # --- Heatmap Cells ---
    cell_idx = 0
    for col in range(num_cols):
        for row in range(7):
            cell = grid[row][col] if col < len(grid[row]) else None
            level = cell["level"] if cell else 0
            fill = HEAT_PALETTE[min(level, 5)]

            x = ox + PAD_L + col * (CELL + GAP)
            y = grid_oy + PAD_T + row * (CELL + GAP)
            
            # Fast, sequential cascade loading effect
            delay = 0.05 + cell_idx * 0.002

            # Use razor-sharp corners rx=RADIUS
            parts.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                f'rx="{RADIUS}" fill="{fill}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{delay:.3f}s" dur="0.15s" fill="freeze"/>'
                f'</rect>'
            )
            cell_idx += 1

    # --- Legend ---
    legend_y = grid_oy + PAD_T + 7 * (CELL + GAP) + 18
    legend_x = ox + PAD_L
    parts.append(
        f'<text x="{legend_x}" y="{legend_y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="9.5" fill="{DIM}" font-weight="bold">LESS</text>'
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
        f'font-size="9.5" fill="{DIM}" font-weight="bold">MORE</text>'
    )

    # --- Tactical Stats Panel (Engineering block layout) ---
    stats_divider_y = legend_y + 14
    parts.append(
        f'<text x="{ox}" y="{stats_divider_y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="10" fill="{DIM}" opacity="0">'
        f'[ STATS_METRICS ] ───────────────────────────────────────────────────────────────────────────────────'
        f'<animate attributeName="opacity" from="0" to="1" begin="1.2s" dur="0.3s" fill="freeze"/>'
        f'</text>'
    )

    stats_y = stats_divider_y + 16
    streak = stats.get("current_streak", 0)
    longest = stats.get("longest_streak", 0)
    parts.append(
        f'<text x="{ox + PAD_L}" y="{stats_y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="11" opacity="0">'
        f'<tspan font-weight="bold" fill="{RED}">[ CURRENT_STREAK ]</tspan> '
        f'<tspan fill="{TEXT}">{streak} DAYS</tspan>  ·  '
        f'<tspan font-weight="bold" fill="{AMBER}">[ LONGEST_STREAK ]</tspan> '
        f'<tspan fill="{TEXT}">{longest} DAYS</tspan>  ·  '
        f'<tspan font-weight="bold" fill="{BLUE}">[ COMPILATION ]</tspan> '
        f'<tspan fill="{TEXT}">NOMINAL</tspan>'
        f'<animate attributeName="opacity" from="0" to="1" begin="1.4s" dur="0.3s" fill="freeze"/>'
        f'</text>'
    )

    # --- Bottom bar content (Consistent with other cards) ---
    parts.append(
        f'<text x="20" y="{H - 11}" font-size="9" fill="{DIM}" font-weight="bold">'
        f'DATABASE // INDEXING : OK'
        f'</text>'
    )
    parts.append(
        f'<text x="{W - 20}" y="{H - 11}" font-size="9" fill="{DIM}" font-weight="bold" text-anchor="end">'
        f'STORAGE_NODE: LOCAL_SHARD_01 // SECURE_FLOW'
        f'</text>'
    )

    svg_body = "\n  ".join(parts)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: 0.02em; }}
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
