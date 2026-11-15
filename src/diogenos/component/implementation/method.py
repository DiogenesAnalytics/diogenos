"""Define installation method types."""

from abc import ABC
from abc import abstractmethod
from enum import Enum
from typing import Tuple

from diogenos.system.base import System


class InstallMethodType(Enum):
    """Define supported installation methods."""

    APT = "apt"
    SNAP = "snap"
    DOCKER = "docker"


class InstallMethodMixin(ABC):
    """Define the installation method interface."""

    METHOD: InstallMethodType


class APTInstallMixin(InstallMethodMixin):
    """Define the APT installation interface."""

    METHOD = InstallMethodType.APT

    @abstractmethod
    def install_apt(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install packages using APT."""


class SnapInstallMixin(InstallMethodMixin):
    """Define the Snap installation interface."""

    METHOD = InstallMethodType.SNAP

    @abstractmethod
    def install_snap(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install packages using Snap."""


class DockerInstallMixin(InstallMethodMixin):
    """Define the Docker installation interface."""

    METHOD = InstallMethodType.DOCKER

    @abstractmethod
    def install_docker(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install packages using Docker."""
