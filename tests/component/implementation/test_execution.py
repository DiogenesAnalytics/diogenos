"""Test command execution utilities."""

from pytest import MonkeyPatch

from diogenos.component.implementation.execution import privileged_command


def test_command_as_root(monkeypatch: MonkeyPatch) -> None:
    """Return the original command when running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 0)

    command = privileged_command(["apt-get", "update"])

    assert command == ["apt-get", "update"]


def test_command_as_non_root(monkeypatch: MonkeyPatch) -> None:
    """Prefix privileged commands with sudo when not running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)

    command = privileged_command(["apt-get", "update"])

    assert command == ["sudo", "apt-get", "update"]


def test_command_does_not_modify_input(
    monkeypatch: MonkeyPatch,
) -> None:
    """Leave the original command unchanged."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    original = ["apt-get", "update"]

    command = privileged_command(original)

    assert command == original
    assert command is not original
