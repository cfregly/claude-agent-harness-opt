# Slack mcp Anthropic Frontier Live Result - 2026-07-01

Passed: no
Live: yes

This retained receipt uses the newly provided Anthropic key against the accessible `claude-opus-4-8` profile.

> [!NOTE]
> The new key passed a smoke test. Later cells in this batch hit Anthropic credit exhaustion, so credit-exhausted rows are retained as provider-state evidence rather than hidden or deleted.

## Matrix Summary

- total: 16
- passed_cases: 0
- failed_cases: 0
- errors: 16
- skipped: 0
- score: 0.0

## Profiles

- `anthropic-opus48-frontier`: `claude-opus-4-8`

## Status By Profile

| Profile | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| `anthropic-opus48-frontier` | 0 | 0 | 16 | 0 |

## Remaining Failure Clusters

- 2x `list channels to find id`: status `error`, chose `error: credit balance is too low`
- 2x `post top level channel message`: status `error`, chose `error: credit balance is too low`
- 2x `reply in existing thread`: status `error`, chose `error: credit balance is too low`
- 2x `read recent channel messages`: status `error`, chose `error: credit balance is too low`
- 2x `read thread replies`: status `error`, chose `error: credit balance is too low`
- 2x `add reaction to message`: status `error`, chose `error: credit balance is too low`
- 2x `list users to find id`: status `error`, chose `error: credit balance is too low`
- 2x `get known user profile`: status `error`, chose `error: credit balance is too low`

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/slack_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
