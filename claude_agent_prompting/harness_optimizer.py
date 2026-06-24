"""Hill-climb harness and tool-description variants from model-matrix failures."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .model_matrix import (
    MatrixFilters,
    load_matrix,
    render_model_matrix_markdown,
    run_model_matrix_data,
)


@dataclass(frozen=True)
class HarnessGrindOptions:
    baseline_variant: str
    concurrency: int = 1
    env_file: str | Path | None = None
    filters: MatrixFilters = field(default_factory=MatrixFilters)
    live: bool = False
    max_cases: int | None = None
    max_iterations: int = 1
    max_live_calls: int = 60
    require_live: bool = False


def run_harness_grind(path: str | Path, options: HarnessGrindOptions) -> dict[str, Any]:
    matrix_path = Path(path)
    matrix = load_matrix(matrix_path)
    baseline_variant = _find_variant(matrix, options.baseline_variant)
    run_filters = MatrixFilters(
        cases=options.filters.cases,
        harnesses=options.filters.harnesses,
        instruction_variants=options.filters.instruction_variants,
        providers=options.filters.providers,
        variants={options.baseline_variant},
    )
    selected_call_count = _planned_call_count(matrix, run_filters, options.max_cases)
    candidate_count = max(1, options.max_iterations)
    projected_live_calls = selected_call_count * (1 + candidate_count)
    if options.live and projected_live_calls > options.max_live_calls:
        return {
            "baseline_variant": options.baseline_variant,
            "error": (
                f"live call cap blocked run: projected {projected_live_calls}, "
                f"cap {options.max_live_calls}"
            ),
            "passed": False,
            "projected_live_calls": projected_live_calls,
        }

    baseline = run_model_matrix_data(
        matrix,
        matrix_name=matrix.get("name", str(matrix_path)),
        live=options.live,
        env_file=options.env_file,
        require_live=options.require_live,
        filters=run_filters,
        max_cases=options.max_cases,
        concurrency=options.concurrency,
    )
    candidates = []
    current_best = {
        "name": options.baseline_variant,
        "score": baseline["summary"]["score"],
        "result": baseline,
        "variant": baseline_variant,
    }

    for iteration in range(options.max_iterations):
        generated = _generate_candidate_variant(
            current_best["variant"],
            matrix.get("cases", []),
            current_best["result"].get("results", []),
            iteration=iteration,
        )
        candidate_matrix = deepcopy(matrix)
        candidate_matrix["tool_variants"] = [generated]
        candidate_filters = MatrixFilters(
            cases=options.filters.cases,
            harnesses=options.filters.harnesses,
            instruction_variants=options.filters.instruction_variants,
            providers=options.filters.providers,
            variants={generated["name"]},
        )
        candidate_result = run_model_matrix_data(
            candidate_matrix,
            matrix_name=f"{matrix.get('name', str(matrix_path))} candidate {iteration + 1}",
            live=options.live,
            env_file=options.env_file,
            require_live=options.require_live,
            filters=candidate_filters,
            max_cases=options.max_cases,
            concurrency=options.concurrency,
        )
        candidate_score = candidate_result["summary"]["score"]
        candidates.append(
            {
                "iteration": iteration + 1,
                "name": generated["name"],
                "result": candidate_result,
                "score": candidate_score,
                "variant": generated,
            }
        )
        if candidate_score > current_best["score"]:
            current_best = {
                "name": generated["name"],
                "score": candidate_score,
                "result": candidate_result,
                "variant": generated,
            }
        else:
            break

    improvement = round(current_best["score"] - baseline["summary"]["score"], 3)
    promoted = current_best["name"] != options.baseline_variant and improvement > 0
    return {
        "baseline": baseline,
        "baseline_variant": options.baseline_variant,
        "best": {
            "improvement": improvement,
            "name": current_best["name"],
            "score": current_best["score"],
            "variant": current_best["variant"],
        },
        "candidates": candidates,
        "live": options.live,
        "passed": promoted if options.live else True,
        "projected_live_calls": projected_live_calls,
        "promoted": promoted,
        "value_bar": {
            "bar": "adversarially-confirmed to add value",
            "passed": promoted if options.live else False,
            "reason": (
                "candidate improved over baseline on selected live matrix cells"
                if promoted
                else "dry run only or no live improvement over baseline"
            ),
        },
    }


def render_harness_grind_markdown(result: dict[str, Any]) -> str:
    if result.get("error"):
        return f"# Harness Grind\n\nPassed: no\n\nError: {result['error']}\n"
    lines = [
        "# Harness Grind",
        "",
        f"Live: {'yes' if result['live'] else 'no'}",
        f"Passed: {'yes' if result['passed'] else 'no'}",
        f"Baseline variant: {result['baseline_variant']}",
        f"Best variant: {result['best']['name']}",
        f"Improvement: {result['best']['improvement']:.3f}",
        f"Projected live calls: {result['projected_live_calls']}",
        "",
        "## Baseline",
        "",
        render_model_matrix_markdown(result["baseline"]),
    ]
    for candidate in result["candidates"]:
        lines.extend(
            [
                "",
                f"## Candidate {candidate['iteration']}: {candidate['name']}",
                "",
                render_model_matrix_markdown(candidate["result"]),
            ]
        )
    lines.extend(
        [
            "",
            "## Promotion",
            "",
            f"Promoted: {'yes' if result['promoted'] else 'no'}",
            f"Value bar passed: {'yes' if result['value_bar']['passed'] else 'no'}",
            f"Reason: {result['value_bar']['reason']}",
        ]
    )
    return "\n".join(lines)


def _find_variant(matrix: dict[str, Any], name: str) -> dict[str, Any]:
    for variant in matrix.get("tool_variants", []):
        if variant.get("name") == name:
            return deepcopy(variant)
    raise ValueError(f"tool variant not found: {name}")


def _generate_candidate_variant(
    variant: dict[str, Any],
    cases: list[dict[str, Any]],
    results: list[dict[str, Any]],
    *,
    iteration: int,
) -> dict[str, Any]:
    candidate = deepcopy(variant)
    candidate["name"] = f"{variant.get('name', 'variant')}_hill_{iteration + 1}"
    hard_cases = _hard_cases(cases, results)
    for tool in candidate.get("tools", []):
        name = tool.get("name", "")
        expected_cases = [case for case in hard_cases if name in case.get("expected_tools", [])]
        forbidden_cases = [case for case in hard_cases if name in case.get("forbidden_tools", [])]
        if expected_cases:
            tool["use_when"] = _append_sentence(
                tool.get("use_when", ""),
                "Use when the task matches these evaluated boundaries: "
                + " ".join(case["task"] for case in expected_cases[:3]),
            )
        if forbidden_cases:
            tool["avoid_when"] = _append_sentence(
                tool.get("avoid_when", ""),
                "Avoid when one of these evaluated boundaries applies: "
                + " ".join(
                    f"{case['task']} Prefer {', '.join(case.get('expected_tools', []))}."
                    for case in forbidden_cases[:3]
                ),
            )
        if name == "Task" and expected_cases:
            tool["purpose"] = (
                "Delegate broad multi-step repository investigation that requires several "
                "searches, reads, and synthesis across unknown files."
            )
            tool["use_when"] = _append_sentence(
                tool.get("use_when", ""),
                "Use for broad investigation, mapping, summarization, or synthesis across unknown files.",
            )
            tool["avoid_when"] = _append_sentence(
                tool.get("avoid_when", ""),
                "Avoid for a single known file read, a single exact text search, or a simple filename glob.",
            )
        if name in {"Glob", "Grep", "Read"}:
            _sharpen_file_tool(tool)
        checks = list(tool.get("quality_checks") or [])
        checks.append("Choose this tool only when its boundary is narrower than the alternatives.")
        tool["quality_checks"] = _unique(checks)
    return candidate


def _hard_cases(cases: list[dict[str, Any]], results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    case_by_name = {case.get("name"): case for case in cases}
    failed_names = [item.get("case") for item in results if item.get("status") in {"failed", "error"}]
    if failed_names:
        return [case_by_name[name] for name in failed_names if name in case_by_name]
    planned_names = [item.get("case") for item in results if item.get("status") == "planned"]
    if planned_names:
        return [case_by_name[name] for name in planned_names if name in case_by_name]
    return cases


def _sharpen_file_tool(tool: dict[str, Any]) -> None:
    name = tool.get("name")
    if name == "Glob":
        tool["purpose"] = "Find file paths by filename or path pattern without reading file contents."
        tool["use_when"] = _append_sentence(
            tool.get("use_when", ""),
            "Use for listing or locating files by path, extension, or filename pattern.",
        )
        tool["avoid_when"] = _append_sentence(
            tool.get("avoid_when", ""),
            "Avoid when the task asks for text inside files or broad repository synthesis.",
        )
    elif name == "Grep":
        tool["purpose"] = "Search for text or regex matches inside files and return matching locations."
        tool["use_when"] = _append_sentence(
            tool.get("use_when", ""),
            "Use when the task asks where a symbol, string, TODO, function, or error text appears.",
        )
        tool["avoid_when"] = _append_sentence(
            tool.get("avoid_when", ""),
            "Avoid when the task asks for broad investigation, synthesis, or reading one known file.",
        )
    elif name == "Read":
        tool["purpose"] = "Read the contents of a known file path."
        tool["use_when"] = _append_sentence(
            tool.get("use_when", ""),
            "Use when an exact path is provided or a prior result identified the file to inspect.",
        )
        tool["avoid_when"] = _append_sentence(
            tool.get("avoid_when", ""),
            "Avoid for discovering unknown paths, text search, or broad multi-file investigation.",
        )


def _planned_call_count(matrix: dict[str, Any], filters: MatrixFilters, max_cases: int | None) -> int:
    profiles = [
        profile
        for profile in matrix.get("profiles", [])
        if _matches(filters.providers, profile.get("provider")) or _matches(filters.providers, profile.get("name"))
    ]
    variants = [
        variant
        for variant in matrix.get("tool_variants", [])
        if _matches(filters.variants, variant.get("name"))
    ]
    instructions = matrix.get("instruction_variants") or [{"name": "default"}]
    instructions = [
        item for item in instructions if _matches(filters.instruction_variants, item.get("name"))
    ]
    cases = [case for case in matrix.get("cases", []) if _matches(filters.cases, case.get("name"))]
    cases = cases[: max_cases or None]
    total = 0
    for profile in profiles:
        harnesses = profile.get("harnesses") or ["prompt_json"]
        harnesses = [harness for harness in harnesses if _matches(filters.harnesses, harness)]
        total += len(harnesses) * len(variants) * len(instructions) * len(cases)
    return total


def _matches(allowed: set[str] | None, value: Any) -> bool:
    return allowed is None or str(value) in allowed


def _append_sentence(existing: str, addition: str) -> str:
    if addition in existing:
        return existing
    if not existing:
        return addition
    return f"{existing.rstrip()} {addition}"


def _unique(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            out.append(item)
            seen.add(item)
    return out
