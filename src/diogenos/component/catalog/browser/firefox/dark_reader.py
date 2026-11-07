"""Define the Firefox Dark Reader component."""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import Tuple

from diogenos.component import ArchComponentImplementation
from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import FedoraComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.execution import prepare_command
from diogenos.system.base import System


FIREFOX_POLICY_DIRECTORY = Path("/etc/firefox/policies")
FIREFOX_POLICY_FILE = FIREFOX_POLICY_DIRECTORY / "policies.json"

DARK_READER_EXTENSION_ID = "addon@darkreader.org"
DARK_READER_INSTALL_URL = (
    "https://addons.mozilla.org/firefox/downloads/latest/"
    "addon@darkreader.org/latest.xpi"
)


class FirefoxDarkReaderImplementation:
    """Provide shared Firefox Dark Reader policy management."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Firefox Dark Reader implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Configure Firefox to install Dark Reader."""
        self._run(
            prepare_command(
                ["install", "-d", "-m", "0755", str(FIREFOX_POLICY_DIRECTORY)],
                privileged=True,
            ),
            check=True,
        )

        policy = self._read_policy()

        policies = policy.setdefault("policies", {})
        extension_settings = policies.setdefault("ExtensionSettings", {})

        extension_settings[DARK_READER_EXTENSION_ID] = {
            "installation_mode": "normal_installed",
            "install_url": DARK_READER_INSTALL_URL,
        }

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".json",
        ) as policy_file:
            json.dump(policy, policy_file, indent=4)
            policy_file.write("\n")
            policy_file.flush()

            self._run(
                prepare_command(
                    [
                        "install",
                        "-m",
                        "0644",
                        policy_file.name,
                        str(FIREFOX_POLICY_FILE),
                    ],
                    privileged=True,
                ),
                check=True,
            )

    def verify(self, system: System) -> bool:
        """Verify that Firefox is configured to install Dark Reader."""
        return self._is_configured()

    def _read_policy(self) -> Dict[str, Any]:
        """Read the existing Firefox policy configuration."""
        result = self._run(
            prepare_command(
                ["cat", str(FIREFOX_POLICY_FILE)],
                privileged=True,
            ),
            capture_output=True,
            check=False,
            text=True,
        )

        if result.returncode != 0:
            return {}

        policy = json.loads(result.stdout)

        if not isinstance(policy, dict):
            raise ValueError("Firefox policy configuration must be a JSON object.")

        return policy

    def _is_configured(self) -> bool:
        """Determine whether the Dark Reader policy is configured."""
        try:
            policy = self._read_policy()
        except (json.JSONDecodeError, OSError, ValueError):
            return False

        policies = policy.get("policies", {})
        if not isinstance(policies, dict):
            return False

        extension_settings = policies.get("ExtensionSettings", {})
        if not isinstance(extension_settings, dict):
            return False

        return bool(
            extension_settings.get(DARK_READER_EXTENSION_ID)
            == {
                "installation_mode": "normal_installed",
                "install_url": DARK_READER_INSTALL_URL,
            }
        )


class UbuntuFirefoxDarkReader(
    FirefoxDarkReaderImplementation,
    UbuntuComponentImplementation,
):
    """Represent the Ubuntu Firefox Dark Reader implementation."""


class DebianFirefoxDarkReader(
    FirefoxDarkReaderImplementation,
    DebianComponentImplementation,
):
    """Represent the Debian Firefox Dark Reader implementation."""


class FedoraFirefoxDarkReader(
    FirefoxDarkReaderImplementation,
    FedoraComponentImplementation,
):
    """Represent the Fedora Firefox Dark Reader implementation."""


class ArchFirefoxDarkReader(
    FirefoxDarkReaderImplementation,
    ArchComponentImplementation,
):
    """Represent the Arch Linux Firefox Dark Reader implementation."""


class FirefoxDarkReader(Component):
    """Represent the Firefox Dark Reader component."""

    registry_id = "firefox_dark_reader"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Firefox Dark Reader component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Firefox is configured to install Dark Reader."""
        implementation = FirefoxDarkReaderImplementation(run=self._run)
        return implementation.verify(system)

    def implementations(self) -> Tuple[ComponentImplementation, ...]:
        """Return the available implementations."""
        return (
            UbuntuFirefoxDarkReader(run=self._run),
            DebianFirefoxDarkReader(run=self._run),
            FedoraFirefoxDarkReader(run=self._run),
            ArchFirefoxDarkReader(run=self._run),
        )
