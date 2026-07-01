# Humwork MCP Finding

Share link: [Humwork packet](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/humwork)

## Human Summary

Send this as a guardrail packet for Humwork. The tested consultation workflow already selected the
right tools on the retained slice, so the useful artifact is the coverage case set rather than an
upstream change request.

## Full Bundle

Bundle folder: [Humwork retained guardrail bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/humwork_mcp_guardrail_2026-06-28)

- Finding folder: [Humwork finding](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/humwork)
- No-change packet: [PR_BODY.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/humwork_mcp_guardrail_2026-06-28/PR_BODY.md)
- Reproduction doc: [REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/humwork_mcp_guardrail_2026-06-28/REPRODUCTION.md)
- Evidence JSON: [evidence.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/humwork_mcp_guardrail_2026-06-28/evidence.json)
- Matrix: [humwork_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/humwork_mcp_tool_selection.json)
- Frontier stress receipt: [humwork_mcp_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_frontier_available_live_2026-07-01.md)
- Frontier JSON receipt: [humwork_mcp_tool_selection_frontier_available_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_frontier_available_live_2026-07-01.json)
- Anthropic Opus receipt: [humwork_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md)
- Anthropic Opus JSON: [humwork_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
- Receipt: [humwork_mcp_tool_selection_2026-06-28.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_2026-06-28.md)
- Sweep: [YC P2026 MCP Sweep](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/yc-p2026-mcp-sweep.md)
- Reproduce: [Humwork reproduction doc](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/humwork_mcp_guardrail_2026-06-28/REPRODUCTION.md)

## Result

Guardrail. No upstream change is promoted.

Current frontier stress receipt: 28 current available-frontier cells, 25 passed, 3 failed, 0 errors on OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools`. Treat this as hill-descending coverage for the next tuning pass, not as a replacement for the promoted baseline-to-tuned result.

Anthropic Opus frontier receipt: 14 Anthropic Opus cells, 14 passed, 0 failed, 0 errors. The new key passed smoke testing, then later Anthropic calls hit credit exhaustion where shown in the receipt.

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
- Frontier stress receipt: [humwork_mcp_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_frontier_available_live_2026-07-01.md)
- Receipt: [humwork_mcp_tool_selection_2026-06-28.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_2026-06-28.md)
- Guardrail packet: [humwork_mcp_guardrail_2026-06-28](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/humwork_mcp_guardrail_2026-06-28)
- YC sweep: [YC P2026 MCP Sweep](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/yc-p2026-mcp-sweep.md)

## Reproduce

```bash
make optimize mcp=humwork
```
