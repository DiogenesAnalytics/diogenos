"""Define the feature list command."""

import click

from diogenos.feature.registry import FeatureRegistry


@click.command(name="list")
def list_features() -> None:
    """List available features."""
    registry = FeatureRegistry()

    for registry_id in registry.list():
        click.echo(registry_id)
