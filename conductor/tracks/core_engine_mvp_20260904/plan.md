# Implementation Plan: Kaleidos Core Engine & CLI (MVP)

Follow strict Test-Driven Development (TDD: Red-Green-Refactor) for each component.

## Phase 1: Project Scaffolding & Configuration Schema
- [ ] Task: Project Scaffolding
  - [ ] Initialize `pyproject.toml` with `hatchling`, defining dependencies (`pydantic>=2.7`, `click>=8.1`, `tomli-w>=1.0`).
  - [ ] Set up project structure: `src/kaleidos/`, `tests/`.
  - [ ] Configure `pytest` and `ruff` linting configurations.
- [ ] Task: TDD - TOML Configuration & Preset Models
  - [ ] Write unit tests for `Preset` and `Config` models in `tests/test_config.py` (loading, parsing, default generation, validation errors).
  - [ ] Implement `src/kaleidos/config.py` using `pydantic` and `tomllib` / `tomli_w`.
- [ ] Task: Phase 1 Verification & Checkpoint
  - [ ] Run test suite with `pytest` ensuring 100% pass rate.

## Phase 2: Atomic KDE & Plasma Configuration Writer
- [ ] Task: TDD - INI / KConfig File Modifier
  - [ ] Write unit tests for safe, atomic key/value manipulation preserving existing file sections and comments (`tests/test_writer.py`).
  - [ ] Implement atomic file writer in `src/kaleidos/plasma_writer.py` targeting `kwinrc`, `ksplashrc`, `kdeglobals`, and `kvconfig`.
- [ ] Task: TDD - Desktop Reload Coordination
  - [ ] Write unit tests mocking D-Bus and process calls for desktop reloading (`tests/test_reload.py`).
  - [ ] Implement reloading coordination (`src/kaleidos/reloader.py`) calling `qdbus6 org.kde.KWin /KWin reconfigure` cleanly.
- [ ] Task: Phase 2 Verification & Checkpoint
  - [ ] Run test suite with `pytest`.

## Phase 3: Display Profile Engine Integration
- [ ] Task: TDD - KScreen Display Loader
  - [ ] Write unit tests in `tests/test_display.py` verifying parsing of `kde-display-profiles` JSON structures and `kscreen-doctor` command generation.
  - [ ] Implement `src/kaleidos/display.py` to execute display configuration via `kscreen-doctor`.
- [ ] Task: Phase 3 Verification & Checkpoint
  - [ ] Run test suite with `pytest`.

## Phase 4: CLI Application & End-to-End Core Switcher
- [ ] Task: TDD - Core Orchestrator
  - [ ] Write unit tests for `KaleidosEngine` in `tests/test_engine.py` verifying coordinated execution of config writes, display switches, and reloads.
  - [ ] Implement `src/kaleidos/engine.py`.
- [ ] Task: TDD - Click CLI Commands
  - [ ] Write unit tests for CLI commands (`kaleidos switch`, `kaleidos list`, `kaleidos status`) in `tests/test_cli.py` using Click test runner.
  - [ ] Implement `src/kaleidos/cli.py` with commands `switch`, `list`, `status`.
- [ ] Task: Phase 4 Verification & Checkpoint
  - [ ] Run full test suite and verify CLI execution against live test configurations.
