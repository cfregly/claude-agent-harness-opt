# Supabase mcp database Anthropic Frontier Live Result - 2026-07-01

Passed: no
Live: yes

This retained receipt uses the newly provided Anthropic key against the accessible `claude-opus-4-8` profile.

> [!NOTE]
> The new key passed a smoke test. Later cells in this batch hit Anthropic credit exhaustion, so credit-exhausted rows are retained as provider-state evidence rather than hidden or deleted.

## Matrix Summary

- total: 24
- passed_cases: 0
- failed_cases: 0
- errors: 24
- skipped: 0
- score: 0.0

## Profiles

- `anthropic-opus48-frontier`: `claude-opus-4-8`

## Status By Profile

| Profile | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| `anthropic-opus48-frontier` | 0 | 0 | 24 | 0 |

## Remaining Failure Clusters

- 2x `list public tables`: status `error`, chose `error: credit balance is too low`
- 2x `inspect table columns`: status `error`, chose `error: credit balance is too low`
- 2x `list applied migrations`: status `error`, chose `error: credit balance is too low`
- 2x `list installed extensions`: status `error`, chose `error: credit balance is too low`
- 2x `run read only report query`: status `error`, chose `error: credit balance is too low`
- 2x `ddl create table uses migration`: status `error`, chose `error: credit balance is too low`
- 2x `ddl alter table uses migration`: status `error`, chose `error: credit balance is too low`
- 2x `ddl create index uses migration`: status `error`, chose `error: credit balance is too low`
- 2x `rls policy uses migration`: status `error`, chose `error: credit balance is too low`
- 2x `unknown relation error inspects schema`: status `error`, chose `error: credit balance is too low`

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_database_tool_selection_frontier_anthropic_live_2026-07-01.json)
