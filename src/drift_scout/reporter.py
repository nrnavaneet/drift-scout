"""
Reporting helpers for drift scan results.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, List

from rich.console import Console
from rich.table import Table

from .config import BaselineConfig
from .scanner import DriftResult
from .integrations.slack import SlackNotifier


def render_table(results: Iterable[DriftResult]) -> str:
    table = Table(title="Drift Summary")
    table.add_column("Service")
    table.add_column("Expected Hash")
    table.add_column("Observed Hashes")
    table.add_column("Severity")
    table.add_column("Score", justify="right")

    for result in results:
        table.add_row(
            result.service,
            result.expected_hash,
            ", ".join(result.observed_hashes) or "missing",
            result.severity,
            f"{result.drift_score:.2f}",
        )

    console = Console(record=True, width=100)
    console.print(table)
    return console.export_text()


def dispatch_notifications(
    baseline: BaselineConfig, results: List[DriftResult]
) -> List[str]:
    """Send notifications to configured endpoints. Returns list of channel ids."""
    destinations: List[str] = []
    if not results:
        return destinations

    if baseline.notifications.slack_webhook:
        notifier = SlackNotifier(baseline.notifications.slack_webhook)
        notifier.send(results)
        destinations.append("slack")

    # Email/ticketing integrations intentionally omitted to keep the repo focused.
    return destinations

