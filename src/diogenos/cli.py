"""Define the DiogenOS command-line interface."""

import click

from diogenos.feature.registry import FeatureRegistry


@click.group(no_args_is_help=True)
def main() -> None:
    """Configure and manage a DiogenOS environment."""


@main.group(no_args_is_help=True)
def feature() -> None:
    """Discover and manage features."""


@feature.command(name="list")
def list_features() -> None:
    """List available features."""
    registry = FeatureRegistry()

    for registry_id in registry.list():
        click.echo(registry_id)


if __name__ == "__main__":
    main()
