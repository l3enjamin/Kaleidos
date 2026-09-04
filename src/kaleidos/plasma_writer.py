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

    # 1. Update kwinrc (Aurorae window decoration)
    update_ini_file(files.kwinrc, "org.kde.kdecoration2", "theme", theme.aurorae_theme)
    update_ini_file(files.kwinrc, "org.kde.kdecoration2", "library", "org.kde.kwin.aurorae")

    # 2. Update ksplashrc (Splash Screen engine and theme lock)
    update_ini_file(files.ksplashrc, "Splash", "Theme", theme.splash_theme)
    update_ini_file(files.ksplashrc, "Splash", "Engine", theme.splash_engine)

    # 3. Update kdeglobals (Color scheme & KDE widget style)
    update_ini_file(files.kdeglobals, "General", "ColorScheme", theme.color_scheme)
    update_ini_file(files.kdeglobals, "KDE", "widgetStyle", theme.widget_style)

    # 4. Update Kvantum configuration
    update_ini_file(files.kvconfig, "General", "theme", theme.kvantum_theme)
