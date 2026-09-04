# Specification: Kaleidos Core Engine & CLI (MVP)

## 1. Overview
The MVP of **Kaleidos** delivers the foundational atomic environment and theme switching engine along with a fast, deterministic CLI (`kaleidos`). It replaces the inconsistent behavior of fragmented scripts (like `koi-aurorae-day.sh`) by providing unified, atomic writes across KDE Plasma 6 configuration files (`kwinrc`, `ksplashrc`, `kdeglobals`, `kvconfig`) and seamless execution of KScreen display layouts (`kscreen-doctor`), followed by a single synchronized D-Bus refresh without desktop stutter or screen flickering.

## 2. Functional Requirements
- **FR1: Preset Schema & TOML Configuration Storage**
  - Store all user presets and system configurations in a single TOML configuration file at `~/.config/kaleidos/config.toml` (auto-generating default templates if absent).
  - Presets define:
    - `name`: Identifier (e.g., `"Day"`, `"Night"`)
    - `display`: Path to KScreen JSON profile (e.g. `~/.local/share/kde-display-profiles/Day.json`) or inline display configs.
    - `theme`:
      - `mode`: `"light"` or `"dark"`
      - `widget_style`: KDE Application style (e.g., `"kvantum"`, `"kvantum-dark"`)
      - `kvantum_theme`: Active Kvantum style name (e.g., `"WhiteSur"`, `"WhiteSurDark"`)
      - `aurorae_theme`: Aurorae window decoration (e.g., `"__aurorae__svg__WhiteSur"`, `"__aurorae__svg__WhiteSur-dark"`)
      - `color_scheme`: KDE color scheme (e.g., `"WhiteSur"`, `"WhiteSurDark"`)
      - `splash_theme`: Preserved Splash theme (e.g., `"com.github.vinceliuice.WhiteSur"`)
      - `splash_engine`: Splash engine (e.g., `"KSplashQML"`)
      - `plasma_style`: (Optional) Desktop theme name
- **FR2: Atomic Multi-Config Writer**
  - Safely write configuration keys without wiping unrelated sections or comments:
    - `kwinrc`: `[org.kde.kdecoration2] theme=<aurorae_theme>`, `library=org.kde.kwin.aurorae`
    - `ksplashrc`: `[Splash] Theme=<splash_theme>`, `Engine=<splash_engine>`
    - `kdeglobals`: `[General] ColorScheme=<color_scheme>`, `[KDE] widgetStyle=<widget_style>`
    - `~/.config/Kvantum/kvantum.kvconfig`: `[General] theme=<kvantum_theme>`
- **FR3: Display Layout Execution**
  - Load and apply display configurations via `kscreen-doctor` directly, compatible with existing `kde-display-profiles` JSON exports.
- **FR4: Coordinated Desktop Reload**
  - Trigger a single coordinated reload via D-Bus (`qdbus6 org.kde.KWin /KWin reconfigure`) so windows and decorations reload smoothly in a single pass.
- **FR5: CLI Commands**
  - `kaleidos switch <preset_name>`: Apply the specified preset atomically.
  - `kaleidos list`: List all available presets and mark the currently active preset.
  - `kaleidos status`: Inspect currently detected system theme parameters (Aurorae, Kvantum, Splash, Display).

## 3. Non-Functional Requirements
- **Performance:** Complete all file writes and D-Bus signaling in under 250ms.
- **Safety & Reversibility:** Atomic file replacements using temporary files (`replace()`) to prevent config corruption on unexpected termination.
- **Strict Validation:** Use `pydantic` v2 models for preset parsing with clear, readable validation error reporting.

## 4. Out of Scope for this Track
- Daemon background scheduling (Sunrise/Sunset cron loop) — reserved for Track 2.
- Wallpaper-based Material You Monet color extraction — reserved for Track 3.
- Native Plasma 6 QML Widget — reserved for Track 4.
- Home Assistant webhook client — reserved for Track 5.
