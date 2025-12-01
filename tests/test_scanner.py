from drift_scout.config import BaselineConfig, ServiceBaseline
from drift_scout.inventory import ResourceRecord
from drift_scout.scanner import DriftScanner


def test_scanner_detects_drift() -> None:
    baseline = BaselineConfig(
        environment="prod",
        schedule="0 * * * *",
        services=[
            ServiceBaseline(
                name="web",
                owner="edge",
                control_hash="sha:expected",
                severity="high",
            )
        ],
    )
    inventory = [
        ResourceRecord(
            service="web",
            checksum="sha:observed",
            tags={},
            drift_score=2.5,
        )
    ]

    scanner = DriftScanner(baseline)
    results = scanner.scan(inventory)

    assert len(results) == 1
    assert results[0].observed_hashes == ["sha:observed"]

