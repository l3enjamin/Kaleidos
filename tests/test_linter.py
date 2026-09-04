import pytest
from pathlib import Path
from click.testing import CliRunner
from kaleidos.linter import lint_config_file, kaleidliner_cli
from kaleidos.config import Config, Preset, ThemeConfig, save_config

def test_linter_passes_on_valid_config(tmp_path: Path):
    cfg_file = tmp_path / "config.toml"
    theme = ThemeConfig(
        mode="dark",
        color_scheme="MaterialYouDark",
        application_style="kvantum",
        kvantum_theme="WhiteSurDark",
        aurorae_theme="__aurorae__svg__WhiteSur-dark"
    )
    cfg = Config(default_preset="Main", presets={"Main": Preset(name="Main", theme=theme)})
    save_config(cfg, cfg_file)

    issues = lint_config_file(cfg_file)
    assert len(issues) == 0

def test_linter_warns_on_privileged_properties(tmp_path: Path):
    cfg_file = tmp_path / "config.toml"
    theme = ThemeConfig(
        mode="dark",
        application_style="Breeze",
        boot_screen_theme="arch-silence",
        login_screen_theme="breeze"
    )
    cfg = Config(default_preset="Main", presets={"Main": Preset(name="Main", theme=theme)})
    save_config(cfg, cfg_file)

    issues = lint_config_file(cfg_file)
    assert any("Privileged system setting" in i.message for i in issues)

def test_kaleidliner_cli_command(tmp_path: Path):
    runner = CliRunner()
    cfg_file = tmp_path / "config.toml"
    theme = ThemeConfig(mode="light", application_style="Breeze", color_scheme="Breeze")
    cfg = Config(default_preset="Main", presets={"Main": Preset(name="Main", theme=theme)})
    save_config(cfg, cfg_file)

    result = runner.invoke(kaleidliner_cli, [str(cfg_file)])
    assert result.exit_code == 0
    assert "No errors found" in result.output
