# Github mcp Anthropic Frontier Live Result - 2026-07-01

Passed: no
Live: yes

This retained receipt uses the newly provided Anthropic key against the accessible `claude-opus-4-8` profile.

> [!NOTE]
> The new key passed a smoke test. Later cells in this batch hit Anthropic credit exhaustion, so credit-exhausted rows are retained as provider-state evidence rather than hidden or deleted.

## Matrix Summary

- total: 32
- passed_cases: 30
- failed_cases: 2
- errors: 0
- skipped: 0
- score: 0.938

## Profiles

- `anthropic-opus48-frontier`: `claude-opus-4-8`

## Status By Profile

| Profile | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| `anthropic-opus48-frontier` | 30 | 2 | 0 | 0 |

## Remaining Failure Clusters

- 2x `file not found recovers with code search`: status `failed`, chose `search_code`

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/github_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
