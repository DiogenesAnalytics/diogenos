"""Define the software installation method abstraction."""

from abc import ABC
from abc import abstractmethod
from typing import Tuple

from diogenos.component.implementation.command import Command

from .operations import Operation
from .options import MethodOptions


class Method(ABC):
    """Define a software installation method."""

    OPERATIONS: Tuple[Operation, ...] = ()

    def __init__(self, options: MethodOptions) -> None:
        """Initialize the method with its options."""
        self.options = options

    def supports(self, operation: Operation) -> bool:
        """Determine whether the method supports an operation."""
        return operation in self.OPERATIONS

    @abstractmethod
    def build(
        self,
        operation: Operation,
        arguments: Tuple[str, ...] = (),
    ) -> Command:
        """Build a command for the specified operation."""
