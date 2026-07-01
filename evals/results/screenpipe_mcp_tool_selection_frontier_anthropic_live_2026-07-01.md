# Screenpipe mcp Anthropic Frontier Live Result - 2026-07-01

Passed: no
Live: yes

This retained receipt uses the newly provided Anthropic key against the accessible `claude-opus-4-8` profile.

> [!NOTE]
> The new key passed a smoke test. Later cells in this batch hit Anthropic credit exhaustion, so credit-exhausted rows are retained as provider-state evidence rather than hidden or deleted.

## Matrix Summary

- total: 22
- passed_cases: 0
- failed_cases: 0
- errors: 22
- skipped: 0
- score: 0.0

## Profiles

- `anthropic-opus48-frontier`: `claude-opus-4-8`

## Status By Profile

| Profile | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| `anthropic-opus48-frontier` | 0 | 0 | 22 | 0 |

## Remaining Failure Clusters

- 2x `broad morning recap starts summary`: status `error`, chose `error: credit balance is too low`
- 2x `exact keyword uses keyword search`: status `error`, chose `error: credit balance is too low`
- 2x `speaker transcript uses content search`: status `error`, chose `error: credit balance is too low`
- 2x `ui button lookup uses elements`: status `error`, chose `error: credit balance is too low`
- 2x `known frame detail uses frame context`: status `error`, chose `error: credit balance is too low`
- 2x `create recurring automation uses pipe`: status `error`, chose `error: credit balance is too low`
- 2x `verify pipe output uses logs`: status `error`, chose `error: credit balance is too low`
- 2x `export video uses video export`: status `error`, chose `error: credit balance is too low`
- 2x `meeting inventory uses list meetings`: status `error`, chose `error: credit balance is too low`
- 2x `known frame elements use element tree`: status `error`, chose `error: credit balance is too low`

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
