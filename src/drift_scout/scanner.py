"""
Core drift detection logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence

from .config import BaselineConfig, ServiceBaseline
from .inventory import ResourceRecord


@dataclass
class DriftResult:
    service: str
    expected_hash: str
    observed_hashes: List[str]
    severity: str
    drift_score: float

    def to_summary(self) -> Dict[str, object]:
        return {
            "service": self.service,
            "expected_hash": self.expected_hash,
            "observed_hashes": self.observed_hashes,
            "severity": self.severity,
            "drift_score": self.drift_score,
        }


class DriftScanner:
    def __init__(self, baseline: BaselineConfig):
        self._baseline = baseline

    def scan(self, inventory: Sequence[ResourceRecord]) -> List[DriftResult]:
        results: List[DriftResult] = []
        for service in self._baseline.services:
            observed = [item for item in inventory if item.service == service.name]
            if not observed:
                results.append(
                    DriftResult(
                        service=service.name,
                        expected_hash=service.control_hash,
                        observed_hashes=[],
                        severity=self._normalize_severity(service),
                        drift_score=5.0,
                    )
                )
                continue

            hashes = {item.checksum for item in observed}
            if hashes == {service.control_hash}:
                continue

            drift_score = max(item.drift_score for item in observed)
            results.append(
                DriftResult(
                    service=service.name,
                    expected_hash=service.control_hash,
                    observed_hashes=sorted(hashes),
                    severity=self._normalize_severity(service),
                    drift_score=round(drift_score, 3),
                )
            )
        return results

    def _normalize_severity(self, service: ServiceBaseline) -> str:
        severity = service.severity
        if isinstance(severity, int):
            mapping = {
                1: "low",
                2: "moderate",
                3: "high",
                4: "critical",
                5: "critical",
            }
            return mapping.get(severity, "moderate")
        return severity

