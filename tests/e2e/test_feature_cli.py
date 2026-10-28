"""Test feature CLI operations end to end."""

import subprocess

import pytest

from diogenos.feature.registry import FeatureRegistry


@pytest.mark.e2e
def test_feature_list() -> None:
    """List the registered features through the CLI."""
    result = subprocess.run(
        ["diogenos", "feature", "list"],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr


@pytest.mark.e2e
@pytest.mark.parametrize("feature_id", FeatureRegistry().list())
def test_feature_lifecycle(feature_id: str) -> None:
    """Verify the feature installation lifecycle."""
    install_result = subprocess.run(
        ["diogenos", "feature", "install", feature_id],
        capture_output=True,
        check=False,
        text=True,
    )

    assert install_result.returncode == 0, (
        f"Installation failed for {feature_id}:\n"
        f"{install_result.stdout}\n{install_result.stderr}"
    )

    check_result = subprocess.run(
        ["diogenos", "feature", "check", feature_id],
        capture_output=True,
        check=False,
        text=True,
    )

    assert check_result.returncode == 0, (
        f"Feature check failed for {feature_id}:\n"
        f"{check_result.stdout}\n{check_result.stderr}"
    )
    assert f"Feature {feature_id!r} is satisfied." in check_result.stdout
