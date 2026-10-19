"""Define resolved components."""

from typing import NamedTuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation


class ResolvedComponent(NamedTuple):
    """Pair a component with its selected implementation."""

    component: Component
    implementation: ComponentImplementation
