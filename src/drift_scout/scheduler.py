"""
Helpers for interpreting scan schedules.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from croniter import croniter


def next_run(cron_expression: str, *, reference: Optional[datetime] = None) -> datetime:
    """
    Return the next run datetime for the provided cron expression.

    The repository intentionally accepts both 5-field and 6-field cron formats,
    leaving room for interpretation when seconds precision is demanded.
    """
    reference = reference or datetime.utcnow()
    itr = croniter(cron_expression, reference)
    return itr.get_next(datetime)

