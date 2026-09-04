import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from kaleidos.config import Config, Preset, ThemeConfig
from kaleidos.engine import KaleidosEngine

@patch("kaleidos.engine.apply_display_profile")
@patch("kaleidos.engine.apply_plasma_theme")
@patch("kaleidos.engine.notify_plasma_theme_change")
def test_engine_switch_preset(mock_notify, mock_theme, mock_display, tmp_path: Path):
    dummy_profile = tmp_path / "Night.json"
    dummy_profile.write_text("{}")

    theme = ThemeConfig(
        mode="dark",
        widget_style="kvantum-dark",
        kvantum_theme="WhiteSurDark",
        aurorae_theme="__aurorae__svg__WhiteSur-dark",
        color_scheme="WhiteSurDark",
        splash_theme="com.github.vinceliuice.WhiteSur-dark"
    )
    config = Config(
        default_preset="Night",
        presets={"Night": Preset(name="Night", display_profile=str(dummy_profile), theme=theme)}
    )

    engine = KaleidosEngine(config=config)
    engine.switch_preset("Night")

    mock_theme.assert_called_once_with(theme)
    mock_display.assert_called_once_with(dummy_profile)
    mock_notify.assert_called_once()
