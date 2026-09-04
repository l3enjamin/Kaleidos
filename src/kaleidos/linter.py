from __future__ import annotations
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal
import click
from pydantic import ValidationError
from kaleidos.config import Config

@dataclass
class LintIssue:
    severity: Literal["error", "warning", "info"]
    preset: str
    property: str
    message: str

def lint_config_file(config_path: Path | str) -> List[LintIssue]:
    path = Path(config_path).expanduser()
    if not path.exists():
        return [LintIssue("error", "*", "file", f"Configuration file not found: {path}")]

    try:
        with open(path, "rb") as f:
            raw_data = tomllib.load(f)
        cfg = Config.model_validate(raw_data)
    except ValidationError as ve:
        issues = []
        for err in ve.errors():
            loc = ".".join(str(x) for x in err["loc"])
            issues.append(LintIssue("error", loc, "validation", err["msg"]))
        return issues
    except Exception as e:
        return [LintIssue("error", "*", "syntax", f"Failed to parse TOML: {e}")]

    issues: List[LintIssue] = []

    if cfg.default_preset not in cfg.presets:
        issues.append(LintIssue(
            "error",
            cfg.default_preset,
            "default_preset",
            f"default_preset '{cfg.default_preset}' does not match any defined preset."
        ))

    for name, preset in cfg.presets.items():
        theme = preset.theme
        
        # Check privileged properties
        if theme.boot_screen_theme:
            issues.append(LintIssue(
                "warning",
                name,
                "boot_screen_theme",
                f"Privileged system setting '{theme.boot_screen_theme}' requires root/sudo and will be skipped by the unprivileged daemon 'kaleid'."
            ))
        if theme.login_screen_theme:
            issues.append(LintIssue(
                "warning",
                name,
                "login_screen_theme",
                f"Privileged system setting '{theme.login_screen_theme}' requires root/sudo and will be skipped by the unprivileged daemon 'kaleid'."
            ))

        # Check theme dependencies
        if theme.application_style and "kvantum" in theme.application_style.lower() and not theme.kvantum_theme:
            issues.append(LintIssue(
                "error",
                name,
                "kvantum_theme",
                "When application_style is set to 'kvantum', kvantum_theme cannot be empty."
            ))

    return issues

@click.command("kaleidliner")
@click.argument("config_file", type=click.Path(dir_okay=False, path_type=Path), default=Path.home() / ".config/kaleidos/config.toml")
def kaleidliner_cli(config_file: Path) -> None:
    """Kaleidliner: Strict Linter & Validator for Kaleidos configuration."""
    click.echo(f"🔍 Linting Kaleidos configuration: {config_file}")
    issues = lint_config_file(config_file)

    if not issues:
        click.secho("✨ No errors found! Configuration is valid, atomic, and safe.", fg="green")
        return

    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]

    for issue in issues:
        color = "red" if issue.severity == "error" else "yellow"
        badge = f"[{issue.severity.upper()}]"
        click.secho(f"  {badge:9} Preset '{issue.preset}' -> {issue.property}: {issue.message}", fg=color)

    click.echo()
    if errors:
        click.secho(f"❌ Found {len(errors)} error(s) and {len(warnings)} warning(s).", fg="red")
        raise click.ClickException("Linting failed. Please resolve the errors above.")
    else:
        click.secho(f"⚠️ Passed with {len(warnings)} warning(s).", fg="yellow")
