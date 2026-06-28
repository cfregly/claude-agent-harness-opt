"""Offline eval helpers for agent transcripts and final state."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EvaluationResult:
    passed: bool
    score: float
    details: list[str]

    def to_json(self) -> str:
        return json.dumps(
            {"passed": self.passed, "score": self.score, "details": self.details},
            indent=2,
            sort_keys=True,
        )


def load_eval_case(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def evaluate_case(case: dict[str, Any]) -> EvaluationResult:
    case_type = case.get("type")
    if case_type == "answer_accuracy":
        return evaluate_answer_accuracy(case)
    if case_type == "tool_use_accuracy":
        return evaluate_tool_use(case)
    if case_type == "final_state_accuracy":
        return evaluate_final_state(case)
    raise ValueError(f"unknown eval type: {case_type}")


def evaluate_answer_accuracy(case: dict[str, Any]) -> EvaluationResult:
    output = str(case.get("output", ""))
    checks = case.get("checks", {})
    details: list[str] = []
    passed_checks = 0
    total_checks = 0

    for text in checks.get("expected_contains", []):
        total_checks += 1
        if text.lower() in output.lower():
            passed_checks += 1
            details.append(f"found expected text: {text}")
        else:
            details.append(f"missing expected text: {text}")

    for item in checks.get("expected_any", []):
        label, options = _labeled_options(item)
        total_checks += 1
        matched = [option for option in options if option.lower() in output.lower()]
        if matched:
            passed_checks += 1
            details.append(f"found acceptable wording for {label}: {matched[0]}")
        else:
            details.append(f"missing acceptable wording for {label}: {options}")

    for item in checks.get("expected_regex", []):
        label, pattern = _labeled_pattern(item)
        total_checks += 1
        if re.search(pattern, output, flags=re.IGNORECASE):
            passed_checks += 1
            details.append(f"matched expected pattern for {label}")
        else:
            details.append(f"missing expected pattern for {label}: {pattern}")

    for text in checks.get("forbidden_contains", []):
        total_checks += 1
        if text.lower() in output.lower():
            details.append(f"found forbidden text: {text}")
        else:
            passed_checks += 1
            details.append(f"did not find forbidden text: {text}")

    for item in checks.get("forbidden_regex", []):
        label, pattern = _labeled_pattern(item)
        total_checks += 1
        if re.search(pattern, output, flags=re.IGNORECASE):
            details.append(f"found forbidden pattern for {label}: {pattern}")
        else:
            passed_checks += 1
            details.append(f"did not find forbidden pattern for {label}")

    for numeric in checks.get("numeric_ranges", []):
        total_checks += 1
        numbers = _extract_numbers(output)
        low = float(numeric["min"])
        high = float(numeric["max"])
        if any(low <= number <= high for number in numbers):
            passed_checks += 1
            details.append(f"found number in range for {numeric['label']}")
        else:
            details.append(f"no number in range for {numeric['label']}")

    if total_checks == 0:
        raise ValueError("answer_accuracy case has no checks")
    score = passed_checks / total_checks
    return EvaluationResult(score == 1, round(score, 3), details)


def evaluate_tool_use(case: dict[str, Any]) -> EvaluationResult:
    transcript = case.get("transcript", {})
    calls = transcript.get("tool_calls", [])
    names = [call.get("name") for call in calls]
    requirements = case.get("requirements", {})
    details: list[str] = []
    passed_checks = 0
    total_checks = 0

    for name, minimum in requirements.get("at_least", {}).items():
        total_checks += 1
        count = names.count(name)
        if count >= int(minimum):
            passed_checks += 1
            details.append(f"{name} called {count} times")
        else:
            details.append(f"{name} called {count} times, expected at least {minimum}")

    for name, maximum in requirements.get("at_most", {}).items():
        total_checks += 1
        count = names.count(name)
        if count <= int(maximum):
            passed_checks += 1
            details.append(f"{name} stayed within limit {maximum}")
        else:
            details.append(f"{name} called {count} times, expected at most {maximum}")

    for name in requirements.get("forbidden", []):
        total_checks += 1
        if name in names:
            details.append(f"forbidden tool used: {name}")
        else:
            passed_checks += 1
            details.append(f"forbidden tool not used: {name}")

    sequence = requirements.get("required_sequence")
    if sequence:
        total_checks += 1
        if _contains_sequence(names, sequence):
            passed_checks += 1
            details.append("required sequence found")
        else:
            details.append("required sequence missing")

    valid_paths = requirements.get("valid_tool_paths", [])
    if valid_paths:
        total_checks += 1
        if any(_contains_sequence(names, path) for path in valid_paths):
            passed_checks += 1
            details.append("one valid tool path found")
        else:
            details.append("no valid tool path found")

    for expected in requirements.get("required_args", []):
        total_checks += 1
        if _tool_call_with_args(calls, expected["name"], expected["args"]):
            passed_checks += 1
            details.append(f"found required args for {expected['name']}")
        else:
            details.append(f"missing required args for {expected['name']}")

    if total_checks == 0:
        raise ValueError("tool_use_accuracy case has no requirements")
    score = passed_checks / total_checks
    return EvaluationResult(score == 1, round(score, 3), details)


def evaluate_final_state(case: dict[str, Any]) -> EvaluationResult:
    actual = case.get("final_state")
    expected = case.get("expected_subset")
    if expected is None:
        raise ValueError("final_state_accuracy case missing expected_subset")

    details = []
    if _contains_subset(actual, expected):
        details.append("final state contains expected subset")
        return EvaluationResult(True, 1.0, details)
    details.append("final state does not contain expected subset")
    return EvaluationResult(False, 0.0, details)


def build_judge_prompt(case: dict[str, Any]) -> str:
    rubric = case.get("rubric", "Judge whether the output satisfies the checks.")
    output = case.get("output", "")
    return (
        "You are grading an agent output against a rubric.\n\n"
        "<rubric>\n"
        f"{rubric}\n"
        "</rubric>\n\n"
        "<agent_output>\n"
        f"{output}\n"
        "</agent_output>\n\n"
        "Return JSON with keys passed, score, and rationale. Do not include extra text.\n"
    )


def _extract_numbers(text: str) -> list[float]:
    values = []
    for match in re.findall(r"[-+]?\d[\d,]*(?:\.\d+)?", text):
        values.append(float(match.replace(",", "")))
    return values


def _labeled_options(item: Any) -> tuple[str, list[str]]:
    if isinstance(item, dict):
        label = str(item.get("label", "acceptable wording"))
        options = [str(option) for option in item.get("options", [])]
        return label, options
    if isinstance(item, list):
        return "acceptable wording", [str(option) for option in item]
    return "acceptable wording", [str(item)]


def _labeled_pattern(item: Any) -> tuple[str, str]:
    if isinstance(item, dict):
        return str(item.get("label", "pattern")), str(item.get("pattern", ""))
    return "pattern", str(item)


def _contains_sequence(names: list[str], sequence: list[str]) -> bool:
    position = 0
    for name in names:
        if name == sequence[position]:
            position += 1
            if position == len(sequence):
                return True
    return False


def _tool_call_with_args(calls: list[dict[str, Any]], name: str, args: dict[str, Any]) -> bool:
    for call in calls:
        if call.get("name") != name:
            continue
        call_args = call.get("args", {})
        if all(call_args.get(key) == value for key, value in args.items()):
            return True
    return False


def _contains_subset(actual: Any, expected: Any) -> bool:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(key in actual and _contains_subset(actual[key], value) for key, value in expected.items())
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return False
        return all(any(_contains_subset(item, expected_item) for item in actual) for expected_item in expected)
    return actual == expected
