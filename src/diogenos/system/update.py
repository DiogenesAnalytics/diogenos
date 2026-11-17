"""Define system update operations."""

from diogenos.component.internal.system_update import SystemUpdate
from diogenos.resolver.implementations import ImplementationResolver
from diogenos.system.base import System


class SystemUpdater:
    """Update the operating system."""

    def __init__(self) -> None:
        """Initialize the system updater."""
        self._resolver = ImplementationResolver()

    def update(self, system: System) -> None:
        """Update the operating system."""
        component = SystemUpdate()
        implementation = self._resolver.resolve(component, system)
        implementation.install(system)
