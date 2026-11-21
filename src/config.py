import os

# Project Information
APP_NAME = "AHTube"
APP_SUBTITLE = "Audio (MP3/WAV/M4A) & Video (MP4) Studio Workstation"
OUTPUT_DIR = "downloads"
IMAGE_OUTPUT_DIR = "converted_images"

# Supported Image Formats
SUPPORTED_IMAGE_INPUT_EXTS = (
    ".png", ".jpg", ".jpeg", ".jfif", ".heic", ".heif",
    ".webp", ".bmp", ".tiff", ".tif", ".ico", ".gif"
)
SUPPORTED_IMAGE_OUTPUT_FORMATS = ["PNG", "JPEG", "WEBP", "BMP", "TIFF", "ICO", "PDF"]

# Asset Paths
LOGO_ALPHA_PATH = os.path.join("src", "assets", "AHTyler_Logo_der.PNG")
STEP1_IMG_PATH = os.path.join("src", "assets", "step_paste_link.jpg")
STEP2_IMG_PATH = os.path.join("src", "assets", "step_select_format.jpg")
STEP3_IMG_PATH = os.path.join("src", "assets", "step_download.jpg")

# Sky / Slate Studio Design System CSS Tokens
CUSTOM_CSS = """
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
  --accent-foreground: #f8fafc;
  --border: #1e293b;
  --ring: #38bdf8;
  --sidebar: #0f172a;
  --sidebar-foreground: #94a3b8;
  --sidebar-border: #1e293b;
  --amber: #f59e0b;
  --success: #10b981;
  --destructive: #ef4444;
  --radius: 0.75rem;
  --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --shadow-2xs: 0 1px 2px 0 rgba(15, 23, 42, 0.04);
  --shadow-xs:  0 1px 2px 0 rgba(15, 23, 42, 0.06);
  --shadow-sm:  0 1px 3px 0 rgba(15, 23, 42, 0.10), 0 1px 2px -1px rgba(15, 23, 42, 0.08);
  --shadow-md:  0 6px 12px -2px rgba(15, 23, 42, 0.14), 0 3px 6px -3px rgba(15, 23, 42, 0.10);
}

html, body, [data-testid="stAppViewContainer"], .stApp {
  background-color: var(--background) !important;
  color: var(--foreground) !important;
  font-family: var(--font-sans) !important;
}

header[data-testid="stHeader"] { background-color: transparent !important; }
[data-testid="stSidebar"] {
  background-color: var(--sidebar) !important;
  border-right: 1px solid var(--sidebar-border) !important;
}
.block-container { max-width: 1180px !important; padding-top: 2rem !important; }

/* Material Symbols font binding */
.material-symbols-rounded {
  font-family: 'Material Symbols Rounded' !important;
  font-weight: normal;
  font-style: normal;
  font-size: 1.15rem;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  vertical-align: middle;
  white-space: nowrap;
}

/* Tabular Numerals & Monospace */
code, pre, [data-testid="stMetricValue"], .tabular-nums {
  font-family: var(--font-mono) !important;
  font-variant-numeric: tabular-nums !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
  background-color: var(--secondary) !important;
  color: var(--foreground) !important;
  border: 1px solid var(--border) !important;
  border-radius: calc(var(--radius) - 0.15rem) !important;
  font-family: var(--font-sans) !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25) !important;
}

/* Primary & Secondary Buttons */
.stButton > button {
  border-radius: calc(var(--radius) - 0.15rem) !important;
  font-weight: 600 !important;
  transition: all 0.15s ease !important;
}
.stButton > button[kind="primary"],
.stButton > button:not([kind="secondary"]):first-child {
  background-color: var(--primary) !important;
  color: var(--primary-foreground) !important;
  border: none !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button:not([kind="secondary"]):first-child:hover {
  background-color: var(--accent) !important;
  color: #ffffff !important;
  box-shadow: 0 0 12px rgba(56, 189, 248, 0.4) !important;
}
.stButton > button[kind="secondary"] {
  background-color: var(--card) !important;
  color: var(--foreground) !important;
  border: 1px solid var(--border) !important;
}

/* Micro-Cards (.dad-micro-card) */
.dad-micro-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.9rem 1.15rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow-xs);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}
.dad-micro-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--foreground);
  margin: 0 0 0.18rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.dad-micro-sub { font-size: 0.86rem; color: var(--muted-foreground); margin: 0; }

/* Pill Badges (.dad-badge) */
.dad-badge {
  background: var(--secondary);
  color: var(--primary);
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  font-size: 0.76rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  border: 1px solid var(--border);
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.dad-badge-audio {
  background: rgba(56, 189, 248, 0.12);
  color: var(--primary);
  border-color: rgba(56, 189, 248, 0.3);
}
.dad-badge-video {
  background: rgba(168, 85, 247, 0.12);
  color: #c084fc;
  border-color: rgba(168, 85, 247, 0.3);
}
.dad-badge-image {
  background: rgba(16, 185, 129, 0.12);
  color: #34d399;
  border-color: rgba(16, 185, 129, 0.3);
}
.dad-badge-amber {
  background: rgba(245, 158, 11, 0.14);
  color: var(--amber);
  border-color: rgba(245, 158, 11, 0.35);
}

/* Step Progress Indicator Bar (.dad-step-bar) */
.dad-step-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}
.dad-step-item {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.7rem 0.95rem;
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
  background: rgba(14, 165, 233, 0.12);
}
.dad-step-num {
  width: 1.65rem;
  height: 1.65rem;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  font-size: 0.8rem;
  font-weight: 700;
  background: var(--muted);
  color: var(--muted-foreground);
  flex-shrink: 0;
}
.dad-step-item.active .dad-step-num {
  background: var(--primary);
  color: var(--primary-foreground);
}
.dad-step-item.done .dad-step-num {
  background: var(--accent);
  color: #ffffff;
}
.dad-step-label { font-size: 0.86rem; font-weight: 600; color: var(--foreground); }

/* High-Visibility Amber Callout (.dad-callout) */
.dad-callout {
  background: var(--card);
  border: 1px solid var(--border);
  border-left: 4px solid var(--amber);
  border-radius: var(--radius);
  padding: 0.85rem 1.1rem;
  margin: 0.85rem 0;
}
.dad-callout-header {
  font-weight: 700;
  font-size: 0.88rem;
  color: var(--amber);
  margin-bottom: 0.45rem;
  display: flex;
  align-items: center;
  gap: 0.45rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.dad-callout-item {
  margin: 0.4rem 0;
  font-size: 0.88rem;
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  color: var(--foreground);
}
.dad-callout-num {
  background: var(--amber);
  color: #020617;
  font-weight: 700;
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  font-size: 0.75rem;
  border-radius: 999px;
  width: 1.35rem;
  height: 1.35rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* DAW Preview Card */
.preview-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.15rem;
  margin: 1rem 0;
  box-shadow: var(--shadow-sm);
}
.file-title {
  color: var(--foreground);
  font-size: 0.95rem;
  font-weight: 600;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.file-meta {
  color: var(--muted-foreground);
  font-size: 0.82rem;
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  margin-top: 3px;
}
.file-counter {
  color: var(--muted-foreground);
  font-size: 0.86rem;
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
}
</style>
"""
