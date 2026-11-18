"""Define the GNOME Super key component."""

import subprocess
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


MUTTER_SCHEMA = "org.gnome.mutter"
OVERLAY_KEY = "overlay-key"
OVERLAY_KEY_VALUE = ""


def _is_gnome_super_key_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether the standalone Super key behavior is disabled."""
    result = run(
        ["gsettings", "get", MUTTER_SCHEMA, OVERLAY_KEY],
        capture_output=True,
        check=False,
        text=True,
    )

    return result.returncode == 0 and result.stdout.strip() == f"{OVERLAY_KEY_VALUE!r}"


class UbuntuGnomeSuperKey(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of the GNOME Super key."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu GNOME Super key implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Disable the standalone Super key behavior on Ubuntu."""
        self._run(
            [
                "gsettings",
                "set",
                MUTTER_SCHEMA,
                OVERLAY_KEY,
                OVERLAY_KEY_VALUE,
            ],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that the standalone Super key behavior is disabled."""
        return _is_gnome_super_key_satisfied(self._run)


class GnomeSuperKey(Component):
    """Represent the GNOME Super key configuration."""

    registry_id = "gnome_super_key"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GNOME Super key component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether the standalone Super key behavior is disabled."""
        return _is_gnome_super_key_satisfied(self._run)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for the GNOME Super key."""
        return (UbuntuGnomeSuperKey(run=self._run),)
