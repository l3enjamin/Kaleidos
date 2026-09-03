# Technology Stack: Kaleidos

## Backend Daemon & Core CLI (`kaleidosd` / `kaleidos`)
- **Primary Language:** Python 3.12+ (standard on CachyOS / Arch Linux)
- **Packaging & Environment:** `pyproject.toml` with `hatchling` or `flit`, managed via `uv`
- **IPC / D-Bus Service:** `dbus-fast` or `sdbus-python` (high-performance asynchronous D-Bus binding exporting `org.kde.Kaleidos`)
- **Config & Preset Validation:** `pydantic` v2 (strict JSON schema validation for Profile Presets)
- **CLI Framework:** `click` (fast, clean command-line interface)
- **Dynamic Theming / Color Extraction:** `material-color-utilities-python` / `pillow` (Google Monet algorithm implementation)
- **KDE System Tools Integration:**
  - `kscreen-doctor` for display configuration
  - `kwriteconfig6` / in-memory INI parsers (`configparser` with case preservation)
  - `qdbus6` / native D-Bus calls to `org.kde.KWin`, `org.kde.plasmashell`
- **Event Scheduling:** Solar calculations via `astral` or `SunRise` algorithm + standard async event loop (`asyncio`)

## Frontend Plasma 6 Applet (`org.kde.kaleidos`)
- **Framework:** Qt 6.7+ / KDE Frameworks 6 (KF6)
- **Languages:** QML (QtQuick 2, PlasmaComponents3, Kirigami)
- **Backend Communication:** Native Qt D-Bus declarative bindings to `org.kde.Kaleidos`

## Testing & Quality Assurance
- **Unit & Integration Testing:** `pytest`, `pytest-asyncio`
- **Linting & Formatting:** `ruff`, `mypy` (strict type annotations)
