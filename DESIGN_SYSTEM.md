# Sky / Slate Studio — Design System Specification

A modern, high-contrast, technical audio-workstation (DAW) design system built for precision tools, audio editors, and developer-grade applications. It provides full dual-mode parity (Dark Mode first, with a clean Light Mode alternative).

---

## 1. Visual Identity & Design Principles

- **Cyber-Studio Aesthetic**: Dark slate obsidian foundations paired with luminous electric cyan/sky accents (`#38bdf8`), evoking professional digital audio workstations (Ableton, FL Studio, Reaper).
- **Technical Precision**: Heavy reliance on monospaced typography (`JetBrains Mono`) with `tabular-nums` for timestamps, sample rates, frequencies, BPMs, and hashes.
- **Cognitive Clarity**: Low-noise surfaces (`#020617` and `#0f172a`) where content and waveforms take center stage.
- **High-Visibility Accents**: Semantic amber (`#f59e0b`) for user alerts, interactive step callouts, and key operational guide markers, avoiding visual clash with the primary cyan/sky blues.

---

## 2. Color Palettes & Design Tokens

### 2.1 Dark Mode (Default / Studio Theme)

| Token Name | Hex Code | Role & Description |
|---|---|---|
| `--background` | `#020617` | Slate 950 deep obsidian canvas background |
| `--foreground` | `#f8fafc` | Slate 50 high-contrast primary text |
| `--card` / `--popover` | `#0f172a` | Slate 900 surface for cards, modals, containers |
| `--card-foreground` | `#f8fafc` | High-contrast text on card surfaces |
| `--primary` | `#38bdf8` | Sky 400 electric blue for active states, main buttons, playhead |
| `--primary-foreground` | `#020617` | Deep slate text inside primary buttons |
| `--secondary` | `#1e293b` | Slate 800 subtle background for chips, inactive tabs, code |
| `--secondary-foreground` | `#f8fafc` | Text on secondary elements |
| `--muted` | `#1e293b` | Muted backgrounds and container fills |
| `--muted-foreground` | `#94a3b8` | Slate 400 captions, secondary labels, helper hints |
| `--accent` | `#0ea5e9` | Sky 500 interactive focus, hover states, waveform peaks |
| `--accent-foreground` | `#f8fafc` | Text on accent surfaces |
| `--border` / `--input` | `#1e293b` | Slate 800 borders for cards, inputs, dividers |
| `--ring` | `#38bdf8` | Focus ring glow for keyboard accessibility |
| `--sidebar` | `#0f172a` | Fixed sidebar background |
| `--sidebar-foreground` | `#94a3b8` | Sidebar navigation label color |
| `--sidebar-border` | `#1e293b` | Sidebar right border divider |

### 2.2 Light Mode (Clean Studio Alternative)

| Token Name | Hex Code | Role & Description |
|---|---|---|
| `--background` | `#f8fafc` | Slate 50 clean light canvas background |
| `--foreground` | `#0f172a` | Slate 900 crisp dark primary text |
| `--card` / `--popover` | `#ffffff` | Pure white elevated surfaces |
| `--card-foreground` | `#0f172a` | Primary text on white surfaces |
| `--primary` | `#0284c7` | Sky 600 saturated deep blue for primary actions |
| `--primary-foreground` | `#ffffff` | White text inside primary buttons |
| `--secondary` | `#e0f2fe` | Sky 100 soft tinted secondary background |
| `--secondary-foreground` | `#0369a1` | Sky 700 text on secondary chips |
| `--muted` | `#f1f5f9` | Slate 100 muted fills |
| `--muted-foreground` | `#64748b` | Slate 500 secondary captions and subtitles |
| `--accent` | `#0ea5e9` | Sky 500 interactive highlights |
| `--border` / `--input` | `#e2e8f0` | Slate 200 light borders |
| `--ring` | `#0284c7` | Sky 600 focus ring |
| `--sidebar` | `#ffffff` | Pure white sidebar background |
| `--sidebar-border` | `#e2e8f0` | Slate 200 sidebar divider |

### 2.3 Semantic & Data Visualization Colors

