"""Test the Emacs shortcuts feature."""

import pytest

from diogenos.component.catalog.keyboard.emacs_keymap import EmacsKeymap
from diogenos.component.catalog.keyboard.gtk import GtkEmacsKeymap
from diogenos.component.catalog.keyboard.keyd import Keyd
from diogenos.feature.catalog.emacs_shortcuts import EmacsShortcuts


@pytest.mark.feature
def test_emacs_shortcuts_contains_keyboard_components() -> None:
    """Verify that the Emacs shortcuts feature contains its keyboard components."""
    feature = EmacsShortcuts()

    assert len(feature.components) == 3
    assert isinstance(feature.components[0], Keyd)
    assert isinstance(feature.components[1], EmacsKeymap)
    assert isinstance(feature.components[2], GtkEmacsKeymap)
