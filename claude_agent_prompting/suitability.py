"""Score whether a task is a good fit for an autonomous agent."""

from __future__ import annotations

from typing import Any


POSITIVE_FIELDS = ("complexity", "value", "viability", "recoverability")
NEGATIVE_FIELDS = ("cost_of_error",)


def score_use_case(use_case: dict[str, Any]) -> dict[str, Any]:
    scores = {field: _score(use_case, field) for field in POSITIVE_FIELDS + NEGATIVE_FIELDS}
    adjusted = [
        scores["complexity"],
        scores["value"],
        scores["viability"],
        scores["recoverability"],
        6 - scores["cost_of_error"],
    ]
    readiness = round(sum(adjusted) / len(adjusted), 2)

    if scores["cost_of_error"] >= 5 and scores["recoverability"] <= 2:
        verdict = "human_in_loop"
        reason = "error cost is high and recovery is weak"
    elif readiness >= 4:
        verdict = "agent"
        reason = "task is complex, valuable, viable, and recoverable"
    elif readiness >= 3:
        verdict = "workflow_or_agent_with_review"
        reason = "task may work as an agent if review and stop criteria are strong"
    else:
        verdict = "workflow_or_direct_prompt"
        reason = "task does not justify an autonomous loop yet"

    return {
        "readiness": readiness,
        "verdict": verdict,
        "reason": reason,
        "scores": scores,
    }


def _score(use_case: dict[str, Any], field: str) -> int:
    value = int(use_case.get(field, 1))
    if value < 1 or value > 5:
        raise ValueError(f"{field} must be from 1 to 5")
    return value
