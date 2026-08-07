#!/usr/bin/env python3
"""Generate a highly-engineered, industrial-brutalist neofetch-style info card SVG with tactical terminal aesthetics."""

import os

# --- Tactical Telemetry Palette ---
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
MAUVE         = "#B388FF"  # High-altitude purple
PEACH         = "#FF9E80"  # Sensor-range orange
PINK          = "#FF4081"  # Target-acquired magenta

TITLE = "Mr-IR0k-oo1@mainframe"

# Neofetch-style rows: (label, value, value_color)
ROWS = [
    ("OS",       "Arch Linux x86_64",                  BLUE),
    ("HOST",     "Linux Kernel 6.x // Hardened",       TEXT),
    ("SHELL",    "bash 5.2.26-release",                TEXT),
    ("EDITOR",   "Neovim 0.10.x + tmux 3.4",           GREEN),
    ("TERM",     "Alacritty // Minimal & Fast",        TEXT),
    ("CPU",      "Systems security architecture",      PEACH),
    ("MEMORY",   "Rust · Python · TypeScript · Bash",  MAUVE),
    ("FOCUS",    "CVE scanning · WiFi diag · SDR",     AMBER),
    ("STATUS",   "Active - Building CVE storage",      GREEN),
    ("METHOD",   "Linux-first, minimal, defensive",    PEACH),
]

# Tactical radar / crosshair ASCII logo
LOGO = [
    "  .──▲──.  ",
    " /   │   \\ ",
    "◄───[●]───►",
    " \\   │   / ",
    "  '──▼──'  ",
    "  [READY]  ",
]

# --- Dimensions ---
W = 490
H = 280


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg() -> str:
    lines = []

    # --- Container and main grid ---
    # Draw solid 90-degree outer container with razor-sharp border
    lines.append(f'<rect width="{W}" height="{H}" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>')

    # Blueprint Grid Lines (structural design)
    lines.append(f'<line x1="110" y1="0" x2="110" y2="{H}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="2,2"/>')
    lines.append(f'<line x1="0" y1="26" x2="{W}" y2="26" stroke="{BORDER}" stroke-width="1"/>')
    lines.append(f'<line x1="0" y1="254" x2="{W}" y2="254" stroke="{BORDER}" stroke-width="1"/>')

    # Corner registration crosshairs (+) to enforce the blueprint aesthetic
    lines.append(f'<text x="6" y="12" font-size="9" fill="{DIM}" font-weight="bold">+</text>')
    lines.append(f'<text x="{W - 13}" y="12" font-size="9" fill="{DIM}" font-weight="bold">+</text>')
    lines.append(f'<text x="6" y="{H - 6}" font-size="9" fill="{DIM}" font-weight="bold">+</text>')
    lines.append(f'<text x="{W - 13}" y="{H - 6}" font-size="9" fill="{DIM}" font-weight="bold">+</text>')

    # --- Header bar contents ---
    # Flashing system status square on the left
    lines.append(
        f'<rect x="20" y="10" width="6" height="6" fill="{GREEN}">'
        f'<animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    lines.append(f'<text x="32" y="16" font-size="9" font-weight="bold" fill="{GREEN}">[ SESSION: ACTIVE ]</text>')

    # Centered telemetry indicator
    lines.append(
        f'<text x="{W//2}" y="16" text-anchor="middle" font-size="9" fill="{DIM}" font-weight="bold">'
        f'TELEMETRY CORE // CONSOLE v2.0'
        f'</text>'
    )

    # Right side security warning
    lines.append(f'<text x="{W - 20}" y="16" text-anchor="end" font-size="9" fill="{RED}" font-weight="bold">SEC_LEVEL: HIGH</text>')

    # --- Left Column: Tactical ASCII Logo ---
    y_logo_start = 55
    logo_line_h = 18
    for i, row in enumerate(LOGO):
        ly = y_logo_start + i * logo_line_h
        delay = 0.1 + i * 0.05
        # Radar center dot should glow
        row_color = GREEN if i in (2, 5) else BLUE
        lines.append(
            f'<text x="20" y="{ly}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="12" fill="{row_color}" font-weight="bold" opacity="0">'
            f'{esc(row)}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.2s" fill="freeze"/>'
            f'</text>'
        )

    # --- Right Column: User Title & Separator ---
    lines.append(
        f'<text x="130" y="55" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="14" font-weight="bold" fill="{BLUE}" opacity="0">'
        f'{esc(TITLE)}'
        f'<animate attributeName="opacity" from="0" to="1" begin="0.1s" dur="0.2s" fill="freeze"/>'
        f'</text>'
    )
    lines.append(
        f'<text x="130" y="68" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="10" fill="{DIM}" opacity="0">'
        f'──────────────────────────────────────────'
        f'<animate attributeName="opacity" from="0" to="1" begin="0.15s" dur="0.2s" fill="freeze"/>'
        f'</text>'
    )

    # --- Information Rows ---
    row_y_start = 86
    row_h = 16
    for i, (label, value, val_color) in enumerate(ROWS):
        delay = 0.2 + i * 0.08
        y_pos = row_y_start + i * row_h

        # Label in brackets: e.g. [ OS ]
        label_str = f"[ {label:<6} ]"
        lines.append(
            f'<text x="130" y="{y_pos}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="11" opacity="0">'
            f'<tspan font-weight="bold" fill="{RED}">{esc(label_str)}</tspan>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.2s" fill="freeze"/>'
            f'</text>'
        )

        # Value
        lines.append(
            f'<text x="210" y="{y_pos}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="11" fill="{val_color}" opacity="0">'
            f'{esc(value)}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay + 0.04:.2f}s" dur="0.2s" fill="freeze"/>'
            f'</text>'
        )

    # --- Blinking Command Line Cursor ---
    cursor_y = row_y_start + len(ROWS) * row_h + 3
    lines.append(
        f'<rect x="130" y="{cursor_y - 10}" width="8" height="12" fill="{BLUE}" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;1;0" dur="1.0s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    # --- Bottom bar content ---
    lines.append(
        f'<text x="20" y="269" font-size="9" fill="{DIM}" font-weight="bold">'
        f'STATUS // STORAGE_ENGAGED : ACTIVE'
        f'</text>'
    )

    # Brutalist vertical color blocks as a modern terminal palette indicator
    palette_colors = [RED, AMBER, GREEN, BLUE, MAUVE, PEACH, PINK, TEXT]
    for i, c in enumerate(palette_colors):
        bx = W - 142 + i * 15
        lines.append(
            f'<rect x="{bx}" y="262" width="10" height="8" fill="{c}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{1.2 + i * 0.05:.2f}s" dur="0.2s" fill="freeze"/>'
            f'</rect>'
        )

    svg_body = "\n  ".join(lines)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: 0.02em; }}
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
