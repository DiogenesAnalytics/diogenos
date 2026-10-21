"""Provide shared support for feature tests."""

from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component.resolved import ResolvedComponent
from diogenos.feature.base import Feature
from diogenos.resolver import Resolver
from diogenos.system.base import System


class FakeImplementation(ComponentImplementation):
    """Provide a controllable component implementation."""

    OS = "ubuntu"

    def __init__(
        self,
        verified: bool = True,
        on_install: Optional[Callable[[], None]] = None,
    ) -> None:
        """Initialize the implementation."""
        self.verified = verified
        self.on_install = on_install
        self.install_called = False
        self.verify_called = False

    def install(self, system: System) -> None:
        """Record installation and apply its simulated effect."""
        self.install_called = True

        if self.on_install is not None:
            self.on_install()

    def verify(self, system: System) -> bool:
        """Record verification and return its configured result."""
        self.verify_called = True
        return self.verified


class FakeComponent(Component):
    """Provide a controllable component."""

    def __init__(
        self,
        satisfied: bool,
        implementation: FakeImplementation,
    ) -> None:
        """Initialize the component."""
        self.satisfied = satisfied
        self.implementation = implementation
        self.satisfaction_checks = 0

    def is_satisfied(self, system: System) -> bool:
        """Return whether the component is satisfied."""
        self.satisfaction_checks += 1
        return self.satisfied

    def install(self) -> None:
        """Mark the component as satisfied."""
        self.satisfied = True

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the available implementation."""
        return (self.implementation,)


class FakeResolver(Resolver):
    """Provide a resolver that records its calls."""

    def __init__(self) -> None:
        """Initialize the resolver."""
        self.components: Optional[Tuple[Component, ...]] = None
        self.system: Optional[System] = None
        self.implementation: Optional[ComponentImplementation] = None

    def resolve_dependencies(
        self,
        components: Tuple[Component, ...],
    ) -> Tuple[Component, ...]:
        """Return the supplied components without resolving dependencies."""
        return components

    def resolve_implementation(
        self,
        component: Component,
        system: System,
    ) -> ResolvedComponent:
        """Resolve the configured implementation for a component."""
        self.components = (component,)
        self.system = system

        if self.implementation is None:
            raise ValueError("no implementation configured")

        return ResolvedComponent(
            component=component,
            implementation=self.implementation,
        )


class ConcreteFeature(Feature):
    """Provide a concrete feature for testing."""
