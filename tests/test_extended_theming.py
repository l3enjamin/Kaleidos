import pytest
from pathlib import Path
from kaleidos.config import ThemeConfig, Preset, Config, load_config
from kaleidos.plasma_writer import KDEConfigFiles, apply_plasma_theme
from kaleidos.clone import capture_current_system_preset

def test_extended_theme_config_validation():
    theme = ThemeConfig(
        mode="dark",
        color_scheme="MaterialYouDark",
        application_style="kvantum",
        toolbar_button_style="TextUnderIcon",
        gtk_theme="Breeze",
        plasma_style="WhiteSur-alt",
        aurorae_theme="__aurorae__svg__WhiteSur-dark",
        aurorae_buttons_left="SFE",
        aurorae_buttons_right="",
        aurorae_border_size="Tiny",
        icon_theme="WhiteSurcle",
        cursor_theme="WhiteSur-cursors",
        cursor_size=36,
        sound_theme="ocean",
        splash_theme="com.github.vinceliuice.WhiteSur-alt",
        splash_engine="KSplashQML",
        lock_screen_wallpaper="luisbocanegra.smart.video.wallpaper.reborn",
        kvantum_theme="WhiteSurDark"
    )
    assert theme.mode == "dark"
    assert theme.cursor_size == 36
    assert theme.toolbar_button_style == "TextUnderIcon"

def test_kvantum_requires_kvantum_theme():
    # If application_style is kvantum, kvantum_theme cannot be empty
    with pytest.raises(ValueError, match="kvantum_theme"):
        ThemeConfig(
            mode="dark",
            application_style="kvantum",
            kvantum_theme=""
        )

def test_apply_extended_plasma_theme_writes_all_files(tmp_path: Path):
    config_dir = tmp_path / ".config"
    kvantum_dir = config_dir / "Kvantum"
    config_dir.mkdir(parents=True)
    kvantum_dir.mkdir(parents=True)

    kwinrc = config_dir / "kwinrc"
    ksplashrc = config_dir / "ksplashrc"
    kdeglobals = config_dir / "kdeglobals"
    plasmarc = config_dir / "plasmarc"
    kcminputrc = config_dir / "kcminputrc"
    kscreenlockerrc = config_dir / "kscreenlockerrc"
    kvconfig = kvantum_dir / "kvantum.kvconfig"

    files = KDEConfigFiles(
        kwinrc=kwinrc,
        ksplashrc=ksplashrc,
        kdeglobals=kdeglobals,
        plasmarc=plasmarc,
        kcminputrc=kcminputrc,
        kscreenlockerrc=kscreenlockerrc,
        kvconfig=kvconfig
    )

    theme = ThemeConfig(
        mode="dark",
        color_scheme="MaterialYouDark",
        application_style="kvantum",
        toolbar_button_style="TextUnderIcon",
        gtk_theme="Breeze",
        plasma_style="WhiteSur-alt",
        aurorae_theme="__aurorae__svg__WhiteSur-dark",
        aurorae_buttons_left="SFE",
        aurorae_buttons_right="",
        aurorae_border_size="Tiny",
        icon_theme="WhiteSurcle",
        cursor_theme="WhiteSur-cursors",
        cursor_size=36,
        sound_theme="ocean",
        splash_theme="com.github.vinceliuice.WhiteSur-alt",
        splash_engine="KSplashQML",
        lock_screen_wallpaper="luisbocanegra.smart.video.wallpaper.reborn",
        kvantum_theme="WhiteSurDark"
    )

    apply_plasma_theme(theme, files)

    assert "theme=__aurorae__svg__WhiteSur-dark" in kwinrc.read_text()
    assert "ButtonsOnLeft=SFE" in kwinrc.read_text()
    assert "BorderSize=Tiny" in kwinrc.read_text()

    assert "name=WhiteSur-alt" in plasmarc.read_text()
    assert "cursorTheme=WhiteSur-cursors" in kcminputrc.read_text()
    assert "cursorSize=36" in kcminputrc.read_text()

    assert "Theme=WhiteSurcle" in kdeglobals.read_text()
    assert "GtkTheme=Breeze" in kdeglobals.read_text()
    assert "ToolButtonStyle=TextUnderIcon" in kdeglobals.read_text()
    assert "Theme=ocean" in kdeglobals.read_text()

    assert "WallpaperPlugin=luisbocanegra.smart.video.wallpaper.reborn" in kscreenlockerrc.read_text()
