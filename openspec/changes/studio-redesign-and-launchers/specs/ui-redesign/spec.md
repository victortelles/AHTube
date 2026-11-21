# Specification: Studio Redesign and Multi-Platform Launchers

## ADDED Requirements

### Requirement: Sky / Slate Studio Visual Identity
The application MUST apply the Sky / Slate Studio design system specification across all views and navigation elements.

#### Scenario: Dark mode color tokens applied
- **GIVEN** a user opens the web application in Streamlit
- **WHEN** the page is loaded
- **THEN** the canvas background MUST be Slate 950 (`#020617`)
- **AND** container cards MUST have Slate 900 background (`#0f172a`) and Slate 800 borders (`#1e293b`)
- **AND** primary buttons and active indicators MUST use Sky 400 (`#38bdf8`) with high-contrast text (`#020617`).

#### Scenario: Monospace typography with tabular numerals
- **GIVEN** audio/video or file metadata is displayed (durations, file sizes, bitrates, dimensions)
- **WHEN** the metadata is rendered in metrics, badges, or preview cards
- **THEN** the numbers MUST use `'JetBrains Mono', monospace` with `font-variant-numeric: tabular-nums`.

#### Scenario: Component primitives presence
- **GIVEN** any sub-view (Home, Image Converter, Guide, Terms, About)
- **WHEN** the view renders its header and sections
- **THEN** each view MUST feature a `.dad-micro-card` summary unit
- **AND** technical tags MUST use `.dad-badge` pill formatting
- **AND** actionable steps MUST feature `.dad-step-bar` progress units
- **AND** operational notes or warnings MUST use the Amber Callout styling (`#f59e0b` accent).

---

### Requirement: Cross-Platform Fast Startup Launchers
The repository MUST provide executable launch scripts for Windows, macOS, and Linux that automate environment checks and application startup.

#### Scenario: Launch on Windows via batch or powershell
- **GIVEN** a user runs `run.bat` or `run.ps1` on a Windows operating system
- **WHEN** the script executes
- **THEN** it MUST check if Python 3.10+ and `pip` are installed
- **AND** it MUST inspect git status and inform the user of uncommitted/incoming changes
- **AND** it MUST create the `.venv` virtual environment if it does not exist
- **AND** it MUST verify or install dependencies from `requirements.txt`
- **AND** it MUST start `streamlit run app.py` using the virtual environment interpreter.

#### Scenario: Launch on Unix / macOS / Linux via shell script
- **GIVEN** a user runs `./run.sh` on Linux, macOS, or Git Bash
- **WHEN** the script executes
- **THEN** it MUST validate `python3` and `pip` availability
- **AND** it MUST verify git status
- **AND** it MUST bootstrap `.venv` and install `requirements.txt` if needed
- **AND** it MUST launch Streamlit cleanly.

---

### Requirement: File Size and Modular Architecture Limit
Every source file in the project MUST respect a maximum limit of 350 lines of code.

#### Scenario: File line count audit
- **GIVEN** the codebase under `src/` and the root application entry points
- **WHEN** an automated line count audit is executed
- **THEN** every `.py` file MUST have `<= 350` lines of code
- **AND** any file exceeding 350 lines MUST be split into modular components or services.
