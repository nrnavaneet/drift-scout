from pathlib import Path

import pytest

from drift_scout.config import BaselineConfig, load_baseline


def test_load_baseline(tmp_path: Path) -> None:
    data = """
environment: staging
schedule: "*/5 * * * *"
services:
  - name: api
    owner: core
    control_hash: "sha:abc"
    severity: moderate
"""
    file_path = tmp_path / "baseline.yaml"
    file_path.write_text(data, encoding="utf-8")

    cfg = load_baseline(file_path)
    assert cfg.environment == "staging"
    assert cfg.services[0].severity == "moderate"


def test_reject_invalid_severity(tmp_path: Path) -> None:
    data = """
environment: prod
schedule: "* * * * *"
services:
  - name: db
    owner: data
    control_hash: "sha:1"
    severity: 9
"""
    file_path = tmp_path / "baseline.yaml"
    file_path.write_text(data, encoding="utf-8")

    with pytest.raises(ValueError):
        load_baseline(file_path)

