# Implementation Plan: Kaleidos Core Engine & CLI (MVP)

Follow strict Test-Driven Development (TDD: Red-Green-Refactor) for each component.

## Phase 1: Project Scaffolding & Configuration Schema
- [x] Task: Project Scaffolding
  - [x] Initialize `pyproject.toml` with `hatchling`, defining dependencies (`pydantic>=2.7`, `click>=8.1`, `tomli-w>=1.0`).
  - [x] Set up project structure: `src/kaleidos/`, `tests/`.
  - [x] Configure `pytest` and `ruff` linting configurations.
- [x] Task: TDD - TOML Configuration & Preset Models
  - [x] Write unit tests for `Preset` and `Config` models in `tests/test_config.py` (loading, parsing, default generation, validation errors).
  - [x] Implement `src/kaleidos/config.py` using `pydantic` and `tomllib` / `tomli_w`.
- [x] Task: Phase 1 Verification & Checkpoint
  - [x] Run test suite with `pytest` ensuring 100% pass rate.

## Phase 2: Atomic KDE & Plasma Configuration Writer
- [x] Task: TDD - INI / KConfig File Modifier
  - [x] Write unit tests for safe, atomic key/value manipulation preserving existing file sections and comments (`tests/test_writer.py`).
  - [x] Implement atomic file writer in `src/kaleidos/plasma_writer.py` targeting `kwinrc`, `ksplashrc`, `kdeglobals`, and `kvconfig`.
- [x] Task: TDD - Desktop Reload Coordination
  - [x] Write unit tests mocking D-Bus and process calls for desktop reloading (`tests/test_reload.py`).
  - [x] Implement reloading coordination (`src/kaleidos/reloader.py`) calling `qdbus6 org.kde.KWin /KWin reconfigure` cleanly.
- [x] Task: Phase 2 Verification & Checkpoint
  - [x] Run test suite with `pytest`.

## Phase 3: Display Profile Engine Integration
- [x] Task: TDD - KScreen Display Loader
  - [x] Write unit tests in `tests/test_display.py` verifying parsing of `kde-display-profiles` JSON structures and `kscreen-doctor` command generation.
  - [x] Implement `src/kaleidos/display.py` to execute display configuration via `kscreen-doctor`.
- [x] Task: Phase 3 Verification & Checkpoint
  - [x] Run test suite with `pytest`.

## Phase 4: CLI Application & End-to-End Core Switcher
- [x] Task: TDD - Core Orchestrator
  - [x] Write unit tests for `KaleidosEngine` in `tests/test_engine.py` verifying coordinated execution of config writes, display switches, and reloads.
  - [x] Implement `src/kaleidos/engine.py`.
- [x] Task: TDD - Click CLI Commands
  - [x] Write unit tests for CLI commands (`kaleidos switch`, `kaleidos list`, `kaleidos status`) in `tests/test_cli.py` using Click test runner.
  - [x] Implement `src/kaleidos/cli.py` with commands `switch`, `list`, `status`.
- [x] Task: Phase 4 Verification & Checkpoint
  - [x] Run full test suite and verify CLI execution against live test configurations.
