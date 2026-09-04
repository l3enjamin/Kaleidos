from __future__ import annotations
from pathlib import Path
from typing import Optional
from kaleidos.config import Config, Preset, load_config
from kaleidos.plasma_writer import apply_plasma_theme
from kaleidos.display import apply_display_profile, apply_display_outputs
from kaleidos.reloader import notify_plasma_theme_change

class KaleidosEngine:
    def __init__(self, config: Optional[Config] = None, config_path: Optional[Path] = None):
        if config is not None:
            self.config = config
        else:
            self.config = load_config(config_path) if config_path else load_config()

    def switch_preset(self, name: str) -> None:
        if name not in self.config.presets:
            raise KeyError(f"Preset '{name}' not found in configuration.")

        preset: Preset = self.config.presets[name]

        # 1. Apply Atomic Plasma & Theme configs
        apply_plasma_theme(preset.theme)

        # 2. Apply Native TOML Display configuration
        if preset.displays:
            apply_display_outputs(preset.displays)
        elif preset.display_profile:
            # Backward-compatible fallback for legacy json profiles
            p = Path(preset.display_profile).expanduser()
            if p.exists():
                apply_display_profile(p)

        # 3. Coordinated Desktop Reload (single pass)
        notify_plasma_theme_change()
