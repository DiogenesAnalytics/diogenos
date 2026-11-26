"""Define the Keyd application mapper component."""

import subprocess
from pathlib import Path
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.dependency import Dependency
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


KEYD_EXTENSION_SOURCE = Path("/usr/local/share/keyd/gnome-extension-45")
KEYD_EXTENSION_UUID = "keyd@keyd.rvaiya.github.com"

MAPPER_EXECUTABLE = "/usr/local/bin/keyd-application-mapper"

SERVICE_DIRECTORY = Path.home() / ".config/systemd/user"
SERVICE_PATH = SERVICE_DIRECTORY / "keyd-application-mapper.service"

SERVICE_CONTENT = """\
[Unit]
Description=Keyd Application Mapper
After=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 -u /usr/local/bin/keyd-application-mapper --verbose
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
"""


def _get_extension_directory() -> Path:
    """Return the Keyd GNOME extension directory."""
    return Path.home() / ".local/share/gnome-shell/extensions" / KEYD_EXTENSION_UUID


def _is_extension_enabled(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether the Keyd GNOME extension is enabled."""
    result = run(
        ["gnome-extensions", "info", KEYD_EXTENSION_UUID],
        capture_output=True,
        check=False,
        text=True,
    )

    return (
        result.returncode == 0
        and "Enabled: Yes" in result.stdout
        and "State: ACTIVE" in result.stdout
    )


def _is_mapper_service_enabled(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether the mapper service is enabled."""
    return _validate_user_service(run, "is-enabled") and _validate_user_service(
        run, "is-active"
    )


def _validate_user_service(
    run: Callable[..., subprocess.CompletedProcess[str]],
    action: str,
) -> bool:
    """Validate the requested mapper service state."""
    result = run(
        ["systemctl", "--user", action, "keyd-application-mapper.service"],
        capture_output=True,
        check=False,
        text=True,
    )

    return result.returncode == 0


class UbuntuKeydApplicationMapper(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of the Keyd application mapper."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu application mapper."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install and enable the Keyd application mapper."""
        extension_directory = _get_extension_directory()

        self._run(
            ["rm", "-rf", str(extension_directory)],
            check=True,
        )
        self._run(
            ["mkdir", "-p", str(extension_directory.parent)],
            check=True,
        )
        self._run(
            ["cp", "-r", str(KEYD_EXTENSION_SOURCE), str(extension_directory)],
            check=True,
        )

        self._run(
            ["gnome-extensions", "enable", KEYD_EXTENSION_UUID],
            check=True,
        )

        self._run(
            ["mkdir", "-p", str(SERVICE_DIRECTORY)],
            check=True,
        )
        self._run(
            ["tee", str(SERVICE_PATH)],
            input=SERVICE_CONTENT,
            capture_output=True,
            check=True,
            text=True,
        )

        self._run(
            ["systemctl", "--user", "daemon-reload"],
            check=True,
        )
        self._run(
            [
                "systemctl",
                "--user",
                "enable",
                "--now",
                "keyd-application-mapper.service",
            ],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that the extension and mapper service are operational."""
        return _is_extension_enabled(self._run) and _is_mapper_service_enabled(
            self._run
        )


class KeydApplicationMapper(Component):
    """Represent the Keyd application mapper."""

    registry_id = "keyd.application_mapper"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Keyd application mapper."""
        self._run = run

    def dependencies(self) -> Tuple[Dependency, ...]:
        """Return the component dependencies."""
        return (Dependency("keyd.config.user"),)

    def is_satisfied(self, system: System) -> bool:
        """Determine whether the application mapper is configured."""
        return _is_extension_enabled(self._run) and _is_mapper_service_enabled(
            self._run
        )

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the available application mapper implementations."""
        return (UbuntuKeydApplicationMapper(run=self._run),)
