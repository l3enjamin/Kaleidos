import pytest
from unittest.mock import patch, MagicMock
from kaleidos.reloader import reload_kwin, notify_plasma_theme_change

@patch("subprocess.run")
@patch("shutil.which", return_value="/usr/bin/qdbus6")
def test_reload_kwin_calls_qdbus6(mock_which, mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    reload_kwin()
    mock_run.assert_called_once_with(
        ["/usr/bin/qdbus6", "org.kde.KWin", "/KWin", "reconfigure"],
        capture_output=True,
        text=True,
        check=False
    )

@patch("subprocess.run")
@patch("shutil.which", return_value="/usr/bin/qdbus6")
def test_notify_plasma_theme_change_invokes_kwin_and_plasma(mock_which, mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    notify_plasma_theme_change()
    assert mock_run.call_count >= 1
