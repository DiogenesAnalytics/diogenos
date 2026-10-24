"""Test component validation utilities."""

import subprocess
from unittest.mock import Mock

from diogenos.component.validation import validate_command


def test_validate_command_returns_true_when_command_succeeds() -> None:
    """Return True when the command exits successfully."""
    run = Mock(
        return_value=subprocess.CompletedProcess(
            args=["example", "--version"],
            returncode=0,
            stdout="example 1.0\n",
            stderr="",
        ),
    )

    result = validate_command(run, ["example", "--version"])

    assert result is True
    run.assert_called_once_with(
        ["example", "--version"],
        capture_output=True,
        check=False,
        text=True,
    )


def test_validate_command_returns_false_when_command_fails() -> None:
    """Return False when the command exits unsuccessfully."""
    run = Mock(
        return_value=subprocess.CompletedProcess(
            args=["example", "--version"],
            returncode=1,
            stdout="",
            stderr="command failed\n",
        ),
    )

    result = validate_command(run, ["example", "--version"])

    assert result is False
    run.assert_called_once_with(
        ["example", "--version"],
        capture_output=True,
        check=False,
        text=True,
    )


def test_validate_command_returns_false_when_executable_is_missing() -> None:
    """Return False when the executable cannot be found."""
    run = Mock(side_effect=FileNotFoundError)

    result = validate_command(run, ["missing-command", "--version"])

    assert result is False
    run.assert_called_once_with(
        ["missing-command", "--version"],
        capture_output=True,
        check=False,
        text=True,
    )
