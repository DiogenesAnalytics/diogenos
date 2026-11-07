"""Test the GTK Emacs shortcuts feature."""

from diogenos.feature.catalog.emacs_shortcuts import GtkEmacsShortcuts


def test_gtk_emacs_shortcuts_registry_id() -> None:
    """Test the GTK Emacs shortcuts feature registry identifier."""
    assert GtkEmacsShortcuts.registry_id == "gtk_emacs_shortcuts"
