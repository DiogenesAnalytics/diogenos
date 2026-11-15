"""Define the DiogenOS command-line interface."""

from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import cast

import click

from diogenos.component.implementation.method import InstallMethodType
from diogenos.feature.base import Feature
from diogenos.feature.registry import FeatureRegistry
from diogenos.system.base import System
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


def parse_component_methods(
    selections: Tuple[str, ...],
) -> Dict[str, InstallMethodType]:
    """Parse component installation method selections."""
    install_methods: Dict[str, InstallMethodType] = {}

    for selection in selections:
        component_id, separator, method_name = selection.partition("=")

        if not separator or not component_id or not method_name:
            raise click.UsageError(
                f"Invalid component selection {selection!r}. "
                "Expected COMPONENT_ID=METHOD."
            )

        if component_id in install_methods:
            raise click.UsageError(
                f"Installation method specified more than once "
                f"for component {component_id!r}."
            )

        try:
            install_methods[component_id] = InstallMethodType(method_name)
        except ValueError as error:
            available_methods = ", ".join(method.value for method in InstallMethodType)
            raise click.UsageError(
                f"Unknown installation method {method_name!r}. "
                f"Available methods: {available_methods}."
            ) from error

    return install_methods


def resolve_features(
    registry: FeatureRegistry,
    registry_ids: Tuple[str, ...],
) -> Tuple[List[Tuple[str, Optional[Feature]]], bool]:
    """Resolve the requested features."""
    selected_features: List[Tuple[str, Optional[Feature]]] = []
    all_found = True

    for registry_id in registry_ids:
        try:
            feature_class = registry.get(registry_id)
        except KeyError:
            click.echo(
                f"Error: {registry_id} is not a registered feature.",
                err=True,
            )
            selected_features.append((registry_id, None))
            all_found = False
            continue

        feature_factory = cast(Callable[[], Feature], feature_class)
        selected_features.append((registry_id, feature_factory()))

    return selected_features, all_found


def validate_component_methods(
    features: List[Feature],
    system: System,
    install_methods: Dict[str, InstallMethodType],
) -> None:
    """Validate component installation method selections."""
    components = {
        component.registry_id: component
        for selected_feature in features
        for component in selected_feature.resolved_components
    }

    for component_id, method in install_methods.items():
        component = components.get(component_id)

        if component is None:
            raise click.UsageError(
                f"Component {component_id!r} is not part of the selected features."
            )

        implementation = next(
            (
                implementation
                for implementation in component.implementations()
                if implementation.supports(system)
            ),
            None,
        )

        if implementation is None:
            raise click.UsageError(
                f"Component {component_id!r} has no implementation "
                "for the detected system."
            )

        if method not in implementation.install_methods:
            raise click.UsageError(
                f"Component {component_id!r} does not support "
                f"installation method {method.value!r}."
            )


def apply_features(
    selected_features: List[Tuple[str, Optional[Feature]]],
    system: System,
    install_methods: Dict[str, InstallMethodType],
) -> bool:
    """Apply the selected features."""
    all_installed = True

    for registry_id, selected_feature in selected_features:
        if selected_feature is None:
            continue

        try:
            if install_methods:
                selected_feature.apply(system, install_methods)
            else:
                selected_feature.apply(system)
        except Exception as error:
            click.echo(
                f"Error: installation of feature {registry_id!r} failed: {error}",
                err=True,
            )
            all_installed = False
            continue

        click.echo(f"Feature {registry_id!r} installed successfully.")

    return all_installed


@feature.command(name="install")
@click.argument("registry_ids", nargs=-1)
@click.option(
    "--all",
    "all_features",
    is_flag=True,
    help="Install all registered features.",
)
@click.option(
    "--component",
    "component_selections",
    multiple=True,
    metavar="COMPONENT_ID=METHOD",
    help="Select an installation method for a component.",
)
def install_feature(
    registry_ids: Tuple[str, ...],
    all_features: bool,
    component_selections: Tuple[str, ...],
) -> None:
    """Install features and their required components."""
    if all_features and registry_ids:
        raise click.UsageError("Specify either --all or feature IDs, not both.")

    if not all_features and not registry_ids:
        raise click.UsageError("Specify one or more feature IDs or use --all.")

    install_methods = parse_component_methods(component_selections)

    registry = FeatureRegistry()

    if all_features:
        registry_ids = registry.list()

    selected_features, all_found = resolve_features(registry, registry_ids)

    if not all_found and install_methods:
        raise click.UsageError(
            "Cannot validate component selections because a feature was not found."
        )

    system = SystemDetector().detect()

    if install_methods:
        validate_component_methods(
            [
                selected_feature
                for _, selected_feature in selected_features
                if selected_feature is not None
            ],
            system,
            install_methods,
        )

    all_installed = apply_features(selected_features, system, install_methods)

    if not all_found or not all_installed:
        raise click.exceptions.Exit(1)


@feature.command(name="components")
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


if __name__ == "__main__":
    main()
