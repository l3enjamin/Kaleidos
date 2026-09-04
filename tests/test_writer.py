import pytest
from pathlib import Path
from kaleidos.config import ThemeConfig
from kaleidos.plasma_writer import (
    update_ini_file,
    apply_plasma_theme,
    KDEConfigFiles
)

def test_update_ini_file_preserves_content_and_modifies_keys(tmp_path: Path):
    target = tmp_path / "testrc"
    target.write_text(
        "[General]\n"
        "# A comment\n"
        "ExistingKey=OriginalValue\n"
        "\n"
        "[AnotherSection]\n"
        "OtherKey=OtherVal\n"
    )

    update_ini_file(
        target,
        section="General",
        key="ExistingKey",
        value="NewValue"
    )

    update_ini_file(
        target,
        section="General",
        key="AddedKey",
        value="AddedVal"
    )

    content = target.read_text()
    assert "ExistingKey=NewValue" in content
    assert "AddedKey=AddedVal" in content
    assert "[AnotherSection]" in content
    assert "OtherKey=OtherVal" in content
    assert "# A comment" in content

def test_apply_plasma_theme_updates_all_target_configs(tmp_path: Path):
    config_dir = tmp_path / ".config"
    kvantum_dir = config_dir / "Kvantum"
    config_dir.mkdir(parents=True)
    kvantum_dir.mkdir(parents=True)

    kwinrc = config_dir / "kwinrc"
    ksplashrc = config_dir / "ksplashrc"
    kdeglobals = config_dir / "kdeglobals"
    kvconfig = kvantum_dir / "kvantum.kvconfig"

    # Pre-populate with existing sections
    kwinrc.write_text("[org.kde.kdecoration2]\nButtonsOnLeft=XAI\ntheme=old\n")
    ksplashrc.write_text("[Splash]\nEngine=oldEngine\nTheme=oldTheme\n")
    kdeglobals.write_text("[General]\nColorScheme=OldColor\n[KDE]\nwidgetStyle=oldStyle\n")
    kvconfig.write_text("[General]\ntheme=OldKvantum\n")

    files = KDEConfigFiles(
        kwinrc=kwinrc,
        ksplashrc=ksplashrc,
        kdeglobals=kdeglobals,
        kvconfig=kvconfig
    )

    theme = ThemeConfig(
        mode="dark",
        widget_style="kvantum-dark",
        kvantum_theme="WhiteSurDark",
        aurorae_theme="__aurorae__svg__WhiteSur-dark",
        color_scheme="WhiteSurDark",
        splash_theme="com.github.vinceliuice.WhiteSur-dark",
        splash_engine="KSplashQML",
        plasma_style="WhiteSur-dark"
    )

    apply_plasma_theme(theme, files)

    # Verify atomic updates
    assert "theme=__aurorae__svg__WhiteSur-dark" in kwinrc.read_text()
    assert "ButtonsOnLeft=XAI" in kwinrc.read_text()
    assert "library=org.kde.kwin.aurorae" in kwinrc.read_text()

    assert "Theme=com.github.vinceliuice.WhiteSur-dark" in ksplashrc.read_text()
    assert "Engine=KSplashQML" in ksplashrc.read_text()

    assert "ColorScheme=WhiteSurDark" in kdeglobals.read_text()
    assert "widgetStyle=kvantum-dark" in kdeglobals.read_text()

    assert "theme=WhiteSurDark" in kvconfig.read_text()
