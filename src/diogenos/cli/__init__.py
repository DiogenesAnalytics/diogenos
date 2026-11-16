"""Define the DiogenOS command-line interface."""

import click

from . import feature as feature_commands


@click.group(no_args_is_help=True)
def main() -> None:
    """Configure and manage a DiogenOS environment."""


@main.group(no_args_is_help=True)
def feature() -> None:
    """Discover and manage features."""


feature.add_command(feature_commands.list_features)
feature.add_command(feature_commands.check_feature)
feature.add_command(feature_commands.install_feature)
feature.add_command(feature_commands.list_feature_components)
