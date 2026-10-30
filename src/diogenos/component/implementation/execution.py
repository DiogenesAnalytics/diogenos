"""Provide command execution utilities."""

import os
import subprocess
from typing import Callable
from typing import Optional
from typing import Sequence


class CommandRunner:
    """Execute commands with optional privilege escalation."""

    def __init__(
        self,
        run: Optional[Callable[..., subprocess.CompletedProcess[str]]] = None,
    ) -> None:
        """Initialize the command runner."""
        self._run = run or subprocess.run

    def run(
        self,
        command: Sequence[str],
        *,
        privileged: bool = False,
        check: bool = False,
        capture_output: bool = False,
        text: bool = False,
        input: Optional[str] = None,
    ) -> subprocess.CompletedProcess[str]:
        """Execute a command, optionally with elevated privileges."""
        executable = list(command)

        if privileged and os.geteuid() != 0:
            executable.insert(0, "sudo")

        if input is not None:
            return self._run(
                executable,
                check=check,
                capture_output=capture_output,
                text=text,
                input=input,
            )

        return self._run(
            executable,
            check=check,
            capture_output=capture_output,
            text=text,
        )
