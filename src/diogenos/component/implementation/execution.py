"""Provide command execution utilities."""

import os
from typing import List
from typing import Sequence


def privileged_command(command: Sequence[str]) -> List[str]:
    """Prepare a command for privileged execution."""
    if os.geteuid() == 0:
        return list(command)

    return ["sudo", *command]


def prepare_command(
    command: Sequence[str],
    *,
    privileged: bool = False,
) -> List[str]:
    """Prepare a command for execution."""
    executable = list(command)

    if privileged:
        executable = privileged_command(executable)

    return executable
