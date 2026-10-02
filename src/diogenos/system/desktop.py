"""Detect and represent the desktop environment of a system."""

import os
from dataclasses import dataclass


DESKTOP_NAMES = {
    "GNOME": "GNOME",
    "GNOME-Flashback": "GNOME Flashback",
    "KDE": "KDE Plasma",
    "XFCE": "Xfce",
    "LXDE": "LXDE",
    "LXQt": "LXQt",
    "MATE": "MATE",
    "Cinnamon": "Cinnamon",
    "X-CINNAMON": "Cinnamon",
    "Unity": "Unity",
    "Pantheon": "Pantheon",
    "DDE": "Deepin",
    "Deepin": "Deepin",
    "TDE": "Trinity",
    "EDE": "EDE",
    "COSMIC": "COSMIC",
    "Phosh": "Phosh",
}


@dataclass(frozen=True)
class Desktop:
    """Represent the desktop environment of a system."""

    name: str
    pretty_name: str


class DesktopDetector:
    """Detect the desktop environment of the current system."""

    def detect(self) -> Desktop:
        """Detect the desktop environment of the current system."""
        name = os.getenv("XDG_CURRENT_DESKTOP")

        if not name:
            name = os.getenv("DESKTOP_SESSION", "")

        name = name.strip()
        identifiers = name.split(":")

        pretty_name = next(
            (
                DESKTOP_NAMES[identifier]
                for identifier in identifiers
                if identifier in DESKTOP_NAMES
            ),
            name,
        )

        return Desktop(
            name=name,
            pretty_name=pretty_name,
        )
