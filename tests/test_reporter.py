from drift_scout.config import BaselineConfig, NotificationSettings, ServiceBaseline
from drift_scout.reporter import render_table
from drift_scout.scanner import DriftResult


def test_render_table_contains_service_name() -> None:
    result = DriftResult(
        service="web",
        expected_hash="sha:1",
        observed_hashes=["sha:2"],
        severity="high",
        drift_score=3.2,
    )
    output = render_table([result])
    assert "web" in output
    assert "sha:2" in output

