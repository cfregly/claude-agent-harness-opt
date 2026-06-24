"""Prompt recipes, task-fit scoring, and evals for Claude-style agents."""

from .adapters import claude_messages_to_trace
from .agent_audit import review_agent_bundle
from .claude_judge import judge_trace_with_claude
from .evals import evaluate_case
from .prompt_builder import lint_tools, load_recipe, render_prompt, validate_recipe
from .suitability import score_use_case
from .trace_suite import run_trace_suite
from .trace_review import review_trace
from .value_bar import evaluate_value_bar

__all__ = [
    "evaluate_case",
    "evaluate_value_bar",
    "claude_messages_to_trace",
    "judge_trace_with_claude",
    "lint_tools",
    "load_recipe",
    "render_prompt",
    "review_agent_bundle",
    "review_trace",
    "run_trace_suite",
    "score_use_case",
    "validate_recipe",
]
