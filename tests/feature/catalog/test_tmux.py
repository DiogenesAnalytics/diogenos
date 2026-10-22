"""Test the Tmux feature."""

import pytest

from diogenos.component.catalog.tmux.config import TmuxConfig
from diogenos.component.catalog.tmux.tmux import TmuxPackage
from diogenos.feature.catalog.tmux import Tmux


@pytest.mark.feature
def test_tmux_contains_components() -> None:
    """Verify that the Tmux feature contains its components."""
    feature = Tmux()

    assert len(feature.components) == 2
    assert any(isinstance(component, TmuxPackage) for component in feature.components)
    assert any(isinstance(component, TmuxConfig) for component in feature.components)
