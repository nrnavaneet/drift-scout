from pathlib import Path

from drift_scout.inventory import ResourceRecord, filter_inventory, load_inventory


def test_load_inventory(tmp_path: Path) -> None:
    path = tmp_path / "inventory.json"
    path.write_text(
        '[{"service": "api", "checksum": "abc", "tags": {"env": "dev"}}]',
        encoding="utf-8",
    )

    records = load_inventory(path)
    assert len(records) == 1
    assert records[0].service == "api"


def test_filter_inventory() -> None:
    records = [
        ResourceRecord(service="web", checksum="1", tags={}, drift_score=1.0),
        ResourceRecord(service="api", checksum="2", tags={}, drift_score=1.0),
    ]
    filtered = filter_inventory(records, service="api")
    assert len(filtered) == 1
    assert filtered[0].service == "api"

