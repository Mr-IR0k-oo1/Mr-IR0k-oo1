# Design System: Mr-IR0k-oo1 — GitHub Profile (Industrial-Brutalist Telemetry)
**Project ID:** n/a (GitHub profile repo). Source of truth: `scripts/theme.py`, `contrib-heatmap.svg`, `profile-stats.svg`, `info-card.svg`, `workspace-card.svg`.

## 1. Visual Theme & Atmosphere
Dense, utilitarian, "tactical telemetry." Reads like a classified systems console or declassified blueprint: a deep charcoal canvas, razor-sharp 90-degree corners, hairline steel gridlines, corner registration crosshairs, flashing status squares, uppercase bracketed labels, and monospace phosphor type. Nothing decorative — every element behaves like instrument output. Dark mode is the signature expression (deep space/charcoal `#0B0C10`); a light "blueprint paper" adaptation flips in automatically via `prefers-color-scheme`.

## 2. Color Palette & Roles
Each role lists the dark value first, light value second.

- **Deep Space Charcoal** `#0B0C10` / **Blueprint Paper** `#E8ECF1` — canvas/background of every card.
- **Inner Shroud Graphite** `#10131B` / **Fogged Steel** `#DCE3EB` — nested container fill: project rows, language-bar tracks.
- **Dark Steel Gridline** `#1F2430` / **Silver Blueprint Line** `#B6C0CE` — hairline structural dividers, borders, gridlines.
- **Brushed Steel Highlight** `#3F4D66` / **Iron Blue** `#6B7A8F` — active-frame highlight.
- **Phosphor Off-White** `#E2E8F0` / **Charcoal Ink** `#171B23` — primary text and values.
- **Blueprint Slate** `#5A6578` (both modes) — secondary metadata, labels, legend text.
- **Alarm Crimson** `#FF3E3E` / `#C02626` — hazards, warnings, status labels (`SEC_LEVEL`, `INGEST_STATE`).
- **Matrix Phosphor Green** `#00FF66` / `#00A64E` — active/success state, peak heat intensity.
- **Cyber-Cyan** `#00F0FF` / `#00A6C8` — commands, interactive prompts, links.
- **Tactical Amber** `#FFB700` / `#A87A00` — staging/pending states (`STAGED`).
- **High-Altitude Violet** `#B388FF` / `#7A4DD0` — stack/memory-style accent.
- **Sensor-Range Orange** `#FF9E80` / `#C85A2E` — hardware/CPU-style accent.
- **Target-Acquired Magenta** `#FF4081` / `#C2276A` — accent and cursor block.
- **Heat Ramp** (6 levels, dark): `#12151D → #0D3A1F → #145E32 → #218C4A → #2DBC62 → #00FF66`; light: `#E8ECF1 → #B4E5C0 → #6CD48A → #2DB15E → #1E8A48 → #00A64E` — contribution intensity 0–5.

## 3. Typography Rules
Single monospace stack: `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`; `letter-spacing: 0.02em`. Uppercase bracketed labels (`[ SESSION: ACTIVE ]`) at 9px bold; shell prompts at 11px; primary content and values at 11–13px; headers are communicated by weight (bold), never by size. No decorative type anywhere.

## 4. Component Stylings
- **Terminal window cards:** razor-sharp 90-degree corners (`rx ≈ 1px`), 1.5px steel border, flat — no shadows. 26px header bar: flashing status square, centered telemetry label, right-aligned alarm. Corner registration crosshairs. 20px inner padding.
- **Status badges:** uppercase text in `[ ... ]`, color-coded by state — green = active, amber = staged, red = alarm.
- **Project rows:** flat bordered box with vertical divider; status label left, name + description center, `[ LANG ]` badge right-aligned.
- **Stats rows:** label in blue brackets, dim `=` separator, off-white value.
- **Heatmap cells:** 13px squares, 3px gaps, razor corners, green intensity ramp, sequential cascade fade-in (0.15s per cell).
- **Language bars:** flat surface track, colored fill, right-aligned percentage; fill cascades in.
- **Cursor:** solid rectangular block blinking on/off.

## 5. Layout Principles
Strict blueprint grid — everything aligns to hairline dividers, with 26px structural bars top and bottom. Terminal logic: prompts left, telemetry centered, status right. Heatmap uses a 7-row week matrix; consistent 20px window padding; density over whitespace; information presented as instrument readouts rather than marketing copy.
