# Postgres mcp Pro Anthropic Frontier Live Result - 2026-07-01

Passed: no
Live: yes

This retained receipt uses the newly provided Anthropic key against the accessible `claude-opus-4-8` profile.

> [!NOTE]
> The new key passed a smoke test. Later cells in this batch hit Anthropic credit exhaustion, so credit-exhausted rows are retained as provider-state evidence rather than hidden or deleted.

## Matrix Summary

- total: 18
- passed_cases: 0
- failed_cases: 0
- errors: 18
- skipped: 0
- score: 0.0

## Profiles

- `anthropic-opus48-frontier`: `claude-opus-4-8`

## Status By Profile

| Profile | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| `anthropic-opus48-frontier` | 0 | 0 | 18 | 0 |

## Remaining Failure Clusters

- 2x `discover schemas`: status `error`, chose `error: credit balance is too low`
- 2x `list schema objects`: status `error`, chose `error: credit balance is too low`
- 2x `inspect table structure`: status `error`, chose `error: credit balance is too low`
- 2x `run ready read query`: status `error`, chose `error: credit balance is too low`
- 2x `get query plan`: status `error`, chose `error: credit balance is too low`
- 2x `rank slow workload queries`: status `error`, chose `error: credit balance is too low`
- 2x `workload index tuning`: status `error`, chose `error: credit balance is too low`
- 2x `specific query index tuning`: status `error`, chose `error: credit balance is too low`
- 2x `database health check`: status `error`, chose `error: credit balance is too low`

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/postgres_mcp_pro_tool_selection_frontier_anthropic_live_2026-07-01.json)
