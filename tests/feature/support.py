"""Define shared test support utilities."""

import subprocess
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple


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
