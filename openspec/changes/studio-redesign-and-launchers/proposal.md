# Proposal: Studio Redesign, Multi-Platform Launchers, and Code Modularization

## Intent

Upgrade AHTube with the **Sky / Slate Studio** design system (`DESIGN_SYSTEM.md`), applying the `frontend-design` and `developing-with-streamlit` principles for a distinctive Cyber-Studio audio-workstation aesthetic. Simultaneously implement automated cross-platform startup scripts (`.bat`, `.ps1`, `.sh`) and enforce a strict codebase rule where every source file remains `<= 350 LOC`.

## Scope

### In Scope
1. **Design System & Theme Overhaul**:
   - Align `.streamlit/config.toml` and `src/config.py` with Sky/Slate Studio tokens (Dark obsidian `#020617`, surface `#0f172a`, sky blue `#38bdf8`, accent `#0ea5e9`, amber `#f59e0b`, border `#1e293b`).
   - Import typography: `Inter` (sans-serif) and `JetBrains Mono` (`tabular-nums` for timestamps, bitrates, sample rates, counters).
   - Integrate UI primitives: `.dad-micro-card`, `.dad-badge`, step progress indicators, amber guide callout boxes.
   - Refactor views (`home.py`, `image_converter.py`, `guide.py`, `terms.py`, `about.py`) and UI components (`components.py`).
2. **Cross-Platform Startup Launchers**:
   - `run.bat` (Windows Command Prompt)
   - `run.ps1` (Windows PowerShell)
   - `run.sh` (Linux / macOS / Git Bash)
   - Scripts check for git status/changes, validate Python (3.10+) and Pip, bootstrap `.venv` if missing, install `requirements.txt` if needed, and run `streamlit run app.py`.
3. **Modularization & LOC Constraints**:
   - Audit all files to verify that every file is `<= 350 lines of code`.
   - Break down oversized components or services into focused submodules if any exceed or approach 350 lines.

### Out of Scope
- Modifying core video/audio downloading mechanics (`yt-dlp` postprocessors).
- Modifying image format conversion algorithms in `image_converter.py`.

## Capabilities

### New Capabilities
- `studio-theme`: Cyber-Studio visual identity, color tokens, and typographic layout.
- `cross-platform-launchers`: Zero-friction environment bootstrap and app runners for Windows, macOS, and Linux.
- `modular-architecture`: Component-based UI and modular service boundaries ensuring `<= 350 LOC` per file.

### Modified Capabilities
- None (preserves all functional requirements and endpoints).

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `.streamlit/config.toml` | Modified | Update color palette tokens to match Slate 950 / Sky 400 |
| `src/config.py` | Modified | Update custom CSS tokens, fonts, and component classes |
| `src/ui/components.py` | Modified | Update header banner, sidebar navigation styles, preview cards |
| `src/ui/views/*.py` | Modified | Apply micro-cards, badges, step progress, and amber callouts |
| `run.bat`, `run.ps1`, `run.sh` | New | Multi-platform startup scripts |
| `tests/` | New/Modified | Verification tests for modules |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Streamlit CSS specificity overrides | Low | Use dedicated class names and clean token variables matching Streamlit 1.61 DOM structure |
| Platform differences in launcher execution | Med | Provide distinct native scripts for `cmd.exe`, PowerShell, and POSIX `sh`/`bash` with error trapping |
| File size inflation during styling | Low | Componentize UI templates into dedicated helper modules |

## Rollback Plan

Revert the git branch `feat/studio-redesign-and-launchers` or checkout the previous commit on `dev`.

## Success Criteria

- [ ] All views adhere to `DESIGN_SYSTEM.md` (colors, typography, micro-cards, badges).
- [ ] No Python or UI source file exceeds 350 lines of code.
- [ ] `run.bat`, `run.ps1`, and `run.sh` validate Python, `.venv`, requirements, and launch Streamlit seamlessly.
- [ ] Automated verification and test execution pass without regressions.
