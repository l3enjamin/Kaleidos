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

    # 1. Colors & Application style
    color_scheme = read_ini_value(files.kdeglobals, ["General"], "ColorScheme", "WhiteSur")
    application_style = read_ini_value(files.kdeglobals, ["KDE"], "widgetStyle", "kvantum")
    toolbar_button_style = read_ini_value(files.kdeglobals, ["Toolbar style"], "ToolButtonStyle", "TextUnderIcon")
    gtk_theme = read_ini_value(files.kdeglobals, ["GTK"], "GtkTheme", "Breeze")
    icon_theme = read_ini_value(files.kdeglobals, ["Icons"], "Theme", "WhiteSurcle")
    sound_theme = read_ini_value(files.kdeglobals, ["Sounds"], "Theme", "ocean")

    # 2. Plasma Desktop Style
    plasma_style = read_ini_value(files.plasmarc, ["Theme"], "name", "WhiteSur")

    # 3. Aurorae Window decoration
    aurorae_theme = read_ini_value(files.kwinrc, ["org.kde.kdecoration2"], "theme", "__aurorae__svg__WhiteSur")
    aurorae_buttons_left = read_ini_value(files.kwinrc, ["org.kde.kdecoration2"], "ButtonsOnLeft", "SFE")
    aurorae_buttons_right = read_ini_value(files.kwinrc, ["org.kde.kdecoration2"], "ButtonsOnRight", "")
    aurorae_border_size = read_ini_value(files.kwinrc, ["org.kde.kdecoration2"], "BorderSize", "Tiny")

    # 4. Cursor Theme & Size
    cursor_theme = read_ini_value(files.kcminputrc, ["Mouse"], "cursorTheme", "WhiteSur-cursors")
    cursor_size_raw = read_ini_value(files.kcminputrc, ["Mouse"], "cursorSize", "24")
    cursor_size = int(cursor_size_raw) if cursor_size_raw.isdigit() else 24

    # 5. Splash Screen (Theme & Engine)
    splash_theme = read_ini_value(files.ksplashrc, ["Splash", "KSplash"], "Theme", "com.github.vinceliuice.WhiteSur")
    splash_engine = read_ini_value(files.ksplashrc, ["Splash", "KSplash"], "Engine", "KSplashQML")

    # 6. Lock screen wallpaper plugin
    lock_screen_wallpaper = read_ini_value(files.kscreenlockerrc, ["Greeter"], "WallpaperPlugin", "")

    # 7. Kvantum Theme
    kvantum_theme = read_ini_value(files.kvconfig, ["General"], "theme", "WhiteSur")

    # Determine mode heuristic
    is_dark = (
        "dark" in aurorae_theme.lower() or
        "dark" in color_scheme.lower() or
        "dark" in kvantum_theme.lower() or
        "dark" in application_style.lower()
    )
    mode = "dark" if is_dark else "light"

    theme = ThemeConfig(
        mode=mode,
        color_scheme=color_scheme,
        application_style=application_style,
        toolbar_button_style=toolbar_button_style,
        gtk_theme=gtk_theme,
        plasma_style=plasma_style,
        aurorae_theme=aurorae_theme,
        aurorae_buttons_left=aurorae_buttons_left,
        aurorae_buttons_right=aurorae_buttons_right,
        aurorae_border_size=aurorae_border_size,
        icon_theme=icon_theme,
        cursor_theme=cursor_theme,
        cursor_size=cursor_size,
        sound_theme=sound_theme,
        splash_theme=splash_theme,
        splash_engine=splash_engine,
        lock_screen_wallpaper=lock_screen_wallpaper or None,
        kvantum_theme=kvantum_theme
    )

    displays: List[DisplayOutputConfig] = []
    if capture_displays:
        displays = capture_current_displays()

    return Preset(
        name=name,
        displays=displays,
        theme=theme
    )
