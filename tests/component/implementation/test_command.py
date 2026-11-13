"""Test the command abstractions."""

from dataclasses import FrozenInstanceError

import pytest

from diogenos.component.implementation.command import Command
from diogenos.component.implementation.command import CommandSequence
from diogenos.component.implementation.command import Executable


@pytest.mark.component
def test_from_arguments() -> None:
    """Test creating a command from an argument sequence."""
    arguments = ("apt-get", "update")

    command = Command.from_arguments(arguments)

    assert command.arguments == arguments


@pytest.mark.component
def test_initialization() -> None:
    """Test initializing a command."""
    arguments = ("apt-get", "update")

    command = Command(arguments)

    assert command.arguments == arguments


@pytest.mark.component
def test_and() -> None:
    """Test composing commands with AND semantics."""
    first = Command.from_arguments(("apt-get", "update"))
    second = Command.from_arguments(("apt-get", "upgrade", "-y"))

    executable = first & second

    assert isinstance(executable, CommandSequence)
    assert executable.commands == (first, second)


@pytest.mark.component
def test_and_flattens_sequences() -> None:
    """Test that composing sequences produces a flat sequence."""
    first = Command.from_arguments(("apt-get", "update"))
    second = Command.from_arguments(("apt-get", "upgrade"))
    third = Command.from_arguments(("apt-get", "install", "curl"))

    executable = (first & second) & third

    assert isinstance(executable, CommandSequence)
    assert executable.commands == (first, second, third)


@pytest.mark.component
def test_command_is_executable() -> None:
    """Test that a command is an executable."""
    command = Command.from_arguments(("apt-get", "update"))

    assert isinstance(command, Executable)


@pytest.mark.component
def test_command_sequence_is_executable() -> None:
    """Test that a command sequence is an executable."""
    command = Command.from_arguments(("apt-get", "update"))
    executable = CommandSequence((command,))

    assert isinstance(executable, Executable)


@pytest.mark.component
def test_empty_command() -> None:
    """Test that an empty command raises an error."""
    with pytest.raises(ValueError, match="command arguments cannot be empty"):
        Command(())


@pytest.mark.component
def test_empty_command_sequence() -> None:
    """Test that an empty command sequence raises an error."""
    with pytest.raises(ValueError, match="command sequence cannot be empty"):
        CommandSequence(())


@pytest.mark.component
def test_command_sequence_rejects_non_executable() -> None:
    """Test that a command sequence rejects non-executable members."""
    with pytest.raises(TypeError, match="all sequence members must be executable"):
        CommandSequence((("apt-get", "update"),))  # type: ignore[arg-type]


@pytest.mark.component
def test_command_immutable() -> None:
    """Test that a command cannot be modified."""
    command = Command.from_arguments(("apt-get", "update"))

    with pytest.raises(FrozenInstanceError):
        command.arguments = ("apt-get", "upgrade")  # type: ignore[misc]


@pytest.mark.component
def test_command_sequence_immutable() -> None:
    """Test that a command sequence cannot be modified."""
    command = Command.from_arguments(("apt-get", "update"))
    executable = CommandSequence((command,))

    with pytest.raises(FrozenInstanceError):
        executable.commands = ()  # type: ignore[misc]
