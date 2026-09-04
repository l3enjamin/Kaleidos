import pytest
from pathlib import Path
from kaleidos.config import ThemeConfig, Preset, Config, load_config, save_config

def test_preset_model_validation():
    theme = ThemeConfig(
        mode="dark",
        widget_style="kvantum-dark",
        kvantum_theme="WhiteSurDark",
        aurorae_theme="__aurorae__svg__WhiteSur-dark",
        color_scheme="WhiteSurDark",
        splash_theme="com.github.vinceliuice.WhiteSur-dark",
        splash_engine="KSplashQML",
        plasma_style="WhiteSur-dark",
    )
    preset = Preset(
        name="Night",
        display_profile="/path/to/Night.json",
        theme=theme
    )
    assert preset.name == "Night"
    assert preset.theme.mode == "dark"
    assert preset.theme.kvantum_theme == "WhiteSurDark"

def test_load_default_config_if_missing(tmp_path: Path):
    config_file = tmp_path / "config.toml"
    assert not config_file.exists()
    
    config = load_config(config_file)
    assert config_file.exists()
    assert config.default_preset == "Day"
    assert "Day" in config.presets
    assert "Night" in config.presets
    assert config.presets["Day"].theme.mode == "light"
    assert config.presets["Night"].theme.mode == "dark"

def test_save_and_reload_config(tmp_path: Path):
    config_file = tmp_path / "config.toml"
    config = load_config(config_file)
    
    # Modify a preset
    config.presets["Gaming"] = Preset(
        name="Gaming",
        theme=ThemeConfig(
            mode="dark",
            widget_style="kvantum-dark",
            kvantum_theme="WhiteSurDark",
            aurorae_theme="__aurorae__svg__WhiteSur-dark",
            color_scheme="WhiteSurDark",
            splash_theme="com.github.vinceliuice.WhiteSur-dark"
        )
    )
    save_config(config, config_file)
    
    reloaded = load_config(config_file)
    assert "Gaming" in reloaded.presets
    assert reloaded.presets["Gaming"].theme.mode == "dark"
