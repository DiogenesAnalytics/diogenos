"""Test the Tmux feature."""

import pytest

from diogenos.component.catalog.tmux.tmux import TmuxPackage
from diogenos.feature.catalog.tmux import Tmux


@pytest.mark.feature
def test_tmux_contains_tmux_package() -> None:
    """Verify that the Tmux feature contains the Tmux package component."""
    feature = Tmux()

    assert len(feature.components) == 1
    assert isinstance(feature.components[0], TmuxPackage)
