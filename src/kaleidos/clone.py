from __future__ import annotations
import re
from pathlib import Path
from typing import Optional, List
from kaleidos.config import Preset, ThemeConfig, DisplayOutputConfig
from kaleidos.plasma_writer import KDEConfigFiles
from kaleidos.display import capture_current_displays

def read_ini_value(file_path: Path, sections: list[str], key: str, default: str = "") -> str:
    p = Path(file_path).expanduser()
    if not p.exists():
        return default

    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    in_target_section = False
    section_patterns = [re.compile(rf"^\s*\[\s*{re.escape(s)}\s*\]\s*$") for s in sections]
    any_section_pattern = re.compile(r"^\s*\[.*\]\s*$")
    key_pattern = re.compile(rf"^\s*{re.escape(key)}\s*=\s*(.*)$")

    for line in lines:
        if any_section_pattern.match(line):
            in_target_section = any(sp.match(line) for sp in section_patterns)
            continue
        if in_target_section:
            m = key_pattern.match(line)
            if m:
                return m.group(1).strip()

    return default

def capture_current_system_preset(
    name: str,
    files: Optional[KDEConfigFiles] = None,
    capture_displays: bool = True
) -> Preset:
    if files is None:
        files = KDEConfigFiles()

    # 1. Window decoration (Aurorae)
    aurorae_theme = read_ini_value(files.kwinrc, ["org.kde.kdecoration2"], "theme", "__aurorae__svg__WhiteSur")

    # 2. Splash Screen (Theme & Engine)
    splash_theme = read_ini_value(files.ksplashrc, ["Splash", "KSplash"], "Theme", "com.github.vinceliuice.WhiteSur")
    splash_engine = read_ini_value(files.ksplashrc, ["Splash", "KSplash"], "Engine", "KSplashQML")

    # 3. Color scheme & Widget style
    color_scheme = read_ini_value(files.kdeglobals, ["General"], "ColorScheme", "WhiteSur")
    widget_style = read_ini_value(files.kdeglobals, ["KDE"], "widgetStyle", "kvantum")

    # 4. Kvantum Theme
    kvantum_theme = read_ini_value(files.kvconfig, ["General"], "theme", "WhiteSur")

    # Determine mode heuristic
    is_dark = (
        "dark" in aurorae_theme.lower() or
        "dark" in color_scheme.lower() or
        "dark" in kvantum_theme.lower() or
        "dark" in widget_style.lower()
    )
    mode = "dark" if is_dark else "light"

    theme = ThemeConfig(
        mode=mode,
        widget_style=widget_style,
        kvantum_theme=kvantum_theme,
        aurorae_theme=aurorae_theme,
        color_scheme=color_scheme,
        splash_theme=splash_theme,
        splash_engine=splash_engine,
        plasma_style=None
    )

    displays: List[DisplayOutputConfig] = []
    if capture_displays:
        displays = capture_current_displays()

    return Preset(
        name=name,
        displays=displays,
        theme=theme
    )
