import pytest
from pathlib import Path
from kaleidos.config import Config, Preset
from kaleidos.clone import capture_current_system_preset
from kaleidos.plasma_writer import KDEConfigFiles

def test_capture_current_system_preset(tmp_path: Path):
    config_dir = tmp_path / ".config"
    kvantum_dir = config_dir / "Kvantum"
    config_dir.mkdir(parents=True)
    kvantum_dir.mkdir(parents=True)

    kwinrc = config_dir / "kwinrc"
    ksplashrc = config_dir / "ksplashrc"
    kdeglobals = config_dir / "kdeglobals"
    kvconfig = kvantum_dir / "kvantum.kvconfig"

    kwinrc.write_text("[org.kde.kdecoration2]\ntheme=__aurorae__svg__WhiteSur-dark\n")
    ksplashrc.write_text("[KSplash]\nTheme=com.github.vinceliuice.WhiteSur-alt\nEngine=KSplashQML\n")
    kdeglobals.write_text("[General]\nColorScheme=MaterialYouDark\n[KDE]\nwidgetStyle=kvantum\n")
    kvconfig.write_text("[General]\ntheme=WhiteSurDark\n")

    files = KDEConfigFiles(
        kwinrc=kwinrc,
        ksplashrc=ksplashrc,
        kdeglobals=kdeglobals,
        kvconfig=kvconfig
    )

    preset = capture_current_system_preset(
        name="ClonedSetup",
        files=files,
        capture_displays=False
    )

    assert preset.name == "ClonedSetup"
    assert preset.theme.mode == "dark"
    assert preset.theme.aurorae_theme == "__aurorae__svg__WhiteSur-dark"
    assert preset.theme.splash_theme == "com.github.vinceliuice.WhiteSur-alt"
    assert preset.theme.color_scheme == "MaterialYouDark"
    assert preset.theme.widget_style == "kvantum"
    assert preset.theme.kvantum_theme == "WhiteSurDark"
