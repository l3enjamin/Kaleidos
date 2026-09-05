# Specification: Kaleidos Core Engine, Theming Taxonomy & Linter (MVP)

## 1. Overview
The MVP of **Kaleidos** delivers the foundational atomic environment and theme switching engine, full KDE Plasma 6 theming taxonomy, native TOML display configuration, and the strict `kaleidliner` validation tool along with a fast, deterministic CLI (`kaleidos`). It directly addresses the pain points of fragmented tools, desynchronized themes, and plasmashell crashes by providing unified, atomic writes across all relevant KDE Plasma 6 configuration files (`kwinrc`, `ksplashrc`, `kdeglobals`, `plasmarc`, `kcminputrc`, `kscreenlockerrc`, `kvantum.kvconfig`) and native execution of multi-monitor KScreen layouts via `kscreen-doctor`.

## 2. Functional Requirements
- **FR1: Unified TOML Configuration Storage & First-Class Displays**
  - Store all user presets and system configurations in `~/.config/kaleidos/config.toml`.
  - Presets define full KDE theming taxonomy:
    - `mode`: `"light"` or `"dark"`
    - `color_scheme`: KDE color scheme (e.g., `"MaterialYouDark"`, `"WhiteSurDark"`)
    - `application_style`: Qt/KDE Widget Style (e.g., `"kvantum"`, `"Breeze"`)
    - `toolbar_button_style`: e.g. `"TextUnderIcon"`
    - `kvantum_theme`: Active Kvantum style (e.g., `"WhiteSurDark"`)
    - `gtk_theme`: GTK application theme (e.g., `"Breeze"`)
    - `plasma_style`: Desktop panel/widget SVG skin (e.g., `"WhiteSur-dark"`)
    - `aurorae_theme`, `aurorae_buttons_left`, `aurorae_buttons_right`, `aurorae_border_size`: Window decoration
    - `icon_theme`, `cursor_theme`, `cursor_size`, `sound_theme`: System assets
    - `splash_theme`, `splash_engine`: Splash screen retention lock
    - `lock_screen_wallpaper`: Lock screen wallpaper plugin
    - `displays`: Inline native TOML array of output configurations (mode, scale, position, rotation, primary, HDR, VRR, brightness).
- **FR2: Atomic Multi-Config Writer**
  - Safely write configuration keys across `kwinrc`, `ksplashrc`, `kdeglobals`, `plasmarc`, `kcminputrc`, `kscreenlockerrc`, and `kvantum.kvconfig` using temporary atomic file replacement (`NamedTemporaryFile` + `replace()`) without wiping comments.
- **FR3: Native Display Layout Execution (Zero JSON Intermediates)**
  - Map TOML display attributes directly into atomic `kscreen-doctor` CLI commands without intermediary JSON files or escaping overhead.
- **FR4: System Snapshot via `kaleidos clone`**
  - Extract the live desktop state (displays, aurorae, splash, styles, colors, cursors, toolbar styles) directly into a clean, human-readable TOML preset in `config.toml`.
- **FR5: Strict Linter & Validator (`kaleidliner`)**
  - Validate syntax, preset references, and dependencies (e.g., ensuring `kvantum_theme` is provided when `application_style="kvantum"`).
  - Enforce privileged property isolation (warning that boot/login themes require root and cannot be run by unprivileged daemons).
- **FR6: CLI & Daemon Executables**
  - `kaleidos switch <preset>`: Atomically apply the full environment and reload KWin in a single pass.
  - `kaleidos list`, `kaleidos status`, `kaleidos clone <name>`: Management subcommands.
  - `kaleidliner [config_file]`: Configuration validator.
  - `kaleid`: Reserved daemon entrypoint for Track 2.

## 3. Non-Functional Requirements
- **Performance:** Execution of config writes and KWin D-Bus reload in under 250ms.
- **Robustness:** 100% test coverage for all parser, writer, linter, and CLI modules.
- **Crash Prevention:** Single-coordinator execution eliminating simultaneous multi-daemon race conditions against `plasmashell`.

## 4. Out of Scope for this Track
- Background daemon solar scheduling loop & KWin Night Light D-Bus subscriber (`kaleid`) — reserved for Track 2.
- Wallpaper-based Material You Monet color extraction — reserved for Track 3.
- Desktop Panel / Widget screen anchoring against laptop undock scrambling — reserved for Track 4.
- Native Plasma 6 QML Widget (`org.kde.kaleidos`) — reserved for Track 5.
- Home Assistant webhook client — reserved for Track 6.
