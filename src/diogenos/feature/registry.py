"""Discover and look up features."""

from typing import Type
from typing import cast

import diogenos.feature.catalog
from diogenos.feature.base import Feature
from diogenos.registry import Registry


class FeatureRegistry(Registry):
    """Discover features and look them up by identifier."""

    def __init__(self) -> None:
        """Initialize the feature registry."""
        package = diogenos.feature.catalog

        super().__init__(
            base_class=Feature,
            package_name=package.__name__,
            package_path=package.__path__,
            item_name="feature",
        )

    def get(self, registry_id: str) -> Type[Feature]:
        """Return a feature class by identifier."""
        return cast(Type[Feature], super().get(registry_id))
