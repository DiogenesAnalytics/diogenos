"""Define the DiogenOS command-line interface."""

from typing import Callable
from typing import cast

import click

from diogenos.feature.base import Feature
from diogenos.feature.registry import FeatureRegistry
from diogenos.system.base import SystemDetector


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


@feature.command(name="check")
@click.argument("registry_id")
def check_feature(registry_id: str) -> None:
    """Check whether a feature is satisfied."""
    registry = FeatureRegistry()

    try:
        feature_class = registry.get(registry_id)
    except KeyError:
        click.echo(
            f"Error: {registry_id} is not a registered feature.",
            err=True,
        )
        raise click.exceptions.Exit(1) from None

    feature_factory = cast(Callable[[], Feature], feature_class)
    selected_feature = feature_factory()
    system = SystemDetector().detect()

    if selected_feature.is_satisfied(system):
        click.echo(f"Feature {registry_id!r} is satisfied.")
        return

    click.echo(f"Feature {registry_id!r} is not satisfied.")
    raise click.exceptions.Exit(1)


if __name__ == "__main__":
    main()
