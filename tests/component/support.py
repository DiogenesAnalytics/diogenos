"""Provide shared support for component tests."""

import subprocess
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.system.base import System


class ComponentImplementationStub(ComponentImplementation):
    """Provide a minimal component implementation for testing."""

    def supports(self, system: System) -> bool:
        """Determine whether the implementation supports the system."""
        return True

    def install(self, system: System) -> None:
        """Install the component."""
        pass

    def verify(self, system: System) -> bool:
        """Verify the component."""
        return True


class ComponentStub(Component):
    """Provide a minimal component for testing."""

    def __init__(self, satisfied: bool = False) -> None:
        """Initialize the component stub."""
        self.satisfied = satisfied
        self.implementation_stub = ComponentImplementationStub()

    def is_satisfied(self, system: System) -> bool:
        """Return whether the component is satisfied."""
        return self.satisfied

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the component implementations."""
        return (self.implementation_stub,)


class RunStub:
    """Stub subprocess.run and record its calls."""

    def __init__(self, returncode: int = 0) -> None:
        """Initialize the stub with a command return code."""
        self.returncode = returncode
        self.calls: List[Tuple[List[str], Dict[str, Any]]] = []

    def __call__(
        self,
        command: List[str],
        **kwargs: Any,
    ) -> subprocess.CompletedProcess[str]:
        """Record a command and return a simulated result."""
        self.calls.append((command, kwargs))

        result = subprocess.CompletedProcess(
            args=command,
            returncode=self.returncode,
            stdout="",
            stderr="",
        )

        if kwargs.get("check", False) and result.returncode != 0:
            raise subprocess.CalledProcessError(
                returncode=result.returncode,
                cmd=command,
                output=result.stdout,
                stderr=result.stderr,
            )

        return result
