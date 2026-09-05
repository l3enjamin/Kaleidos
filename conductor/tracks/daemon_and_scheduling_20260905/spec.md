# Specification: Background Daemon & Solar/Night Light Scheduling (kaleid)

## 1. Overview
Track 2 delivers **`kaleid`**, the background scheduling and event daemon for Kaleidos designed to replace Koi without causing plasmashell crashes or disrupting the user's active workflow. The daemon runs as an unprivileged systemd user service, calculating astronomical sunrise/sunset times, listening to KWin Night Light D-Bus state changes, and reacting to display hotplug events. Crucially, the daemon prioritizes **zero disruption**: it guarantees idempotent switches, debounces transient hardware signals, and eliminates desktop flickering.

## 2. Target Personas & User Value
- **Persona 1: The SE.RA.PH Architect (センパイ):** Needs seamless, rock-solid Day/Night automation that operates silently in the background without causing plasmashell crashes or interrupting active sessions.
- **Persona 2: The Rice Enthusiast:** Expects automated visual harmony where color schemes and styles adapt seamlessly to time of day or Night Light states.

## 3. Functional Requirements

### FR1: Astronomical Solar Engine (`solar.py`)
- Calculate exact local sunrise, sunset, and twilight times given latitude, longitude, and zenith angles using pure Python algorithms (zero heavyweight external dependencies).
- Support configurable elevation/zenith angles (official sunrise/sunset, civil twilight, nautical twilight).
- Compute duration until next transition to allow precise event-driven sleeps instead of busy polling.

### FR2: KWin Night Light Reactive Listener (`dbus_listener.py`)
- Subscribe asynchronously via D-Bus (`org.freedesktop.DBus` / `qdbus6` / `sdbus` or async dbus) to KWin's Night Light status changes on `org.kde.KWin.NightLight` (e.g., `currentTemperatureChanged`, `inhibitedChanged`, or `runningChanged`).
- Trigger preset switching immediately when Night Light activates/deactivates, allowing synchronization with KDE's built-in night light schedule.

### FR3: Event-Driven Daemon Engine (`daemon.py`)
- Core asyncio event loop coordinating:
  1. Solar transition timers.
  2. D-Bus Night Light signals.
  3. Hotplug debounce queue.
- **Zero-Disruption & Idempotency Guarantee:**
  - Before applying any preset, inspect the active environment state. If the target preset is already applied, skip all configuration writes and D-Bus reloads.
  - Debounce rapid successive events (e.g., monitor plugging/unplugging triggering multiple udev/KScreen signals) with a configurable window (default 1.5s).
- Run modes:
  - `kaleid --foreground`: Run in terminal for debugging.
  - `kaleid --install-service`: Generate and enable systemd user service (`~/.config/systemd/user/kaleid.service`).
  - `kaleid --status`: Check daemon status and next scheduled transition.

### FR4: Systemd User Service Integration
- Provide clean systemd user unit definition:
  - `WantedBy=graphical-session.target`
  - `PartOf=graphical-session.target`
  - `Restart=on-failure`
  - `RestartSec=5s`
- Ensure graceful termination on `SIGTERM` / `SIGINT` without orphaned processes.

## 4. Non-Functional Requirements
- **Resource Footprint:** Resident memory under 25MB RSS when idle; negligible (<0.1%) CPU utilization between events.
- **Non-Disruption:** Transitions must never steal focus, lock the screen, or trigger multi-pass screen flickers.
- **Robustness:** If coordinates are omitted or D-Bus signals are unavailable, the daemon logs a warning and falls back gracefully to secondary schedule modes without crashing.

## 5. Deliverables & Acceptance Criteria

### Deliverables
1. `src/kaleidos/solar.py`: Pure-Python solar calculation engine.
2. `src/kaleidos/dbus_listener.py`: Async KWin Night Light D-Bus monitor.
3. `src/kaleidos/daemon.py`: Full event-driven async daemon implementation.
4. `systemd/kaleid.service`: Systemd user service unit template and install helper.
5. Unit and integration tests in `tests/test_solar.py`, `tests/test_daemon.py`, `tests/test_dbus_listener.py`.

### Acceptance Criteria
- [ ] **AC1: Accurate Astronomical Math:** `solar.py` calculates sunrise/sunset times matching NOAA standard references within +/- 2 minutes.
- [ ] **AC2: Idempotent Execution:** Switching to the currently active preset results in 0 file writes and 0 D-Bus reload invocations.
- [ ] **AC3: Night Light Reactivity:** Activating or deactivating KWin Night Light triggers immediate transition to the corresponding night/day preset.
- [ ] **AC4: Hotplug Debouncing:** Multiple rapid trigger events within 1.5 seconds collapse into a single atomic switch.
- [ ] **AC5: Low Resource Footprint:** Idle daemon consumes < 25MB RSS and < 0.1% CPU.
- [ ] **AC6: Clean Systemd Lifecycle:** `kaleid.service` starts with `graphical-session.target` and shuts down cleanly on logout.
- [ ] **AC7: Automated Test Coverage:** 100% pass rate across all solar, listener, and daemon tests.
