"""Discover and look up components."""

from typing import Type
from typing import cast

import diogenos.component.catalog
from diogenos.component.base import Component
from diogenos.registry import Registry


class ComponentRegistry(Registry):
    """Discover components and look them up by identifier."""

    def __init__(self) -> None:
        """Initialize the component registry."""
        package = diogenos.component.catalog

        super().__init__(
            base_class=Component,
            package_name=package.__name__,
            package_path=package.__path__,
            item_name="component",
        )

    def get(self, registry_id: str) -> Type[Component]:
        """Return a component class by identifier."""
        return cast(Type[Component], super().get(registry_id))
