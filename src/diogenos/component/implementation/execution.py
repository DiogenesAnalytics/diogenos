"""Provide command execution utilities."""

import os
from typing import List
from typing import Sequence


def privileged_command(command: Sequence[str]) -> List[str]:
    """Prepare a command for privileged execution."""
    if os.geteuid() == 0:
        return list(command)

    return ["sudo", *command]
