"""Define the command abstractions."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Tuple


class Executable:
    """Represent an executable operation."""

    def __and__(self, other: Executable) -> CommandSequence:
        """Compose executables into a sequence."""
        commands = self.commands if isinstance(self, CommandSequence) else (self,)
        other_commands = (
            other.commands if isinstance(other, CommandSequence) else (other,)
        )

        return CommandSequence(commands + other_commands)


@dataclass(frozen=True)
class Command(Executable):
    """Represent a process invocation."""

    arguments: Tuple[str, ...]

    @classmethod
    def from_arguments(
        cls,
        arguments: Tuple[str, ...],
        *,
        privileged: bool = False,
    ) -> Command:
        """Create a command from an argument sequence."""
        return cls(cls.prepare(arguments, privileged=privileged))

    @staticmethod
    def prepare(
        arguments: Tuple[str, ...],
        *,
        privileged: bool = False,
    ) -> Tuple[str, ...]:
        """Prepare command arguments for execution."""
        if privileged and os.geteuid() != 0:
            return ("sudo",) + arguments

        return arguments

    def __post_init__(self) -> None:
        """Validate the command arguments."""
        if not self.arguments:
            raise ValueError("command arguments cannot be empty")


@dataclass(frozen=True)
class CommandSequence(Executable):
    """Represent an ordered sequence of commands."""

    commands: Tuple[Executable, ...]

    def __post_init__(self) -> None:
        """Validate the command sequence."""
        if not self.commands:
            raise ValueError("command sequence cannot be empty")

        if any(not isinstance(command, Executable) for command in self.commands):
            raise TypeError("all sequence members must be executable")
