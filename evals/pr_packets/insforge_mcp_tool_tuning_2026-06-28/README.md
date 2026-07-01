# InsForge MCP Tool Tuning PR Packet

Share link: [InsForge MCP Tool Tuning full PR/evidence bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28)

## Human Summary

Send this packet to InsForge maintainers when discussing deployment safety. It packages the matrix, retained live receipt, reproduction command, and proposed wording for requiring absolute sourceDirectory values before create-deployment.

## Full Bundle

[Current frontier stress receipts](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/frontier-stress-2026-07-01.md) tracks all retained current available-frontier receipts.

Bundle folder: [insforge_mcp_tool_tuning_2026-06-28](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28)

- Finding folder: [InsForge MCP Tool Tuning finding](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/insforge)
- PR title: [PR_TITLE.txt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28/PR_TITLE.txt)
- PR body: [PR_BODY.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28/PR_BODY.md)
- Reproduction doc: [REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28/REPRODUCTION.md)
- Evidence JSON: [evidence.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28/evidence.json)
- Matrix: [insforge_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/insforge_mcp_tool_selection.json)
- Frontier stress receipt: [insforge_mcp_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_available_live_2026-07-01.md)
- Frontier JSON receipt: [insforge_mcp_tool_selection_frontier_available_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_available_live_2026-07-01.json)
- Anthropic Opus receipt: [insforge_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md)
- Anthropic Opus JSON: [insforge_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
- Live result: [insforge_mcp_tool_selection_2026-06-28.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_2026-06-28.md)
- Detailed note: [insforge-mcp-tool-tuning.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/insforge-mcp-tool-tuning.md)

## Result

Current frontier stress receipt: 76 current available-frontier cells, 64 passed, 11 failed, 1 error on OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools`. Treat this as hill-descending coverage for the next tuning pass.

Anthropic Opus frontier receipt: 38 Anthropic Opus cells, 28 passed, 5 failed, 5 errors. The new key passed smoke testing, then later Anthropic calls hit credit exhaustion where shown in the receipt.

Confirmed improvement. This clears the adversarially-confirmed to add value bar.

The live Anthropic prompt JSON run moved from 15/16 baseline passes to 16/16 tuned passes by routing the relative-path deployment request to NO_TOOL.

## Evidence

- Source: [InsForge MCP repo](https://github.com/InsForge/insforge-mcp)
- Matrix: [insforge_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/insforge_mcp_tool_selection.json)
- Live result: [insforge_mcp_tool_selection_2026-06-28.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_2026-06-28.md)
- Detailed note: [insforge-mcp-tool-tuning.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/insforge-mcp-tool-tuning.md)
- Ledger: [Confirmed Improvements](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/confirmed-improvements.md)

## Reproduce

[REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28/REPRODUCTION.md) contains the exact command and pinned matrix surface.
