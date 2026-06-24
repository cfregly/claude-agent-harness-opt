"""Review tool descriptions against trace evidence and selection cases."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .prompt_builder import lint_tools
from .trace_review import load_trace, review_trace


@dataclass(frozen=True)
class ToolSelectionFinding:
    check: str
    passed: bool
    detail: str
    recommendation: str
    severity: str = "medium"

    def to_dict(self) -> dict[str, Any]:
        return {
            "check": self.check,
            "detail": self.detail,
            "passed": self.passed,
            "recommendation": self.recommendation,
            "severity": self.severity,
        }


@dataclass(frozen=True)
class ToolSelectionReview:
    passed: bool
    score: float
    findings: list[ToolSelectionFinding]
    recommendations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "findings": [finding.to_dict() for finding in self.findings],
            "passed": self.passed,
            "recommendations": self.recommendations,
            "score": self.score,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


def review_tool_selection_bundle(path: str | Path) -> ToolSelectionReview:
    bundle_path = Path(path)
    with bundle_path.open("r", encoding="utf-8") as handle:
        bundle = json.load(handle)
    return review_tool_selection(bundle, bundle_path.parent)


def review_tool_selection(bundle: dict[str, Any], base_dir: str | Path) -> ToolSelectionReview:
    """Review whether tool descriptions support correct selection and arguments."""

    tools = bundle.get("tools", [])
    traces = bundle.get("traces", [])
    cases = bundle.get("tool_selection_cases", [])
    base_path = Path(base_dir)
    findings: list[ToolSelectionFinding] = []

    findings.extend(_inventory_findings(tools))
    findings.extend(_selection_case_findings(cases, tools))
    findings.extend(_trace_selection_findings(traces, tools, base_path))

    score = _weighted_score(findings)
    failed_high = any(not finding.passed and finding.severity == "high" for finding in findings)
    passed = score >= 0.9 and not failed_high
    recommendations = sorted(
        {
            finding.recommendation
            for finding in findings
            if not finding.passed and finding.recommendation
        }
    )
    return ToolSelectionReview(
        findings=findings,
        passed=passed,
        recommendations=recommendations,
        score=score,
    )


def render_tool_selection_markdown(review: ToolSelectionReview) -> str:
    lines = [
        "# Tool Selection Optimizer",
        "",
        f"Passed: {'yes' if review.passed else 'no'}",
        f"Score: {review.score:.3f}",
        "",
        "## Recommendations",
        "",
    ]
    if review.recommendations:
        lines.extend(f"- {item}" for item in review.recommendations)
    else:
        lines.append("No required changes.")

    lines.extend(
        [
            "",
            "## Findings",
            "",
            "| Check | Severity | Passed | Detail |",
            "|---|---|---:|---|",
        ]
    )
    for finding in review.findings:
        detail = finding.detail.replace("|", "\\|")
        lines.append(
            f"| {finding.check} | {finding.severity} | "
            f"{'yes' if finding.passed else 'no'} | {detail} |"
        )
    return "\n".join(lines) + "\n"


def _inventory_findings(tools: list[dict[str, Any]]) -> list[ToolSelectionFinding]:
    findings: list[ToolSelectionFinding] = []
    lint_issues = lint_tools(tools)
    if lint_issues:
        findings.extend(
            ToolSelectionFinding(
                "inventory.lint",
                False,
                issue,
                "Rewrite overlapping or thin tool descriptions with distinct purpose, use_when, and avoid_when fields.",
                "high",
            )
            for issue in lint_issues
        )
    else:
        findings.append(
            ToolSelectionFinding(
                "inventory.lint",
                True,
                "tool names and basic descriptions are distinct",
                "",
                "high",
            )
        )

    for tool in tools:
        name = str(tool.get("name", "")).strip() or "<unnamed>"
        has_schema = _has_input_schema(tool)
        findings.append(
            ToolSelectionFinding(
                "inventory.input_schema",
                has_schema,
                f"{name} declares input schema or parameter shape",
                (
                    f"Add an input_schema or parameters block to {name} "
                    "so the agent can form valid calls."
                    if not has_schema
                    else ""
                ),
                "medium",
            )
        )
        quality_checks = tool.get("quality_checks") or []
        has_quality_checks = bool(quality_checks)
        findings.append(
            ToolSelectionFinding(
                "inventory.quality_checks",
                has_quality_checks,
                f"{name} states result quality checks",
                (
                    f"Add quality_checks to {name} so the agent knows how to inspect results "
                    "before the next call."
                    if not has_quality_checks
                    else ""
                ),
                "medium",
            )
        )
    return findings


def _selection_case_findings(
    cases: list[dict[str, Any]],
    tools: list[dict[str, Any]],
) -> list[ToolSelectionFinding]:
    tool_names = _tool_names(tools)
    has_cases = bool(cases)
    findings: list[ToolSelectionFinding] = [
        ToolSelectionFinding(
            "selection_cases.present",
            has_cases,
            f"found {len(cases)} tool-selection calibration cases",
            (
                "Add tool_selection_cases that contrast when each similar tool should "
                "and should not be used."
                if not has_cases
                else ""
            ),
            "high",
        )
    ]
    for case in cases:
        name = str(case.get("name", "<unnamed>"))
        expected = set(case.get("expected_tools", []))
        forbidden = set(case.get("forbidden_tools", []))
        unknown_expected = sorted(expected - tool_names)
        unknown_forbidden = sorted(forbidden - tool_names)
        findings.append(
            ToolSelectionFinding(
                "selection_cases.expected_tools_known",
                not unknown_expected,
                f"{name} expected tools are present: {sorted(expected)}",
                (
                    f"Add or rename missing expected tools for case {name}: {unknown_expected}"
                    if unknown_expected
                    else ""
                ),
                "high",
            )
        )
        findings.append(
            ToolSelectionFinding(
                "selection_cases.forbidden_tools_known",
                not unknown_forbidden,
                f"{name} forbidden tools are present: {sorted(forbidden)}",
                (
                    f"Add or rename missing forbidden tools for case {name}: {unknown_forbidden}"
                    if unknown_forbidden
                    else ""
                ),
                "medium",
            )
        )
        has_contrast = bool(forbidden or case.get("contrast_with"))
        findings.append(
            ToolSelectionFinding(
                "selection_cases.has_contrast",
                has_contrast,
                f"{name} states a contrast against a wrong tool",
                (
                    f"Add a forbidden_tools or contrast_with entry to case {name}."
                    if not has_contrast
                    else ""
                ),
                "medium",
            )
        )
        has_rationale = bool(str(case.get("rationale", "")).strip())
        findings.append(
            ToolSelectionFinding(
                "selection_cases.has_rationale",
                has_rationale,
                f"{name} explains why the expected tool is correct",
                (
                    f"Add a rationale to case {name} so failures explain "
                    "the prompt or tool-description fix."
                    if not has_rationale
                    else ""
                ),
                "low",
            )
        )
    return findings


def _trace_selection_findings(
    traces: list[dict[str, Any]],
    tools: list[dict[str, Any]],
    base_path: Path,
) -> list[ToolSelectionFinding]:
    tool_names = _tool_names(tools)
    findings: list[ToolSelectionFinding] = []
    used_names: set[str] = set()

    for item in traces:
        trace_path = _resolve(base_path, item["trace"])
        trace_name = str(item.get("name", trace_path.stem))
        trace = load_trace(trace_path)
        review = review_trace(trace)
        calls = [step for step in trace.get("steps", []) if step.get("type") == "tool_call"]
        used_names.update(str(call.get("name", "")) for call in calls)

        unknown_used = sorted({str(call.get("name", "")) for call in calls} - tool_names)
        findings.append(
            ToolSelectionFinding(
                "trace.used_tools_known",
                not unknown_used,
                f"{trace_name} used catalog tools only",
                (
                    f"Add missing tools to the catalog or fix trace tool names: {unknown_used}"
                    if unknown_used
                    else ""
                ),
                "high",
            )
        )

        for required in trace.get("rubric", {}).get("required_tools", []):
            findings.append(
                ToolSelectionFinding(
                    "trace.required_tool_in_catalog",
                    required in tool_names,
                    f"{trace_name} required tool {required!r} exists in catalog",
                    (
                        f"Add {required} to the tool inventory or change the trace rubric."
                        if required not in tool_names
                        else ""
                    ),
                    "high",
                )
            )

        for trace_finding in review.findings:
            if trace_finding.passed or not trace_finding.check.startswith("tool_use."):
                continue
            findings.append(
                ToolSelectionFinding(
                    f"trace.{trace_finding.check}",
                    False,
                    f"{trace_name}: {trace_finding.detail}",
                    _recommend_for_trace_failure(trace_finding.check),
                    trace_finding.severity,
                )
            )

        for name in _tools_with_error_results(trace):
            findings.append(
                ToolSelectionFinding(
                    "trace.error_result",
                    False,
                    f"{trace_name} received an error from {name}",
                    f"Clarify {name} input_schema, validation rules, and recovery examples.",
                    "medium",
                )
            )

    if traces:
        unused = sorted(_tool_names(tools) - used_names)
        findings.append(
            ToolSelectionFinding(
                "trace.catalog_coverage",
                not unused,
                f"representative traces did not use: {unused}",
                (
                    f"Add representative traces or selection cases for unused tools: {unused}"
                    if unused
                    else ""
                ),
                "low",
            )
        )
    return findings


def _recommend_for_trace_failure(check: str) -> str:
    if check == "tool_use.required_tool":
        return "Strengthen use_when, avoid_when, and selection cases for the missed required tool."
    if check == "tool_use.forbidden_tool":
        return "Add a negative selection case and avoid_when rule for the forbidden tool."
    if check == "tool_use.expected_args":
        return "Add argument schema details and one expected argument example for the tool."
    if check == "tool_use.duplicate_calls":
        return "Add stop criteria that tell the agent when a repeated call adds no value."
    if check in {"tool_use.min_tool_calls", "tool_use.max_tool_calls"}:
        return "Adjust tool-call budgets and done criteria from observed trace behavior."
    return "Update tool descriptions or trace rubrics from the observed selection failure."


def _tools_with_error_results(trace: dict[str, Any]) -> set[str]:
    call_names = {
        str(step.get("id")): str(step.get("name"))
        for step in trace.get("steps", [])
        if step.get("type") == "tool_call"
    }
    names: set[str] = set()
    for step in trace.get("steps", []):
        if step.get("type") != "tool_result":
            continue
        if step.get("ok") is False or step.get("error"):
            names.add(call_names.get(str(step.get("tool_call_id")), "<unknown>"))
    return names


def _has_input_schema(tool: dict[str, Any]) -> bool:
    return bool(tool.get("input_schema") or tool.get("parameters") or tool.get("args_schema"))


def _tool_names(tools: list[dict[str, Any]]) -> set[str]:
    return {
        str(tool.get("name", "")).strip()
        for tool in tools
        if str(tool.get("name", "")).strip()
    }


def _weighted_score(findings: list[ToolSelectionFinding]) -> float:
    if not findings:
        return 0.0
    weights = {"high": 3, "medium": 2, "low": 1}
    possible = sum(weights.get(finding.severity, 2) for finding in findings)
    passed = sum(weights.get(finding.severity, 2) for finding in findings if finding.passed)
    return round(passed / possible, 3)


def _resolve(base_dir: Path, path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return (base_dir / candidate).resolve()
