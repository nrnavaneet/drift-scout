## Drift Scout

Drift Scout is a small but production-ready reference project for modeling
infrastructure drift detection, remediation simulation, and reporting workflows.
It is designed for the Ambiguous Coding Task project to exercise reasoning in a
Python-based DevOps/infrastructure context while remaining realistic and
approachable.

### Highlights
- Python 3.10+ with a modern `pyproject.toml` build
- `typer` CLI with sub-commands for scanning inventories, simulating changes,
  and managing historical baselines
- Pydantic-powered configuration validation for declarative YAML baselines
- Extensible notification interfaces (Slack webhook example included)
- Deterministic unit tests covering the core orchestration logic

### Repository Layout

```
drift-scout/
├── configs/
│   └── baseline.yaml
├── docs/
│   ├── ARCHITECTURE.md
│   └── OPERATIONS.md
├── src/
│   └── drift_scout/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── inventory.py
│       ├── reporter.py
│       ├── scanner.py
│       ├── scheduler.py
│       ├── state.py
│       └── integrations/
│           └── slack.py
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_inventory.py
│   ├── test_reporter.py
│   └── test_scanner.py
├── pyproject.toml
└── README.md
```

### Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
drift-scout scan configs/baseline.yaml --inventory docs/examples/web.json
```

### Testing

```bash
pytest
```

### Ambiguity Hooks

The codebase intentionally contains a few areas that require clarification,
mirroring real DevOps assignments:

- Different modules disagree on how strict schedule validation should be.
- `docs/OPERATIONS.md` references an `azure-devops` integration that is only
  partially scaffolded.
- Baseline drift severities mix numeric and textual levels, leaving room for
  interpretation.

These subtle gaps encourage requesters to ask clarifying questions rather than
blindly implement changes.

