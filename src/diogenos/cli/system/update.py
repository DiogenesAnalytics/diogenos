"""Define the system update command."""

import click

from diogenos.system.base import SystemDetector
from diogenos.system.update import SystemUpdater


@click.command(name="update")
def update_system() -> None:
    """Update the operating system."""
    system = SystemDetector().detect()

    try:
        SystemUpdater().update(system)
    except Exception as error:
        click.echo(f"Error: system update failed: {error}", err=True)
        raise click.exceptions.Exit(1) from error

    click.echo("System update completed successfully.")
