"""Test the software installation method abstraction."""

from typing import Tuple

import pytest

from diogenos.component.implementation.command import Command
from diogenos.component.implementation.command import Executable
from diogenos.component.implementation.method.base import Method
from diogenos.component.implementation.method.operations import APTOperation
from diogenos.component.implementation.method.operations import Operation
from diogenos.component.implementation.method.options import MethodOptions


class DummyMethodOptions(MethodOptions):
    """Provide test method options."""


class DummyMethod(Method):
    """Provide a test installation method."""

    def build(
        self,
        operation: Operation,
        arguments: Tuple[str, ...] = (),
    ) -> Executable:
        """Build a test installation executable."""
        return Command.from_arguments(arguments)


@pytest.fixture
def options() -> DummyMethodOptions:
    """Provide test method options."""
    return DummyMethodOptions()


@pytest.mark.component
def test_initialization(options: DummyMethodOptions) -> None:
    """Test initialization with method options."""
    method = DummyMethod(options)

    assert method.options is options


@pytest.mark.component
def test_build(options: DummyMethodOptions) -> None:
    """Test building an installation executable."""
    method = DummyMethod(options)
    packages = ("firefox",)

    executable = method.build(APTOperation.INSTALL, packages)

    assert isinstance(executable, Executable)
    assert executable == Command.from_arguments(packages)


@pytest.mark.component
def test_build_is_abstract(options: DummyMethodOptions) -> None:
    """Test that build must be implemented by subclasses."""

    class IncompleteMethod(Method):
        """Provide an incomplete installation method."""

    with pytest.raises(TypeError, match="abstract method"):
        IncompleteMethod(options)  # type: ignore[abstract]
