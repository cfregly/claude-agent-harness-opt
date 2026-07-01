# Screenpipe MCP Finding

Share link: [Screenpipe packet](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/screenpipe)

## Human Summary

Send this to Screenpipe maintainers when discussing exact phrase lookup. The confirmed fix is to
route literal term and phrase searches to `keyword-search`, while keeping broader transcript and
screen-content filtering on `search-content`.

## Full Bundle

Bundle folder: [Screenpipe full PR/evidence bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/screenpipe_mcp_tool_tuning_2026-06-28)

- Finding folder: [Screenpipe finding](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/screenpipe)
- PR body: [PR_BODY.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/screenpipe_mcp_tool_tuning_2026-06-28/PR_BODY.md)
- Reproduction doc: [REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/screenpipe_mcp_tool_tuning_2026-06-28/REPRODUCTION.md)
- Evidence JSON: [evidence.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/screenpipe_mcp_tool_tuning_2026-06-28/evidence.json)
- Matrix: [screenpipe_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/screenpipe_mcp_tool_selection.json)
- Frontier stress receipt: [screenpipe_mcp_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_frontier_available_live_2026-07-01.md)
- Frontier JSON receipt: [screenpipe_mcp_tool_selection_frontier_available_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_frontier_available_live_2026-07-01.json)
- Anthropic Opus receipt: [screenpipe_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md)
- Anthropic Opus JSON: [screenpipe_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
- Receipt: [screenpipe_mcp_tool_selection_2026-06-28.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_2026-06-28.md)
- Detailed note: [Screenpipe MCP Tool Tuning](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/screenpipe-mcp-tool-tuning.md)
- Reproduce: [Screenpipe reproduction doc](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/screenpipe_mcp_tool_tuning_2026-06-28/REPRODUCTION.md)

## Result

Confirmed improvement. This clears the adversarially-confirmed to add value bar.

Current frontier stress receipt: 44 current available-frontier cells, 43 passed, 1 failed, 0 errors on OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools`. Treat this as hill-descending coverage for the next tuning pass, not as a replacement for the promoted baseline-to-tuned result.

Anthropic Opus frontier receipt: 22 Anthropic Opus cells, 0 passed, 0 failed, 22 errors. The new key passed smoke testing, then later Anthropic calls hit credit exhaustion where shown in the receipt.

The live Anthropic prompt JSON run moved from 6/7 to 7/7.

## What Failed

The baseline chose `search-content` for exact phrase lookup:

```text
Find every screen or transcript where I typed or saw the exact phrase "Stripe webhook" yesterday.
```

That is too broad for a literal keyword task. Screenpipe has a dedicated `keyword-search` tool.

The tuned version chose `keyword-search`.

## Suggested Change

Make the split explicit:

```text
Use keyword-search for literal terms and exact phrases.

Use search-content for transcript lines, screen text, speaker or window filters, tags, memories,
and broader content search.
```

## Evidence

- Source: [Screenpipe repo](https://github.com/screenpipe/screenpipe)
- Matrix: [screenpipe_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/screenpipe_mcp_tool_selection.json)
- Frontier stress receipt: [screenpipe_mcp_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_frontier_available_live_2026-07-01.md)
- Receipt: [screenpipe_mcp_tool_selection_2026-06-28.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_2026-06-28.md)
- PR packet: [screenpipe_mcp_tool_tuning_2026-06-28](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/screenpipe_mcp_tool_tuning_2026-06-28)
- Detailed note: [Screenpipe MCP Tool Tuning](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/screenpipe-mcp-tool-tuning.md)

## Reproduce

```bash
make optimize mcp=screenpipe
```
