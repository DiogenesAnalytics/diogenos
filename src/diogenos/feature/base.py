"""Define the feature abstraction."""

from typing import Dict
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component.implementation.method import InstallMethodType
from diogenos.resolver import Resolver
from diogenos.system.base import System


class Feature:
    """Represent a feature composed of components."""

    registry_id: Optional[str] = None

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

    @property
    def resolved_components(self) -> Tuple[Component, ...]:
        """Return the components that comprise the feature, including dependencies."""
        return self._resolver.resolve_dependencies(self._components)

    def is_satisfied(self, system: System) -> bool:
        """Determine if all components and their dependencies are satisfied."""
        return all(
            component.is_satisfied(system) for component in self.resolved_components
        )

    def apply(
        self,
        system: System,
        install_methods: Optional[Dict[str, InstallMethodType]] = None,
    ) -> None:
        """Apply the feature to bring the system into its desired state."""
        if install_methods is None:
            install_methods = {}

        for component in self.resolved_components:
            if component.is_satisfied(system):
                continue

            resolved_component = self._resolver.resolve_implementation(
                component,
                system,
            )

            implementation = resolved_component.implementation
            component_id = component.registry_id

            method = (
                install_methods.get(component_id) if component_id is not None else None
            )

            if method is not None and method not in implementation.install_methods:
                raise ValueError(
                    f"unsupported installation method {method.value!r} "
                    f"for component {component_id!r}"
                )

            try:
                implementation.install(system, method)
            except Exception as error:
                raise RuntimeError(
                    f"installation failed for component "
                    f"{type(component).__name__}: {error}"
                ) from error

            if not implementation.verify(system):
                raise RuntimeError(
                    f"verification failed for component "
                    f"{type(component).__name__} using "
                    f"{type(implementation).__name__}",
                )

        if not self.is_satisfied(system):
            raise RuntimeError(
                f"feature {type(self).__name__} remains unsatisfied",
            )
