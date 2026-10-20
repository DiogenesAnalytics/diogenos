"""Define the component resolver."""

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.resolver.implementations import ImplementationResolver
from diogenos.system.base import System


class Resolver:
    """Resolve component implementations and dependencies."""

    def __init__(self) -> None:
        """Initialize the resolver."""
        self._implementation_resolver = ImplementationResolver()

    def resolve(
        self,
        component: Component,
        system: System,
    ) -> ComponentImplementation:
        """Resolve an implementation for a component and system."""
        return self._implementation_resolver.resolve(component, system)
