# Product Definition: Kaleidos

## Overview
**Kaleidos** is a unified, atomic system environment, display profile, and dynamic theming manager designed natively for **KDE Plasma 6** on Arch Linux / CachyOS (Wayland). It eliminates the conflicts, flickering, and race conditions of fragmented desktop tools by replacing and consolidating the capabilities of **Koi** (scheduled light/dark theming), **kde-material-you-colors** (wallpaper-based Monet palette generation), and **kde-display-profiles** (KScreen multi-monitor layout switching) into a unified single source of truth.

## Core Value Proposition
- **Atomic Theme & Environment Switching:** Eliminates multi-step desktop stutter and desynchronization by performing unified writes to `kwinrc`, `ksplashrc`, `kdeglobals`, and `kvantum.kvconfig`, then triggering a single synchronized D-Bus refresh.
- **Flawless Aurorae & Kvantum Synchronization:** Directly controls KWin window decorations (`org.kde.kdecoration2`), Application widgetStyle (`widgetStyle=kvantum` / `kvantum-dark`), and active Kvantum themes without dropping state.
- **Login Animation (Splash Screen) Protection:** Explicitly preserves user-configured `ksplashrc` engines and themes across all profile transitions, preventing Plasma's global theme engine from wiping splash screens back to defaults.
- **KScreen Display Profile Integration:** Directly interfaces with `kscreen-doctor` and KScreen JSON profiles, allowing monitor configurations, refresh rates, and HDR toggles to switch seamlessly alongside themes.
- **Material You Dynamic Monet Extraction:** Inspects active wallpapers, extracts dominant tonal palettes via Google Monet algorithms, and patches Plasma color schemes without breaking underlying application styles.
- **D-Bus Event Triggering & External Synchronization:** Exposes a high-level D-Bus service (`org.kde.Kaleidos`) while actively subscribing to system signals (such as KWin Night Light state transitions, screen hotplug events, and power status) for reactive switching.
- **Smart Home Automation & Webhook Integration (Roadmap):** Features a generic webhook client / server event listener capable of querying or reacting to Home Assistant entity states (e.g., room illuminance sensors, circadian rhythm lighting, sleep/wake modes) to trigger desktop profile transitions automatically.
- **Zero-Flicker Architecture:** Decouples user-facing UI from backend scheduling via a lightweight background daemon (`kaleidosd`), an instant CLI (`kaleidos`), and a native Qt6/QML Plasma 6 applet (`org.kde.kaleidos`).

## Target Audience
- Linux desktop power users on KDE Plasma 6 / Wayland requiring multi-monitor workflow presets (e.g., Work, Gaming, Night, Battery).
- Themers and customization enthusiasts using Aurorae SVG window borders, Kvantum themes, and custom splash screens that break under stock KDE tools.
- Smart home enthusiasts who want desktop environments to harmonize seamlessly with ambient room lighting and Home Assistant automation.
