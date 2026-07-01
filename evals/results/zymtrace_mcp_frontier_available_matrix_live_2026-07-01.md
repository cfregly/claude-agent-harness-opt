# Zymtrace MCP Frontier Matrix Live Result - 2026-07-01

Passed: no
Live: yes

This is the retained frontier stress/descent receipt for the Zymtrace MCP tool-selection matrix. It uses the available frontier providers after the Anthropic frontier run was blocked by API credit exhaustion.

## Matrix Summary

- total: 272
- passed_cases: 233
- failed_cases: 27
- errors: 12
- skipped: 0
- score: 0.857

## Profiles

- `gemini-31-pro-customtools-frontier`: `gemini-3.1-pro-preview-customtools`
- `openai-gpt55-frontier`: `gpt-5.5`

## Status By Profile

| Profile | Passed | Failed | Errors |
|---|---:|---:|---:|
| `gemini-31-pro-customtools-frontier` | 116 | 19 | 1 |
| `openai-gpt55-frontier` | 117 | 8 | 11 |

## Status By Variant

| Tool Variant | Instruction Variant | Passed | Failed | Errors |
|---|---|---:|---:|---:|
| `stock_zymtrace_mcp` | `zymtrace_host_and_skill_rules` | 49 | 17 | 2 |
| `stock_zymtrace_mcp` | `zymtrace_host_rules` | 58 | 6 | 4 |
| `tuned_zymtrace_mcp_boundaries` | `zymtrace_host_and_skill_rules` | 62 | 3 | 3 |
| `tuned_zymtrace_mcp_boundaries` | `zymtrace_host_rules` | 64 | 1 | 3 |

## Remaining Failure Clusters

- 3x `selected trace drilldown is bounded`: status `failed`, chose `hot_traces`
- 3x `hot trace discovery is bounded`: status `failed`, chose `hot_traces`
- 3x `project top hosts endpoint`: status `error`, chose `none/error`
- 2x `project top pods endpoint`: status `error`, chose `none/error`
- 2x `default project metrics discovery skips search`: status `failed`, chose `project_metrics_activity_aggr`
- 2x `default project raw sample skips search`: status `failed`, chose `project_events_raw`
- 2x `gpu inference workflow starts with metrics`: status `failed`, chose `project_metrics_activity_aggr`
- 2x `project json flamegraph stays project scoped`: status `failed`, chose `flamegraph`
- 2x `project top deployments endpoint`: status `error`, chose `none/error`
- 2x `project top scripts endpoint`: status `error`, chose `none/error`
- 2x `project top executables endpoint`: status `failed`, chose `topentities`
- 2x `project top namespaces endpoint`: status `failed`, chose `topentities`

## Command

```bash
python -m claude_agent_harness_opt model-matrix evals/model_matrix/zymtrace_mcp_tool_selection.json --env-file .env --live --require-live --providers openai-gpt55-frontier,gemini-31-pro-customtools-frontier --harnesses prompt_json --variants stock_zymtrace_mcp,tuned_zymtrace_mcp_boundaries --out evals/results/zymtrace_mcp_frontier_available_matrix_live_2026-07-01.json --concurrency 8
```

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_frontier_available_matrix_live_2026-07-01.json)
