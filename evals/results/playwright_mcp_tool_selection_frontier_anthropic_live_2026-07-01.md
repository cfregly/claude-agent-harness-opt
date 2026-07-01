# Playwright mcp Anthropic Frontier Live Result - 2026-07-01

Passed: no
Live: yes

This retained receipt uses the newly provided Anthropic key against the accessible `claude-opus-4-8` profile.

> [!NOTE]
> The new key passed a smoke test. Later cells in this batch hit Anthropic credit exhaustion, so credit-exhausted rows are retained as provider-state evidence rather than hidden or deleted.

## Matrix Summary

- total: 26
- passed_cases: 0
- failed_cases: 0
- errors: 26
- skipped: 0
- score: 0.0

## Profiles

- `anthropic-opus48-frontier`: `claude-opus-4-8`

## Status By Profile

| Profile | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| `anthropic-opus48-frontier` | 0 | 0 | 26 | 0 |

## Remaining Failure Clusters

- 2x `navigate to url`: status `error`, chose `error: credit balance is too low`
- 2x `inspect page for actionable refs`: status `error`, chose `error: credit balance is too low`
- 2x `capture full page visual proof`: status `error`, chose `error: credit balance is too low`
- 2x `click known target`: status `error`, chose `error: credit balance is too low`
- 2x `type search and submit`: status `error`, chose `error: credit balance is too low`
- 2x `fill multi field form`: status `error`, chose `error: credit balance is too low`
- 2x `select dropdown option`: status `error`, chose `error: credit balance is too low`
- 2x `wait for success text`: status `error`, chose `error: credit balance is too low`
- 2x `evaluate local storage`: status `error`, chose `error: credit balance is too low`
- 2x `press escape key`: status `error`, chose `error: credit balance is too low`

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/playwright_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