| Role | Hex Code | Purpose |
|---|---|---|
| **Amber Accent** | `#f59e0b` | Guide callout badges, numbered guide overlays, attention flags |
| **Success / Valid** | `#10b981` | Verified audio checks, matching checksums, active playback beats |
| **Destructive / Error**| `#ef4444` | Validation firewall rejections, delete markers, missing files |
| **Purple Accent** | `#a855f7` | Multi-tempo flag section 4 |
| **Rose Accent** | `#f43f5e` | Multi-tempo flag section 5 |

---

## 3. Typography & Iconography

### 3.1 Web Fonts Imports
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');
```

### 3.2 Font Families & Usages
- **UI & Prose (`--font-sans`)**: `Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif`
  - Body copy: `400` / `500` weight, line-height `1.5`.
  - Headings: `600` / `700` weight, letter-spacing `-0.02em`.
- **Numbers, Audio Metrics & Code (`--font-mono`)**: `'JetBrains Mono', monospace`
  - Always enforce `font-variant-numeric: tabular-nums;` to prevent layout jitter on dynamically updating counters, timestamps (`01:24.321`), or BPM values (`128.00`).
- **Icons (`Material Symbols Rounded`)**:
  - Rendered inline: `font-family: 'Material Symbols Rounded' !important;`
  - Font size default: `1.15rem` (or `14px` inside compact buttons).
  - Vertical alignment: `middle; display: inline-flex; align-items: center;`.

---

## 4. Spacing, Radii & Shadows

### 4.1 Radii System
- Large Containers & Cards: `--radius: 0.75rem` (`12px`)
- Buttons & Text Inputs: `calc(var(--radius) - 0.15rem)` (`9.6px`)
- Small Inputs / Sub-tabs: `calc(var(--radius) - 0.20rem)` (`8.8px`)
- Badges, Status Dots & Metronome Lights: `999px` (fully rounded pills/circles)

### 4.2 Elevation Shadows
```css
--shadow-2xs: 0 1px 2px 0 rgba(15, 23, 42, 0.04);
--shadow-xs:  0 1px 2px 0 rgba(15, 23, 42, 0.06);
--shadow-sm:  0 1px 3px 0 rgba(15, 23, 42, 0.10), 0 1px 2px -1px rgba(15, 23, 42, 0.08);
--shadow-md:  0 6px 12px -2px rgba(15, 23, 42, 0.14), 0 3px 6px -3px rgba(15, 23, 42, 0.10);
```

---

## 5. UI Component Primitives

### 5.1 Micro-Card (`.dad-micro-card`)
A compact header unit used at the top of wizard steps and views to summarize the module.
```html
<div class="dad-micro-card">
  <div>
    <p class="dad-micro-title">Título de la Vista</p>
    <p class="dad-micro-sub">Descripción corta de 1 línea</p>
  </div>
  <span class="dad-badge">Estado / Tag</span>
</div>
```
```css
.dad-micro-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.9rem 1.15rem;
  margin-bottom: 0.85rem;
  box-shadow: var(--shadow-xs);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}
.dad-micro-title {
  font-size: 1.02rem;
  font-weight: 700;
  color: var(--foreground);
  margin: 0 0 0.18rem 0;
}
.dad-micro-sub {
  font-size: 0.86rem;
  color: var(--muted-foreground);
  margin: 0;
}
```

### 5.2 Pill Badge (`.dad-badge`)
Compact, technical pill with monospace font.
```css
.dad-badge {
  background: var(--secondary);
  color: var(--primary);
  font-family: var(--font-mono);
  font-size: 0.76rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  border: 1px solid var(--border);
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}
```

### 5.3 Step Progress Indicator Bar (`.dad-step-bar`)
A 3-column responsive grid displaying active, completed, and pending states.
```css
.dad-step-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.1rem;
}
.dad-step-item {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.65rem 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.65rem;
  box-shadow: var(--shadow-2xs);
  transition: all 0.15s ease;
}
.dad-step-item.active {
  border-color: var(--primary);
  background: var(--secondary);
  box-shadow: var(--shadow-sm);
}
.dad-step-item.done {
  border-color: #0284c7;
  background: rgba(14, 165, 233, 0.14);
}
.dad-step-num {
  width: 1.65rem;
  height: 1.65rem;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 700;
  background: var(--muted);
  color: var(--muted-foreground);
}
.dad-step-item.active .dad-step-num {
  background: var(--primary);
  color: var(--primary-foreground);
}
.dad-step-item.done .dad-step-num {
  background: var(--accent);
  color: #ffffff;
}
.dad-step-label {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--foreground);
}
```

### 5.4 Amber Guide Callout Box
High-visibility instruction banner that avoids visual collision with cyan buttons.
```html
<div style="background:var(--secondary);border:1px solid var(--border);border-left:3px solid #f59e0b;border-radius:var(--radius);padding:0.75rem 0.95rem;margin-top:0.6rem;">
  <div style="font-weight:700;font-size:0.86rem;color:#f59e0b;margin-bottom:0.45rem;display:flex;align-items:center;gap:6px;">
    <span class="material-symbols-rounded" style="font-size:1.05rem;color:#f59e0b;">center_focus_strong</span>
    PUNTOS CLAVE DESTACADOS
  </div>
  <div style="margin:0.35rem 0;font-size:0.88rem;display:flex;align-items:flex-start;gap:8px;">
    <span style="background:#f59e0b;color:#020617;font-weight:700;font-size:0.75rem;border-radius:999px;width:1.35rem;height:1.35rem;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;">1</span>
    <span style="color:var(--foreground);">Instrucción o punto destacado.</span>
  </div>
