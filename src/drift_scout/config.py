"""
Configuration parsing and validation for drift baselines.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator


class NotificationSettings(BaseModel):
    slack_webhook: Optional[str] = Field(
        default=None, description="Incoming webhook URL for Slack alerts."
    )
    email: Optional[List[str]] = Field(
        default=None, description="List of email recipients for drift reports."
    )
    ticketing_label: Optional[str] = Field(
        default=None,
        description="Label to apply when creating backlog tickets (Jira, Linear, etc.).",
    )

    def destinations(self) -> List[str]:
        dests: List[str] = []
        if self.slack_webhook:
            dests.append("slack")
        if self.email:
            dests.append("email")
        if self.ticketing_label:
            dests.append("ticketing")
        return dests


class ServiceBaseline(BaseModel):
    name: str
    owner: str
    control_hash: str = Field(
        ...,
        description="Checksum/hash representing the expected IaC snapshot for the service.",
    )
    severity: Union[str, int] = Field(
        ...,
        description="Severity may be textual or numeric depending on the team.",
    )
    metadata: Dict[str, Union[str, int, float]] = Field(
        default_factory=dict,
        description="Free-form metadata describing service expectations.",
    )

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, value: Union[str, int]) -> Union[str, int]:
        if isinstance(value, int):
            if value < 1 or value > 5:
                raise ValueError("numeric severity must be between 1 and 5")
            return value
        allowed = {"low", "moderate", "high", "critical"}
        if value.lower() not in allowed:
            raise ValueError(f"severity '{value}' is not in {allowed}")
        return value.lower()


class BaselineConfig(BaseModel):
    environment: str = Field(..., description="Environment name, e.g. production.")
    schedule: str = Field(
        ...,
        description="CRON expression used to decide scan frequency. Seconds field optional.",
    )
    services: List[ServiceBaseline] = Field(default_factory=list)
    notifications: NotificationSettings = Field(
        default_factory=NotificationSettings,
        description="Notification channels that should receive drift summaries.",
    )
    metadata: Dict[str, Union[str, int, float]] = Field(default_factory=dict)

    @field_validator("schedule")
    @classmethod
    def validate_schedule(cls, value: str) -> str:
        parts = value.split()
        if len(parts) not in {5, 6}:
            raise ValueError(
                "schedule must be a valid cron expression with 5 or 6 fields"
            )
        return value

    def lookup_service(self, name: str) -> Optional[ServiceBaseline]:
        return next((svc for svc in self.services if svc.name == name), None)


def load_baseline(path: Union[str, Path]) -> BaselineConfig:
    """Load a YAML baseline file and return a validated config."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    try:
        return BaselineConfig.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(f"baseline configuration invalid: {exc}") from exc

