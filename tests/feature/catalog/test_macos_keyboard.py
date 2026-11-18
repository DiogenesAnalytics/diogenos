"""Test the macOS keyboard feature."""

import pytest

from diogenos.feature.catalog.macos_keyboard import MacOSKeyboard


@pytest.mark.feature
def test_macos_keyboard_registry_id() -> None:
    """Test the macOS keyboard feature registry ID."""
    assert MacOSKeyboard.registry_id == "macos_keyboard"
