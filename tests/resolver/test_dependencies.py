"""Test component dependency resolution."""

from unittest.mock import Mock

import pytest

from diogenos.component.registry import ComponentRegistry
from diogenos.resolver.dependencies import DependencyResolver
from tests.resolver.support import ComponentStub


@pytest.mark.resolver
def test_resolve_component_without_dependencies() -> None:
    """Return a component that has no dependencies."""
    component = ComponentStub(registry_id="example")
    registry = Mock(spec=ComponentRegistry)
    resolver = DependencyResolver(registry)

    resolved = resolver.resolve((component,))

    assert resolved == (component,)
    registry.get.assert_not_called()
