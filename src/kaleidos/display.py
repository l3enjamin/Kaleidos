from __future__ import annotations
import json
import subprocess
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

BOOL_ENABLE_MAP = {"true": "enable", "false": "disable"}
BOOL_ALLOW_MAP = {"true": "allow", "false": "disallow"}
RGB_RANGE_MAP = {
    "0": "automatic", "1": "full", "2": "limited",
    "automatic": "automatic", "full": "full", "limited": "limited"
}
ROTATION_MAP = {"1": "normal", "2": "left", "4": "inverted", "8": "right"}
VRR_POLICY_MAP = {
    "0": "never", "1": "always", "2": "automatic",
    "never": "never", "always": "always", "automatic": "automatic"
}

def get_mode_string(output: Dict[str, Any], mode_id: str) -> Optional[str]:
    for mode in output.get("modes", []):
        if str(mode.get("id")) == str(mode_id):
            width = mode["size"]["width"]
            height = mode["size"]["height"]
            refresh_rate = round(mode["refreshRate"])
            return f"{width}x{height}@{refresh_rate}"
    return None

def build_kscreen_commands(profile_data: Dict[str, Any]) -> List[str]:
    outputs = profile_data.get("outputs", [])
    commands: List[str] = []

    def add_attr(output_name: str, attribute: str, value: Any, value_map: Optional[Dict[str, str]] = None) -> None:
        if value is None or isinstance(value, (list, dict)):
            return
        str_val = str(value).lower()
        if value_map and str_val in value_map:
            value = value_map[str_val]
        commands.append(f"output.{output_name}.{attribute}.{value}")

    # 1. Handle enable/disable status first
    for out in outputs:
        status = "enable" if out.get("enabled") else "disable"
        commands.append(f"output.{out['name']}.{status}")

    # 2. Collect attributes for enabled outputs
    for out in outputs:
        if not out.get("enabled"):
            continue
        name = out["name"]
        
        # Display settings
        add_attr(name, "wcg", out.get("wcg"), BOOL_ENABLE_MAP)
        add_attr(name, "sdr-brightness", out.get("sdr-brightness"))
        add_attr(name, "vrrpolicy", out.get("vrrPolicy"), VRR_POLICY_MAP)
        add_attr(name, "rgbrange", out.get("rgbRange"), RGB_RANGE_MAP)
        add_attr(name, "overscan", out.get("overscan"))
        add_attr(name, "hdr", out.get("hdr"), BOOL_ENABLE_MAP)

        brightness = out.get("brightness")
        if brightness is not None:
            try:
                add_attr(name, "brightness", int(float(brightness) * 100))
            except (ValueError, TypeError):
                pass

        max_bpc = out.get("maxBpc")
        if max_bpc == 0:
            max_bpc = "automatic"
        add_attr(name, "maxbpc", max_bpc)

        add_attr(name, "ddcCi", out.get("ddcCiAllowed"), BOOL_ALLOW_MAP)

        # Mirroring
        rep_source = out.get("replicationSource", 0)
        if rep_source != 0:
            source_name = "none"
            for other_out in outputs:
                if other_out.get("id") == rep_source:
                    source_name = other_out["name"]
                    break
            add_attr(name, "mirror", source_name)
        else:
            add_attr(name, "mirror", "none")

        icc_path = out.get("iccProfilePath")
        if icc_path:
            add_attr(name, "iccProfilePath", icc_path)

        mode_id = out.get("currentModeId")
        if mode_id:
            mode_str = get_mode_string(out, str(mode_id))
            if mode_str:
                add_attr(name, "mode", mode_str)

        pos = out.get("pos")
        if pos:
            add_attr(name, "position", f"{pos['x']},{pos['y']}")

        add_attr(name, "scale", out.get("scale"))
        add_attr(name, "rotation", out.get("rotation"), ROTATION_MAP)

        priority = out.get("priority")
        if priority is not None:
            if priority == 1:
                commands.append(f"output.{name}.primary")
            commands.append(f"output.{name}.priority.{priority}")

    return commands

def apply_display_profile(profile_path: Path | str) -> None:
    path = Path(profile_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Display profile not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    commands = build_kscreen_commands(data)
    if not commands:
        return

    kscreen_bin = shutil.which("kscreen-doctor") or "kscreen-doctor"
    subprocess.run([kscreen_bin] + commands, check=False)
