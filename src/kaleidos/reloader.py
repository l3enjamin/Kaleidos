from __future__ import annotations
import subprocess
import shutil

def reload_kwin() -> None:
    qdbus_bin = shutil.which("qdbus6") or shutil.which("qdbus")
    if not qdbus_bin:
        return
    subprocess.run(
        [qdbus_bin, "org.kde.KWin", "/KWin", "reconfigure"],
        capture_output=True,
        text=True,
        check=False
    )

def notify_plasma_theme_change() -> None:
    reload_kwin()
