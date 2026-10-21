"""Test the feature abstraction."""

import pytest

from diogenos.resolver import Resolver
from diogenos.system.base import System
from tests.feature.support import ConcreteFeature
from tests.feature.support import FakeComponent
from tests.feature.support import FakeImplementation
from tests.feature.support import FakeResolver


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


@pytest.fixture
def feature(
    component: FakeComponent,
    resolver: FakeResolver,
) -> ConcreteFeature:
    """Provide a feature with a component and a fake resolver."""
    return ConcreteFeature((component,), resolver=resolver)


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
    feature: ConcreteFeature,
) -> None:
    """Return true when all components are satisfied."""
    assert feature.is_satisfied(system)


@pytest.mark.feature
def test_is_not_satisfied_when_a_component_is_unsatisfied(
    system: System,
    component: FakeComponent,
    unsatisfied_component: FakeComponent,
    resolver: FakeResolver,
) -> None:
    """Return false when any component is unsatisfied."""
    feature = ConcreteFeature(
        (component, unsatisfied_component),
        resolver=resolver,
    )

    assert not feature.is_satisfied(system)


@pytest.mark.feature
def test_apply_does_nothing_when_feature_is_satisfied(
    system: System,
    implementation: FakeImplementation,
    feature: ConcreteFeature,
) -> None:
    """Skip installation when the feature is already satisfied."""
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

    assert resolver.components == (unsatisfied_component,)
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


def test_apply_skips_implementation_resolution_for_satisfied_component(
    system: System,
) -> None:
    """Skip implementation resolution for a satisfied component."""
    component = FakeComponent(
        satisfied=True,
        implementation=FakeImplementation(),
    )
    resolver = FakeResolver()
    feature = ConcreteFeature((component,), resolver=resolver)

    feature.apply(system)

    assert resolver.components is None
    assert resolver.implementation is None
