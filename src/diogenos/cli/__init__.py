"""Define the DiogenOS command-line interface."""

import click

from . import feature as feature_commands
from . import system as system_commands


@click.group(no_args_is_help=True)
def main() -> None:
    """Configure and manage a DiogenOS environment."""


@main.group(no_args_is_help=True)
def feature() -> None:
    """Discover and manage features."""


@main.group(no_args_is_help=True)
def system() -> None:
    """Inspect and manage the operating system."""


feature.add_command(feature_commands.list_features)
feature.add_command(feature_commands.check_feature)
feature.add_command(feature_commands.install_feature)
feature.add_command(feature_commands.list_feature_components)

system.add_command(system_commands.show_system)
system.add_command(system_commands.update_system)
