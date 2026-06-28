# OpenWork UI MCP Finding

Share link: [OpenWork packet](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/openwork)

## Result

Guardrail. No upstream change is promoted.

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
- Receipt: [openwork_ui_mcp_tool_selection_2026-06-28.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_2026-06-28.md)
- YC sweep: [YC P2026 MCP Sweep](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/yc-p2026-mcp-sweep.md)

## Reproduce

```bash
make optimize mcp=openwork
```
