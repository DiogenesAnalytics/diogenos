"""Define the component implementation abstraction."""

from abc import ABC
from abc import abstractmethod
from typing import Optional
from typing import Tuple

from diogenos.component.implementation.method import InstallMethodMixin
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


class ComponentImplementation(ABC):
    """Define a component implementation."""

    OS: str
    DEFAULT_INSTALL_METHOD: Optional[InstallMethodType] = None

    def supports(self, system: System) -> bool:
        """Determine whether this implementation supports the system."""
        return system.platform.os == self.OS

    @property
    def install_methods(self) -> Tuple[InstallMethodType, ...]:
        """Get the installation methods supported by this implementation."""
        return tuple(
            implementation.METHOD
            for implementation in type(self).__mro__
            if issubclass(implementation, InstallMethodMixin)
            and implementation is not InstallMethodMixin
            and "METHOD" in implementation.__dict__
        )

    def install_packages(
        self,
        system: System,
        packages: Tuple[str, ...],
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install packages using the selected installation method."""
        if method is None:
            method = self.DEFAULT_INSTALL_METHOD

        if method is None:
            raise ValueError("No installation method specified.")

        if method not in self.install_methods:
            raise ValueError(f"Unsupported installation method: {method.value}")

        installer = getattr(self, f"install_{method.value}")
        installer(system, packages)

    @abstractmethod
    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install the component."""

    @abstractmethod
    def verify(self, system: System) -> bool:
        """Verify that the component was installed correctly."""
