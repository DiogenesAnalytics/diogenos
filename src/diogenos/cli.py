"""Define the DiogenOS command-line interface."""

from typing import Callable
from typing import Tuple
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
@click.argument("registry_ids", nargs=-1)
@click.option(
    "--all",
    "all_features",
    is_flag=True,
    help="Check all registered features.",
)
def check_feature(
    registry_ids: Tuple[str, ...],
    all_features: bool,
) -> None:
    """Check whether features are satisfied."""
    if all_features and registry_ids:
        raise click.UsageError("Specify either --all or feature IDs, not both.")

    if not all_features and not registry_ids:
        raise click.UsageError("Specify one or more feature IDs or use --all.")

    registry = FeatureRegistry()

    if all_features:
        registry_ids = registry.list()

    system = SystemDetector().detect()
    all_satisfied = True

    for registry_id in registry_ids:
        try:
            feature_class = registry.get(registry_id)
        except KeyError:
            click.echo(
                f"Error: {registry_id} is not a registered feature.",
                err=True,
            )
            all_satisfied = False
            continue

        feature_factory = cast(Callable[[], Feature], feature_class)
        selected_feature = feature_factory()

        if selected_feature.is_satisfied(system):
            click.echo(f"Feature {registry_id!r} is satisfied.")
        else:
            click.echo(f"Feature {registry_id!r} is not satisfied.")
            all_satisfied = False

    if not all_satisfied:
        raise click.exceptions.Exit(1)


@feature.command(name="install")
@click.argument("registry_ids", nargs=-1)
@click.option(
    "--all",
    "all_features",
    is_flag=True,
    help="Install all registered features.",
)
def install_feature(
    registry_ids: Tuple[str, ...],
    all_features: bool,
) -> None:
    """Install features and their required components."""
    if all_features and registry_ids:
        raise click.UsageError("Specify either --all or feature IDs, not both.")

    if not all_features and not registry_ids:
        raise click.UsageError("Specify one or more feature IDs or use --all.")

    registry = FeatureRegistry()

    if all_features:
        registry_ids = registry.list()

    system = SystemDetector().detect()
    all_installed = True

    for registry_id in registry_ids:
        try:
            feature_class = registry.get(registry_id)
        except KeyError:
            click.echo(
                f"Error: {registry_id} is not a registered feature.",
                err=True,
            )
            all_installed = False
            continue

        feature_factory = cast(Callable[[], Feature], feature_class)
        selected_feature = feature_factory()

        try:
            selected_feature.apply(system)
        except Exception as error:
            click.echo(
                f"Error: installation of feature {registry_id!r} failed: " f"{error}",
                err=True,
            )
            all_installed = False
            continue

        click.echo(f"Feature {registry_id!r} installed successfully.")

    if not all_installed:
        raise click.exceptions.Exit(1)


if __name__ == "__main__":
    main()
