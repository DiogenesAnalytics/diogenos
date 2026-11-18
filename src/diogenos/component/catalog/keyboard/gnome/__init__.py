"""Define GNOME keyboard configuration components."""

from diogenos.component.catalog.keyboard.gnome.overview_keybindings import (
    GnomeOverviewKeybindings,
)
from diogenos.component.catalog.keyboard.gnome.super_key import GnomeSuperKey
from diogenos.component.catalog.keyboard.gnome.workspace_navigation import (
    GnomeWorkspaceNavigation,
)


__all__ = [
    "GnomeOverviewKeybindings",
    "GnomeSuperKey",
    "GnomeWorkspaceNavigation",
]
