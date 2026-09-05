# Product Definition: Kaleidos

## Overview
**Kaleidos** is a unified, atomic system environment, display profile, and dynamic theming manager designed natively for **KDE Plasma 6** on Arch Linux / CachyOS (Wayland). It eliminates the conflicts, flickering, and race conditions of fragmented desktop tools by replacing and consolidating the capabilities of **Koi** (scheduled light/dark theming), **kde-material-you-colors** (wallpaper-based Monet palette generation), and **kde-display-profiles** (KScreen multi-monitor layout switching) into a unified single source of truth.

## Goal
To **atomically harmonize fragmented desktop configurations into unified, zero-flicker system presets**.

## Target Audience & User Personas

The user spectrum for Kaleidos follows a clear capability gradient:
1. **The Architect (Technically Capable)**: Deep customizer, diagnosing root causes, writing automation.
2. **The Rice Enthusiast (Ordinary Competent User)**: Visual perfectionist, comfortable with configs and curated themes.
3. **The Converted Windows Migrant (The Incapable / Baseline User)**: Lured by glorious YouTube ricing videos, easily stranded by brittle Linux theming quirks.

---

### Persona 1: The SE.RA.PH Architect (センパイ / Desktop Power Optimizer)
- **Persona:** An advanced Linux power user running a customized, performance-tuned CachyOS / KDE Plasma 6 environment (SE.RA.PH OS). Prioritizes identifying root causes and programmatic solutions over superficial band-aids.
- **Aspirations:** 
  - Seamlessly transition the desktop environment between Day, Night, Gaming, and Work workflows with a single trigger.
  - Integrate workstation states with broader ambient automations (such as Home Assistant smart room illumination).
  - Maintain a pristine, rock-solid system architecture without race conditions, crashes, or config file corruption.
- **Available Resources:**
  - Multi-monitor hardware setup (e.g., primary 4K 120Hz/HDR display, secondary rotated display, and switchable internal laptop display).
  - Custom thematic assets: Aurorae SVG window borders (WhiteSur variants), customized Kvantum styling, personalized splash screens, and video lock screen wallpapers.
  - Python 3.12+ execution runtime, `uv` packaging toolchain, and full D-Bus / KDE Frameworks 6 system interfaces.
- **Technical Capabilities:**
  - Solid command-line fluency and shell scripting experience (`kwriteconfig6`, `qdbus6`, `kscreen-doctor`).
  - Strong architectural mindset capable of diagnosing cross-process interference and identifying missing abstraction layers.
- **Decisions to be Made:**
  - When to switch environments: Automatic solar time calculation vs. reactive synchronization with KWin Night Light signals vs. Home Assistant entity triggers.
  - Scope of preset application: Full atomic refresh (theme + display profile) vs. granular partial toggles.
  - Privileged execution boundaries: Explicit user consent for system-wide elements (boot/login splash) versus unprivileged user-space daemon operations.
- **Painpoints:**
  - **Theming Desynchronization & Blind Spots:** Tools like Koi alter Kvantum and basic color schemes but ignore Aurorae window decorations, Application style dropdowns, toolbar button configurations, and custom Splash screens.
  - **Login Animation (Splash Screen) Reset Bug:** Standard Plasma Global Theme transitions frequently erase custom `ksplashrc` configurations, falling back to stock Breeze.
  - **Config Format Fragmentation & Escaping Hell:** Maintaining display layouts in separate raw JSON dumps (`kde-display-profiles`) while themes live in disparate INI files leads to nested escaping errors, missing state guarantees, and multi-step desktop screen flickering.
  - **Displaced Desktop Widgets on Display Unplug:** Unplugging external workstation monitors to carry the laptop around scrambles desktop panels and icon/widget positions across virtual screens.
  - **Login & Lock Screen Blind-Firing (No Previews):** Applying user themes to login or lock screens without pre-flight validation can silently fail to render QML elements, leaving users locked out or facing broken black screens.
  - **Tool Interference & Plasmashell Crashes:** Running independent daemons simultaneously (Koi, Material You, KScreen daemons) creates race conditions and file-write conflicts that frequently crash `plasmashell`.

---

