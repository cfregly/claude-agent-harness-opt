# Humwork MCP Finding

Share link: [Humwork packet](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/humwork)

## Result

Guardrail. No upstream change is promoted.

The README-level and skill-tuned variants both passed 7/7 on Anthropic prompt JSON. That means this
did not clear the adversarially-confirmed to add value bar as an improvement, because there was no
baseline failure to fix.

## What Was Tested

The slice covered:

- starting an expert consultation
- sending a follow-up to an active session
- reading expert replies
- closing a resolved chat
- rating a closed chat
- avoiding expert spend for a basic docs question
- avoiding external chat when secrets or customer exports would be shared

## Evidence

- Source: [Humwork MCP repo](https://github.com/humworkai/humwork-mcp)
- Matrix: [humwork_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/humwork_mcp_tool_selection.json)
- Receipt: [humwork_mcp_tool_selection_2026-06-28.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_2026-06-28.md)
- YC sweep: [YC P2026 MCP Sweep](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/yc-p2026-mcp-sweep.md)

## Reproduce

```bash
make optimize mcp=humwork
```
