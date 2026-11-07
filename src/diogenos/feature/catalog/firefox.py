"""Define the Firefox feature."""

from diogenos.component.catalog.browser.firefox.dark_reader import FirefoxDarkReader
from diogenos.component.catalog.browser.firefox.firefox import FirefoxPackage
from diogenos.feature import Feature


class Firefox(Feature):
    """Represent the Firefox feature."""

    registry_id = "firefox"

    def __init__(self) -> None:
        """Initialize the Firefox feature."""
        super().__init__(
            components=(
                FirefoxPackage(),
                FirefoxDarkReader(),
            ),
        )
