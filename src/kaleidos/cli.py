from __future__ import annotations
from pathlib import Path
import click
from kaleidos.config import load_config, DEFAULT_CONFIG_PATH
from kaleidos.engine import KaleidosEngine

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
        click.echo(f"  {prefix} {name} (Mode: {preset.theme.mode}, Kvantum: {preset.theme.kvantum_theme}, Aurorae: {preset.theme.aurorae_theme})")

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

def main() -> None:
    cli(obj={})

if __name__ == "__main__":
    main()
