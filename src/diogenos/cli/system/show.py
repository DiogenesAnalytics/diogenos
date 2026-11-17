"""Define the system show command."""

import click

from diogenos.system.base import SystemDetector


@click.command(name="show")
def show_system() -> None:
    """Show information about the current system."""
    system = SystemDetector().detect()

    click.echo(f"Operating System: {system.platform.pretty_name}")
    click.echo(f"Distribution:     {system.platform.os}")
    click.echo(f"Version:          {system.platform.version}")
    click.echo(f"Codename:         {system.platform.codename or 'N/A'}")
    click.echo()
    click.echo(f"Machine:          {system.hardware.machine}")
    click.echo(f"Processor:        {system.hardware.processor or 'N/A'}")
    click.echo(f"Architecture:     {system.hardware.architecture}")
    click.echo()
    click.echo(f"Desktop:          {system.desktop.pretty_name or 'N/A'}")
    click.echo(f"Identifier:       {system.desktop.name or 'N/A'}")
