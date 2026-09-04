import pytest
from kaleidos.config import DisplayOutputConfig, Preset, ThemeConfig
from kaleidos.display import build_kscreen_commands_from_outputs, capture_current_displays

def test_build_kscreen_commands_from_toml_outputs():
    outputs = [
        DisplayOutputConfig(
            name="eDP-1",
            enabled=True,
            primary=True,
            priority=1,
            mode="2560x1600@165",
            scale=1.25,
            hdr=False,
            position="0,0",
            rotation="normal"
        ),
        DisplayOutputConfig(
            name="DP-1",
            enabled=False
        )
    ]

    cmds = build_kscreen_commands_from_outputs(outputs)
    assert "output.eDP-1.enable" in cmds
    assert "output.DP-1.disable" in cmds
    assert "output.eDP-1.primary" in cmds
    assert "output.eDP-1.priority.1" in cmds
    assert "output.eDP-1.mode.2560x1600@165" in cmds
    assert "output.eDP-1.scale.1.25" in cmds
    assert "output.eDP-1.hdr.disable" in cmds
    assert "output.eDP-1.position.0,0" in cmds
    assert "output.eDP-1.rotation.normal" in cmds
