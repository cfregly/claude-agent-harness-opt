# Firecrawl MCP Tool Tuning PR Packet

Share link: [Firecrawl MCP Tool Tuning full PR/evidence bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25)

## Human Summary

Send this packet to Firecrawl maintainers when discussing scrape-versus-extract routing. It packages the matrix, live single-page result, reproduction command, and proposed wording for routing one exact product page with structured fields to firecrawl_scrape.

## Full Bundle

[Current frontier stress receipts](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/frontier-stress-2026-07-01.md) tracks all retained current available-frontier receipts.

Bundle folder: [firecrawl_mcp_tool_tuning_2026-06-25](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25)

- Finding folder: [Firecrawl MCP Tool Tuning finding](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/firecrawl)
- PR title: [PR_TITLE.txt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25/PR_TITLE.txt)
- PR body: [PR_BODY.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25/PR_BODY.md)
- Reproduction doc: [REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25/REPRODUCTION.md)
- Evidence JSON: [evidence.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25/evidence.json)
- Matrix: [firecrawl_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/firecrawl_mcp_tool_selection.json)
- Frontier stress receipt: [firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.md)
- Frontier JSON receipt: [firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.json)
- Anthropic Opus receipt: [firecrawl_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md)
- Anthropic Opus JSON: [firecrawl_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
- Live result: [firecrawl_mcp_single_page_live_2026-06-25.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_single_page_live_2026-06-25.md)
- Detailed note: [firecrawl-mcp-tool-tuning.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/firecrawl-mcp-tool-tuning.md)

## Result

Current frontier stress receipt: 60 current available-frontier cells, 51 passed, 9 failed, 0 errors on OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools`. Treat this as hill-descending coverage for the next tuning pass.

Anthropic Opus frontier receipt: 30 Anthropic Opus cells, 26 passed, 4 failed, 0 errors. The new key passed smoke testing, then later Anthropic calls hit credit exhaustion where shown in the receipt.

Confirmed improvement. This clears the adversarially-confirmed to add value bar.

The adversarial single-page structured-fields cell moved from 0/6 legacy passes to 6/6 tuned passes across Anthropic, OpenAI, Gemini, native tools, and prompt JSON.

## Evidence

- Source: [Firecrawl MCP server](https://github.com/firecrawl/firecrawl-mcp-server)
- Matrix: [firecrawl_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/firecrawl_mcp_tool_selection.json)
- Live result: [firecrawl_mcp_single_page_live_2026-06-25.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_single_page_live_2026-06-25.md)
- Detailed note: [firecrawl-mcp-tool-tuning.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/firecrawl-mcp-tool-tuning.md)
- Ledger: [Confirmed Improvements](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/confirmed-improvements.md)

## Reproduce

[REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25/REPRODUCTION.md) contains the exact command and pinned matrix surface.
