"""Define the feature check command."""

from typing import Callable
from typing import List
from typing import Tuple
from typing import cast

import click

from diogenos.feature.base import Feature
from diogenos.feature.registry import FeatureRegistry
from diogenos.system.base import SystemDetector


@click.command(name="check")
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
    results: List[Tuple[str, str]] = []
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
            status = "Satisfied"
        else:
            status = "Not satisfied"
            all_satisfied = False

        results.append((registry_id, status))

    feature_width = max(
        len("Feature"),
        max((len(registry_id) for registry_id, _ in results), default=0),
    )
    status_width = max(
        len("Status"),
        max((len(status) for _, status in results), default=0),
    )

    click.echo(f"{'Feature':<{feature_width}}  Status")
    click.echo(f"{'-' * feature_width}  {'-' * status_width}")

    for registry_id, status in results:
        click.echo(f"{registry_id:<{feature_width}}  {status}")

    if not all_satisfied:
        raise click.exceptions.Exit(1)
