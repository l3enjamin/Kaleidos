from __future__ import annotations
import tomllib
from pathlib import Path
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field
import tomli_w

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "kaleidos" / "config.toml"

class ThemeConfig(BaseModel):
    mode: Literal["light", "dark"] = "dark"
    widget_style: str = "kvantum"
    kvantum_theme: str = "WhiteSur"
    aurorae_theme: str = "__aurorae__svg__WhiteSur"
    color_scheme: str = "WhiteSur"
    splash_theme: str = "com.github.vinceliuice.WhiteSur"
    splash_engine: str = "KSplashQML"
    plasma_style: Optional[str] = "WhiteSur"

class DisplayOutputConfig(BaseModel):
    name: str
    enabled: bool = True
    primary: Optional[bool] = None
    priority: Optional[int] = None
    mode: Optional[str] = None
    scale: Optional[float] = None
    position: Optional[str] = None
    rotation: Optional[str] = None
    hdr: Optional[bool] = None
    vrr: Optional[str] = None
    brightness: Optional[int] = None

class Preset(BaseModel):
    name: str
    display_profile: Optional[str] = None  # Deprecated backward-compatible fallback
    displays: List[DisplayOutputConfig] = Field(default_factory=list)
    theme: ThemeConfig

class Config(BaseModel):
    default_preset: str = "Day"
    presets: Dict[str, Preset] = Field(default_factory=dict)

def get_default_config() -> Config:
    day_theme = ThemeConfig(
        mode="light",
        widget_style="kvantum",
        kvantum_theme="WhiteSur",
        aurorae_theme="__aurorae__svg__WhiteSur",
        color_scheme="WhiteSur",
        splash_theme="com.github.vinceliuice.WhiteSur",
        splash_engine="KSplashQML",
        plasma_style="WhiteSur"
    )
    night_theme = ThemeConfig(
        mode="dark",
        widget_style="kvantum-dark",
        kvantum_theme="WhiteSurDark",
        aurorae_theme="__aurorae__svg__WhiteSur-dark",
        color_scheme="WhiteSurDark",
        splash_theme="com.github.vinceliuice.WhiteSur-dark",
        splash_engine="KSplashQML",
        plasma_style="WhiteSur-dark"
    )
    
    return Config(
        default_preset="Day",
        presets={
            "Day": Preset(name="Day", theme=day_theme),
            "Night": Preset(name="Night", theme=night_theme)
        }
    )

def load_config(path: Path = DEFAULT_CONFIG_PATH) -> Config:
    path = Path(path).expanduser()
    if not path.exists():
        cfg = get_default_config()
        save_config(cfg, path)
        return cfg
    
    with open(path, "rb") as f:
        data = tomllib.load(f)
    return Config.model_validate(data)

def save_config(config: Config, path: Path = DEFAULT_CONFIG_PATH) -> None:
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    raw_dict = config.model_dump(mode="python", exclude_none=True)
    with open(path, "wb") as f:
        tomli_w.dump(raw_dict, f)
