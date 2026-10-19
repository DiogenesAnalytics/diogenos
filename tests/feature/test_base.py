"""Test the feature abstraction."""

from typing import Callable
from typing import Optional
from typing import Tuple

import pytest

from diogenos.component import Component
from diogenos.component import ComponentImplementation
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
        self.component: Optional[Component] = None
        self.system: Optional[System] = None
        self.implementation: Optional[ComponentImplementation] = None

    def resolve(
        self,
        component: Component,
        system: System,
    ) -> ComponentImplementation:
        """Record the request and return the configured implementation."""
        self.component = component
        self.system = system

        if self.implementation is None:
            raise ValueError("no implementation configured")

        return self.implementation


class ConcreteFeature(Feature):
    """Provide a concrete feature for testing."""


@pytest.fixture
def implementation() -> FakeImplementation:
    """Provide a controllable component implementation."""
    return FakeImplementation()


@pytest.fixture
def component(
    implementation: FakeImplementation,
) -> FakeComponent:
    """Provide a satisfied component."""
    return FakeComponent(
        satisfied=True,
        implementation=implementation,
    )


@pytest.fixture
def unsatisfied_component() -> FakeComponent:
    """Provide an unsatisfied component with an implementation."""
    component = FakeComponent(
        satisfied=False,
        implementation=FakeImplementation(),
    )
    component.implementation = FakeImplementation(
        on_install=component.install,
    )
    return component


@pytest.fixture
def resolver() -> FakeResolver:
    """Provide a controllable resolver."""
    return FakeResolver()


@pytest.mark.feature
def test_components_returns_configured_components(
    component: FakeComponent,
) -> None:
    """Return the components supplied during initialization."""
    components = (component,)
    feature = ConcreteFeature(components)

    assert feature.components is components


@pytest.mark.feature
def test_default_resolver_is_created(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Create a resolver when none is supplied."""
    resolver = Resolver()

    monkeypatch.setattr(
        "diogenos.feature.base.Resolver",
        lambda: resolver,
    )

    feature = ConcreteFeature(())

    assert feature._resolver is resolver


@pytest.mark.feature
def test_custom_resolver_is_retained(
    resolver: FakeResolver,
) -> None:
    """Retain the resolver supplied during initialization."""
    feature = ConcreteFeature((), resolver=resolver)

    assert feature._resolver is resolver


@pytest.mark.feature
def test_is_satisfied_when_all_components_are_satisfied(
    system: System,
    implementation: FakeImplementation,
    component: FakeComponent,
) -> None:
    """Return true when all components are satisfied."""
    another_component = FakeComponent(
        satisfied=True,
        implementation=FakeImplementation(),
    )
    feature = ConcreteFeature((component, another_component))

    assert feature.is_satisfied(system)


@pytest.mark.feature
def test_is_not_satisfied_when_a_component_is_unsatisfied(
    system: System,
    component: FakeComponent,
    unsatisfied_component: FakeComponent,
) -> None:
    """Return false when any component is unsatisfied."""
    feature = ConcreteFeature((component, unsatisfied_component))

    assert not feature.is_satisfied(system)


@pytest.mark.feature
def test_apply_does_nothing_when_feature_is_satisfied(
    system: System,
    implementation: FakeImplementation,
    component: FakeComponent,
) -> None:
    """Skip installation when the feature is already satisfied."""
    feature = ConcreteFeature((component,))

    feature.apply(system)

    assert not implementation.install_called
    assert not implementation.verify_called


@pytest.mark.feature
def test_apply_installs_unsatisfied_component(
    system: System,
    unsatisfied_component: FakeComponent,
    resolver: FakeResolver,
) -> None:
    """Resolve, install, and verify an unsatisfied component."""
    implementation = unsatisfied_component.implementation
    resolver.implementation = implementation
    feature = ConcreteFeature(
        (unsatisfied_component,),
        resolver=resolver,
    )

    feature.apply(system)

    assert resolver.component is unsatisfied_component
    assert resolver.system is system
    assert implementation.install_called
    assert implementation.verify_called
    assert unsatisfied_component.satisfied


@pytest.mark.feature
def test_apply_skips_satisfied_components(
    system: System,
    implementation: FakeImplementation,
    component: FakeComponent,
    unsatisfied_component: FakeComponent,
    resolver: FakeResolver,
) -> None:
    """Install only components that are not already satisfied."""
    unsatisfied_implementation = unsatisfied_component.implementation
    resolver.implementation = unsatisfied_implementation

    feature = ConcreteFeature(
        (component, unsatisfied_component),
        resolver=resolver,
    )

    feature.apply(system)

    assert not implementation.install_called
    assert unsatisfied_implementation.install_called
    assert component.satisfied
    assert unsatisfied_component.satisfied


@pytest.mark.feature
def test_apply_raises_when_verification_fails(
    system: System,
    resolver: FakeResolver,
) -> None:
    """Raise an error when implementation verification fails."""
    implementation = FakeImplementation(verified=False)
    component = FakeComponent(False, implementation)
    resolver.implementation = implementation
    feature = ConcreteFeature((component,), resolver=resolver)

    with pytest.raises(RuntimeError, match="installation failed"):
        feature.apply(system)


@pytest.mark.feature
def test_apply_raises_when_feature_remains_unsatisfied(
    system: System,
    resolver: FakeResolver,
) -> None:
    """Raise an error when installation does not satisfy the feature."""
    implementation = FakeImplementation()
    component = FakeComponent(False, implementation)
    resolver.implementation = implementation
    feature = ConcreteFeature((component,), resolver=resolver)

    with pytest.raises(RuntimeError, match="remains unsatisfied"):
        feature.apply(system)
