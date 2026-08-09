#!/usr/bin/env python3
"""Shared theme CSS for all profile SVGs — adapts to GitHub light/dark mode.

GitHub strips external CSS from READMEs but renders inline <style> inside
embedded SVGs, including @media (prefers-color-scheme). Defining the whole
palette as CSS custom properties lets every card flip theme automatically.

DARK matches the industrial-brutalist "tactical telemetry" palette used by
the info/workspace/heatmap cards; LIGHT is a blueprint-paper adaptation.
"""

DARK = {
    "--bg":            "#0B0C10",  # Deep space/charcoal technical background
    "--surface":       "#10131B",  # Inner card / project box fill
    "--border":        "#1F2430",  # Dark steel grid line
    "--border-bright": "#3F4D66",  # Active frame highlight
    "--text":          "#E2E8F0",  # Crisp off-white phosphor text
    "--dim":           "#5A6578",  # Blueprint slate gray for metadata
    "--red":           "#FF3E3E",  # Aviation hazard / alarm red
    "--green":         "#00FF66",  # Matrix phosphor active green
    "--blue":          "#00F0FF",  # Hyper-cyber blue/teal
    "--amber":         "#FFB700",  # Tactical warning amber
    "--yellow":        "#FFB700",  # Alias of amber
    "--mauve":         "#B388FF",  # High-altitude purple
    "--peach":         "#FF9E80",  # Sensor-range orange
    "--pink":          "#FF4081",  # Target-acquired magenta
    "--teal":          "#00F0FF",  # Alias of hyper-cyber blue
    # Tactical monochromatic green heat ramp
    "--cell-0":        "#12151D",  # Inactive deep charcoal
    "--cell-1":        "#0D3A1F",  # Low-intensity phosphor
    "--cell-2":        "#145E32",  # Medium-low intensity
    "--cell-3":        "#218C4A",  # Medium-high intensity
    "--cell-4":        "#2DBC62",  # High-intensity active
    "--cell-5":        "#00FF66",  # Maximum activity glow
}

LIGHT = {
    "--bg":            "#E8ECF1",  # Blueprint paper background
    "--surface":       "#DCE3EB",  # Inner card / project box fill
    "--border":        "#B6C0CE",  # Steel grid line
    "--border-bright": "#6B7A8F",  # Active frame highlight
    "--text":          "#171B23",  # Dark phosphor text
    "--dim":           "#5A6578",  # Blueprint slate gray for metadata
    "--red":           "#C02626",  # Alarm red
    "--green":         "#00A64E",  # Phosphor active green
    "--blue":          "#00A6C8",  # Cyber blue/teal
    "--amber":         "#A87A00",  # Tactical warning amber
    "--yellow":        "#A87A00",  # Alias of amber
    "--mauve":         "#7A4DD0",  # High-altitude purple
    "--peach":         "#C85A2E",  # Sensor-range orange
    "--pink":          "#C2276A",  # Target-acquired magenta
    "--teal":          "#00A6C8",  # Alias of cyber blue
    "--cell-0":        "#E8ECF1",  # Inactive paper
    "--cell-1":        "#B4E5C0",  # Low-intensity
    "--cell-2":        "#6CD48A",  # Medium-low intensity
    "--cell-3":        "#2DB15E",  # Medium-high intensity
    "--cell-4":        "#1E8A48",  # High-intensity
    "--cell-5":        "#00A64E",  # Maximum activity
}


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
text {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  letter-spacing: 0.02em;
}}
</style>"""
