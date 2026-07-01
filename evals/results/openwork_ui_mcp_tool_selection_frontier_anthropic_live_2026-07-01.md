# Openwork ui mcp Anthropic Frontier Live Result - 2026-07-01

Passed: no
Live: yes

This retained receipt uses the newly provided Anthropic key against the accessible `claude-opus-4-8` profile.

> [!NOTE]
> The new key passed a smoke test. Later cells in this batch hit Anthropic credit exhaustion, so credit-exhausted rows are retained as provider-state evidence rather than hidden or deleted.

## Matrix Summary

- total: 14
- passed_cases: 0
- failed_cases: 0
- errors: 14
- skipped: 0
- score: 0.0

## Profiles

- `anthropic-opus48-frontier`: `claude-opus-4-8`

## Status By Profile

| Profile | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| `anthropic-opus48-frontier` | 0 | 0 | 14 | 0 |

## Remaining Failure Clusters

- 2x `bridge check uses status`: status `error`, chose `error: credit balance is too low`
- 2x `unknown current screen uses snapshot`: status `error`, chose `error: credit balance is too low`
- 2x `action discovery uses list actions`: status `error`, chose `error: credit balance is too low`
- 2x `known action id executes action`: status `error`, chose `error: credit balance is too low`
- 2x `unknown action id lists actions first`: status `error`, chose `error: credit balance is too low`
- 2x `coordinate click avoids semantic bridge`: status `error`, chose `error: credit balance is too low`
- 2x `app maybe closed checks status before action`: status `error`, chose `error: credit balance is too low`

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
