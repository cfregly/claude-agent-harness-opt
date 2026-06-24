# claude-agent-prompting

[![ci](https://github.com/cfregly/claude-agent-prompting/actions/workflows/ci.yml/badge.svg)](https://github.com/cfregly/claude-agent-prompting/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A runnable prompt kit for Claude-style agents: decide whether a task deserves an agent, render a
structured system prompt, check tool design, and run local evals over agent transcripts.

The repo turns the main ideas from Anthropic's "Prompting for Agents" talk into code and templates.
It is intentionally offline. No API key is required, and the examples run with the Python standard
library.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .

python -m claude_agent_prompting render recipes/agentic_search.json
python -m claude_agent_prompting score recipes/agentic_search.json
python -m claude_agent_prompting lint-tools recipes/agentic_search.json
python -m claude_agent_prompting eval evals/examples/search_answer.json
python -m claude_agent_prompting judge-prompt evals/examples/search_answer.json
```

## What it implements

The kit encodes the agent prompting patterns that show up repeatedly in the talk and the current
Claude prompt engineering docs:

- task-fit scoring across complexity, value, viability, error cost, and recoverability
- simple starting prompts that grow only from observed failures
- explicit tool-selection guidance instead of relying on short tool descriptions
- distinct tool names and descriptions, with linting for overlap
- initial planning, reflection after tool results, source verification, and self-checks
- tool-call budgets for simple, standard, and complex work
- stop criteria, fallback behavior, and rollback of harmful prompt changes
- reversibility rules for destructive, shared, or hard to undo actions
- context strategy through progress files, compaction notes, and subagent summaries
- parallel tool calls when work is independent
- evals for answer accuracy, tool use accuracy, and final state accuracy
- small realistic eval sets, LLM judge rubrics, and manual review
- examples added only after failures show where they help

## Layout

```
claude_agent_prompting/
  prompt_builder.py  # recipe validation and system prompt rendering
  suitability.py     # agent task-fit scoring
  evals.py           # offline answer, tool-use, and final-state evals
  cli.py             # render, score, lint-tools, eval, judge-prompt
recipes/             # ready-to-edit agent recipes
evals/examples/      # small local eval cases
prompts/             # reusable prompt snippets
docs/                # technique map and source map
tests/               # standard-library unit tests
scripts/             # prose gate for public artifacts
```

## Verify it

```bash
python scripts/deslop_check.py
python -m compileall claude_agent_prompting scripts
python -m unittest discover -s tests -q
python -m claude_agent_prompting eval evals/examples/search_answer.json
```

## Sources

The technique map is grounded in Anthropic's public video and docs. See
[docs/source-map.md](docs/source-map.md) for the source list and timestamps used while building the
repo.

## License

MIT.
