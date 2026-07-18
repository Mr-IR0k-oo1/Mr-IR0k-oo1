#!/usr/bin/env python3
"""Generate an enhanced neofetch-style info card SVG with terminal chrome."""

import os

STATIC = os.environ.get("STATIC", "0") == "1"

# --- Catppuccin Mocha palette ---
BG       = "#1e1e2e"
SURFACE  = "#313244"
OVERLAY  = "#45475a"
TEXT     = "#cdd6f4"
DIM      = "#6c7086"
BLUE     = "#89b4fa"
GREEN    = "#a6e3a1"
YELLOW   = "#f9e2af"
RED      = "#f38ba8"
MAUVE    = "#cba6f7"
PEACH    = "#fab387"
TEAL     = "#94e2d5"
PINK     = "#f5c2e7"

# --- Config ---
TITLE = "Mr-IR0k-oo1"
SUBTITLE = "github.com"

# Neofetch-style rows: (label_color, label, value)
ROWS = [
    (BLUE,   "os",       "Arch Linux x86_64"),
    (BLUE,   "host",     "Linux 6.x"),
    (BLUE,   "shell",    "bash 5.2"),
    (BLUE,   "editor",   "Neovim 0.10 + tmux"),
    (BLUE,   "terminal", "Alacritty"),
    (BLUE,   "cpu",      "systems & security"),
    (BLUE,   "memory",   "Rust · Python · TypeScript · Bash"),
    (GREEN,  "focus",    "CVE scanning · WiFi diag · AI infra · SDR"),
    (MAUVE,  "now",      "Building CVE engine storage layer"),
    (PEACH,  "uptime",   "Linux-first, minimal, hardened by default"),
]

# Tiny Rust gear ASCII for the left side
LOGO = [
    "   ___  ",
    "  / _ \\ ",
    " | | | |",
    " | |_| |",
    "  \\___/ ",
    "        ",
]

# --- Dimensions ---
LINE_H    = 22
PAD_X     = 20
PAD_Y     = 16
BAR_H     = 34        # title bar height
LOGO_W    = 80        # logo column width
INFO_X    = PAD_X + LOGO_W + 8
ROWS_H    = len(ROWS) * LINE_H
LOGO_H    = len(LOGO) * LINE_H
W = 490
H = PAD_Y + BAR_H + max(ROWS_H, LOGO_H) + PAD_Y + 4


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg() -> str:
    lines = []
    y_start = PAD_Y + BAR_H + 16  # first content baseline

    # --- Title bar ---
    lines.append(f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{SURFACE}" stroke-width="1"/>')
    lines.append(f'<rect width="{W}" height="{BAR_H}" rx="10" fill="{SURFACE}"/>')
    lines.append(f'<rect y="24" width="{W}" height="10" fill="{SURFACE}"/>')
    # Traffic lights
    lines.append(f'<circle cx="18" cy="{BAR_H//2}" r="5" fill="{RED}"/>')
    lines.append(f'<circle cx="36" cy="{BAR_H//2}" r="5" fill="{YELLOW}"/>')
    lines.append(f'<circle cx="54" cy="{BAR_H//2}" r="5" fill="{GREEN}"/>')
    # Title
    lines.append(
        f'<text x="{W//2}" y="{BAR_H//2 + 5}" text-anchor="middle" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="12" fill="{DIM}">{esc(SUBTITLE)} — neofetch</text>'
    )

    # --- Logo (left column) ---
    for i, row in enumerate(LOGO):
        ly = y_start + i * LINE_H
        delay = 0.2 + i * 0.08
        lines.append(
            f'<text x="{PAD_X}" y="{ly}" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="13" fill="{MAUVE}" opacity="0">'
            f'{esc(row)}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.3s" fill="freeze"/>'
            f'</text>'
        )

    # --- Username + separator (right column) ---
    uy = y_start
    lines.append(
        f'<text x="{INFO_X}" y="{uy}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="14" font-weight="bold" fill="{PINK}" opacity="0">'
        f'{esc(TITLE)}'
        f'<animate attributeName="opacity" from="0" to="1" begin="0.3s" dur="0.3s" fill="freeze"/>'
        f'</text>'
    )
    uy += LINE_H
    lines.append(
        f'<text x="{INFO_X}" y="{uy}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="11" fill="{DIM}" opacity="0">'
        f'────────────────────────────────────'
        f'<animate attributeName="opacity" from="0" to="1" begin="0.4s" dur="0.3s" fill="freeze"/>'
        f'</text>'
    )
    uy += LINE_H

    # --- Info rows ---
    for i, (color, label, value) in enumerate(ROWS):
        delay = 0.5 + i * 0.18
        uy_row = y_start + (i + 2) * LINE_H  # +2 for username + separator
        lines.append(
            f'<text x="{INFO_X}" y="{uy_row}" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="12" opacity="0">'
            f'<tspan font-weight="bold" fill="{color}">{esc(label):>10}</tspan>'
            f'  <tspan fill="{TEXT}">{esc(value)}</tspan>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.3s" fill="freeze"/>'
            f'</text>'
        )

    # --- Blinking cursor at bottom ---
    cursor_y = y_start + (len(ROWS) + 2) * LINE_H + 4
    lines.append(
        f'<rect x="{INFO_X}" y="{cursor_y - 11}" width="8" height="14" fill="{TEXT}" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;1;0" dur="1.2s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    # --- Color palette bar at bottom ---
    palette_colors = [RED, YELLOW, GREEN, TEAL, BLUE, MAUVE, PINK, PEACH]
    bar_y = H - PAD_Y - 12
    for i, c in enumerate(palette_colors):
        bx = PAD_X + i * 18
        lines.append(
            f'<rect x="{bx}" y="{bar_y}" width="14" height="8" rx="2" fill="{c}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{2.0 + i * 0.05:.2f}s" dur="0.3s" fill="freeze"/>'
            f'</rect>'
        )

    svg_body = "\n  ".join(lines)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  </style>
  {svg_body}
</svg>'''


def main():
    svg = build_svg()
    out = os.path.join(os.path.dirname(__file__), "..", "info-card.svg")
    with open(out, "w") as f:
        f.write(svg)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
