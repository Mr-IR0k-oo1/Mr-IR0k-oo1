#!/usr/bin/env python3
"""Generate a highly-engineered, industrial-brutalist neofetch-style info card SVG with tactical terminal aesthetics.

Theme-aware: palette comes from theme.css custom properties so the card adapts
to GitHub light/dark mode while keeping the tactical telemetry look in dark mode.
"""

import os

import theme

TITLE = "Mr-IR0k-oo1@mainframe"

# Neofetch-style rows: (label, value, value_color)
ROWS = [
    ("OS",       "Arch Linux x86_64",                  "var(--blue)"),
    ("HOST",     "Linux Kernel 6.x // Hardened",       "var(--text)"),
    ("SHELL",    "bash 5.2.26-release",                "var(--text)"),
    ("EDITOR",   "Neovim 0.10.x + tmux 3.4",           "var(--green)"),
    ("TERM",     "Alacritty // Minimal & Fast",        "var(--text)"),
    ("CPU",      "Systems security architecture",      "var(--peach)"),
    ("MEMORY",   "Rust · Python · TypeScript · Bash",  "var(--mauve)"),
    ("FOCUS",    "CVE scanning · WiFi diag · SDR",     "var(--amber)"),
    ("STATUS",   "Active - Building CVE storage",      "var(--green)"),
    ("METHOD",   "Linux-first, minimal, defensive",    "var(--peach)"),
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
    lines.append(f'<rect width="{W}" height="{H}" fill="var(--bg)" stroke="var(--border)" stroke-width="1.5"/>')

    # Blueprint Grid Lines (structural design)
    lines.append(f'<line x1="110" y1="0" x2="110" y2="{H}" stroke="var(--border)" stroke-width="1" stroke-dasharray="2,2"/>')
    lines.append(f'<line x1="0" y1="26" x2="{W}" y2="26" stroke="var(--border)" stroke-width="1"/>')
    lines.append(f'<line x1="0" y1="254" x2="{W}" y2="254" stroke="var(--border)" stroke-width="1"/>')

    # Corner registration crosshairs (+)
    lines.append(f'<text x="6" y="12" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')
    lines.append(f'<text x="{W - 13}" y="12" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')
    lines.append(f'<text x="6" y="{H - 6}" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')
    lines.append(f'<text x="{W - 13}" y="{H - 6}" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')

    # --- Header bar contents ---
    lines.append(
        f'<rect x="20" y="10" width="6" height="6" fill="var(--green)">'
        f'{theme.smil("opacity", "1;0.3;1", "1.5s", repeat="indefinite")}'
        f'</rect>'
    )
    lines.append(f'<text x="32" y="16" font-size="9" font-weight="bold" fill="var(--green)">[ SESSION: ACTIVE ]</text>')

    lines.append(
        f'<text x="{W//2}" y="16" text-anchor="middle" font-size="9" fill="var(--dim)" font-weight="bold">'
        f'TELEMETRY CORE // CONSOLE v2.0'
        f'</text>'
    )

    lines.append(f'<text x="{W - 20}" y="16" text-anchor="end" font-size="9" fill="var(--red)" font-weight="bold">SEC_LEVEL: HIGH</text>')

    # --- Left Column: Tactical ASCII Logo ---
    y_logo_start = 55
    logo_line_h = 18
    for i, row in enumerate(LOGO):
        ly = y_logo_start + i * logo_line_h
        delay = 0.1 + i * 0.05
        row_color = "var(--green)" if i in (2, 5) else "var(--blue)"
        op, anim = theme.fade(f"{delay:.2f}s")
        lines.append(
            f'<text x="20" y="{ly}" font-size="12" fill="{row_color}" font-weight="bold" {op}>'
            f'{esc(row)}'
            f'{anim}'
            f'</text>'
        )

    # --- Right Column: User Title & Separator ---
    op, anim = theme.fade("0.1s")
    lines.append(
        f'<text x="130" y="55" font-size="14" font-weight="bold" fill="var(--blue)" {op}>'
        f'{esc(TITLE)}'
        f'{anim}'
        f'</text>'
    )
    op, anim = theme.fade("0.15s")
    lines.append(
        f'<text x="130" y="68" font-size="10" fill="var(--dim)" {op}>'
        f'──────────────────────────────────────────'
        f'{anim}'
        f'</text>'
    )

    # --- Information Rows ---
    row_y_start = 86
    row_h = 16
    for i, (label, value, val_color) in enumerate(ROWS):
        delay = 0.2 + i * 0.08
        y_pos = row_y_start + i * row_h

        label_str = f"[ {label:<6} ]"
        op, anim = theme.fade(f"{delay:.2f}s")
        lines.append(
            f'<text x="130" y="{y_pos}" font-size="11" {op}>'
            f'<tspan font-weight="bold" fill="var(--red)">{esc(label_str)}</tspan>'
            f'{anim}'
            f'</text>'
        )

        op, anim = theme.fade(f"{delay + 0.04:.2f}s")
        lines.append(
            f'<text x="210" y="{y_pos}" font-size="11" fill="{val_color}" {op}>'
            f'{esc(value)}'
            f'{anim}'
            f'</text>'
        )

    # --- Blinking Command Line Cursor ---
    cursor_y = row_y_start + len(ROWS) * row_h + 3
    if theme.REDUCE_MOTION:
        cursor_op = 'opacity="0.6"'
        cursor_anim = ""
    else:
        cursor_op = 'opacity="0"'
        cursor_anim = theme.smil("opacity", "0;1;1;0", "1.0s", repeat="indefinite")
    lines.append(
        f'<rect x="130" y="{cursor_y - 10}" width="8" height="12" fill="var(--blue)" {cursor_op}>'
        f'{cursor_anim}'
        f'</rect>'
    )

    # --- Bottom bar content ---
    lines.append(
        f'<text x="20" y="269" font-size="9" fill="var(--dim)" font-weight="bold">'
        f'STATUS // STORAGE_ENGAGED : ACTIVE'
        f'</text>'
    )

    # Brutalist vertical color blocks as a modern terminal palette indicator
    palette_colors = ["var(--red)", "var(--amber)", "var(--green)", "var(--blue)",
                      "var(--mauve)", "var(--peach)", "var(--pink)", "var(--text)"]
    for i, c in enumerate(palette_colors):
        bx = W - 142 + i * 15
        op, anim = theme.fade(f"{1.2 + i * 0.05:.2f}s")
        lines.append(
            f'<rect x="{bx}" y="262" width="10" height="8" fill="{c}" {op}>'
            f'{anim}'
            f'</rect>'
        )

    svg_body = "\n  ".join(lines)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Hallmark · system: industrial-brutalist (DESIGN.md) · card: info · motion: SMIL cascade · reduced-motion: {"yes" if theme.REDUCE_MOTION else "no"} -->
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="ic-title ic-desc">
  <title id="ic-title">System profile</title>
  <desc id="ic-desc">{esc(TITLE)} — system, editor, tooling, and focus areas.</desc>
  {theme.css()}
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
