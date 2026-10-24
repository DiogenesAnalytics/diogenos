"""Provide component validation utilities."""

import subprocess
from typing import Callable
from typing import Sequence


def validate_command(
    run: Callable[..., subprocess.CompletedProcess[str]],
    command: Sequence[str],
) -> bool:
    """Determine whether a command executes successfully."""
    try:
        result = run(
            list(command),
            capture_output=True,
            check=False,
            text=True,
        )
    except FileNotFoundError:
        return False

    return result.returncode == 0
