from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional
from kaleidos.config import ThemeConfig

@dataclass
class KDEConfigFiles:
    kwinrc: Path = Path.home() / ".config" / "kwinrc"
    ksplashrc: Path = Path.home() / ".config" / "ksplashrc"
    kdeglobals: Path = Path.home() / ".config" / "kdeglobals"
    plasmarc: Path = Path.home() / ".config" / "plasmarc"
    kcminputrc: Path = Path.home() / ".config" / "kcminputrc"
    kscreenlockerrc: Path = Path.home() / ".config" / "kscreenlockerrc"
    kvconfig: Path = Path.home() / ".config" / "Kvantum" / "kvantum.kvconfig"

def update_ini_file(file_path: Path, section: str, key: str, value: str) -> None:
    file_path = Path(file_path).expanduser()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not file_path.exists():
        lines = []
    else:
        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    
    section_pattern = re.compile(rf"^\s*\[\s*{re.escape(section)}\s*\]\s*$")
    any_section_pattern = re.compile(r"^\s*\[.*\]\s*$")
    key_pattern = re.compile(rf"^\s*{re.escape(key)}\s*=.*$")

    section_found = False
    in_section = False
    key_found = False
    new_lines = []

    for line in lines:
        if any_section_pattern.match(line):
            if in_section and not key_found:
                new_lines.append(f"{key}={value}\n")
                key_found = True
            in_section = bool(section_pattern.match(line))
            if in_section:
                section_found = True
            new_lines.append(line)
            continue

        if in_section and key_pattern.match(line):
            new_lines.append(f"{key}={value}\n")
            key_found = True
            continue

        new_lines.append(line)

    if not section_found:
        if new_lines and not new_lines[-1].endswith("\n"):
            new_lines.append("\n")
        new_lines.append(f"\n[{section}]\n")
        new_lines.append(f"{key}={value}\n")
    elif in_section and not key_found:
        new_lines.append(f"{key}={value}\n")

    # Atomic file write using NamedTemporaryFile
    with NamedTemporaryFile("w", dir=file_path.parent, delete=False, encoding="utf-8") as tf:
        tf.writelines(new_lines)
        temp_name = tf.name
    Path(temp_name).replace(file_path)

def apply_plasma_theme(theme: ThemeConfig, files: Optional[KDEConfigFiles] = None) -> None:
    if files is None:
        files = KDEConfigFiles()

    # 1. Window decoration (Aurorae)
    if theme.aurorae_theme:
        update_ini_file(files.kwinrc, "org.kde.kdecoration2", "theme", theme.aurorae_theme)
        update_ini_file(files.kwinrc, "org.kde.kdecoration2", "library", "org.kde.kwin.aurorae")
    if theme.aurorae_buttons_left is not None:
        update_ini_file(files.kwinrc, "org.kde.kdecoration2", "ButtonsOnLeft", theme.aurorae_buttons_left)
    if theme.aurorae_buttons_right is not None:
        update_ini_file(files.kwinrc, "org.kde.kdecoration2", "ButtonsOnRight", theme.aurorae_buttons_right)
    if theme.aurorae_border_size is not None:
        update_ini_file(files.kwinrc, "org.kde.kdecoration2", "BorderSize", theme.aurorae_border_size)

    # 2. Splash Screen (lock both Splash and KSplash sections)
    if theme.splash_theme:
        update_ini_file(files.ksplashrc, "Splash", "Theme", theme.splash_theme)
        update_ini_file(files.ksplashrc, "KSplash", "Theme", theme.splash_theme)
    if theme.splash_engine:
        update_ini_file(files.ksplashrc, "Splash", "Engine", theme.splash_engine)
        update_ini_file(files.ksplashrc, "KSplash", "Engine", theme.splash_engine)

    # 3. Colors & Application Style (kdeglobals)
    if theme.color_scheme:
        update_ini_file(files.kdeglobals, "General", "ColorScheme", theme.color_scheme)
    if theme.application_style:
        update_ini_file(files.kdeglobals, "KDE", "widgetStyle", theme.application_style)
    if theme.toolbar_button_style:
        update_ini_file(files.kdeglobals, "Toolbar style", "ToolButtonStyle", theme.toolbar_button_style)
    if theme.gtk_theme:
        update_ini_file(files.kdeglobals, "GTK", "GtkTheme", theme.gtk_theme)
    if theme.icon_theme:
        update_ini_file(files.kdeglobals, "Icons", "Theme", theme.icon_theme)
    if theme.sound_theme:
        update_ini_file(files.kdeglobals, "Sounds", "Theme", theme.sound_theme)

    # 4. Plasma Style (Desktop theme: Panel & Widgets)
    if theme.plasma_style:
        update_ini_file(files.plasmarc, "Theme", "name", theme.plasma_style)

    # 5. Cursor Theme & Size (kcminputrc)
    if theme.cursor_theme:
        update_ini_file(files.kcminputrc, "Mouse", "cursorTheme", theme.cursor_theme)
    if theme.cursor_size is not None:
        update_ini_file(files.kcminputrc, "Mouse", "cursorSize", str(theme.cursor_size))

    # 6. Lock screen wallpaper plugin / config
    if theme.lock_screen_wallpaper:
        update_ini_file(files.kscreenlockerrc, "Greeter", "WallpaperPlugin", theme.lock_screen_wallpaper)

    # 7. Kvantum configuration
    if theme.kvantum_theme:
        update_ini_file(files.kvconfig, "General", "theme", theme.kvantum_theme)
