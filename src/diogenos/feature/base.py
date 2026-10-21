"""Define the feature abstraction."""

from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.resolver import Resolver
from diogenos.system.base import System


class Feature:
    """Represent a feature composed of components."""

    def __init__(
        self,
        components: Tuple[Component, ...],
        resolver: Optional[Resolver] = None,
    ) -> None:
        """Initialize the feature with its components and resolver."""
        self._components = components
        self._resolver = resolver if resolver is not None else Resolver()

    @property
    def components(self) -> Tuple[Component, ...]:
        """Return the components that comprise the feature."""
        return self._components

    def is_satisfied(self, system: System) -> bool:
        """Determine whether all components and their dependencies are satisfied."""
        dependency_resolved_components = self._resolver.resolve_dependencies(
            self._components,
        )

        return all(
            component.is_satisfied(system)
            for component in dependency_resolved_components
        )

    def apply(self, system: System) -> None:
        """Apply the feature to bring the system into its desired state."""
        dependency_resolved_components = self._resolver.resolve_dependencies(
            self._components,
        )

        for component in dependency_resolved_components:
            if component.is_satisfied(system):
                continue

            resolved_component = self._resolver.resolve_implementation(
                component,
                system,
            )

            implementation = resolved_component.implementation
            implementation.install(system)

            if not implementation.verify(system):
                raise RuntimeError(
                    f"installation failed for component " f"{type(component).__name__}",
                )

        if not self.is_satisfied(system):
            raise RuntimeError(
                f"feature {type(self).__name__} remains unsatisfied",
            )
