"""Define the command abstraction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Command:
    """Represent a command or sequence of commands."""

    commands: Tuple[Tuple[str, ...], ...]

    @classmethod
    def from_arguments(cls, arguments: Tuple[str, ...]) -> Command:
        """Create a command from an argument sequence."""
        return cls((arguments,))

    def __and__(self, other: Command) -> Command:
        """Compose commands with AND semantics."""
        return Command(self.commands + other.commands)

    def __post_init__(self) -> None:
        """Validate the command sequence."""
        if not self.commands:
            raise ValueError("command sequence cannot be empty")

        if any(not command for command in self.commands):
            raise ValueError("commands cannot be empty")
