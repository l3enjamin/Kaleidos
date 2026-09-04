import pytest
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch
from kaleidos.cli import cli
from kaleidos.config import load_config

def test_cli_list_command(tmp_path: Path):
    runner = CliRunner()
    config_path = tmp_path / "config.toml"
    load_config(config_path)

    result = runner.invoke(cli, ["--config", str(config_path), "list"])
    assert result.exit_code == 0
    assert "Day" in result.output
    assert "Night" in result.output

def test_cli_status_command(tmp_path: Path):
    runner = CliRunner()
    config_path = tmp_path / "config.toml"
    load_config(config_path)

    result = runner.invoke(cli, ["--config", str(config_path), "status"])
    assert result.exit_code == 0
    assert "Default Preset:" in result.output

@patch("kaleidos.engine.KaleidosEngine.switch_preset")
def test_cli_switch_command(mock_switch, tmp_path: Path):
    runner = CliRunner()
    config_path = tmp_path / "config.toml"
    load_config(config_path)

    result = runner.invoke(cli, ["--config", str(config_path), "switch", "Day"])
    assert result.exit_code == 0
    assert "Successfully switched to preset 'Day'" in result.output
    mock_switch.assert_called_once_with("Day")

def test_cli_clone_command(tmp_path: Path):
    runner = CliRunner()
    config_path = tmp_path / "config.toml"
    load_config(config_path)

    result = runner.invoke(cli, ["--config", str(config_path), "clone", "MyCurrentSetup"])
    assert result.exit_code == 0
    assert "Successfully cloned current system setup into preset 'MyCurrentSetup'" in result.output

    # Verify saved
    cfg = load_config(config_path)
    assert "MyCurrentSetup" in cfg.presets
