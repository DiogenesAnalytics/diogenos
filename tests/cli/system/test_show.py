"""Test the system show command."""

from unittest.mock import Mock

import pytest
from click.testing import CliRunner

from diogenos.cli import main
from diogenos.cli.system import show
from diogenos.system.base import System


@pytest.mark.cli
def test_system_show_succeeds(
    detector: Mock,
    system: System,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that showing system information succeeds."""
    detector.detect.return_value = system

    monkeypatch.setattr(
        show,
        "SystemDetector",
        Mock(return_value=detector),
    )

    result = CliRunner().invoke(
        main,
        ["system", "show"],
    )

    assert result.exit_code == 0
    assert result.output == (
        f"Operating System: {system.platform.pretty_name}\n"
        f"Distribution:     {system.platform.os}\n"
        f"Version:          {system.platform.version}\n"
        f"Codename:         {system.platform.codename or 'N/A'}\n"
        "\n"
        f"Machine:          {system.hardware.machine}\n"
        f"Processor:        {system.hardware.processor or 'N/A'}\n"
        f"Architecture:     {system.hardware.architecture}\n"
        "\n"
        f"Desktop:          {system.desktop.pretty_name or 'N/A'}\n"
        f"Identifier:       {system.desktop.name or 'N/A'}\n"
    )
    detector.detect.assert_called_once_with()
