"""Render structured agent system prompts from JSON recipes."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class RecipeError(ValueError):
    """Raised when a recipe is missing fields needed to render a prompt."""


REQUIRED_TOP_LEVEL = {
    "name",
    "role",
    "task",
    "success_criteria",
    "done_when",
    "tools",
    "budgets",
    "thinking",
    "guardrails",
    "context",
}


def load_recipe(path: str | Path) -> dict[str, Any]:
    recipe_path = Path(path)
    with recipe_path.open("r", encoding="utf-8") as handle:
        recipe = json.load(handle)
    validate_recipe(recipe)
    return recipe


def validate_recipe(recipe: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL - set(recipe))
    if missing:
        raise RecipeError(f"recipe missing required fields: {', '.join(missing)}")

    if not isinstance(recipe["tools"], list) or not recipe["tools"]:
        raise RecipeError("recipe.tools must be a non-empty list")

    for tool in recipe["tools"]:
        for field in ("name", "purpose", "use_when"):
            if not tool.get(field):
                raise RecipeError(f"tool is missing {field}: {tool!r}")

    budgets = recipe["budgets"]
    for label in ("simple", "standard", "complex"):
        if label not in budgets:
            raise RecipeError(f"recipe.budgets missing {label}")
        if int(budgets[label]) <= 0:
            raise RecipeError(f"recipe.budgets.{label} must be positive")


def lint_tools(recipe_or_tools: dict[str, Any] | list[dict[str, Any]]) -> list[str]:
    tools = recipe_or_tools["tools"] if isinstance(recipe_or_tools, dict) else recipe_or_tools
    issues: list[str] = []
    seen: set[str] = set()
    normalized_words: dict[str, str] = {}

    for tool in tools:
        name = str(tool.get("name", "")).strip()
        if not name:
            issues.append("tool name is empty")
            continue
        normalized = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
        if normalized in seen:
            issues.append(f"duplicate or near-duplicate tool name: {name}")
        seen.add(normalized)

        words = {word for word in re.split(r"[_\W]+", normalized) if word}
        for word in words:
            previous = normalized_words.setdefault(word, name)
            if previous != name and word in {"search", "fetch", "read", "query", "lookup"}:
                issues.append(
                    f"tool names may overlap around '{word}': {previous} and {name}"
                )

        purpose = str(tool.get("purpose", "")).strip()
        use_when = str(tool.get("use_when", "")).strip()
        if len(purpose.split()) < 4:
            issues.append(f"tool purpose is too thin: {name}")
        if len(use_when.split()) < 4:
            issues.append(f"tool use_when is too thin: {name}")
        if "avoid_when" not in tool:
            issues.append(f"tool should state avoid_when: {name}")

    return sorted(set(issues))


def render_prompt(recipe: dict[str, Any]) -> str:
    validate_recipe(recipe)

    lines = [
        recipe["role"].strip(),
        "",
        "<agent_task>",
        recipe["task"].strip(),
        "</agent_task>",
        "",
        _section("success_criteria", recipe["success_criteria"]),
        _section("done_when", recipe["done_when"]),
        _budget_section(recipe["budgets"]),
        _tool_section(recipe["tools"]),
        _thinking_section(recipe["thinking"]),
        _value_bar_section(),
        _guardrail_section(recipe["guardrails"]),
        _context_section(recipe["context"]),
        _operating_loop(recipe),
    ]

    return "\n".join(line.rstrip() for line in lines if line is not None).strip() + "\n"


def _section(name: str, items: list[str]) -> str:
    return f"<{name}>\n{_bullets(items)}\n</{name}>\n"


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _budget_section(budgets: dict[str, Any]) -> str:
    return (
        "<tool_call_budgets>\n"
        f"- simple: use up to {budgets['simple']} tool calls before reassessing.\n"
        f"- standard: use up to {budgets['standard']} tool calls before reassessing.\n"
        f"- complex: use up to {budgets['complex']} tool calls before reassessing.\n"
        "- If the answer is found early, stop searching and verify instead of expanding scope.\n"
        "- If the perfect source or action path is unavailable, state the limitation and proceed "
        "with the best supported answer.\n"
        "</tool_call_budgets>\n"
    )


def _tool_section(tools: list[dict[str, Any]]) -> str:
    lines = ["<tool_selection>"]
    for tool in tools:
        lines.extend(
            [
                f"- {tool['name']}: {tool['purpose']}",
                f"  Use when: {tool['use_when']}",
                f"  Avoid when: {tool.get('avoid_when', 'another tool is more direct')}",
            ]
        )
        checks = tool.get("quality_checks") or []
        if checks:
            lines.append(f"  Quality checks: {', '.join(checks)}")
    lines.append("</tool_selection>\n")
    return "\n".join(lines)


def _thinking_section(thinking: dict[str, list[str]]) -> str:
    lines = ["<thinking_guidance>"]
    for label, items in thinking.items():
        lines.append(f"- {label.replace('_', ' ')}:")
        lines.extend(f"  - {item}" for item in items)
    lines.append("</thinking_guidance>\n")
    return "\n".join(lines)


def _guardrail_section(guardrails: dict[str, list[str]]) -> str:
    lines = ["<safety_and_reversibility>"]
    confirm_before = guardrails.get("confirm_before", [])
    never = guardrails.get("never", [])
    if confirm_before:
        lines.append("- Ask before actions that are hard to reverse or visible to others:")
        lines.extend(f"  - {item}" for item in confirm_before)
    if never:
        lines.append("- Never use these as shortcuts:")
        lines.extend(f"  - {item}" for item in never)
    lines.append("</safety_and_reversibility>\n")
    return "\n".join(lines)


def _value_bar_section() -> str:
    return (
        "<value_bar>\n"
        "- Treat work as complete only when it is adversarially-confirmed to add value.\n"
        "- Name the value claim, baseline, minimum improvement threshold, and adversarial challenge.\n"
        "- If the value claim has open adversarial objections, state them instead of calling the work done.\n"
        "</value_bar>\n"
    )


def _context_section(context: dict[str, Any]) -> str:
    lines = [
        "<context_management>",
        f"- strategy: {context.get('strategy', 'track progress explicitly')}",
    ]
    if context.get("progress_file"):
        lines.append(f"- progress file: {context['progress_file']}")
    if context.get("compact_when"):
        lines.append(f"- compact when: {context['compact_when']}")
    if context.get("subagent_policy"):
        lines.append(f"- subagents: {context['subagent_policy']}")
    lines.append("- preserve decisions, sources, open questions, and next actions.")
    lines.append("</context_management>\n")
    return "\n".join(lines)


def _operating_loop(recipe: dict[str, Any]) -> str:
    parallel = recipe.get("parallel_tool_calls", False)
    parallel_line = (
        "- Use independent tool calls in parallel when their inputs do not depend on each other."
        if parallel
        else "- Use tools sequentially unless there is a clear speed benefit."
    )
    return (
        "<operating_loop>\n"
        "- Start with the smallest useful plan, then act.\n"
        "- Observe tool results before choosing the next step.\n"
        "- Reflect on whether the result is reliable, stale, incomplete, or contradicted.\n"
        f"{parallel_line}\n"
        "- Keep iterating until the done criteria are met or a stop condition is reached.\n"
        "- Finish with the answer, evidence used, uncertainty, and any follow-up needed.\n"
        "</operating_loop>"
    )
