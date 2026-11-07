"""Test the Firefox Dark Reader component."""

import json
import subprocess
from dataclasses import replace
from pathlib import Path
from typing import Callable

import pytest

from diogenos.component import ComponentImplementation
from diogenos.component.catalog.browser.firefox.dark_reader import (
    DARK_READER_EXTENSION_ID,
)
from diogenos.component.catalog.browser.firefox.dark_reader import (
    DARK_READER_INSTALL_URL,
)
from diogenos.component.catalog.browser.firefox.dark_reader import (
    FIREFOX_POLICY_DIRECTORY,
)
from diogenos.component.catalog.browser.firefox.dark_reader import FIREFOX_POLICY_FILE
from diogenos.component.catalog.browser.firefox.dark_reader import ArchFirefoxDarkReader
from diogenos.component.catalog.browser.firefox.dark_reader import (
    DebianFirefoxDarkReader,
)
from diogenos.component.catalog.browser.firefox.dark_reader import (
    FedoraFirefoxDarkReader,
)
from diogenos.component.catalog.browser.firefox.dark_reader import FirefoxDarkReader
from diogenos.component.catalog.browser.firefox.dark_reader import (
    FirefoxDarkReaderImplementation,
)
from diogenos.component.catalog.browser.firefox.dark_reader import (
    UbuntuFirefoxDarkReader,
)
from diogenos.component.implementation.execution import prepare_command
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.fixture
def system_with_platform(
    system: System,
) -> Callable[[str], System]:
    """Return a system with the specified operating system."""

    def create(operating_system: str) -> System:
        return replace(
            system,
            platform=replace(system.platform, os=operating_system),
        )

    return create


@pytest.mark.component
def test_firefox_dark_reader_registry_id() -> None:
    """Test the Firefox Dark Reader component registry identifier."""
    assert FirefoxDarkReader.registry_id == "firefox_dark_reader"


