"""Define the feature components command."""

from typing import Callable
from typing import List
from typing import Tuple
from typing import cast

import click

from diogenos.feature.base import Feature
from diogenos.feature.registry import FeatureRegistry
from diogenos.system.base import SystemDetector


@click.command(name="components")
@click.argument("registry_ids", nargs=-1, required=True)
def list_feature_components(registry_ids: Tuple[str, ...]) -> None:
    """List components and their dependencies for features."""
    registry = FeatureRegistry()
    system = SystemDetector().detect()
    all_found = True

    for registry_id in registry_ids:
        try:
            feature_class = registry.get(registry_id)
        except KeyError:
            click.echo(
                f"Error: {registry_id} is not a registered feature.",
                err=True,
            )
            all_found = False
            continue

        feature_factory = cast(Callable[[], Feature], feature_class)
        selected_feature = feature_factory()

        rows: List[Tuple[str, str]] = []

        for component in selected_feature.resolved_components:
            implementation = next(
                (
                    implementation
                    for implementation in component.implementations()
                    if implementation.supports(system)
                ),
                None,
            )

            if implementation is None:
                install_methods = "Not supported"
            elif implementation.install_methods:
                install_methods = ", ".join(
                    method.value for method in implementation.install_methods
                )
            else:
                install_methods = "Not applicable"

            component_id = component.registry_id or "<unnamed>"
            rows.append((component_id, install_methods))

        component_width = max(
            [len("Component")] + [len(component_id) for component_id, _ in rows]
        )

        click.echo(f"Feature {registry_id!r}")
        click.echo()
        click.echo(f"  {'Component':<{component_width}}  Install methods")
        click.echo(f"  {'-' * component_width}  ---------------")

        for component_id, install_methods in rows:
            click.echo(f"  {component_id:<{component_width}}  {install_methods}")

        click.echo()

    if not all_found:
        raise click.exceptions.Exit(1)
