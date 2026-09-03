# Product Guidelines: Kaleidos

## Voice and Tone
- **Precision & Reliability:** System administration tools must inspire total confidence. Messages, logs, and CLI feedback should be informative, deterministic, and free of vague ambiguity.
- **KDE Human Interface Guidelines (HIG) Alignment:** Respect KDE conventions, visual hierarchy, standard icon names (from Freedesktop Icon Theme spec), and system color palettes.
- **Fail-Safe Operation:** Never leave the desktop in a broken or half-applied state. Any failure in applying a single component must roll back or log an actionable diagnostic message without crashing the desktop.

## UX Principles
1. **Zero Distraction (Silent Power):** Profile transitions occur seamlessly in the background without stealing window focus, popping up intrusive dialogs, or flashing the screen multiple times.
2. **Instant Responsiveness:** CLI actions and D-Bus commands must execute with near-zero latency (< 200ms for atomic config commit and D-Bus signal broadcast).
3. **One-Click Simplicity, Unlimited Customizability:** Basic users can select "Day" or "Night" from the Plasmoid with a single click. Power users can edit JSON presets to combine HDR modes, custom refresh rates, Aurorae themes, and external Home Assistant webhook triggers.
4. **Resilience to Desktop Crashes:** The daemon (`kaleidosd`) operates independently of `plasmashell` and `kwin`. If Plasma restarts, Kaleidos automatically resumes state without re-running heavy scripts.
