"""Test command execution utilities."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest import CaptureFixture
from pytest import MonkeyPatch

from diogenos.component.implementation.execution import download_file
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


def test_download_file(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Download a file and report progress."""
    content = b"Hello, DiogenOS!"

    response = MagicMock()
    response.headers = {"Content-Length": str(len(content))}
    response.read.side_effect = [content, b""]
    response.__enter__.return_value = response

    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda *args, **kwargs: response,
    )

    destination = tmp_path / "download.txt"

    download_file("https://example.com/download.txt", destination)

    assert destination.read_bytes() == content
    assert "100.0%" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == [destination]


def test_download_file_without_content_length(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Report downloaded bytes when content length is unavailable."""
    content = b"Hello, DiogenOS!"

    response = MagicMock()
    response.headers = {}
    response.read.side_effect = [content, b""]
    response.__enter__.return_value = response

    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda *args, **kwargs: response,
    )

    destination = tmp_path / "download.txt"

    download_file("https://example.com/download.txt", destination)

    assert destination.read_bytes() == content
    assert f"{len(content):,} bytes" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == [destination]


def test_download_file_incomplete(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Raise an error and clean up when the download is incomplete."""
    response = MagicMock()
    response.headers = {"Content-Length": "100"}
    response.read.side_effect = [b"Hello", b""]
    response.__enter__.return_value = response

    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda *args, **kwargs: response,
    )

    destination = tmp_path / "download.txt"

    with pytest.raises(RuntimeError, match="incomplete download"):
        download_file("https://example.com/download.txt", destination)

    assert not destination.exists()
    assert list(tmp_path.iterdir()) == []


def test_download_file_preserves_existing_destination(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Preserve the existing destination when the download fails."""
    destination = tmp_path / "download.txt"
    original_content = b"Existing content"
    destination.write_bytes(original_content)

    response = MagicMock()
    response.headers = {"Content-Length": "100"}
    response.read.side_effect = [b"Hello", b""]
    response.__enter__.return_value = response

    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda *args, **kwargs: response,
    )

    with pytest.raises(RuntimeError, match="incomplete download"):
        download_file("https://example.com/download.txt", destination)

    assert destination.read_bytes() == original_content
    assert list(tmp_path.iterdir()) == [destination]
