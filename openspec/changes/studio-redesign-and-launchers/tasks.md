# Tasks: Studio Redesign, Multi-Platform Launchers, and Code Modularization

## Phase 1: Design Tokens & UI Primitives Setup
- [ ] 1.1 Update `.streamlit/config.toml` with the Sky / Slate Studio palette (`#020617` background, `#0f172a` card/surface, `#38bdf8` primary accent, `#1e293b` borders).
- [ ] 1.2 Update `src/config.py` with the complete CSS token system from `DESIGN_SYSTEM.md`, including Google Fonts (`Inter`, `JetBrains Mono`, `Material Symbols Rounded`), monospace tabular numerals, and responsive studio classes.
- [ ] 1.3 Create `src/ui/primitives.py` providing reusable Python renderers for `.dad-micro-card`, `.dad-badge`, `.dad-step-bar`, and amber callout banners (`#f59e0b`).

## Phase 2: UI Views & Components Redesign
- [ ] 2.1 Refactor `src/ui/components.py` to use studio branding, styled sidebar navigation with electric sky highlights, and DAW-styled preview cards.
- [ ] 2.2 Update `src/ui/views/home.py` with micro-card header, extraction method selector, and studio-themed downloads gallery.
- [ ] 2.3 Update `src/ui/views/image_converter.py` with micro-card summary, format pill badges, and converted gallery cards.
- [ ] 2.4 Update `src/ui/views/guide.py` using step progress indicator and high-visibility amber callout boxes.
- [ ] 2.5 Update `src/ui/views/terms.py` and `src/ui/views/about.py` aligning with technical audio workstation styling and legal disclaimers.

## Phase 3: Multi-Platform Startup Launchers
- [ ] 3.1 Create `run.bat` for Windows CMD (git change check, python 3.10+ validation, `.venv` bootstrap, `requirements.txt` check, and `streamlit run app.py`).
- [ ] 3.2 Create `run.ps1` for Windows PowerShell (ansi-colored status indicators, git check, virtual environment check, automated package installation, app launch).
- [ ] 3.3 Create `run.sh` for Linux, macOS, and Git Bash (POSIX shell script, git status check, python3 detection, venv activation/creation, dependency sync, app launch).

## Phase 4: Modularization, Line-Budget Audit & Testing
- [ ] 4.1 Perform an automated lines-of-code audit ensuring all source files are strictly `<= 350 LOC`.
- [ ] 4.2 Add unit test coverage in `tests/test_services.py` for extractor, converter, and explorer to fulfill TDD verification.
- [ ] 4.3 Verify execution with python compilation and `unittest discover`.
