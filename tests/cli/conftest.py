"""Define shared CLI test fixtures."""

from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from diogenos.cli.feature import check
from diogenos.cli.feature import components
from diogenos.cli.feature import install
from diogenos.cli.feature import list
from diogenos.system.base import System


@pytest.fixture
def registry(monkeypatch: MonkeyPatch) -> Mock:
    """Provide a mocked feature registry."""
    registry = Mock()

    for module in (list, check, install, components):
        monkeypatch.setattr(
            module,
            "FeatureRegistry",
            lambda: registry,
        )

    return registry


@pytest.fixture
def detector(monkeypatch: MonkeyPatch, system: System) -> Mock:
    """Provide a mocked system detector."""
    detector = Mock()
    detector.detect.return_value = system

    for module in (check, install, components):
        monkeypatch.setattr(
            module,
            "SystemDetector",
            lambda: detector,
        )

    return detector
