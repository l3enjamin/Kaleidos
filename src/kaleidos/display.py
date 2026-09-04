from __future__ import annotations
import json
import subprocess
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional
from kaleidos.config import DisplayOutputConfig

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

def build_kscreen_commands_from_outputs(outputs: List[DisplayOutputConfig]) -> List[str]:
    commands: List[str] = []

    # 1. Status (enable / disable)
    for out in outputs:
        status = "enable" if out.enabled else "disable"
        commands.append(f"output.{out.name}.{status}")

    # 2. Properties for enabled outputs
    for out in outputs:
        if not out.enabled:
            continue
        name = out.name
        if out.primary:
            commands.append(f"output.{name}.primary")
        if out.priority is not None:
            commands.append(f"output.{name}.priority.{out.priority}")
        if out.mode:
            commands.append(f"output.{name}.mode.{out.mode}")
        if out.scale is not None:
            commands.append(f"output.{name}.scale.{out.scale}")
        if out.position:
            commands.append(f"output.{name}.position.{out.position}")
        if out.rotation:
            commands.append(f"output.{name}.rotation.{out.rotation}")
        if out.hdr is not None:
            hdr_str = "enable" if out.hdr else "disable"
            commands.append(f"output.{name}.hdr.{hdr_str}")
        if out.vrr:
            commands.append(f"output.{name}.vrrpolicy.{out.vrr}")
        if out.brightness is not None:
            commands.append(f"output.{name}.brightness.{out.brightness}")

    return commands

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

    for out in outputs:
        status = "enable" if out.get("enabled") else "disable"
        commands.append(f"output.{out['name']}.{status}")

    for out in outputs:
        if not out.get("enabled"):
            continue
        name = out["name"]
        
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

def capture_current_displays() -> List[DisplayOutputConfig]:
    kscreen_bin = shutil.which("kscreen-doctor") or "kscreen-doctor"
    try:
        proc = subprocess.run([kscreen_bin, "--json"], capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout)
    except Exception:
        return []

    result: List[DisplayOutputConfig] = []
    outputs = data.get("outputs", [])
    for out in outputs:
        name = out.get("name")
        if not name:
            continue
        enabled = bool(out.get("enabled", False))
        if not enabled:
            result.append(DisplayOutputConfig(name=name, enabled=False))
            continue

        priority = out.get("priority")
        primary = (priority == 1)
        scale = out.get("scale")
        hdr = out.get("hdr")

        pos = out.get("pos")
        position = f"{pos['x']},{pos['y']}" if pos else None

        rot_val = str(out.get("rotation", 1))
        rotation = ROTATION_MAP.get(rot_val, "normal")

        mode_str = None
        mode_id = out.get("currentModeId")
        if mode_id:
            mode_str = get_mode_string(out, str(mode_id))

        result.append(DisplayOutputConfig(
            name=name,
            enabled=True,
            primary=primary,
            priority=priority,
            mode=mode_str,
            scale=scale,
            position=position,
            rotation=rotation,
            hdr=hdr
        ))

    return result

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

def apply_display_outputs(outputs: List[DisplayOutputConfig]) -> None:
    if not outputs:
        return
    commands = build_kscreen_commands_from_outputs(outputs)
    if not commands:
        return
    kscreen_bin = shutil.which("kscreen-doctor") or "kscreen-doctor"
    subprocess.run([kscreen_bin] + commands, check=False)