@pytest.mark.component
def test_firefox_dark_reader_is_satisfied(
    run_stub: RunStub,
    system: System,
) -> None:
    """Test that Firefox Dark Reader is satisfied when its policy is configured."""
    run_stub.stdout = json.dumps(
        {
            "policies": {
                "ExtensionSettings": {
                    DARK_READER_EXTENSION_ID: {
                        "installation_mode": "normal_installed",
                        "install_url": DARK_READER_INSTALL_URL,
                    },
                },
            },
        },
    )
    component = FirefoxDarkReader(run=run_stub)

    assert component.is_satisfied(system)

    assert run_stub.calls == [
        (
            prepare_command(
                ["cat", str(FIREFOX_POLICY_FILE)],
                privileged=True,
            ),
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_firefox_dark_reader_is_not_satisfied(
    run_stub: RunStub,
    system: System,
) -> None:
    """Test that Firefox Dark Reader is not satisfied without its policy."""
    run_stub.stdout = json.dumps({"policies": {}})
    component = FirefoxDarkReader(run=run_stub)

    assert not component.is_satisfied(system)


@pytest.mark.component
def test_firefox_dark_reader_implementations(
    run_stub: RunStub,
) -> None:
    """Test the implementations exposed by the component."""
    implementations = FirefoxDarkReader(run=run_stub).implementations()

    assert len(implementations) == 4
    assert isinstance(implementations[0], UbuntuFirefoxDarkReader)
    assert isinstance(implementations[1], DebianFirefoxDarkReader)
    assert isinstance(implementations[2], FedoraFirefoxDarkReader)
    assert isinstance(implementations[3], ArchFirefoxDarkReader)
    assert all(
        isinstance(implementation, ComponentImplementation)
        for implementation in implementations
    )


@pytest.mark.parametrize(
    ("implementation", "operating_system"),
    [
        (UbuntuFirefoxDarkReader, "ubuntu"),
        (DebianFirefoxDarkReader, "debian"),
        (FedoraFirefoxDarkReader, "fedora"),
        (ArchFirefoxDarkReader, "arch"),
    ],
)
@pytest.mark.component
def test_firefox_dark_reader_implementation_supports(
    run_stub: RunStub,
    implementation: Callable[..., ComponentImplementation],
    operating_system: str,
    system_with_platform: Callable[[str], System],
) -> None:
    """Test that each implementation supports its target operating system."""
    component = implementation(run=run_stub)

    assert component.supports(system_with_platform(operating_system))


@pytest.mark.parametrize(
    "implementation",
    [
        UbuntuFirefoxDarkReader,
        DebianFirefoxDarkReader,
        FedoraFirefoxDarkReader,
        ArchFirefoxDarkReader,
    ],
)
@pytest.mark.component
def test_firefox_dark_reader_implementation_rejects_unsupported_system(
    run_stub: RunStub,
    implementation: Callable[..., ComponentImplementation],
    system_with_platform: Callable[[str], System],
) -> None:
    """Test that each implementation rejects unsupported systems."""
    component = implementation(run=run_stub)

    assert not component.supports(system_with_platform("opensuse"))


@pytest.mark.component
def test_firefox_dark_reader_implementation_inheritance() -> None:
    """Test that platform implementations inherit shared behavior."""
    assert issubclass(
        UbuntuFirefoxDarkReader,
        FirefoxDarkReaderImplementation,
    )
    assert issubclass(
        DebianFirefoxDarkReader,
        FirefoxDarkReaderImplementation,
    )
    assert issubclass(
        FedoraFirefoxDarkReader,
        FirefoxDarkReaderImplementation,
    )
    assert issubclass(
        ArchFirefoxDarkReader,
        FirefoxDarkReaderImplementation,
    )


@pytest.mark.component
def test_firefox_dark_reader_install(
    system: System,
) -> None:
    """Test installing the Firefox Dark Reader policy."""
    existing_policy = {
        "policies": {
            "DisableAppUpdate": True,
        },
    }

    installed_policy = {}

    calls = []

    def run(
        command: list[str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        calls.append((command, kwargs))

        if command[-2:] == ["cat", str(FIREFOX_POLICY_FILE)]:
            return subprocess.CompletedProcess(
                command,
                0,
                stdout=json.dumps(existing_policy),
                stderr="",
            )

        if command[-4] == "-m":
            installed_policy.update(
                json.loads(Path(command[-2]).read_text(encoding="utf-8")),
            )

        return subprocess.CompletedProcess(
            command,
            0,
            stdout="",
            stderr="",
        )

    component = UbuntuFirefoxDarkReader(run=run)

    component.install(system)

    assert installed_policy == {
        "policies": {
            "DisableAppUpdate": True,
            "ExtensionSettings": {
                DARK_READER_EXTENSION_ID: {
                    "installation_mode": "normal_installed",
                    "install_url": DARK_READER_INSTALL_URL,
                },
            },
        },
    }

    assert calls[0] == (
        prepare_command(
            [
                "install",
                "-d",
                "-m",
                "0755",
                str(FIREFOX_POLICY_DIRECTORY),
            ],
            privileged=True,
        ),
        {"check": True},
    )

    assert calls[1] == (
        prepare_command(
            ["cat", str(FIREFOX_POLICY_FILE)],
            privileged=True,
        ),
        {
            "capture_output": True,
            "check": False,
            "text": True,
        },
    )

    assert calls[2][0][-4:] == [
        "-m",
        "0644",
        calls[2][0][-2],
        str(FIREFOX_POLICY_FILE),
    ]
    assert calls[2][1] == {"check": True}


@pytest.mark.component
def test_firefox_dark_reader_install_failure(
    system: System,
) -> None:
    """Test that installation stops when creating the policy directory fails."""
    run_stub = RunStub(returncode=1)
    component = UbuntuFirefoxDarkReader(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        component.install(system)

    assert run_stub.calls == [
        (
            prepare_command(
                [
                    "install",
                    "-d",
                    "-m",
                    "0755",
                    str(FIREFOX_POLICY_DIRECTORY),
                ],
                privileged=True,
            ),
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_firefox_dark_reader_verify(
    run_stub: RunStub,
    system: System,
) -> None:
    """Test successful verification of the Firefox Dark Reader policy."""
    run_stub.stdout = json.dumps(
        {
            "policies": {
                "ExtensionSettings": {
                    DARK_READER_EXTENSION_ID: {
                        "installation_mode": "normal_installed",
                        "install_url": DARK_READER_INSTALL_URL,
                    },
                },
            },
        },
    )
    component = UbuntuFirefoxDarkReader(run=run_stub)

    assert component.verify(system)

    assert run_stub.calls == [
        (
            prepare_command(
                ["cat", str(FIREFOX_POLICY_FILE)],
                privileged=True,
            ),
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_firefox_dark_reader_verify_failure(
    run_stub: RunStub,
    system: System,
) -> None:
    """Test unsuccessful verification when the policy is not configured."""
    run_stub.stdout = json.dumps({"policies": {}})
    component = UbuntuFirefoxDarkReader(run=run_stub)

    assert not component.verify(system)


@pytest.mark.component
def test_firefox_dark_reader_policy_paths() -> None:
    """Test the Firefox policy paths."""
    assert FIREFOX_POLICY_DIRECTORY == Path("/etc/firefox/policies")
    assert FIREFOX_POLICY_FILE == FIREFOX_POLICY_DIRECTORY / "policies.json"
