"""Provide fixtures for resolver tests."""

import pytest

from tests.resolver.support import ComponentImplementationStub
from tests.resolver.support import ComponentStub


@pytest.fixture
def implementation() -> ComponentImplementationStub:
    """Provide a supported implementation."""
    return ComponentImplementationStub()


@pytest.fixture
def component(
    implementation: ComponentImplementationStub,
) -> ComponentStub:
    """Provide a component with one supported implementation."""
    return ComponentStub((implementation,))
