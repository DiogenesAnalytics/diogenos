"""Test the feature list command."""

from unittest.mock import Mock

import pytest
from click.testing import CliRunner

from diogenos.cli import main


@pytest.mark.cli
def test_feature_list(registry: Mock) -> None:
    """Verify that the feature list command prints registered identifiers."""
    registry.list.return_value = ("pulsar", "tmux")

    result = CliRunner().invoke(main, ["feature", "list"])

    assert result.exit_code == 0
    assert result.output == "pulsar\ntmux\n"
    registry.list.assert_called_once_with()
