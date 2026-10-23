"""Test the Pulsar component."""

import json
import subprocess
from pathlib import Path
from typing import Any
from typing import Dict
from typing import cast
from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from diogenos.component import ComponentImplementation
from diogenos.component.catalog.pulsar.pulsar import PULSAR_RELEASE_URL
from diogenos.component.catalog.pulsar.pulsar import DebianPulsar
from diogenos.component.catalog.pulsar.pulsar import PulsarPackage
from diogenos.component.catalog.pulsar.pulsar import UbuntuPulsar
from diogenos.system.base import System


@pytest.fixture
def run() -> Mock:
    """Provide a mocked subprocess runner."""
    return Mock(
        return_value=subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="Pulsar version",
            stderr="",
        ),
    )


@pytest.fixture
def system() -> System:
    """Provide a system with AMD64 architecture."""
    return Mock(
        hardware=Mock(architecture="amd64"),
    )


@pytest.fixture
def release() -> Dict[str, Any]:
    """Provide release metadata containing Debian packages."""
    return {
        "assets": [
            {
                "name": "Linux.pulsar_1.132.1_amd64.deb",
                "browser_download_url": (
                    "https://example.com/Linux.pulsar_1.132.1_amd64.deb"
                ),
            },
            {
                "name": "ARM.Linux.pulsar_1.132.1_arm64.deb",
                "browser_download_url": (
                    "https://example.com/ARM.Linux.pulsar_1.132.1_arm64.deb"
                ),
            },
        ],
    }


@pytest.mark.component
def test_pulsar_package_registry_id() -> None:
    """Test the Pulsar component registry identifier."""
    assert PulsarPackage.registry_id == "pulsar"


@pytest.mark.component
def test_pulsar_package_is_satisfied(
    run: Mock,
    system: System,
) -> None:
    """Test that Pulsar is satisfied when its executable succeeds."""
    component = PulsarPackage(run=run)

    assert component.is_satisfied(system)

    run.assert_called_once_with(
        ["pulsar", "--version"],
        capture_output=True,
        check=False,
        text=True,
    )


@pytest.mark.component
def test_pulsar_package_is_not_satisfied(
    run: Mock,
    system: System,
) -> None:
    """Test that Pulsar is not satisfied when its executable fails."""
    run.return_value = subprocess.CompletedProcess(
        args=[],
        returncode=1,
        stdout="",
        stderr="not found",
    )
    component = PulsarPackage(run=run)

    assert not component.is_satisfied(system)


@pytest.mark.component
def test_pulsar_package_implementations(run: Mock) -> None:
    """Test the implementations exposed by the Pulsar component."""
    implementations = PulsarPackage(run=run).implementations()

    assert len(implementations) == 2
    assert isinstance(implementations[0], UbuntuPulsar)
    assert isinstance(implementations[1], DebianPulsar)
    assert all(
        isinstance(implementation, ComponentImplementation)
        for implementation in implementations
    )


