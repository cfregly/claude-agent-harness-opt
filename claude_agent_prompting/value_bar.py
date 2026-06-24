"""Evaluate whether an audit is adversarially-confirmed to add value."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ValueBarResult:
    passed: bool
    score: float
    details: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "details": self.details,
            "passed": self.passed,
            "score": self.score,
        }


def evaluate_value_bar(value_bar: dict[str, Any] | None) -> ValueBarResult:
    if not value_bar:
        return ValueBarResult(
            passed=False,
            score=0.0,
            details=["missing value_bar: audit is not adversarially-confirmed to add value"],
        )

    details: list[str] = []
    checks: list[bool] = []

    claim = str(value_bar.get("claim", "")).strip()
    checks.append(bool(claim))
    details.append("value claim present" if claim else "value claim missing")

    metric = str(value_bar.get("metric", "")).strip()
    checks.append(bool(metric))
    details.append(f"metric present: {metric}" if metric else "metric missing")

    baseline_score = _score(value_bar.get("baseline"))
    candidate_score = _score(value_bar.get("candidate"))
    minimum_delta = float(value_bar.get("minimum_delta", 0.0))
    delta = round(candidate_score - baseline_score, 3)
    improved = delta >= minimum_delta
    checks.append(improved)
    details.append(
        f"candidate improved by {delta:.3f}, minimum required delta is {minimum_delta:.3f}"
    )

    adversarial = value_bar.get("adversarial_review", {})
    challenge = str(adversarial.get("challenge", "")).strip()
    failed_to_disprove = bool(adversarial.get("failed_to_disprove", False))
    open_objections = adversarial.get("open_objections", [])
    if not isinstance(open_objections, list):
        open_objections = [str(open_objections)]

    checks.append(bool(challenge))
    details.append("adversarial challenge present" if challenge else "adversarial challenge missing")

    checks.append(failed_to_disprove)
    details.append(
        "adversarial review failed to disprove the value claim"
        if failed_to_disprove
        else "adversarial review did not confirm the value claim"
    )

    checks.append(not open_objections)
    details.append(
        "no open adversarial objections"
        if not open_objections
        else f"open adversarial objections: {', '.join(map(str, open_objections))}"
    )

    score = round(sum(1 for check in checks if check) / len(checks), 3)
    return ValueBarResult(
        passed=all(checks),
        score=score,
        details=details,
    )


def _score(value: Any) -> float:
    if isinstance(value, dict):
        return float(value.get("score", 0.0))
    return float(value or 0.0)
