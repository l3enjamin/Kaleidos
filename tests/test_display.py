import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from kaleidos.display import build_kscreen_commands, apply_display_profile

SAMPLE_KSCREEN_JSON = {
    "outputs": [
        {
            "name": "eDP-1",
            "enabled": True,
            "priority": 1,
            "scale": 1.25,
            "rotation": 1,
            "pos": {"x": 0, "y": 0},
            "currentModeId": "1",
            "modes": [{"id": "1", "size": {"width": 2560, "height": 1600}, "refreshRate": 165.002}],
            "hdr": False
        },
        {
            "name": "DP-1",
            "enabled": False
        }
    ]
}

def test_build_kscreen_commands():
    cmds = build_kscreen_commands(SAMPLE_KSCREEN_JSON)
    assert "output.eDP-1.enable" in cmds
    assert "output.DP-1.disable" in cmds
    assert "output.eDP-1.primary" in cmds
    assert "output.eDP-1.priority.1" in cmds
    assert "output.eDP-1.scale.1.25" in cmds
    assert "output.eDP-1.mode.2560x1600@165" in cmds
    assert "output.eDP-1.position.0,0" in cmds
    assert "output.eDP-1.rotation.normal" in cmds
    assert "output.eDP-1.hdr.disable" in cmds

@patch("subprocess.run")
@patch("shutil.which", return_value="/usr/bin/kscreen-doctor")
def test_apply_display_profile(mock_which, mock_run, tmp_path: Path):
    profile_path = tmp_path / "Day.json"
    profile_path.write_text(json.dumps(SAMPLE_KSCREEN_JSON))

    mock_run.return_value = MagicMock(returncode=0)
    apply_display_profile(profile_path)

    assert mock_run.called
    called_args = mock_run.call_args[0][0]
    assert called_args[0] == "/usr/bin/kscreen-doctor"
    assert "output.eDP-1.enable" in called_args
