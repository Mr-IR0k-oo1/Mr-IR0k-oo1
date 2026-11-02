# Design System: Mr-IR0k-oo1 — GitHub Profile

Source of truth: `scripts/theme.py`, `scripts/render_heatmap_svg.py`, `README.md`.

## Principles
Clean, restrained, native to GitHub. Content carries the profile; visuals support it. No animation, no simulated terminal chrome, no decorative labels.

## Palette
Mirrors GitHub's UI neutrals and contribution greens; switches with `prefers-color-scheme`.

| Token | Dark | Light | Role |
| --- | --- | --- | --- |
| `--bg` | `#0D1117` | `#FFFFFF` | Card background |
| `--border` | `#30363D` | `#D0D7DE` | Card border, dividers |
| `--text` | `#E6EDF3` | `#1F2328` | Primary text, values |
| `--muted` | `#8B949E` | `#656D76` | Labels, axes, secondary text |
| `--cell-0…4` | `#161B22 → #39D353` | `#EBEDF0 → #216E39` | Contribution intensity |

## Typography
System sans stack (`-apple-system, "Segoe UI", …`). Titles 15px/600, values 12–13px/600, labels 10–12px regular in `--muted`.

## Components
- **Card:** 880px wide, 6px radius, 1px border, 24px padding, no shadow.
- **Heatmap:** 12px cells, 3px gap, 2px radius, weekday labels Mon/Wed/Fri, month labels above, per-cell `<title>` tooltip.
- **Footer metrics:** label in muted, value in bold text; legend right-aligned.

## README Composition
Header (name, role, links) → About → Current Work (table) → Approach → Tech Stack → Activity (heatmap at `width="100%"`) → Collaboration. Plain title-case headings.
