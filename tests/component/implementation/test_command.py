"""Test the command abstraction."""

from dataclasses import FrozenInstanceError

import pytest

from diogenos.component.implementation.command import Command


@pytest.mark.component
def test_from_arguments() -> None:
    """Test creating a command from an argument sequence."""
    arguments = ("apt-get", "update")

    command = Command.from_arguments(arguments)

    assert command.commands == (arguments,)


@pytest.mark.component
def test_initialization() -> None:
    """Test initializing a command with multiple commands."""
    commands = (
        ("apt-get", "update"),
        ("apt-get", "upgrade", "-y"),
    )

    command = Command(commands)

    assert command.commands == commands


@pytest.mark.component
def test_and() -> None:
    """Test composing commands with AND semantics."""
    first = Command.from_arguments(("apt-get", "update"))
    second = Command.from_arguments(("apt-get", "upgrade", "-y"))

    command = first & second

    assert command.commands == (
        ("apt-get", "update"),
        ("apt-get", "upgrade", "-y"),
    )


@pytest.mark.component
def test_empty_commands() -> None:
    """Test that an empty command sequence raises an error."""
    with pytest.raises(ValueError, match="command sequence cannot be empty"):
        Command(())


@pytest.mark.component
def test_empty_command() -> None:
    """Test that an empty individual command raises an error."""
    with pytest.raises(ValueError, match="commands cannot be empty"):
        Command(((),))


@pytest.mark.component
def test_immutable() -> None:
    """Test that a command cannot be modified."""
    command = Command.from_arguments(("apt-get", "update"))

    with pytest.raises(FrozenInstanceError):
        command.commands = (("apt-get", "upgrade"),)  # type: ignore[misc]
