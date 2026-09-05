# Implementation Plan: Background Daemon & Solar/Night Light Scheduling (kaleid)

Follow strict Test-Driven Development (TDD: Red-Green-Refactor) for each component.

## Phase 1: Astronomical Solar Ephemeris Calculation
- [ ] Task: TDD - Solar Calculation Engine
  - [ ] Write unit tests in `tests/test_solar.py` testing sunrise/sunset times, dawn/dusk twilight offsets, and next event delta calculation against known reference coordinates.
  - [ ] Implement pure-Python solar ephemeris calculator in `src/kaleidos/solar.py`.
- [ ] Task: Phase 1 Verification & Checkpoint
  - [ ] Run `pytest tests/test_solar.py` ensuring 100% pass rate.

## Phase 2: Reactive D-Bus Night Light & Signal Listener
- [ ] Task: TDD - KWin Night Light D-Bus Monitor
  - [ ] Write unit tests in `tests/test_dbus_listener.py` mocking D-Bus signals (`org.kde.KWin.NightLight`) and testing signal callback dispatching.
  - [ ] Implement `src/kaleidos/dbus_listener.py` with asynchronous signal monitoring.
- [ ] Task: Phase 2 Verification & Checkpoint
  - [ ] Run `pytest tests/test_dbus_listener.py`.

## Phase 3: Daemon Core, Debouncing & Non-Disruptive Idempotency
- [ ] Task: TDD - Daemon Coordinator & Event Debouncer
  - [ ] Write unit tests in `tests/test_daemon.py` testing event queue debouncing, state caching, and idempotent execution (skipping unchanged presets).
  - [ ] Implement event-driven coordinator in `src/kaleidos/daemon.py` integrating solar scheduling, Night Light signals, and display hotplug debouncing.
- [ ] Task: Phase 3 Verification & Checkpoint
  - [ ] Run `pytest tests/test_daemon.py`.

## Phase 4: Systemd Service Unit & CLI Management
- [ ] Task: TDD - Service Installation & Status Management
  - [ ] Write unit tests for systemd unit file generation and CLI commands (`kaleid --status`, `kaleid --install-service`).
  - [ ] Implement service unit generator and CLI options in `src/kaleidos/daemon.py` and `src/kaleidos/cli.py`.
- [ ] Task: Phase 4 Verification & Checkpoint
  - [ ] Run full test suite with `pytest`.

## Phase 5: Verification & Real-World User Non-Disruption Testing
- [ ] Task: Integration & Live Sanity Verification
  - [ ] Verify `kaleid --foreground` starts cleanly with live desktop state.
  - [ ] Verify that switching while already on preset is truly a no-op (zero I/O, zero D-Bus reload).
  - [ ] Verify memory footprint is < 25MB RSS.
