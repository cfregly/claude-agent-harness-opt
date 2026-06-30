#!/usr/bin/env python3
"""Ensure every public CLI subcommand is exercised by CI."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
HELP_COMMANDS_RE = re.compile(r"\{([^}]+)\}")
CLI_COMMAND_RE = re.compile(r"python -m claude_agent_harness_opt\s+([a-z0-9][a-z0-9-]*)")


def main() -> int:
    failures = check_cli_coverage()
    if failures:
        print("\n".join(sorted(failures)))
        return 1
    print("CLI coverage check passed")
    return 0


def check_cli_coverage(root: Path = ROOT, cli_commands: set[str] | None = None) -> list[str]:
    commands = cli_commands or _load_cli_commands(root)
    ci_path = root / ".github" / "workflows" / "ci.yml"
    if not ci_path.exists():
        return [".github/workflows/ci.yml: missing"]

    ci_text = ci_path.read_text(encoding="utf-8")
    ci_commands = set(CLI_COMMAND_RE.findall(ci_text))
    failures = [
        f".github/workflows/ci.yml: missing direct CLI smoke for {command}"
        for command in sorted(commands - ci_commands)
    ]
    failures.extend(
        f".github/workflows/ci.yml: unknown CLI command {command}"
        for command in sorted(ci_commands - commands)
    )
    return failures


def _load_cli_commands(root: Path = ROOT) -> set[str]:
    result = subprocess.run(
        [sys.executable, "-m", "claude_agent_harness_opt", "--help"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    match = HELP_COMMANDS_RE.search(result.stdout)
    if not match:
        raise RuntimeError("could not parse CLI command list from --help")
    return {command.strip() for command in match.group(1).split(",") if command.strip()}


if __name__ == "__main__":
    raise SystemExit(main())
