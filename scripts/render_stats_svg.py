#!/usr/bin/env python3
"""Render data/stats.json into an industrial-brutalist profile stats SVG.

Theme-aware: palette comes from theme.css custom properties so the card adapts
to GitHub light/dark mode while keeping the tactical telemetry look in dark mode.
"""

import json
import os

import theme

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "profile-stats.svg")

# Terminal chrome & layout
BAR_H = 26
WIN_PAD = 20
PAD_X = 20
LINE_H = 22
BAR_W = 260

LANG_COLORS = {
    "Rust": "#dea584",
    "Python": "#3572a5",
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Shell": "#89e051",
    "C": "#555555",
    "C++": "#f34b7d",
    "Makefile": "#427819",
    "Dockerfile": "#384d54",
    "Go": "#00add8",
    "Lua": "#000080",
    "C#": "#178600",
    "Jupyter Notebook": "#da5b0b",
    "CMake": "#da3434",
    "Nix": "#7e7eff",
    "Java": "#b07219",
    "Zig": "#ec915c",
    "Ruby": "#701516",
}
OTHER_COLOR = "#8b949e"


def esc(t) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def member_since(created_at: str) -> str:
    try:
        return created_at[:4]
    except (TypeError, KeyError):
        return "—"


def build_svg(data: dict) -> str:
    user = data.get("user", {})
    repos = data.get("repos", {})
    langs = data.get("languages", {}) or {}

    stats_rows = [
        ("followers", f'{user.get("followers", 0):,}'),
        ("following", f'{user.get("following", 0):,}'),
        ("public repos", f'{repos.get("count", user.get("public_repos", 0))}'),
        ("stars received", f'{repos.get("total_stars", 0):,}'),
        ("forks", f'{repos.get("total_forks", 0):,}'),
        ("member since", member_since(user.get("created_at", ""))),
    ]

    total_bytes = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    other_pct = max(0.0, 100.0 - (sum(v for _, v in top) / total_bytes * 100.0))

    # --- Layout math ---
    header_h = 2 * LINE_H                       # username + divider
    stats_h = len(stats_rows) * LINE_H
    langs_h = (LINE_H + 12) * len(top) + 4      # name line + bar line per lang
    footer_h = LINE_H
    content_h = header_h + stats_h + langs_h + footer_h
    W = 520
    H = WIN_PAD * 2 + BAR_H + content_h + 6

    ox = WIN_PAD
    oy = BAR_H + WIN_PAD

    parts = []

    # --- Container and blueprint grid ---
    parts.append(f'<rect width="{W}" height="{H}" fill="var(--bg)" stroke="var(--border)" stroke-width="1.5"/>')
    parts.append(f'<line x1="0" y1="26" x2="{W}" y2="26" stroke="var(--border)" stroke-width="1"/>')
    parts.append(f'<line x1="0" y1="{H - 26}" x2="{W}" y2="{H - 26}" stroke="var(--border)" stroke-width="1"/>')

    # Corner registration crosshairs
    parts.append(f'<text x="6" y="12" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')
    parts.append(f'<text x="{W - 13}" y="12" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')
    parts.append(f'<text x="6" y="{H - 6}" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')
    parts.append(f'<text x="{W - 13}" y="{H - 6}" font-size="9" fill="var(--dim)" font-weight="bold">+</text>')

    # --- Header bar contents ---
    parts.append(
        f'<rect x="20" y="10" width="6" height="6" fill="var(--green)">'
        f'<animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    parts.append(f'<text x="32" y="16" font-size="9" font-weight="bold" fill="var(--green)">[ CONSOLE: PROFILER ]</text>')

    parts.append(
        f'<text x="{W//2}" y="16" text-anchor="middle" font-size="9" fill="var(--dim)" font-weight="bold">'
        f'IDENTITY // REPOSITORY_TELEMETRY'
        f'</text>'
    )

    parts.append(f'<text x="{W - 20}" y="16" text-anchor="end" font-size="9" fill="var(--red)" font-weight="bold">GIT_TRAIL: VISIBLE</text>')

    # --- Shell prompt ---
    y = oy + 12
    parts.append(
        f'<text x="{ox}" y="{y}" font-size="11" fill="var(--blue)">'
        f'mr-ir0k-oo1@mainframe:~$ python -c "import me"</text>'
    )
    y += LINE_H
    name = user.get("name") or data.get("username", "user")
    parts.append(
        f'<text x="{ox}" y="{y}" font-size="13" font-weight="bold" fill="var(--text)">'
        f'{esc(name)}</text>'
    )
    y += LINE_H

    # --- Stats rows ---
    for label, value in stats_rows:
        parts.append(
            f'<text x="{ox}" y="{y}" font-size="12">'
            f'<tspan fill="var(--blue)" font-weight="bold">[ {esc(label):>12} ]</tspan>'
            f'<tspan fill="var(--dim)"> =</tspan>'
            f'<tspan fill="var(--text)">  {esc(value)}</tspan>'
            f'</text>'
        )
        y += LINE_H

    # --- Languages ---
    y += 6
    parts.append(
        f'<text x="{ox}" y="{y}" font-size="11" fill="var(--blue)">'
        f'mr-ir0k-oo1@mainframe:~$ du -sh ~/languages</text>'
    )
    y += LINE_H

    if top:
        for lang, size in top:
            pct = size / total_bytes * 100.0
            color = LANG_COLORS.get(lang, OTHER_COLOR)
            parts.append(
                f'<text x="{ox}" y="{y}" font-size="11" fill="{color}" '
                f'font-weight="bold">{esc(lang):>12}</text>'
            )
            parts.append(
                f'<text x="{ox + 150}" y="{y}" font-size="11" fill="var(--dim)">'
                f'{pct:.1f}%</text>'
            )
            y += 6
            bar_y = y + 4
            parts.append(
                f'<rect x="{ox}" y="{bar_y}" width="{BAR_W}" height="6" '
                f'fill="var(--surface)"/>'
            )
            fill_w = max(2.0, BAR_W * pct / 100.0)
            parts.append(
                f'<rect x="{ox}" y="{bar_y}" width="{fill_w:.1f}" height="6" '
                f'fill="{color}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="0.4s" dur="0.4s" fill="freeze"/>'
                f'</rect>'
            )
            y += LINE_H

        if other_pct > 0.5:
            parts.append(
                f'<text x="{ox}" y="{y}" font-size="11" fill="{OTHER_COLOR}" '
                f'font-weight="bold">{"Other":>12}</text>'
            )
            parts.append(
                f'<text x="{ox + 150}" y="{y}" font-size="11" fill="var(--dim)">'
                f'{other_pct:.1f}%</text>'
            )
            y += 6
            bar_y = y + 4
            parts.append(
                f'<rect x="{ox}" y="{bar_y}" width="{BAR_W}" height="6" '
                f'fill="var(--surface)"/>'
            )
            fill_w = max(2.0, BAR_W * other_pct / 100.0)
            parts.append(
                f'<rect x="{ox}" y="{bar_y}" width="{fill_w:.1f}" height="6" '
                f'fill="{OTHER_COLOR}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="0.5s" dur="0.4s" fill="freeze"/>'
                f'</rect>'
            )
            y += LINE_H
    else:
        parts.append(
            f'<text x="{ox}" y="{y}" font-size="11" fill="var(--dim)">'
            f'NO LANGUAGE DATA'
            f'</text>'
        )
        y += LINE_H

    # --- Blinking cursor ---
    parts.append(
        f'<rect x="{ox}" y="{y - 11}" width="8" height="14" fill="var(--text)" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;1;0" dur="1.2s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    # --- Bottom bar content ---
    parts.append(
        f'<text x="20" y="{H - 11}" font-size="9" fill="var(--dim)" font-weight="bold">'
        f'INDEX // FOLLOWERS_LINKED : OK'
        f'</text>'
    )
    parts.append(
        f'<text x="{W - 20}" y="{H - 11}" font-size="9" fill="var(--dim)" font-weight="bold" text-anchor="end">'
        f'GRAVITY_WELL: GITHUB.COM/MR-IR0K-OO1'
        f'</text>'
    )

    body = "\n  ".join(parts)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  {theme.css()}
  {body}
</svg>'''


def main():
    with open(os.path.join(DATA_DIR, "stats.json")) as f:
        data = json.load(f)
    svg = build_svg(data)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
