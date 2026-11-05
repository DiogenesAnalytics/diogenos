"""Define the GNOME color scheme component."""

import subprocess
from typing import Callable
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.system.base import System


COLOR_SCHEME_SCHEMA = "org.gnome.desktop.interface"
COLOR_SCHEME_KEY = "color-scheme"


def verify_color_scheme(
    run: Callable[..., subprocess.CompletedProcess[str]],
    color_scheme: str,
) -> bool:
    """Verify the configured GNOME color scheme."""
    result = run(
        [
            "gsettings",
            "get",
            COLOR_SCHEME_SCHEMA,
            COLOR_SCHEME_KEY,
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    return result.returncode == 0 and result.stdout.strip() == f"{color_scheme!r}"


class UbuntuGnomeColorScheme(UbuntuComponentImplementation):
    """Represent the Ubuntu GNOME color scheme implementation."""

    def __init__(
        self,
        color_scheme: str,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GNOME color scheme implementation."""
        self._color_scheme = color_scheme
        self._run = run

    def install(self, system: System) -> None:
        """Set the GNOME color scheme."""
        self._run(
            [
                "gsettings",
                "set",
                COLOR_SCHEME_SCHEMA,
                COLOR_SCHEME_KEY,
                self._color_scheme,
            ],
            check=True,
            text=True,
        )

    def verify(self, system: System) -> bool:
        """Verify the GNOME color scheme."""
        return verify_color_scheme(self._run, self._color_scheme)


class GnomeColorScheme(Component):
    """Represent the GNOME color scheme."""

    registry_id = "gnome_color_scheme"

    def __init__(
        self,
        color_scheme: str,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GNOME color scheme component."""
        self._color_scheme = color_scheme
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether the GNOME color scheme is configured."""
        return verify_color_scheme(self._run, self._color_scheme)

    def implementations(self) -> Tuple[ComponentImplementation, ...]:
        """Return the available implementations."""
        return (
            UbuntuGnomeColorScheme(
                color_scheme=self._color_scheme,
                run=self._run,
            ),
        )
