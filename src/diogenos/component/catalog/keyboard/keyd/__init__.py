"""Define keyd components."""

from diogenos.component.catalog.keyboard.keyd.application_config import (
    KeydApplicationConfig,
)
from diogenos.component.catalog.keyboard.keyd.application_config import (
    UbuntuKeydApplicationConfig,
)
from diogenos.component.catalog.keyboard.keyd.application_mapper import (
    KeydApplicationMapper,
)
from diogenos.component.catalog.keyboard.keyd.application_mapper import (
    UbuntuKeydApplicationMapper,
)
from diogenos.component.catalog.keyboard.keyd.configuration import KeydConfiguration
from diogenos.component.catalog.keyboard.keyd.configuration import (
    UbuntuKeydConfiguration,
)
from diogenos.component.catalog.keyboard.keyd.emacs_keymap import EmacsKeymap
from diogenos.component.catalog.keyboard.keyd.emacs_keymap import UbuntuEmacsKeymap
from diogenos.component.catalog.keyboard.keyd.keyd import Keyd
from diogenos.component.catalog.keyboard.keyd.keyd import UbuntuKeyd
from diogenos.component.catalog.keyboard.keyd.macos_keymap import MacOSKeymap
from diogenos.component.catalog.keyboard.keyd.macos_keymap import UbuntuMacOSKeymap
from diogenos.component.catalog.keyboard.keyd.user import KeydUserConfig
from diogenos.component.catalog.keyboard.keyd.user import UbuntuKeydUserConfig


__all__ = [
    "EmacsKeymap",
    "Keyd",
    "KeydApplicationConfig",
    "KeydApplicationMapper",
    "KeydConfiguration",
    "KeydUserConfig",
    "MacOSKeymap",
    "UbuntuEmacsKeymap",
    "UbuntuKeyd",
    "UbuntuKeydApplicationConfig",
    "UbuntuKeydApplicationMapper",
    "UbuntuKeydConfiguration",
    "UbuntuKeydUserConfig",
    "UbuntuMacOSKeymap",
]
