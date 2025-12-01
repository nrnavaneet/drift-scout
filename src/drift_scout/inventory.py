"""
Inventory ingestion representing observed infrastructure state.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional


@dataclass(slots=True)
class ResourceRecord:
    service: str
    checksum: str
    tags: Dict[str, str]
    drift_score: float

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "ResourceRecord":
        return cls(
            service=str(data["service"]),
            checksum=str(data["checksum"]),
            tags={str(k): str(v) for k, v in (data.get("tags") or {}).items()},
            drift_score=float(data.get("drift_score", 0.0)),
        )


def load_inventory(path: Path) -> List[ResourceRecord]:
    """Load inventory from JSON file describing observed state."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, list):
        raise ValueError("inventory must be a JSON array")

    return [ResourceRecord.from_dict(item) for item in payload]


def filter_inventory(
    inventory: Iterable[ResourceRecord], *, service: Optional[str] = None
) -> List[ResourceRecord]:
    if service:
        return [item for item in inventory if item.service == service]
    return list(inventory)

