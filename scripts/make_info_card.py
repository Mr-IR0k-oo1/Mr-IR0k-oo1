#!/usr/bin/env python3
"""Generate a neofetch-style info card SVG."""

import os
import textwrap

STATIC = os.environ.get("STATIC", "0") == "1"

# --- Configuration (edit these to match your profile) ---
TITLE = "Mr-IR0k-oo1"
SUBTITLE = "Systems-focused developer"

ROWS = [
    ("Now",    "Building CVE scanning engine & WiFi diagnostics"),
    ("Focus",  "Systems · Security · AI infra · Embedded/RF"),
    ("Stack",  "Rust · Python · TypeScript · Bash"),
    ("OS",     "Linux (Arch)"),
    ("Editor", "Neovim + tmux"),
    ("Shell",  "bash"),
]

ACCENT = "#cdd6f4"    # bright text
LABEL  = "#89b4fa"    # blue labels
DIM    = "#6c7086"    # dim text
BG     = "#1e1e2e"    # card background
BORDER = "#313244"    # border color
TITLE_CLR = "#f5c2e7" # pink title

# --- SVG dimensions ---
LINE_H   = 28
PAD_X    = 28
PAD_Y    = 22
HEADER_H = 52
ROW_H    = len(ROWS) * LINE_H
W = 490
H = PAD_Y + HEADER_H + ROW_H + PAD_Y + 8

def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build_svg() -> str:
    lines = []
    y = PAD_Y + 34  # first text baseline

    # Header
    lines.append(
        f'<text x="{PAD_X}" y="{y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="16" font-weight="bold" fill="{TITLE_CLR}">'
        f'{escape(TITLE)}@github</text>'
    )
    y += 20
    lines.append(
        f'<text x="{PAD_X}" y="{y}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="12" fill="{DIM}">'
        f'──────────────────────────────────────</text>'
    )
    y += 24

    # Rows with fade-in animation
    for i, (label, value) in enumerate(ROWS):
        delay = 0.6 + i * 0.25
        op = "" if STATIC else f''' opacity="0">
      <animate attributeName="opacity" from="0" to="1"
        begin="{delay}s" dur="0.4s" fill="freeze"/>
'''
        close = "" if STATIC else "</tspan>"
        opener = "" if STATIC else '<tspan opacity="0">'

        lines.append(
            f'<text x="{PAD_X}" y="{y}" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="13"{op}>'
            f'{opener}<tspan font-weight="bold" fill="{LABEL}">{escape(label):>8}</tspan>'
            f'  {escape(value)}{close}</text>'
        )
        y += LINE_H

    # Close the SVG
    svg_body = "\n    ".join(lines)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  </style>
  <rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1"/>
  <rect x="0" y="0" width="{W}" height="38" rx="10" fill="{BORDER}"/>
  <rect x="0" y="28" width="{W}" height="10" fill="{BORDER}"/>
  <circle cx="18" cy="19" r="5" fill="#f38ba8"/>
  <circle cx="36" cy="19" r="5" fill="#f9e2af"/>
  <circle cx="54" cy="19" r="5" fill="#a6e3a1"/>
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
