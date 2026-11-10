"""Test the software installation method abstraction."""

from typing import Tuple

import pytest

from diogenos.component.implementation.method.base import Method
from diogenos.component.implementation.method.options import MethodOptions
from diogenos.system.base import System


class DummyMethodOptions(MethodOptions):
    """Provide test method options."""


class DummyMethod(Method):
    """Provide a test installation method."""

    def install(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install the specified packages."""


@pytest.fixture
def options() -> DummyMethodOptions:
    """Provide test method options."""
    return DummyMethodOptions()


def test_initialization(options: DummyMethodOptions) -> None:
    """Test initialization with method options."""
    method = DummyMethod(options)

    assert method.options is options


def test_install_is_abstract(options: DummyMethodOptions) -> None:
    """Test that install must be implemented by subclasses."""

    class IncompleteMethod(Method):
        """Provide an incomplete installation method."""

    with pytest.raises(TypeError, match="abstract method"):
        IncompleteMethod(options)  # type: ignore[abstract]
