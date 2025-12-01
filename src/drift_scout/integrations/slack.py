"""
Minimal Slack webhook integration.
"""

from __future__ import annotations

import json
from typing import Iterable

import httpx

from ..scanner import DriftResult


class SlackNotifier:
    def __init__(self, webhook_url: str):
        self._webhook_url = webhook_url

    def _format_payload(self, results: Iterable[DriftResult]) -> dict:
        lines = [
            f"*{res.service}*: expected `{res.expected_hash}` "
            f"but observed {', '.join(res.observed_hashes) or 'missing'} "
            f"(severity: {res.severity}, score: {res.drift_score})"
            for res in results
        ]
        return {"text": "\n".join(lines)}

    def send(self, results: Iterable[DriftResult]) -> None:
        payload = self._format_payload(results)
        # Caller is expected to handle network issues. For the reference repo we
        # simply raise any exception to surface flaky integrations.
        response = httpx.post(
            self._webhook_url,
            headers={"Content-Type": "application/json"},
            content=json.dumps(payload),
            timeout=5.0,
        )
        response.raise_for_status()

