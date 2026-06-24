"""Command line interface for the prompt kit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .evals import build_judge_prompt, evaluate_case, load_eval_case
from .prompt_builder import lint_tools, load_recipe, render_prompt
from .suitability import score_use_case


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="claude-agent-prompting")
    subparsers = parser.add_subparsers(dest="command", required=True)

    render_parser = subparsers.add_parser("render", help="render a system prompt from a recipe")
    render_parser.add_argument("recipe", type=Path)

    score_parser = subparsers.add_parser("score", help="score whether a recipe fits an agent loop")
    score_parser.add_argument("recipe", type=Path)

    lint_parser = subparsers.add_parser("lint-tools", help="lint tool names and descriptions")
    lint_parser.add_argument("recipe", type=Path)

    eval_parser = subparsers.add_parser("eval", help="run an offline eval case")
    eval_parser.add_argument("case", type=Path)

    judge_parser = subparsers.add_parser("judge-prompt", help="render an LLM judge prompt")
    judge_parser.add_argument("case", type=Path)

    args = parser.parse_args(argv)

    if args.command == "render":
        recipe = load_recipe(args.recipe)
        sys.stdout.write(render_prompt(recipe))
        return 0

    if args.command == "score":
        recipe = load_recipe(args.recipe)
        print(json.dumps(score_use_case(recipe.get("use_case", {})), indent=2, sort_keys=True))
        return 0

    if args.command == "lint-tools":
        recipe = load_recipe(args.recipe)
        issues = lint_tools(recipe)
        print(json.dumps({"passed": not issues, "issues": issues}, indent=2, sort_keys=True))
        return 1 if issues else 0

    if args.command == "eval":
        result = evaluate_case(load_eval_case(args.case))
        print(result.to_json())
        return 0 if result.passed else 1

    if args.command == "judge-prompt":
        sys.stdout.write(build_judge_prompt(load_eval_case(args.case)))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2
