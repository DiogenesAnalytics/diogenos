"""Test the component implementation abstraction."""

from typing import Tuple

import pytest

from diogenos.component import ComponentImplementation
from diogenos.component.implementation.method.base import Method
from diogenos.component.implementation.method.options import MethodOptions
from diogenos.component.implementation.method.types import MethodType
from diogenos.system.base import System
from tests.component.support import (
    ComponentImplementationStub as SharedImplementationStub,
)


class ComponentImplementationStub(ComponentImplementation):
    """Provide an OS-aware component implementation for testing."""

    OS = "ubuntu"

    def __init__(
        self,
        verified: bool = True,
    ) -> None:
        """Initialize the component implementation stub."""
        self.verified = verified
        self.install_called = False
        self.verify_called = False

    def install(self, system: System) -> None:
        """Record that installation was called."""
        self.install_called = True

    def verify(self, system: System) -> bool:
        """Record that verification was called."""
        self.verify_called = True
        return self.verified


class MethodOptionsStub(MethodOptions):
    """Provide dummy installation method options."""


class MethodStub(Method):
    """Provide a dummy installation method."""

    def install(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install the specified packages."""


class AlternateMethodStub(Method):
    """Provide an alternate dummy installation method."""

    def install(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install the specified packages."""


class APTImplementationStub(SharedImplementationStub):
    """Provide an implementation with APT support."""

    METHODS = {
        MethodType.APT: (
            MethodStub,
            MethodOptionsStub(),
        ),
    }


class SnapImplementationStub(SharedImplementationStub):
    """Provide an implementation with Snap support."""

    METHODS = {
        MethodType.SNAP: (
            AlternateMethodStub,
            MethodOptionsStub(),
        ),
    }


class CombinedImplementationStub(
    APTImplementationStub,
    SnapImplementationStub,
):
    """Provide an implementation with APT and Snap support."""


@pytest.mark.component
def test_implementation_is_abstract() -> None:
    """Test that ComponentImplementation cannot be instantiated directly."""
    with pytest.raises(TypeError):
        ComponentImplementation()  # type: ignore[abstract]


@pytest.mark.component
def test_implementation_supports_system(
    system: System,
) -> None:
    """Test that an implementation supports its system."""
    implementation = ComponentImplementationStub()

    assert implementation.supports(system) is True


@pytest.mark.component
def test_implementation_does_not_support_system(
    system: System,
) -> None:
    """Test that an implementation does not support another system."""
    implementation = ComponentImplementationStub()

    system = System(
        platform=system.platform.__class__(
            os="fedora",
            version=system.platform.version,
            codename=system.platform.codename,
            pretty_name="Fedora Linux",
        ),
        hardware=system.hardware,
        desktop=system.desktop,
    )

    assert implementation.supports(system) is False


@pytest.mark.component
def test_implementation_install(
    system: System,
) -> None:
    """Test that installation is called."""
    implementation = ComponentImplementationStub()

    implementation.install(system)

    assert implementation.install_called is True


@pytest.mark.component
def test_implementation_verify(
    system: System,
) -> None:
    """Test that verification is called."""
    implementation = ComponentImplementationStub()

    assert implementation.verify(system) is True
    assert implementation.verify_called is True


@pytest.mark.component
def test_implementation_composes_methods() -> None:
    """Test that methods are composed from parent implementations."""
    assert set(CombinedImplementationStub.METHODS) == {
        MethodType.APT,
        MethodType.SNAP,
    }


@pytest.mark.component
def test_implementation_rejects_duplicate_methods() -> None:
    """Test that duplicate inherited methods are rejected."""

    class DuplicateAPTImplementationStub(SharedImplementationStub):
        """Provide another implementation with APT support."""

        METHODS = {
            MethodType.APT: (
                AlternateMethodStub,
                MethodOptionsStub(),
            ),
        }

    with pytest.raises(TypeError, match="duplicate installation method apt"):

        class InvalidImplementation(
            APTImplementationStub,
            DuplicateAPTImplementationStub,
        ):
            """Provide an invalid implementation."""


@pytest.mark.component
def test_implementation_overrides_inherited_method() -> None:
    """Test that a subclass can override an inherited method."""

    class OverriddenImplementation(APTImplementationStub):
        """Provide an implementation with an overridden method."""

        METHODS = {
            MethodType.APT: (
                AlternateMethodStub,
                MethodOptionsStub(),
            ),
        }

    assert OverriddenImplementation.METHODS[MethodType.APT][0] is AlternateMethodStub


@pytest.mark.component
def test_implementation_resolves_default_method() -> None:
    """Test that the first registered method is selected by default."""
    implementation = APTImplementationStub()

    assert isinstance(implementation.resolve_method(), MethodStub)


@pytest.mark.component
def test_implementation_resolves_explicit_method() -> None:
    """Test that an explicitly requested method is selected."""
    implementation = CombinedImplementationStub()

    assert isinstance(
        implementation.resolve_method(MethodType.SNAP),
        AlternateMethodStub,
    )


@pytest.mark.component
def test_implementation_rejects_unsupported_method() -> None:
    """Test that an unsupported method raises an error."""
    implementation = SharedImplementationStub()

    with pytest.raises(ValueError, match="unsupported installation method: snap"):
        implementation.resolve_method(MethodType.SNAP)


@pytest.mark.component
def test_implementation_resolves_no_method() -> None:
    """Test that an implementation without methods resolves to None."""
    implementation = SharedImplementationStub()

    assert implementation.resolve_method() is None


@pytest.mark.component
def test_implementation_rejects_method_when_none_registered() -> None:
    """Test that an explicit method is rejected when none are registered."""
    implementation = SharedImplementationStub()

    with pytest.raises(ValueError, match="unsupported installation method: apt"):
        implementation.resolve_method(MethodType.APT)
