"""Test the system update command."""

from unittest.mock import Mock

import pytest
from click.testing import CliRunner
from pytest import MonkeyPatch

from diogenos.cli.system import update
from diogenos.system.base import System


@pytest.mark.cli
def test_update_system(
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test the system update command."""
    updater = Mock()

    monkeypatch.setattr(
        update,
        "SystemDetector",
        Mock(return_value=Mock(detect=Mock(return_value=system))),
    )
    monkeypatch.setattr(update, "SystemUpdater", Mock(return_value=updater))

    result = CliRunner().invoke(update.update_system)

    assert result.exit_code == 0
    assert "System update completed successfully." in result.output
    updater.update.assert_called_once_with(system)


@pytest.mark.cli
def test_update_system_detection_failure(
    monkeypatch: MonkeyPatch,
) -> None:
    """Test the system update command when system detection fails."""
    detector = Mock()
    detector.detect.side_effect = RuntimeError("Detection failed")

    monkeypatch.setattr(update, "SystemDetector", Mock(return_value=detector))

    result = CliRunner().invoke(update.update_system)

    assert result.exit_code != 0


@pytest.mark.cli
def test_update_system_failure(
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test the system update command when updating fails."""
    updater = Mock()
    updater.update.side_effect = RuntimeError("Update failed")

    monkeypatch.setattr(
        update,
        "SystemDetector",
        Mock(return_value=Mock(detect=Mock(return_value=system))),
    )
    monkeypatch.setattr(update, "SystemUpdater", Mock(return_value=updater))

    result = CliRunner().invoke(update.update_system)

    assert result.exit_code == 1
    assert "Error: system update failed: Update failed" in result.output
    updater.update.assert_called_once_with(system)