@pytest.mark.parametrize(
    ("architecture", "asset_name"),
    [
        ("amd64", "Linux.pulsar_1.132.1_amd64.deb"),
        ("arm64", "ARM.Linux.pulsar_1.132.1_arm64.deb"),
    ],
)
@pytest.mark.component
def test_ubuntu_pulsar_install(
    monkeypatch: MonkeyPatch,
    run: Mock,
    release: Dict[str, Any],
    tmp_path: Path,
    architecture: str,
    asset_name: str,
) -> None:
    """Test installing the matching Pulsar Debian package."""
    system = Mock(
        hardware=Mock(architecture=architecture),
    )

    response = Mock()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)
    response.read.return_value = json.dumps(release).encode()

    def load_release(response_object: Any) -> Dict[str, Any]:
        """Decode the mocked GitHub release response."""
        return cast(
            Dict[str, Any],
            json.loads(response_object.read().decode()),
        )

    urlopen = Mock(return_value=response)
    urlretrieve = Mock()

    monkeypatch.setattr(
        "diogenos.component.catalog.pulsar.pulsar.urllib.request.urlopen",
        urlopen,
    )
    monkeypatch.setattr(
        "diogenos.component.catalog.pulsar.pulsar.json.load",
        load_release,
    )
    monkeypatch.setattr(
        "diogenos.component.catalog.pulsar.pulsar.tempfile.TemporaryDirectory",
        lambda: Mock(
            __enter__=Mock(return_value=str(tmp_path)),
            __exit__=Mock(return_value=False),
        ),
    )
    monkeypatch.setattr(
        "diogenos.component.catalog.pulsar.pulsar.urllib.request.urlretrieve",
        urlretrieve,
    )

    component = UbuntuPulsar(run=run)
    component.install(system)

    request = urlopen.call_args.args[0]

    assert request.full_url == PULSAR_RELEASE_URL
    assert request.get_header("Accept") == "application/vnd.github+json"

    expected_url = next(
        asset["browser_download_url"]
        for asset in release["assets"]
        if asset["name"] == asset_name
    )

    urlretrieve.assert_called_once_with(
        expected_url,
        tmp_path / "pulsar.deb",
    )

    run.assert_called_once_with(
        [
            "apt-get",
            "install",
            "-y",
            str(tmp_path / "pulsar.deb"),
        ],
        check=True,
    )


@pytest.mark.component
def test_ubuntu_pulsar_rejects_unsupported_architecture(
    run: Mock,
) -> None:
    """Test that unsupported architectures are rejected."""
    system = Mock(
        hardware=Mock(architecture="riscv64"),
    )
    component = UbuntuPulsar(run=run)

    with pytest.raises(RuntimeError, match="unsupported Pulsar architecture"):
        component.install(system)

    run.assert_not_called()


@pytest.mark.component
def test_ubuntu_pulsar_rejects_missing_package(
    monkeypatch: MonkeyPatch,
    run: Mock,
    system: System,
) -> None:
    """Test that installation fails when no matching package exists."""
    response = Mock()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)

    urlopen = Mock(return_value=response)

    monkeypatch.setattr(
        "diogenos.component.catalog.pulsar.pulsar.urllib.request.urlopen",
        urlopen,
    )
    monkeypatch.setattr(
        "diogenos.component.catalog.pulsar.pulsar.json.load",
        lambda _: {"assets": []},
    )

    component = UbuntuPulsar(run=run)

    with pytest.raises(RuntimeError, match="no Pulsar .deb package found"):
        component.install(system)

    run.assert_not_called()


@pytest.mark.component
def test_ubuntu_pulsar_verify(
    run: Mock,
    system: System,
) -> None:
    """Test successful verification of Pulsar."""
    component = UbuntuPulsar(run=run)

    assert component.verify(system)

    run.assert_called_once_with(
        ["pulsar", "--version"],
        capture_output=True,
        check=False,
        text=True,
    )


def test_ubuntu_pulsar_verify_failure(
    run: Mock,
    system: System,
) -> None:
    """Test unsuccessful verification of Pulsar."""
    run.return_value = subprocess.CompletedProcess(
        args=[],
        returncode=1,
        stdout="",
        stderr="error",
    )
    component = UbuntuPulsar(run=run)

    assert not component.verify(system)


def test_debian_pulsar_install(
    run: Mock,
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that the Debian implementation delegates installation."""
    install = Mock()
    monkeypatch.setattr(UbuntuPulsar, "install", install)

    component = DebianPulsar(run=run)
    component.install(system)

    install.assert_called_once_with(system)


def test_debian_pulsar_verify(
    run: Mock,
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that the Debian implementation delegates verification."""
    verify = Mock(return_value=True)
    monkeypatch.setattr(UbuntuPulsar, "verify", verify)

    component = DebianPulsar(run=run)

    assert component.verify(system)

    verify.assert_called_once_with(system)
