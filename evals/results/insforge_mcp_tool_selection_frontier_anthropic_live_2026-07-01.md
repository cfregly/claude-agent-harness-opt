# Insforge mcp Anthropic Frontier Live Result - 2026-07-01

Passed: no
Live: yes

This retained receipt uses the newly provided Anthropic key against the accessible `claude-opus-4-8` profile.

> [!NOTE]
> The new key passed a smoke test. Later cells in this batch hit Anthropic credit exhaustion, so credit-exhausted rows are retained as provider-state evidence rather than hidden or deleted.

## Matrix Summary

- total: 38
- passed_cases: 28
- failed_cases: 5
- errors: 5
- skipped: 0
- score: 0.737

## Profiles

- `anthropic-opus48-frontier`: `claude-opus-4-8`

## Status By Profile

| Profile | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| `anthropic-opus48-frontier` | 28 | 5 | 5 | 0 |

## Remaining Failure Clusters

- 2x `client token uses anon key`: status `failed`, chose `get-anon-key`
- 1x `new project setup reads instructions`: status `failed`, chose `fetch-docs`
- 1x `function logs use container logs`: status `failed`, chose `get-container-logs`
- 1x `relative deploy path avoids tool`: status `failed`, chose `create-deployment`
- 1x `prepared remote upload starts deployment`: status `error`, chose `error: credit balance is too low`
- 1x `relative deploy path avoids tool`: status `error`, chose `error: credit balance is too low`
- 1x `delete storage bucket uses delete bucket`: status `error`, chose `error: credit balance is too low`
- 1x `create function uses create function`: status `error`, chose `error: credit balance is too low`
- 1x `delete function uses delete function`: status `error`, chose `error: credit balance is too low`

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
