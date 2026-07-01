# OpenWork UI MCP Finding

Share link: [OpenWork packet](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/openwork)

## Human Summary

Send this as a guardrail packet for OpenWork. The tested UI bridge flow already selected the right
tools on the retained slice, so the useful artifact is the coverage case set rather than an upstream
change request.

## Full Bundle

Bundle folder: [OpenWork retained guardrail bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/openwork_ui_mcp_guardrail_2026-06-28)

- Finding folder: [OpenWork finding](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/openwork)
- No-change packet: [PR_BODY.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/openwork_ui_mcp_guardrail_2026-06-28/PR_BODY.md)
- Reproduction doc: [REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/openwork_ui_mcp_guardrail_2026-06-28/REPRODUCTION.md)
- Evidence JSON: [evidence.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/openwork_ui_mcp_guardrail_2026-06-28/evidence.json)
- Matrix: [openwork_ui_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/openwork_ui_mcp_tool_selection.json)
- Frontier stress receipt: [openwork_ui_mcp_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_frontier_available_live_2026-07-01.md)
- Frontier JSON receipt: [openwork_ui_mcp_tool_selection_frontier_available_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_frontier_available_live_2026-07-01.json)
- Receipt: [openwork_ui_mcp_tool_selection_2026-06-28.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_2026-06-28.md)
- Sweep: [YC P2026 MCP Sweep](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/yc-p2026-mcp-sweep.md)
- Reproduce: [OpenWork reproduction doc](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/openwork_ui_mcp_guardrail_2026-06-28/REPRODUCTION.md)

## Result

Guardrail. No upstream change is promoted.

Current frontier stress receipt: 28 current available-frontier cells, 27 passed, 0 failed, 1 error on OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools`. Treat this as hill-descending coverage for the next tuning pass, not as a replacement for the promoted baseline-to-tuned result.

The docs-level and source-tuned variants both passed 7/7 on Anthropic prompt JSON. That means this
did not clear the adversarially-confirmed to add value bar as an improvement, because there was no
baseline failure to fix.

## What Was Tested

The slice covered:

- bridge status checks
- current UI snapshot
- available action listing
- known action execution
- unknown action discovery before execution
- coordinate-click no-tool boundary
- app-closed status check

## Evidence

- Source: [OpenWork repo](https://github.com/different-ai/openwork)
- Matrix: [openwork_ui_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/openwork_ui_mcp_tool_selection.json)
- Frontier stress receipt: [openwork_ui_mcp_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_frontier_available_live_2026-07-01.md)
- Receipt: [openwork_ui_mcp_tool_selection_2026-06-28.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_2026-06-28.md)
- Guardrail packet: [openwork_ui_mcp_guardrail_2026-06-28](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/openwork_ui_mcp_guardrail_2026-06-28)
- YC sweep: [YC P2026 MCP Sweep](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/yc-p2026-mcp-sweep.md)

## Reproduce

```bash
make optimize mcp=openwork
```
