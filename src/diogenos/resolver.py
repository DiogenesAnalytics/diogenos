"""Resolve component implementations."""

from diogenos.feature.component import Component
from diogenos.feature.component import ComponentImplementation
from diogenos.system.base import System


class Resolver:
    """Resolve component implementations."""

    def resolve(
        self,
        component: Component,
        system: System,
    ) -> ComponentImplementation:
        """Resolve an implementation for a component and system."""
        for implementation in component.implementations():
            if implementation.supports(system):
                return implementation

        raise ValueError(
            f"no implementation for component {type(component).__name__}",
        )
