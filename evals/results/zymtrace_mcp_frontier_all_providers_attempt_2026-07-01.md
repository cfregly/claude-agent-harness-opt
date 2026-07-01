# Zymtrace MCP Frontier All-Provider Attempt - 2026-07-01

Passed: no
Live: yes

This is the retained all-provider frontier attempt. It includes Anthropic `claude-opus-4-8`, OpenAI `gpt-5.5`, and Gemini `gemini-3.1-pro-preview-customtools`. The run is intentionally retained as descent evidence because Anthropic exhausted API credits during the sweep and the frontier prompt-JSON harness exposed additional parser and routing failures.

## Matrix Summary

- total: 408
- passed_cases: 210
- failed_cases: 89
- errors: 109
- skipped: 0
- score: 0.515

## Status By Profile

| Profile | Model | Passed | Failed | Errors |
|---|---|---:|---:|---:|
| `anthropic-opus48-frontier` | `claude-opus-4-8` | 105 | 12 | 19 |
| `gemini-31-pro-customtools-frontier` | `gemini-3.1-pro-preview-customtools` | 31 | 24 | 81 |
| `openai-gpt55-frontier` | `gpt-5.5` | 74 | 53 | 9 |

## Blockers

- Anthropic `claude-fable-5` was unavailable to the provided key during smoke testing, so the all-provider attempt used accessible `claude-opus-4-8`.
- Anthropic API credit exhaustion stopped many `claude-opus-4-8` cells during the full sweep.
- This all-provider attempt is not the promoted improvement receipt; it is retained failure-discovery evidence.

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_frontier_all_providers_attempt_2026-07-01.json)
