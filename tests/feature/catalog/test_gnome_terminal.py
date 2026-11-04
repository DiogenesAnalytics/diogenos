"""Test the GNOME Terminal feature."""

from diogenos.feature.catalog.gnome_terminal import GnomeTerminal


def test_gnome_terminal_registry_id() -> None:
    """Test the GNOME Terminal feature registry identifier."""
    assert GnomeTerminal.registry_id == "gnome_terminal"
