# Firecrawl mcp Anthropic Frontier Live Result - 2026-07-01

Passed: no
Live: yes

This retained receipt uses the newly provided Anthropic key against the accessible `claude-opus-4-8` profile.

> [!NOTE]
> The new key passed a smoke test. Later cells in this batch hit Anthropic credit exhaustion, so credit-exhausted rows are retained as provider-state evidence rather than hidden or deleted.

## Matrix Summary

- total: 30
- passed_cases: 26
- failed_cases: 4
- errors: 0
- skipped: 0
- score: 0.867

## Profiles

- `anthropic-opus48-frontier`: `claude-opus-4-8`

## Status By Profile

| Profile | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| `anthropic-opus48-frontier` | 26 | 4 | 0 | 0 |

## Remaining Failure Clusters

- 2x `complex autonomous research`: status `failed`, chose `firecrawl_agent`
- 1x `single known page structured fields`: status `failed`, chose `firecrawl_extract`
- 1x `single page concise json avoids markdown`: status `failed`, chose `firecrawl_extract`

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
