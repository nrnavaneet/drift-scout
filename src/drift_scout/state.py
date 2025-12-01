"""
State persistence for scan history.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List


@dataclass
class HistoricalRecord:
    timestamp: datetime
    service: str
    drift_detected: bool
    detail: Dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, object]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "service": self.service,
            "drift_detected": self.drift_detected,
            "detail": self.detail,
        }


class StateStore:
    def __init__(self, path: Path):
        self._path = Path(path)
        self._records: List[HistoricalRecord] = []
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        with self._path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        for item in data:
            self._records.append(
                HistoricalRecord(
                    timestamp=datetime.fromisoformat(item["timestamp"]),
                    service=item["service"],
                    drift_detected=bool(item["drift_detected"]),
                    detail=item.get("detail") or {},
                )
            )

    def append(self, record: HistoricalRecord) -> None:
        self._records.append(record)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as handle:
            json.dump([r.to_dict() for r in self._records], handle, indent=2)

    @property
    def records(self) -> List[HistoricalRecord]:
        return list(self._records)

