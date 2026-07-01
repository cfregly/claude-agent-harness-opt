# Zymtrace mcp Anthropic Frontier Live Result - 2026-07-01

Passed: no
Live: yes

This retained receipt uses the newly provided Anthropic key against the accessible `claude-opus-4-8` profile.

> [!NOTE]
> The new key passed a smoke test. Later cells in this batch hit Anthropic credit exhaustion, so credit-exhausted rows are retained as provider-state evidence rather than hidden or deleted.

## Matrix Summary

- total: 136
- passed_cases: 0
- failed_cases: 0
- errors: 136
- skipped: 0
- score: 0.0

## Profiles

- `anthropic-opus48-frontier`: `claude-opus-4-8`

## Status By Profile

| Profile | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| `anthropic-opus48-frontier` | 0 | 0 | 136 | 0 |

## Remaining Failure Clusters

- 4x `relative time needs date helper`: status `error`, chose `error: credit balance is too low`
- 4x `unknown project id uses search`: status `error`, chose `error: credit balance is too low`
- 4x `cpu hot functions`: status `error`, chose `error: credit balance is too low`
- 4x `hot containers use entities`: status `error`, chose `error: credit balance is too low`
- 4x `first trace discovery is meta only`: status `error`, chose `error: credit balance is too low`
- 4x `high level flamegraph`: status `error`, chose `error: credit balance is too low`
- 4x `discover metrics before query`: status `error`, chose `error: credit balance is too low`
- 4x `known metric query`: status `error`, chose `error: credit balance is too low`
- 4x `generated optimization advice`: status `error`, chose `error: credit balance is too low`
- 4x `raw events are explicit`: status `error`, chose `error: credit balance is too low`

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
