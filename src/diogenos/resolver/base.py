"""Define the component resolver."""

from typing import Tuple

from diogenos.component import Component
from diogenos.component.registry import ComponentRegistry
from diogenos.component.resolved import ResolvedComponent
from diogenos.resolver.dependencies import DependencyResolver
from diogenos.resolver.implementations import ImplementationResolver
from diogenos.system.base import System


class Resolver:
    """Resolve component dependencies and implementations."""

    def __init__(self) -> None:
        """Initialize the resolver."""
        registry = ComponentRegistry()
        self._dependency_resolver = DependencyResolver(registry)
        self._implementation_resolver = ImplementationResolver()

    def resolve_dependencies(
        self,
        components: Tuple[Component, ...],
    ) -> Tuple[Component, ...]:
        """Resolve components and their dependencies in dependency-first order."""
        return self._dependency_resolver.resolve(components)

    def resolve_implementation(
        self,
        component: Component,
        system: System,
    ) -> ResolvedComponent:
        """Resolve the implementation for a component."""
        return ResolvedComponent(
            component=component,
            implementation=self._implementation_resolver.resolve(
                component,
                system,
            ),
        )
