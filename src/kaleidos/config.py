from __future__ import annotations
import tomllib
from pathlib import Path
from typing import Dict, List, Optional, Literal, Any
from pydantic import BaseModel, Field, model_validator
import tomli_w

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "kaleidos" / "config.toml"

class ThemeConfig(BaseModel):
    mode: Literal["light", "dark"] = "dark"
    
    # 1. Colors & Application Style (Qt/KDE)
    color_scheme: Optional[str] = None
    application_style: Optional[str] = "kvantum"
    toolbar_button_style: Optional[str] = None  # TextUnderIcon, IconOnly, TextOnly, TextBesideIcon
    kvantum_theme: Optional[str] = None
    
    # 2. GTK / GNOME Style
    gtk_theme: Optional[str] = None
    
    # 3. Plasma Desktop Style (Panel, Tray, Widgets)
    plasma_style: Optional[str] = None
    
    # 4. Aurorae Window Decoration
    aurorae_theme: Optional[str] = None
    aurorae_buttons_left: Optional[str] = None
    aurorae_buttons_right: Optional[str] = None
    aurorae_border_size: Optional[str] = None
    
    # 5. Icons, Cursors & Sounds
    icon_theme: Optional[str] = None
    cursor_theme: Optional[str] = None
    cursor_size: Optional[int] = None
    sound_theme: Optional[str] = None
    
    # 6. Splash Screen
    splash_theme: Optional[str] = None
    splash_engine: Optional[str] = "KSplashQML"
    
    # 7. Wallpaper & Lock Screen
    wallpaper: Optional[str] = None
    lock_screen_wallpaper: Optional[str] = None
    
    # 8. Privileged Settings (CLI only, requires root)
    boot_screen_theme: Optional[str] = None
    login_screen_theme: Optional[str] = None

    @property
    def widget_style(self) -> Optional[str]:
        return self.application_style

    @model_validator(mode="before")
    @classmethod
    def handle_legacy_widget_style(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "widget_style" in data and "application_style" not in data:
                data["application_style"] = data.pop("widget_style")
        return data

    @model_validator(mode="after")
    def validate_kvantum_dependency(self) -> ThemeConfig:
        if self.application_style and "kvantum" in self.application_style.lower():
            if not self.kvantum_theme:
                raise ValueError("When application_style is set to 'kvantum', kvantum_theme cannot be empty.")
        return self

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
    display_profile: Optional[str] = None  # Deprecated legacy compatibility
    displays: List[DisplayOutputConfig] = Field(default_factory=list)
    theme: ThemeConfig

class Config(BaseModel):
    default_preset: str = "Day"
    presets: Dict[str, Preset] = Field(default_factory=dict)

def get_default_config() -> Config:
    day_theme = ThemeConfig(
        mode="light",
        color_scheme="WhiteSur",
        application_style="kvantum",
        kvantum_theme="WhiteSur",
        aurorae_theme="__aurorae__svg__WhiteSur",
        aurorae_buttons_left="SFE",
        aurorae_border_size="Tiny",
        icon_theme="WhiteSurcle",
        plasma_style="WhiteSur",
        splash_theme="com.github.vinceliuice.WhiteSur",
        splash_engine="KSplashQML"
    )
    night_theme = ThemeConfig(
        mode="dark",
        color_scheme="WhiteSurDark",
        application_style="kvantum-dark",
        kvantum_theme="WhiteSurDark",
        aurorae_theme="__aurorae__svg__WhiteSur-dark",
        aurorae_buttons_left="SFE",
        aurorae_border_size="Tiny",
        icon_theme="WhiteSurcle",
        plasma_style="WhiteSur-dark",
        splash_theme="com.github.vinceliuice.WhiteSur-dark",
        splash_engine="KSplashQML"
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
