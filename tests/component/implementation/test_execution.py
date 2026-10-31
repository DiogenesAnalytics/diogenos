"""Test command execution utilities."""

from pytest import MonkeyPatch

from diogenos.component.implementation.execution import prepare_command
from diogenos.component.implementation.execution import privileged_command


def test_privileged_command_as_root(monkeypatch: MonkeyPatch) -> None:
    """Return the original command when running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 0)

    command = privileged_command(["apt-get", "update"])

    assert command == ["apt-get", "update"]


def test_privileged_command_as_non_root(monkeypatch: MonkeyPatch) -> None:
    """Prefix commands with sudo when not running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)

    command = privileged_command(["apt-get", "update"])

    assert command == ["sudo", "apt-get", "update"]


def test_privileged_command_does_not_modify_input(
    monkeypatch: MonkeyPatch,
) -> None:
    """Leave the original command unchanged."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    original = ["apt-get", "update"]

    command = privileged_command(original)

    assert command == ["sudo", "apt-get", "update"]
    assert original == ["apt-get", "update"]


def test_prepare_command_without_privileges() -> None:
    """Return the original command without privilege escalation."""
    command = prepare_command(["git", "--version"])

    assert command == ["git", "--version"]


def test_prepare_command_privileged_as_root(
    monkeypatch: MonkeyPatch,
) -> None:
    """Prepare privileged commands without sudo when running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 0)

    command = prepare_command(["apt-get", "update"], privileged=True)

    assert command == ["apt-get", "update"]


def test_prepare_command_privileged_as_non_root(
    monkeypatch: MonkeyPatch,
) -> None:
    """Prepare privileged commands with sudo when not running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)

    command = prepare_command(["apt-get", "update"], privileged=True)

    assert command == ["sudo", "apt-get", "update"]
