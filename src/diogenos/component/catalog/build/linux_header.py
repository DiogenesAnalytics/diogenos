"""Define the Linux kernel headers component."""

import subprocess
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.implementation.method import APTInstallMixin
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


PACKAGE_PREFIX = "linux-headers-"


def _get_kernel_headers_package(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> Optional[str]:
    """Return the package name for the running kernel."""
    result = run(
        ["uname", "-r"],
        capture_output=True,
        check=False,
        text=True,
    )

    if result.returncode != 0:
        return None

    kernel_version = result.stdout.strip()

    if not kernel_version:
        return None

    return f"{PACKAGE_PREFIX}{kernel_version}"


def _is_linux_kernel_headers_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether headers for the running kernel are installed."""
    package = _get_kernel_headers_package(run)

    if package is None:
        return False

    result = run(
        ["dpkg-query", "-W", "-f=${db:Status-Status}", package],
        capture_output=True,
        check=False,
        text=True,
    )

    return result.returncode == 0 and result.stdout.strip() == "installed"


class UbuntuLinuxKernelHeaders(
    UbuntuComponentImplementation,
    APTInstallMixin,
):
    """Define the Ubuntu implementation of Linux kernel headers."""

    DEFAULT_INSTALL_METHOD = InstallMethodType.APT

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Linux kernel headers implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install headers for the running kernel on Ubuntu."""
        package = _get_kernel_headers_package(self._run)

        if package is None:
            raise RuntimeError(
                "Unable to determine the running kernel version."
            )

        self.install_packages(system, (package,), method)

    def install_apt(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install packages using APT."""
        self._run(
            prepare_command(["apt-get", "update"], privileged=True),
            check=True,
        )
        self._run(
            prepare_command(
                ["apt-get", "install", "-y", *packages],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that headers for the running kernel are installed."""
        return _is_linux_kernel_headers_satisfied(self._run)


class DebianLinuxKernelHeaders(
    DebianComponentImplementation,
    APTInstallMixin,
):
    """Define the Debian implementation of Linux kernel headers."""

    DEFAULT_INSTALL_METHOD = InstallMethodType.APT

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian Linux kernel headers implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install headers for the running kernel on Debian."""
        package = _get_kernel_headers_package(self._run)

        if package is None:
            raise RuntimeError(
                "Unable to determine the running kernel version."
            )

        self.install_packages(system, (package,), method)

    def install_apt(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install packages using APT."""
        UbuntuLinuxKernelHeaders(run=self._run).install_apt(
            system,
            packages,
        )

    def verify(self, system: System) -> bool:
        """Verify that headers for the running kernel are installed."""
        return _is_linux_kernel_headers_satisfied(self._run)


class LinuxKernelHeaders(Component):
    """Represent the Linux kernel headers component."""

    registry_id = "linux_kernel_headers"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Linux kernel headers component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether headers for the running kernel are installed."""
        return _is_linux_kernel_headers_satisfied(self._run)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Linux kernel headers."""
        return (
            UbuntuLinuxKernelHeaders(run=self._run),
            DebianLinuxKernelHeaders(run=self._run),
        )
