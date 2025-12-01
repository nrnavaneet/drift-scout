## Drift Scout Architecture

Drift Scout models a lightweight infrastructure governance system built around
three primary layers:

1. **Configuration Layer** (`drift_scout.config`)
   - YAML-driven baselines define expected resource hashes, severity levels,
     notification channels, and metadata such as owning teams.
   - Pydantic validators enforce shape and provide helpful error messages.
2. **Execution Layer** (`drift_scout.scanner`, `drift_scout.inventory`)
   - The scanner consumes observed inventory data emitted by CI/CD jobs and
     compares it to baseline control hashes.
   - Each mismatch becomes a `DriftResult` struct containing severity,
     observed state, and drift score modifiers.
3. **Interface Layer** (`drift_scout.cli`, `drift_scout.reporter`)
   - Typer CLI orchestrates scans, schedule inspection, and historical queries.
   - Rich table rendering plus Slack webhook notifications surface findings to
     operators.

### Extension Points

- Add new notification channels by extending `drift_scout.integrations`.
- Replace the default `StateStore` with a database-backed implementation by
  swapping the dependency injected in `cli.scan`.
- Plug additional detectors into `DriftScanner.scan` to support policy-based or
  heuristic drift scoring.

