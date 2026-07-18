#!/usr/bin/env python3
"""Generate a workspace overview SVG — project cards with status indicators."""

import os

STATIC = os.environ.get("STATIC", "0") == "1"

# --- Catppuccin Mocha ---
BG      = "#1e1e2e"
SURFACE = "#313244"
OVERLAY = "#45475a"
TEXT    = "#cdd6f4"
DIM     = "#6c7086"
BLUE    = "#89b4fa"
GREEN   = "#a6e3a1"
YELLOW  = "#f9e2af"
RED     = "#f38ba8"
MAUVE   = "#cba6f7"
PEACH   = "#fab387"
TEAL    = "#94e2d5"
PINK    = "#f5c2e7"

# --- Projects ---
PROJECTS = [
    {
        "name": "cve-scanner",
        "lang": "Rust",
        "lang_color": PEACH,
        "status": "active",
        "status_color": GREEN,
        "desc": "CVE correlation engine — NVD + EPSS risk scoring",
    },
    {
        "name": "wifi-diag",
        "lang": "Python",
        "lang_color": BLUE,
        "status": "active",
        "status_color": GREEN,
        "desc": "802.11 packet sniffer → rogue-AP detection",
    },
    {
        "name": "ai-orchestrator",
        "lang": "Rust",
        "lang_color": PEACH,
        "status": "wip",
        "status_color": YELLOW,
        "desc": "Terminal memory layer for multi-CLI agents",
    },
    {
        "name": "sdr-tracker",
        "lang": "Rust",
        "lang_color": PEACH,
        "status": "wip",
        "status_color": YELLOW,
        "desc": "SGP4 orbital propagation + IQ pipelines",
    },
]

# --- Dimensions ---
BAR_H    = 34
PAD_X    = 20
PAD_Y    = 16
CARD_H   = 44
CARD_GAP = 8
W = 490
H = PAD_Y + BAR_H + len(PROJECTS) * (CARD_H + CARD_GAP) + PAD_Y + 4


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg() -> str:
    parts = []

    # --- Window chrome ---
    parts.append(f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{SURFACE}" stroke-width="1"/>')
    parts.append(f'<rect width="{W}" height="{BAR_H}" rx="10" fill="{SURFACE}"/>')
    parts.append(f'<rect y="24" width="{W}" height="10" fill="{SURFACE}"/>')
    parts.append(f'<circle cx="18" cy="{BAR_H//2}" r="5" fill="{RED}"/>')
    parts.append(f'<circle cx="36" cy="{BAR_H//2}" r="5" fill="{YELLOW}"/>')
    parts.append(f'<circle cx="54" cy="{BAR_H//2}" r="5" fill="{GREEN}"/>')
    parts.append(
        f'<text x="{W//2}" y="{BAR_H//2 + 5}" text-anchor="middle" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="12" fill="{DIM}">workspace — selected projects</text>'
    )

    # --- Section header ---
    cy = PAD_Y + BAR_H + 14
    parts.append(
        f'<text x="{PAD_X}" y="{cy}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="11" fill="{DIM}">$ ls -la ~/projects</text>'
    )
    cy += 8

    # --- Project cards ---
    for i, proj in enumerate(PROJECTS):
        delay = 0.3 + i * 0.2
        card_y = cy + i * (CARD_H + CARD_GAP)

        # Card background
        parts.append(
            f'<rect x="{PAD_X}" y="{card_y}" width="{W - PAD_X*2}" height="{CARD_H}" '
            f'rx="6" fill="{SURFACE}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="0.6" begin="{delay:.2f}s" dur="0.3s" fill="freeze"/>'
            f'</rect>'
        )

        # Status dot
        dot_x = PAD_X + 12
        dot_y = card_y + CARD_H // 2
        parts.append(
            f'<circle cx="{dot_x}" cy="{dot_y}" r="3" fill="{proj["status_color"]}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay + 0.1:.2f}s" dur="0.3s" fill="freeze"/>'
            f'</circle>'
        )

        # Project name
        name_x = PAD_X + 24
        parts.append(
            f'<text x="{name_x}" y="{card_y + 17}" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="12" font-weight="bold" fill="{TEXT}" opacity="0">'
            f'{esc(proj["name"])}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay + 0.1:.2f}s" dur="0.3s" fill="freeze"/>'
            f'</text>'
        )

        # Language badge
        lang_x = name_x + len(proj["name"]) * 7.5 + 12
        parts.append(
            f'<rect x="{lang_x}" y="{card_y + 7}" width="{len(proj["lang"]) * 7 + 10}" height="14" '
            f'rx="3" fill="{proj["lang_color"]}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="0.25" begin="{delay + 0.15:.2f}s" dur="0.3s" fill="freeze"/>'
            f'</rect>'
        )
        parts.append(
            f'<text x="{lang_x + 5}" y="{card_y + 17}" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="9" fill="{proj["lang_color"]}" opacity="0">'
            f'{esc(proj["lang"])}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay + 0.15:.2f}s" dur="0.3s" fill="freeze"/>'
            f'</text>'
        )

        # Description
        parts.append(
            f'<text x="{name_x}" y="{card_y + 34}" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="10" fill="{DIM}" opacity="0">'
            f'{esc(proj["desc"])}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay + 0.2:.2f}s" dur="0.3s" fill="freeze"/>'
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
    svg = build_svg()
    out = os.path.join(os.path.dirname(__file__), "..", "workspace-card.svg")
    with open(out, "w") as f:
        f.write(svg)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
