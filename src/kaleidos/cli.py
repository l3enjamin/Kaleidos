from __future__ import annotations
from pathlib import Path
import click
from kaleidos.config import load_config, save_config, DEFAULT_CONFIG_PATH
from kaleidos.engine import KaleidosEngine
from kaleidos.clone import capture_current_system_preset

@click.group()
@click.option(
    "-c", "--config", "config_path",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_CONFIG_PATH,
    help="Path to Kaleidos config.toml"
)
@click.pass_context
def cli(ctx: click.Context, config_path: Path) -> None:
    """Kaleidos: Unified atomic environment, display profile, and theme manager for KDE Plasma 6."""
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config_path

@cli.command("list")
@click.pass_context
def list_presets(ctx: click.Context) -> None:
    """List all available presets."""
    cfg = load_config(ctx.obj["config_path"])
    click.echo("Available Kaleidos Presets:")
    for name, preset in cfg.presets.items():
        prefix = "*" if name == cfg.default_preset else " "
        display_count = len(preset.displays) if preset.displays else (1 if preset.display_profile else 0)
        click.echo(f"  {prefix} {name} (Mode: {preset.theme.mode}, Kvantum: {preset.theme.kvantum_theme}, Aurorae: {preset.theme.aurorae_theme}, Displays: {display_count})")

@cli.command("status")
@click.pass_context
def show_status(ctx: click.Context) -> None:
    """Show current configuration status."""
    cfg = load_config(ctx.obj["config_path"])
    click.echo(f"Configuration File: {ctx.obj['config_path']}")
    click.echo(f"Default Preset:     {cfg.default_preset}")
    click.echo(f"Total Presets:      {len(cfg.presets)}")

@cli.command("switch")
@click.argument("preset_name")
@click.pass_context
def switch(ctx: click.Context, preset_name: str) -> None:
    """Atomically switch to the specified preset."""
    engine = KaleidosEngine(config_path=ctx.obj["config_path"])
    try:
        engine.switch_preset(preset_name)
        click.echo(f"Successfully switched to preset '{preset_name}'.")
    except Exception as e:
        raise click.ClickException(str(e))

@cli.command("clone")
@click.argument("preset_name")
@click.option(
    "--no-displays", is_flag=True, default=False,
    help="Do not capture current display layouts into the preset"
)
@click.option(
    "--set-default", is_flag=True, default=False,
    help="Set this newly cloned preset as the default preset"
)
@click.pass_context
def clone_cmd(ctx: click.Context, preset_name: str, no_displays: bool, set_default: bool) -> None:
    """Clone currently active KDE Plasma / KWin / Kvantum / Splash and display settings into a new TOML preset."""
    config_path = ctx.obj["config_path"]
    cfg = load_config(config_path)

    preset = capture_current_system_preset(
        name=preset_name,
        capture_displays=(not no_displays)
    )

    cfg.presets[preset_name] = preset
    if set_default:
        cfg.default_preset = preset_name

    save_config(cfg, config_path)
    click.echo(f"Successfully cloned current system setup into preset '{preset_name}':")
    click.echo(f"  Mode:          {preset.theme.mode}")
    click.echo(f"  Aurorae Theme: {preset.theme.aurorae_theme}")
    click.echo(f"  Splash Theme:  {preset.theme.splash_theme}")
    click.echo(f"  Widget Style:  {preset.theme.widget_style}")
    click.echo(f"  Kvantum Theme: {preset.theme.kvantum_theme}")
    click.echo(f"  Color Scheme:  {preset.theme.color_scheme}")
    click.echo(f"  Displays:      {len(preset.displays)} output(s) captured directly into TOML")
    for d in preset.displays:
        status = "enabled" if d.enabled else "disabled"
        click.echo(f"    - {d.name}: {status} (Mode: {d.mode}, Scale: {d.scale}, HDR: {d.hdr})")
    click.echo(f"\nSaved natively to {config_path}")

def main() -> None:
    cli(obj={})

if __name__ == "__main__":
    main()
