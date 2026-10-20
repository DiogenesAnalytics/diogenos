"""Test implementation resolution."""

import pytest

from diogenos.resolver.implementations import ImplementationResolver
from diogenos.system.base import System
from tests.resolver.support import ComponentImplementationStub
from tests.resolver.support import ComponentStub


@pytest.mark.resolver
def test_resolver_returns_supported_implementation(
    system: System,
) -> None:
    """Return a supported implementation."""
    unsupported = ComponentImplementationStub(supported=False)
    supported = ComponentImplementationStub()
    component = ComponentStub((unsupported, supported))

    implementation = ImplementationResolver().resolve(component, system)

    assert implementation is supported


@pytest.mark.resolver
def test_resolver_returns_first_supported_implementation(
    system: System,
) -> None:
    """Return the first supported implementation."""
    first = ComponentImplementationStub()
    second = ComponentImplementationStub()
    component = ComponentStub((first, second))

    implementation = ImplementationResolver().resolve(component, system)

    assert implementation is first


@pytest.mark.resolver
def test_resolver_raises_when_no_implementation_is_supported(
    system: System,
) -> None:
    """Raise an error when no implementation is supported."""
    component = ComponentStub(
        (
            ComponentImplementationStub(supported=False),
            ComponentImplementationStub(supported=False),
        ),
    )

    with pytest.raises(
        ValueError,
        match="no implementation for component ComponentStub",
    ):
        ImplementationResolver().resolve(component, system)
