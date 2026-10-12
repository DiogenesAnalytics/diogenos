"""Define the feature abstraction."""

from typing import Optional
from typing import Tuple

from diogenos.feature.component import Component
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
        """Determine whether all components of the feature are satisfied."""
        return all(component.is_satisfied(system) for component in self._components)

    def apply(self, system: System) -> None:
        """Apply the feature to bring the system into its desired state."""
        if self.is_satisfied(system):
            return

        for component in self._components:
            if component.is_satisfied(system):
                continue

            implementation = self._resolver.resolve(component, system)
            implementation.install(system)

            if not implementation.verify(system):
                raise RuntimeError(
                    f"installation failed for component " f"{type(component).__name__}",
                )

        if not self.is_satisfied(system):
            raise RuntimeError(
                f"feature {type(self).__name__} remains unsatisfied",
            )
