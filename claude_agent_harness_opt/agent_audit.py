"""Review a submitted agent bundle: tools, traces, and optional report."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .claude_judge import (
    JudgeRequestFn,
    judge_tool_selection_with_claude,
    judge_trace_with_claude,
)
from .prompt_builder import lint_tools
from .tool_selection import review_tool_selection
from .trace_review import load_trace, review_trace
from .value_bar import evaluate_value_bar


def load_agent_bundle(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def review_agent_bundle(
    path: str | Path,
    *,
    claude_judge: bool = False,
    require_claude_judge: bool = False,
    judge_model: str | None = None,
    judge_api_key: str | None = None,
    judge_request_fn: JudgeRequestFn | None = None,
) -> dict[str, Any]:
    bundle_path = Path(path)
    bundle = load_agent_bundle(bundle_path)
    base_dir = bundle_path.parent

    tool_issues = lint_tools(bundle.get("tools", []))
    tool_selection = review_tool_selection(bundle, base_dir)
    traces = []
    claude_judges = []
    for item in bundle.get("traces", []):
        trace_path = _resolve(base_dir, item["trace"])
        trace = load_trace(trace_path)
        review = review_trace(trace)
        traces.append(
            {
                "name": item.get("name", trace_path.stem),
                "passed": review.passed,
                "score": review.score,
                "scores": review.scores,
                "trace": str(trace_path),
            }
        )
        if claude_judge:
            semantic = judge_trace_with_claude(
                trace,
                review,
                api_key=judge_api_key,
                model=judge_model,
                request_fn=judge_request_fn,
            )
            claude_judges.append(
                {
                    "name": item.get("name", trace_path.stem),
                    "trace": str(trace_path),
                    **semantic.to_dict(),
                }
            )

    claude_tool_selection = None
    if claude_judge:
        semantic_tool_selection = judge_tool_selection_with_claude(
            bundle,
            tool_selection.to_dict(),
            api_key=judge_api_key,
            model=judge_model,
            request_fn=judge_request_fn,
        )
        claude_tool_selection = semantic_tool_selection.to_dict()

    trace_score = _average([trace["score"] for trace in traces])
    tool_score = 1.0 if not tool_issues else 0.0
    value_bar = evaluate_value_bar(bundle.get("value_bar"))
    component_scores = [tool_score, tool_selection.score, value_bar.score]
    if traces:
        component_scores.append(trace_score)
    if claude_judges:
        component_scores.append(_average([judge["score"] for judge in claude_judges]))
    if claude_tool_selection:
        component_scores.append(claude_tool_selection["score"])
    overall = round(sum(component_scores) / len(component_scores), 3)
    claude_judge_passed = not claude_judges or all(judge["passed"] for judge in claude_judges)
    claude_tool_selection_passed = (
        not claude_tool_selection or bool(claude_tool_selection["passed"])
    )

    return {
        "name": bundle.get("name", bundle_path.stem),
        "overall_score": overall,
        "passed": (
            not tool_issues
            and tool_selection.passed
            and value_bar.passed
            and all(trace["passed"] for trace in traces)
            and (claude_judge_passed or not claude_judge)
            and (claude_tool_selection_passed or not claude_judge)
        ),
        "claude_judge": {
            "enabled": claude_judge,
            "passed": claude_judge_passed and claude_tool_selection_passed,
            "required": require_claude_judge,
            "tool_selection": claude_tool_selection,
            "traces": claude_judges,
        },
        "tool_inventory": {
            "issues": tool_issues,
            "passed": not tool_issues,
            "score": tool_score,
            "tools": len(bundle.get("tools", [])),
        },
        "tool_selection": tool_selection.to_dict(),
        "traces": traces,
        "value_bar": value_bar.to_dict(),
    }


def render_agent_audit_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['name']}",
        "",
        f"Passed: {'yes' if result['passed'] else 'no'}",
        f"Overall score: {result['overall_score']:.3f}",
        "",
        "## Tool Inventory",
        "",
        f"Tools reviewed: {result['tool_inventory']['tools']}",
        f"Tool score: {result['tool_inventory']['score']:.3f}",
    ]

    issues = result["tool_inventory"]["issues"]
    if issues:
        lines.extend(["", "Tool issues:"])
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.extend(["", "No tool inventory issues."])

    lines.extend(
        [
            "",
            "## Tool Selection",
            "",
            f"Tool selection score: {result['tool_selection']['score']:.3f}",
            f"Tool selection passed: {'yes' if result['tool_selection']['passed'] else 'no'}",
        ]
    )
    recommendations = result["tool_selection"].get("recommendations", [])
    if recommendations:
        lines.extend(["", "Tool selection recommendations:"])
        lines.extend(f"- {item}" for item in recommendations)
    else:
        lines.extend(["", "No required tool selection changes."])

    lines.extend(
        [
            "",
            "## Value Bar",
            "",
            f"Value bar score: {result['value_bar']['score']:.3f}",
            f"Value bar passed: {'yes' if result['value_bar']['passed'] else 'no'}",
            "",
            "Value bar details:",
        ]
    )
    lines.extend(f"- {detail}" for detail in result["value_bar"]["details"])

    claude = result.get("claude_judge", {})
    if claude.get("enabled"):
        lines.extend(
            [
                "",
                "## Claude Judge",
                "",
                f"Claude judge passed: {'yes' if claude['passed'] else 'no'}",
                f"Claude judge required: {'yes' if claude['required'] else 'no'}",
                "",
                "| Trace | Model | Score | Passed |",
                "|---|---|---:|---:|",
            ]
        )
        for trace in claude["traces"]:
            lines.append(
                f"| {trace['name']} | {trace['model']} | {trace['score']:.3f} | "
                f"{'yes' if trace['passed'] else 'no'} |"
            )
        tool_selection = claude.get("tool_selection")
        if tool_selection:
            lines.extend(
                [
                    "",
                    "Claude tool selection judge:",
                    f"- Model: {tool_selection['model']}",
                    f"- Score: {tool_selection['score']:.3f}",
                    f"- Passed: {'yes' if tool_selection['passed'] else 'no'}",
                ]
            )

    lines.extend(["", "## Trace Scores", "", "| Trace | Score | Passed |", "|---|---:|---:|"])
    for trace in result["traces"]:
        lines.append(
            f"| {trace['name']} | {trace['score']:.3f} | {'yes' if trace['passed'] else 'no'} |"
        )

    return "\n".join(lines) + "\n"


def _average(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 3)


def _resolve(base_dir: Path, path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return (base_dir / candidate).resolve()
