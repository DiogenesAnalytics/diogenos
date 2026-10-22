"""Define the Tmux configuration component."""

import subprocess
from pathlib import Path
from typing import Callable
from typing import Tuple

from diogenos.component import AlpineComponentImplementation
from diogenos.component import ArchComponentImplementation
from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import FedoraComponentImplementation
from diogenos.component import OpenSUSEComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.dependency import Dependency
from diogenos.system.base import System


REPOSITORY = "https://github.com/DiogenesAnalytics/.tmux.git"


def _is_satisfied(home: Path) -> bool:
    """Determine whether the Tmux configuration is installed."""
    repository = home / ".tmux"
    config = home / ".tmux.conf"
    local_config = home / ".tmux.conf.local"

    return (
        (repository / ".tmux.conf").is_file()
        and config.is_symlink()
        and config.resolve() == (repository / ".tmux.conf").resolve()
        and local_config.is_file()
    )


class TmuxConfigImplementation:
    """Define the shared Tmux configuration behavior."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Tmux configuration implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install the Tmux configuration."""
        home = Path.home()
        repository = home / ".tmux"
        local_config = home / ".tmux.conf.local"

        if not repository.exists():
            self._run(
                ["git", "clone", REPOSITORY],
                check=True,
                cwd=home,
            )

        self._run(
            ["ln", "-s", "-f", ".tmux/.tmux.conf", ".tmux.conf"],
            check=True,
            cwd=home,
        )

        if not local_config.exists():
            self._run(
                ["cp", ".tmux/.tmux.conf.local", ".tmux.conf.local"],
                check=True,
                cwd=home,
            )

    def verify(self, system: System) -> bool:
        """Verify that the Tmux configuration is installed."""
        return _is_satisfied(Path.home())


class UbuntuTmuxConfig(
    TmuxConfigImplementation,
    UbuntuComponentImplementation,
):
    """Define the Ubuntu implementation of Tmux configuration."""


class DebianTmuxConfig(
    TmuxConfigImplementation,
    DebianComponentImplementation,
):
    """Define the Debian implementation of Tmux configuration."""


class FedoraTmuxConfig(
    TmuxConfigImplementation,
    FedoraComponentImplementation,
):
    """Define the Fedora implementation of Tmux configuration."""


class ArchTmuxConfig(
    TmuxConfigImplementation,
    ArchComponentImplementation,
):
    """Define the Arch Linux implementation of Tmux configuration."""


class OpenSUSETmuxConfig(
    TmuxConfigImplementation,
    OpenSUSEComponentImplementation,
):
    """Define the openSUSE implementation of Tmux configuration."""


class AlpineTmuxConfig(
    TmuxConfigImplementation,
    AlpineComponentImplementation,
):
    """Define the Alpine implementation of Tmux configuration."""


class TmuxConfig(Component):
    """Represent the Tmux configuration component."""

    registry_id = "tmux.config"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Tmux configuration component."""
        self._run = run

    def dependencies(self) -> Tuple[Dependency, ...]:
        """Return the component dependencies."""
        return (Dependency("git"),)

    def is_satisfied(self, system: System) -> bool:
        """Determine whether the Tmux configuration is installed."""
        return _is_satisfied(Path.home())

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Tmux configuration."""
        return (
            UbuntuTmuxConfig(run=self._run),
            DebianTmuxConfig(run=self._run),
            FedoraTmuxConfig(run=self._run),
            ArchTmuxConfig(run=self._run),
            OpenSUSETmuxConfig(run=self._run),
            AlpineTmuxConfig(run=self._run),
        )
