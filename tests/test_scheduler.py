from datetime import datetime

from drift_scout.scheduler import next_run


def test_next_run_advances_time() -> None:
    reference = datetime.fromisoformat("2024-01-01T00:00:00")
    result = next_run("0 * * * *", reference=reference)
    assert result > reference

