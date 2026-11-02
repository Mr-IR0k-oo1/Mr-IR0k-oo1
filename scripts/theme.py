#!/usr/bin/env python3
"""Shared theme CSS for profile SVGs — adapts to GitHub light/dark mode.

GitHub strips external CSS from READMEs but renders inline <style> inside
embedded SVGs, including @media (prefers-color-scheme). Defining the palette
as CSS custom properties lets every card follow the viewer's theme.

The palette mirrors GitHub's own UI neutrals and contribution greens so the
cards read as native to the profile page.
"""

DARK = {
    "--bg":     "#0D1117",
    "--border": "#30363D",
    "--text":   "#E6EDF3",
    "--muted":  "#8B949E",
    "--accent": "#3FB950",
    "--cell-0": "#161B22",
    "--cell-1": "#0E4429",
    "--cell-2": "#006D32",
    "--cell-3": "#26A641",
    "--cell-4": "#39D353",
}

LIGHT = {
    "--bg":     "#FFFFFF",
    "--border": "#D0D7DE",
    "--text":   "#1F2328",
    "--muted":  "#656D76",
    "--accent": "#1A7F37",
    "--cell-0": "#EBEDF0",
    "--cell-1": "#9BE9A8",
    "--cell-2": "#40C463",
    "--cell-3": "#30A14E",
    "--cell-4": "#216E39",
}

FONT = ('-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", '
        'Helvetica, Arial, sans-serif')


def css() -> str:
    def block(palette: dict[str, str]) -> str:
        return "\n".join(f"  {k}: {v};" for k, v in palette.items())

    return f"""<style>
:root {{
{block(DARK)}
}}
@media (prefers-color-scheme: light) {{
:root {{
{block(LIGHT)}
}}
}}
text {{ font-family: {FONT}; }}
</style>"""
