"""Test component dependency resolution."""

from typing import Callable
from unittest.mock import Mock

import pytest

from diogenos.component import Dependency
from diogenos.resolver.dependencies import DependencyResolver
from tests.resolver.support import ComponentStub


@pytest.mark.resolver
def test_resolve_component_without_dependencies(
    component_factory: Callable[..., ComponentStub],
    component_registry: Mock,
    dependency_resolver: DependencyResolver,
) -> None:
    """Return a component that has no dependencies."""
    component = component_factory(registry_id="example")

    resolved = dependency_resolver.resolve((component,))

    assert resolved == (component,)
    component_registry.get.assert_not_called()


@pytest.mark.resolver
def test_resolve_component_with_one_dependency(
    component_factory: Callable[..., ComponentStub],
    component_registry: Mock,
    dependency_resolver: DependencyResolver,
) -> None:
    """Resolve a component's dependency before the component."""
    dependency = component_factory(registry_id="dependency")
    component = component_factory(
        registry_id="example",
        dependencies=(Dependency("dependency"),),
    )
    component_registry.get.return_value = lambda: dependency

    resolved = dependency_resolver.resolve((component,))

    assert tuple(item.registry_id for item in resolved) == (
        "dependency",
        "example",
    )
    component_registry.get.assert_called_once_with("dependency")


@pytest.mark.resolver
def test_resolve_component_with_transitive_dependencies(
    component_factory: Callable[..., ComponentStub],
    component_registry: Mock,
    dependency_resolver: DependencyResolver,
) -> None:
    """Resolve transitive dependencies in dependency-first order."""
    component_c = component_factory(registry_id="c")
    component_b = component_factory(
        registry_id="b",
        dependencies=(Dependency("c"),),
    )
    component_a = component_factory(
        registry_id="a",
        dependencies=(Dependency("b"),),
    )

    component_classes = {
        "b": lambda: component_b,
        "c": lambda: component_c,
    }
    component_registry.get.side_effect = component_classes.__getitem__

    resolved = dependency_resolver.resolve((component_a,))

    assert tuple(item.registry_id for item in resolved) == ("c", "b", "a")
    assert component_registry.get.call_count == 2


@pytest.mark.resolver
def test_resolve_components_with_shared_dependency(
    component_factory: Callable[..., ComponentStub],
    component_registry: Mock,
    dependency_resolver: DependencyResolver,
) -> None:
    """Resolve a shared dependency only once."""
    component_c = component_factory(registry_id="c")
    component_a = component_factory(
        registry_id="a",
        dependencies=(Dependency("c"),),
    )
    component_b = component_factory(
        registry_id="b",
        dependencies=(Dependency("c"),),
    )

    component_classes = {
        "c": lambda: component_c,
    }
    component_registry.get.side_effect = component_classes.__getitem__

    resolved = dependency_resolver.resolve((component_a, component_b))

    assert tuple(item.registry_id for item in resolved) == ("c", "a", "b")
    assert component_registry.get.call_count == 2


@pytest.mark.resolver
def test_resolve_component_with_unknown_dependency(
    component_factory: Callable[..., ComponentStub],
    component_registry: Mock,
    dependency_resolver: DependencyResolver,
) -> None:
    """Raise an error when a dependency is not registered."""
    component = component_factory(
        registry_id="example",
        dependencies=(Dependency("unknown"),),
    )
    component_registry.get.side_effect = KeyError(
        "unknown component identifier: unknown",
    )

    with pytest.raises(
        KeyError,
        match="unknown component identifier: unknown",
    ):
        dependency_resolver.resolve((component,))
