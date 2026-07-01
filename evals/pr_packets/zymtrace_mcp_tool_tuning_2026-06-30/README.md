# Zymtrace MCP Tool Tuning PR Packet

Share link: [Zymtrace full PR/evidence bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/zymtrace_mcp_tool_tuning_2026-06-30)

## Human Summary

Send this packet to Zymtrace as the full upstream review bundle. It contains the matrix, live result,
coverage receipt, reproduction command, and PR body for the tuned MCP routing rules that moved the
selected held-out cells from 14/24 stock passes to 24/24 tuned passes. It also includes the
2026-07-01 frontier stress/descent receipt for OpenAI `gpt-5.5` and Gemini
`gemini-3.1-pro-preview-customtools`.

## Full Bundle

[Current frontier stress receipts](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/frontier-stress-2026-07-01.md) tracks all retained current available-frontier receipts.

Bundle folder: [zymtrace_mcp_tool_tuning_2026-06-30](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/zymtrace_mcp_tool_tuning_2026-06-30)

- Finding folder: [Zymtrace finding](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/zymtrace)
- PR title: [PR_TITLE.txt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/zymtrace_mcp_tool_tuning_2026-06-30/PR_TITLE.txt)
- PR body: [PR_BODY.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/zymtrace_mcp_tool_tuning_2026-06-30/PR_BODY.md)
- Reproduction doc: [REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/zymtrace_mcp_tool_tuning_2026-06-30/REPRODUCTION.md)
- Evidence JSON: [evidence.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/zymtrace_mcp_tool_tuning_2026-06-30/evidence.json)
- Matrix: [zymtrace_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/zymtrace_mcp_tool_selection.json)
- Frontier stress receipt: [zymtrace_mcp_frontier_available_matrix_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_frontier_available_matrix_live_2026-07-01.md)
- Frontier JSON receipt: [zymtrace_mcp_frontier_available_matrix_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_frontier_available_matrix_live_2026-07-01.json)
- Anthropic Opus receipt: [zymtrace_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md)
- Anthropic Opus JSON: [zymtrace_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
- Live result: [zymtrace_mcp_matrix_live_2026-06-30.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_matrix_live_2026-06-30.json)
- Coverage audit: [zymtrace_mcp_coverage_2026-06-30.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_coverage_2026-06-30.md)
- Frontier stress result: [zymtrace_mcp_frontier_available_matrix_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_frontier_available_matrix_live_2026-07-01.md)
- Frontier JSON receipt: [zymtrace_mcp_frontier_available_matrix_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_frontier_available_matrix_live_2026-07-01.json)
- All-provider frontier attempt: [zymtrace_mcp_frontier_all_providers_attempt_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_frontier_all_providers_attempt_2026-07-01.md)

## Result

Current frontier stress receipt: 272 current available-frontier cells, 233 passed, 27 failed, 12 errors on OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools`. Treat this as hill-descending coverage for the next tuning pass.

Anthropic Opus frontier receipt: 136 Anthropic Opus cells, 0 passed, 0 failed, 136 errors. The new key passed smoke testing, then later Anthropic calls hit credit exhaustion where shown in the receipt.

Confirmed improvement. This clears the adversarially-confirmed to add value bar.

The tuned Zymtrace MCP boundary rules moved the selected held-out prompt JSON cells from 14/24
stock passes to 24/24 tuned passes across Anthropic, OpenAI, and Gemini.

## Frontier Stress Result

The current frontier sweep was run after adding named frontier profiles to the Zymtrace matrix and
hardening the prompt-JSON parser for fenced, wrapped, and array-shaped model outputs.

OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools` completed 272 live cells with
233 passed, 27 failed, and 12 errors. Treat this as hill-descending evidence for the next tuning
round, not as a replacement for the confirmed 24/24 held-out improvement.

Anthropic `claude-fable-5` was not available to the provided key. The newly provided key passed a `claude-opus-4-8` smoke test, then later sweep cells hit Anthropic API credit exhaustion.
The all-provider attempt is retained here:
[zymtrace_mcp_frontier_all_providers_attempt_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_frontier_all_providers_attempt_2026-07-01.md).

## Reproduce

[REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/zymtrace_mcp_tool_tuning_2026-06-30/REPRODUCTION.md)
contains the exact live matrix command and retained source pins.
