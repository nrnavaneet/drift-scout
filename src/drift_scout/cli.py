"""
Typer CLI entrypoint.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .config import BaselineConfig, load_baseline
from .inventory import load_inventory
from .reporter import dispatch_notifications, render_table
from .scanner import DriftScanner
from .scheduler import next_run
from .state import HistoricalRecord, StateStore

app = typer.Typer(help="Infrastructure drift detection utility.")
console = Console()


def _load_state(path: Optional[Path]) -> Optional[StateStore]:
    if not path:
        return None
    return StateStore(path)


@app.command()
def scan(
    baseline: Path = typer.Argument(..., exists=True, readable=True),
    inventory: Path = typer.Option(
        ...,
        "--inventory",
        "-i",
        exists=True,
        readable=True,
        help="Path to JSON inventory file produced by the deployment pipeline.",
    ),
    history: Optional[Path] = typer.Option(
        None,
        "--history",
        help="Optional path to persist drift history (JSON).",
    ),
) -> None:
    """Compare the provided inventory against the baseline definition."""
    config: BaselineConfig = load_baseline(baseline)
    data = load_inventory(inventory)
    scanner = DriftScanner(config)
    results = scanner.scan(data)

    if not results:
        console.print("[green]No drift detected[/green]")
        return

    console.print(render_table(results))

    state_store = _load_state(history)
    if state_store:
        for result in results:
            state_store.append(
                HistoricalRecord(
                    timestamp=datetime.utcnow(),
                    service=result.service,
                    drift_detected=True,
                    detail=result.to_summary(),
                )
            )

    destinations = dispatch_notifications(config, results)
    if destinations:
        console.print(f"[yellow]Notifications sent to {', '.join(destinations)}[/yellow]")


@app.command()
def schedule(
    baseline: Path = typer.Argument(..., exists=True, readable=True),
    reference: Optional[str] = typer.Option(
        None, "--reference", help="ISO timestamp to seed next-run calculation."
    ),
) -> None:
    """Show next planned execution time for the baseline schedule."""
    config = load_baseline(baseline)
    ref_dt = datetime.fromisoformat(reference) if reference else None
    nxt = next_run(config.schedule, reference=ref_dt)
    console.print(f"Next run for {config.environment}: {nxt.isoformat()}")


@app.command()
def history(
    path: Path = typer.Argument(..., exists=True, readable=True),
    limit: int = typer.Option(10, "--limit", "-n", help="Number of records to show."),
) -> None:
    """Display stored drift history."""
    store = StateStore(path)
    records = store.records[-limit:]
    if not records:
        console.print("No history available.")
        return
    for record in records:
        console.print(
            f"[bold]{record.timestamp.isoformat()}[/bold] "
            f"{record.service}: drift={record.drift_detected} "
            f"{record.detail.get('observed_hashes')}"
        )

