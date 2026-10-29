"""Test command execution utilities."""

import subprocess
from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from diogenos.component.implementation.execution import CommandRunner


@pytest.fixture
def run() -> Mock:
    """Provide a mocked subprocess runner."""
    return Mock(
        return_value=subprocess.CompletedProcess(
            args=["example"],
            returncode=0,
            stdout="",
            stderr="",
        )
    )


def test_run_without_privileges(
    run: Mock,
    monkeypatch: MonkeyPatch,
) -> None:
    """Execute ordinary commands without privilege escalation."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    runner = CommandRunner(run=run)

    runner.run(["example", "--version"], check=True)

    run.assert_called_once_with(
        ["example", "--version"],
        check=True,
        capture_output=False,
        text=False,
    )


def test_run_privileged_as_root(
    run: Mock,
    monkeypatch: MonkeyPatch,
) -> None:
    """Execute privileged commands directly when running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    runner = CommandRunner(run=run)

    runner.run(["apt-get", "update"], check=True, privileged=True)

    run.assert_called_once_with(
        ["apt-get", "update"],
        check=True,
        capture_output=False,
        text=False,
    )


def test_run_privileged_as_non_root(
    run: Mock,
    monkeypatch: MonkeyPatch,
) -> None:
    """Use sudo for privileged commands when not running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    runner = CommandRunner(run=run)

    runner.run(["apt-get", "update"], check=True, privileged=True)

    run.assert_called_once_with(
        ["sudo", "apt-get", "update"],
        check=True,
        capture_output=False,
        text=False,
    )


def test_run_returns_completed_process(run: Mock) -> None:
    """Return the result from the underlying command runner."""
    runner = CommandRunner(run=run)

    result = runner.run(["example"])

    assert result.returncode == 0
    assert result.stdout == ""
