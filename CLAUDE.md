# CLAUDE.md

Conventions for any agent working on `claude-agent-prompting`. Read this first.

## What this is

This repo is a public, standalone prompt kit for Claude-style agents. It renders agent system
prompts from recipes, scores whether a task deserves an agent, lints tool descriptions, and runs
offline evals over agent transcripts and final state.

## Run it

    pip install -e .
    python -m claude_agent_prompting render recipes/agentic_search.json
    python -m claude_agent_prompting score recipes/agentic_search.json
    python -m claude_agent_prompting eval evals/examples/search_answer.json

## Rules

- Keep it standalone. Do not reference parent workspaces, private notes, or local-only files.
- Keep it generic. Do not add interview framing, employer-specific context, or individual names.
- Apply the value bar everywhere. An audit, prompt change, tool change, or eval change passes only
  when it is adversarially-confirmed to add value: it must name the value claim, compare against a
  baseline, meet a minimum improvement threshold, and survive an adversarial check with no open
  objections.
- Source Claude and agent-prompting claims. If a factual claim changes, update
  `docs/source-map.md` with the public source used.
- Keep examples offline. No API key should be required for tests or examples.
- Secrets never get committed. `.env` stays git-ignored.
- Prose is deslop-clean: no em-dashes, no en-dashes, no semicolons, and no buzzwords. Run
  `python scripts/deslop_check.py` before shipping.
