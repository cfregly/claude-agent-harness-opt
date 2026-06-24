---
name: agent-audit
description: Review an agent's tool inventory, tool calls, reasoning summaries, tool outputs, final answers, and value-bar proof using this repo's trace-review harness. Use when asked to audit, test, score, or review agent traces, Claude Messages API transcripts, tool schemas, trace suites, or agent audit bundles for tool-use quality, inter-tool reasoning, recovery behavior, final answer grounding, and whether the work is adversarially-confirmed to add value.
---

# Agent Audit

Use the repo's CLI to produce deterministic trace reviews before giving judgment, then use the
Claude judge for real semantic audits when an API key is available. Prefer existing JSON artifacts
over reconstructing a trace from prose. Treat "adversarially-confirmed to add value" as the pass
bar.

## Decision Tree

1. If the user provides a tool inventory plus traces, use `audit-agent`.
2. If the user provides a regression suite, use `trace-suite`.
3. If the user provides one normalized trace, use `review-trace`.
4. If the user provides Claude Messages API content blocks, use `normalize-claude`, then review the normalized trace.
5. If the user provides raw prose or screenshots, ask for exported JSON unless a small manual trace can be built without guessing.
6. If an audit bundle lacks `value_bar`, treat it as failed until the value claim, baseline,
   candidate, threshold, and adversarial review are supplied.

## Commands

Run from the repo root.

```bash
python -m claude_agent_prompting audit-agent <bundle.json> --markdown
python -m claude_agent_prompting audit-agent <bundle.json> --claude-judge --markdown
python -m claude_agent_prompting trace-suite <suite.json> --markdown
python -m claude_agent_prompting review-trace <trace.json>
python -m claude_agent_prompting review-trace <trace.json> --claude-judge
python -m claude_agent_prompting normalize-claude <messages.json>
python -m claude_agent_prompting trace-judge-prompt <trace.json>
```

Use JSON output when another program will consume the result. Use `--markdown` when reporting to a
human.

## Review Method

1. Run the deterministic command first.
2. Read the failed checks, grouped by `structure`, `tool_use`, `reasoning`, and `final`.
3. Inspect the trace around any failed check before proposing a fix.
4. Check the value bar. Do not pass an audit without baseline improvement and adversarial confirmation.
5. For real audits, run `--claude-judge` so Claude reviews visible reasoning
   summaries, tool outputs, final grounding, and value over baseline.
6. Recommend prompt or tool changes only when they map directly to a failed check or Claude judge
   finding.
7. Use `trace-judge-prompt` only when you need a portable judge prompt instead of a live Claude API
   call.

## What To Look For

- Tools: duplicate names, vague purposes, missing `use_when` or `avoid_when`, overlapping search tools.
- Tool calls: wrong tool, missing required tool, forbidden tool, bad arguments, duplicate calls, over-budget calls.
- Tool outputs: missing result, result linked to no call, errors without recovery.
- Reasoning: no plan before the first tool, no reflection after results, no quality or evidence assessment.
- Final answer: unsupported claims, missing uncertainty, failure to use gathered evidence.
- Value bar: missing value claim, missing baseline, weak delta, no adversarial challenge, open objections.

## Reporting

Lead with the result and score. Then list the highest-impact failed checks and the concrete change
that would address each one.

Use this format:

```text
Result: pass/fail, score X.XXX

Findings:
- [category] failed check: evidence from trace. Suggested change.

Commands run:
- ...
```

Do not claim hidden reasoning exists. Use visible thinking summaries, provider-returned thinking
blocks, or explicit decision notes. If reasoning is unavailable, say the trace is not instrumented
well enough to audit inter-tool reasoning.
