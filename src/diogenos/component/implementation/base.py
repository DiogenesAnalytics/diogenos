"""Define the component implementation abstraction."""

from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Type

from diogenos.component.implementation.method.base import Method
from diogenos.component.implementation.method.options import MethodOptions
from diogenos.component.implementation.method.types import MethodType
from diogenos.system.base import System


class ComponentImplementation(ABC):
    """Define a component implementation."""

    OS: str

    METHODS: Dict[
        MethodType,
        Tuple[Type[Method], MethodOptions],
    ] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Compose installation methods from parent implementations."""
        super().__init_subclass__(**kwargs)

        methods: Dict[
            MethodType,
            Tuple[Type[Method], MethodOptions],
        ] = {}

        for parent in cls.__bases__:
            parent_methods = getattr(parent, "METHODS", {})

            for method_type, method in parent_methods.items():
                if method_type in methods:
                    raise TypeError(
                        f"duplicate installation method "
                        f"{method_type.value} in "
                        f"{cls.__name__}",
                    )

                methods[method_type] = method

        methods.update(cls.__dict__.get("METHODS", {}))

        cls.METHODS = methods

    def supports(self, system: System) -> bool:
        """Determine whether this implementation supports the system."""
        return system.platform.os == self.OS

    def resolve_method(
        self,
        method_type: Optional[MethodType] = None,
    ) -> Optional[Method]:
        """Resolve an installation method."""
        if not self.METHODS:
            if method_type is not None:
                raise ValueError(
                    f"unsupported installation method: {method_type.value}",
                )

            return None

        selected_method_type = (
            method_type if method_type is not None else next(iter(self.METHODS))
        )

        if selected_method_type not in self.METHODS:
            raise ValueError(
                f"unsupported installation method: {selected_method_type.value}",
            )

        method_class, options = self.METHODS[selected_method_type]

        return method_class(options)

    @abstractmethod
    def install(self, system: System) -> None:
        """Install the component."""

    @abstractmethod
    def verify(self, system: System) -> bool:
        """Verify that the component was installed correctly."""
