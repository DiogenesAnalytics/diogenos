"""Define Docker installation options."""

from dataclasses import dataclass
from typing import Optional
from typing import Tuple

from .options import MethodOptions


@dataclass
class DockerOptions(MethodOptions):
    """Define Docker installation options."""

    detach: bool = True
    restart: Optional[str] = None
    environment: Tuple[str, ...] = ()
    ports: Tuple[str, ...] = ()
    volumes: Tuple[str, ...] = ()
