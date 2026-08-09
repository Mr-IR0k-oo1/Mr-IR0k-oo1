#!/usr/bin/env python3
"""Generate a highly-engineered, industrial-brutalist workspace card SVG with tactical terminal aesthetics.

Theme-aware: palette comes from theme.css custom properties so the card adapts
to GitHub light/dark mode while keeping the tactical telemetry look in dark mode.
"""

import os

import theme

# --- Selected Projects Database ---
PROJECTS = [
    {
        "name": "cve-scanner",
        "lang": "Rust",
        "lang_color": "var(--peach)",
        "status": "ACTIVE",
        "status_color": "var(--green)",
        "desc": "CVE correlation engine — NVD + EPSS risk scoring",
    },
    {
        "name": "wifi-diag",
        "lang": "Python",
        "lang_color": "var(--blue)",
        "status": "ACTIVE",
        "status_color": "var(--green)",
        "desc": "802.11 packet sniffer → rogue-AP detection module",
    },
    {
        "name": "ai-orchestrator",
        "lang": "Rust",
        "lang_color": "var(--peach)",
        "status": "STAGED",
        "status_color": "var(--amber)",
        "desc": "Terminal memory layer for multi-CLI agents",
    },
    {
        "name": "sdr-tracker",
        "lang": "Rust",
        "lang_color": "var(--peach)",
        "status": "STAGED",
        "status_color": "var(--amber)",
        "desc": "SGP4 orbital propagation + IQ raw processing pipelines",
    },
]

# --- Dimensions (Matches info_card.svg exactly) ---
W = 490
H = 280
PAD_X = 20


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg() -> str:
    lines = []

    # --- Container and main grid ---
    lines.append(f'<rect width="{W}" height="{H}" fill="var(--bg)" stroke="var(--border)" stroke-width="1.5"/>')

    # Blueprint Grid Lines (aligned with info_card)
    lines.append(f'<line x1="0" y1="26" x2="{W}" y2="26" stroke="var(--border)" stroke-width="1"/>')
    lines.append(f'<line x1="0" y1="254" x2="{W}" y2="254" stroke="var(--border)" stroke-width="1"/>')

    # Corner registration crosshairs (+)
    lines.append(f'<text x="6" y="12" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')
    lines.append(f'<text x="{W - 13}" y="12" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')
    lines.append(f'<text x="6" y="{H - 6}" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')
    lines.append(f'<text x="{W - 13}" y="{H - 6}" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')

    # --- Header bar contents ---
    lines.append(
        f'<rect x="20" y="10" width="6" height="6" fill="var(--blue)">'
        f'<animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    lines.append(f'<text x="32" y="16" font-size="9" font-weight="bold" fill="var(--blue)">[ DIRECTORY: ~/PROJECTS ]</text>')

    lines.append(
        f'<text x="{W//2}" y="16" text-anchor="middle" font-size="9" fill="var(--dim)" font-weight="bold">'
        f'WORKSPACE MODULES // QUERY_OK'
        f'</text>'
    )

    lines.append(f'<text x="{W - 20}" y="16" text-anchor="end" font-size="9" fill="var(--red)" font-weight="bold">TARGET_NODES: 04</text>')

    # --- Section Subheader (Terminal Command Prompt) ---
    lines.append(
        f'<text x="20" y="46" font-size="11" fill="var(--blue)">'
        f'$ workspace --query-active --verbose'
        f'</text>'
    )

    # --- Modular Project Cards (Brutalist Table Rows) ---
    card_y_start = 60
    card_h = 40
    gap = 6

    for i, proj in enumerate(PROJECTS):
        delay = 0.15 + i * 0.12
        card_y = card_y_start + i * (card_h + gap)

        lines.append(
            f'<rect x="{PAD_X}" y="{card_y}" width="{W - PAD_X*2}" height="{card_h}" '
            f'fill="var(--surface)" stroke="var(--border)" stroke-width="1" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.2s" fill="freeze"/>'
            f'</rect>'
        )

        lines.append(
            f'<line x1="90" y1="{card_y}" x2="90" y2="{card_y + card_h}" stroke="var(--border)" stroke-width="1" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.2s" fill="freeze"/>'
            f'</line>'
        )

        status_text = f" {proj['status']} "
        lines.append(
            f'<text x="55" y="{card_y + 24}" font-size="9" font-weight="bold" fill="{proj["status_color"]}" text-anchor="middle" opacity="0">'
            f'{esc(status_text)}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay + 0.05:.2f}s" dur="0.2s" fill="freeze"/>'
            f'</text>'
        )

        lines.append(
            f'<text x="105" y="{card_y + 16}" font-size="12" font-weight="bold" fill="var(--text)" opacity="0">'
            f'{esc(proj["name"])}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay + 0.05:.2f}s" dur="0.2s" fill="freeze"/>'
            f'</text>'
        )

        lang_str = f"[ {proj['lang'].upper()} ]"
        lines.append(
            f'<text x="{W - 32}" y="{card_y + 16}" font-size="10" font-weight="bold" fill="{proj["lang_color"]}" text-anchor="end" opacity="0">'
            f'{esc(lang_str)}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay + 0.08:.2f}s" dur="0.2s" fill="freeze"/>'
            f'</text>'
        )

        lines.append(
            f'<text x="105" y="{card_y + 30}" font-size="9.5" fill="var(--dim)" opacity="0">'
            f'{esc(proj["desc"])}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay + 0.08:.2f}s" dur="0.2s" fill="freeze"/>'
            f'</text>'
        )

    # --- Bottom bar content ---
    lines.append(
        f'<text x="20" y="269" font-size="9" fill="var(--dim)" font-weight="bold">'
        f'ACTIVE_REPOS // INGESTION : NOMINAL'
        f'</text>'
    )
    lines.append(
        f'<text x="{W - 20}" y="269" font-size="9" fill="var(--dim)" font-weight="bold" text-anchor="end">'
        f'NODES_ONLINE: 04 // STREAM: OK'
        f'</text>'
    )

    svg_body = "\n  ".join(lines)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  {theme.css()}
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