### Persona 2: The Modern KDE Customizer & Rice Enthusiast (Ordinary Competent User)
- **Persona:** A desktop aesthetics enthusiast who loves curating polished, bespoke Plasma themes, window shadows, and adaptive color palettes.
- **Aspirations:** Have the desktop's accent and window styling adapt harmoniously to current wallpapers (Material You / Monet) while preserving customized widget borders and icons.
- **Available Resources:** Curated icon packs, wallpapers, custom Aurorae SVG skins, and Kvantum themes.
- **Technical Capabilities:** Comfortable configuring desktop settings via GUI or simple CLI commands; prefers declarative configs.
- **Decisions to be Made:** Whether color palettes should strictly reflect current wallpapers or fixed preset tones.
- **Painpoints:** Changing wallpapers or switching between dark and light themes often causes color conflicts, broken contrast in Qt applications, and unstyled titlebars.

---

### Persona 3: The Converted Windows Migrant (The Baseline / Incapable User)
- **Persona:** A newcomer who switched to Linux after watching a showcase video on YouTube featuring a stunning, customized KDE Plasma setup (e.g. "Make KDE Look Like macOS / Cyberpunk"). Expects things to "just work" like an installer wizard.
- **Aspirations:** Replicate the breathtaking visual experience seen online without needing to understand the underlying separation between KWin, Plasmashell, Kvantum, and display protocols.
- **Available Resources:** Standard single or dual-monitor laptop/desktop, stock distro repositories, and downloaded theme packages.
- **Technical Capabilities:** Minimal terminal experience; relies entirely on GUI dialogs, one-click presets, or copy-pasted CLI commands. Easily intimidated by broken configs or non-booting display modes.
- **Decisions to be Made:** Choosing pre-packaged Presets (e.g., "Day", "Night", "Vibrant") rather than manually tuning individual INI keys or display frequencies.
- **Painpoints:**
  - Downloading a global theme from KDE Store breaks their window borders or resets their widgets, leaving them stranded.
  - Switching themes leaves half the system dark and half light, leading them to believe Linux is fundamentally unstable.
  - Complete inability to recover when a theme or display setting crashes the desktop shell.

---

## Core Value Proposition
- **Atomic Theme & Environment Switching:** Eliminates multi-step desktop stutter and desynchronization by performing unified writes to `kwinrc`, `ksplashrc`, `kdeglobals`, `plasmarc`, `kcminputrc`, and `kvantum.kvconfig`, followed by a single coordinated D-Bus refresh.
- **Comprehensive Theming Taxonomy:** Unifies Color Scheme, Qt/KDE Application Style, Toolbar Button Style, GTK Theme, Plasma Desktop Style, Aurorae Window Decoration, Icon Theme, Cursor Theme & Size, Sound Theme, and Lock Screen Wallpaper in one unified schema.
- **Login Animation (Splash Screen) Protection:** Explicitly preserves and locks user-configured `ksplashrc` engines and themes across all profile transitions, preventing Plasma's global theme engine from wiping splash screens back to defaults.
- **Native TOML Display Integration:** Directly incorporates multi-monitor KScreen layouts (resolutions, refresh rates, scales, rotations, HDR toggles, primary output) as first-class TOML entries, eradicating secondary JSON files and escaping overhead.
- **Desktop Layout & Widget Anchoring (Roadmap):** Preserves applet positions and panel geometries per display configuration, preventing desktop icons and widgets from scrambling when undocking laptops.
- **Pre-Flight Preview & Validation Engine:** Validates theme QML assets and syntax before applying to prevent unrenderable login/lock screen elements from locking out users.
- **Consolidated Anti-Crash Architecture:** Replaces multiple competing background daemons with a single, synchronized coordinator (`kaleid`), completely eliminating the race conditions that crash `plasmashell`.
- **One-Command Desktop Snapshot (`kaleidos clone`):** Instantly captures the active multi-monitor layout, window decorations, cursor sizes, and styling into clean, human-readable TOML presets.
- **Strict Linting & Validation (`kaleidliner`):** Detects dependency mismatches (e.g., Kvantum widget style without matching Kvantum theme) and isolates privileged properties before applying configs.
- **D-Bus Event Triggering & External Synchronization:** Exposes a high-level D-Bus service (`org.kde.Kaleidos`) while actively subscribing to system signals (KWin Night Light, screen hotplug events) for reactive switching.
- **Platform-Agnostic Ambient Automation & Webhooks:** Features a versatile automation bridge supporting Home Assistant, Node-RED, n8n, or any REST-compatible service with dual architectures (local push server listener vs. client polling), declarative header/payload templates, and secure token retrieval via system `secret-tool`.
- **Zero-Flicker Architecture:** Decouples user-facing UI from backend scheduling via a lightweight background daemon (`kaleid`), an instant CLI (`kaleidos`), and a native Qt6/QML Plasma 6 applet (`org.kde.kaleidos`).