</div>
```

---

## 6. Audio Waveform & DAW Player Styling

For audio graphs, Canvas timelines, and interactive waveform displays:

- **Canvas Background**: `#020617` (Dark) / `#f8fafc` (Light)
- **Ruler / Header Bar**: `#0f172a` (Dark) / `#f1f5f9` (Light)
- **Waveform Base (RMS envelope)**: `#38bdf8` with `0.45` fill opacity.
- **Waveform Peak / Outlines**: `#0ea5e9` with `0.8` stroke width.
- **Playhead Needle**: `#f8fafc` (1.8px width solid line) with top badge.
- **Beat Grid Ticks**:
  - Downbeats (Measure 1): `rgba(248, 250, 252, 0.26)`
  - Upbeats (Subdivisions): `rgba(56, 189, 248, 0.18)`
- **Metronome LED Visual Pulse**:
  ```css
  .metro-light {
    width: 11px;
    height: 11px;
    border-radius: 50%;
    background: #1e293b;
    border: 1px solid #94a3b8;
    transition: background-color 0.05s ease, box-shadow 0.05s ease;
  }
  .metro-light.downbeat {
    background: #38bdf8;
    box-shadow: 0 0 8px #38bdf8, 0 0 14px #0ea5e9;
  }
  .metro-light.upbeat {
    background: #0ea5e9;
    box-shadow: 0 0 6px #0ea5e9;
  }
  ```

---

## 7. Streamlit Specific Integration Snippet

To inject this theme directly into any Streamlit app (`app.py`):

```python
import streamlit as st

STUDIO_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

:root {
  --background: #020617;
  --foreground: #f8fafc;
  --card: #0f172a;
  --card-foreground: #f8fafc;
  --primary: #38bdf8;
  --primary-foreground: #020617;
  --secondary: #1e293b;
  --secondary-foreground: #f8fafc;
  --muted: #1e293b;
  --muted-foreground: #94a3b8;
  --accent: #0ea5e9;
  --border: #1e293b;
  --radius: 0.75rem;
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
  background-color: var(--background) !important;
  color: var(--foreground) !important;
  font-family: var(--font-sans) !important;
}

header[data-testid="stHeader"] {
  background-color: transparent !important;
}

[data-testid="stSidebar"] {
  background-color: var(--card) !important;
  border-right: 1px solid var(--border) !important;
}

.block-container {
  max-width: 1180px !important;
  padding-top: 3.5rem !important;
}

.stButton > button[kind="primary"] {
  background-color: var(--primary) !important;
  color: var(--primary-foreground) !important;
  border-radius: calc(var(--radius) - 0.15rem) !important;
  font-weight: 600 !important;
  border: none !important;
}

.stButton > button[kind="secondary"] {
  background-color: var(--card) !important;
  color: var(--foreground) !important;
  border: 1px solid var(--border) !important;
  border-radius: calc(var(--radius) - 0.15rem) !important;
}

code, pre, [data-testid="stMetricValue"] {
  font-family: var(--font-mono) !important;
  font-variant-numeric: tabular-nums;
}
</style>
"""

st.markdown(STUDIO_CSS, unsafe_allow_html=True)
```
