# Firecrawl MCP Finding

Share link: [Firecrawl packet](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/firecrawl)

## Human Summary

Send this to Firecrawl maintainers when discussing the scrape-versus-extract boundary. The confirmed
fix is to route exact known-page structured extraction to `firecrawl_scrape`, while keeping
multi-page field extraction on `firecrawl_extract`.

## Full Bundle

Bundle folder: [Firecrawl full PR/evidence bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25)

- Finding folder: [Firecrawl finding](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/firecrawl)
- PR body: [PR_BODY.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25/PR_BODY.md)
- Reproduction doc: [REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25/REPRODUCTION.md)
- Evidence JSON: [evidence.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25/evidence.json)
- Matrix: [firecrawl_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/firecrawl_mcp_tool_selection.json)
- Frontier stress receipt: [firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.md)
- Frontier JSON receipt: [firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.json)
- Anthropic Opus receipt: [firecrawl_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md)
- Anthropic Opus JSON: [firecrawl_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json)
- Live result: [firecrawl_mcp_single_page_live_2026-06-25.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_single_page_live_2026-06-25.md)
- Detailed note: [Firecrawl MCP Tool Tuning](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/firecrawl-mcp-tool-tuning.md)
- Ledger: [Confirmed Improvements](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/confirmed-improvements.md)
- Reproduce: [Firecrawl reproduction doc](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25/REPRODUCTION.md)

## Result

Confirmed improvement. This clears the adversarially-confirmed to add value bar.

Current frontier stress receipt: 60 current available-frontier cells, 51 passed, 9 failed, 0 errors on OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools`. Treat this as hill-descending coverage for the next tuning pass, not as a replacement for the promoted baseline-to-tuned result.

Anthropic Opus frontier receipt: 30 Anthropic Opus cells, 26 passed, 4 failed, 0 errors. The new key passed smoke testing, then later Anthropic calls hit credit exhaustion where shown in the receipt.

The full Anthropic prompt JSON run moved from 11/12 to 12/12. The adversarial single-case run also
passed across Anthropic, OpenAI, Gemini, native tools, and prompt JSON after tuning.

## What Failed

The baseline chose `firecrawl_extract` for one exact product URL with specific fields.

That should be `firecrawl_scrape` with JSON format. `firecrawl_extract` is better for broader
multi-page extraction jobs.

## Suggested Change

Make the scrape-versus-extract split explicit:

```text
Use firecrawl_scrape when the exact page URL is known and the task needs that page's content,
metadata, screenshot, branding, or structured fields.

Use firecrawl_extract when the user asks for specific fields across several pages or a broader
structured extraction job. Avoid for one known URL.
```

## Evidence

- Source: [Firecrawl MCP server](https://github.com/firecrawl/firecrawl-mcp-server)
- Matrix: [firecrawl_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/firecrawl_mcp_tool_selection.json)
- Frontier stress receipt: [firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.md)
- Live result: [firecrawl_mcp_single_page_live_2026-06-25.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_single_page_live_2026-06-25.md)
- PR packet: [firecrawl_mcp_tool_tuning_2026-06-25](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/firecrawl_mcp_tool_tuning_2026-06-25)
- Detailed note: [Firecrawl MCP Tool Tuning](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/firecrawl-mcp-tool-tuning.md)
- Ledger: [Confirmed Improvements](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/confirmed-improvements.md)

## Reproduce

```bash
make optimize mcp=firecrawl
```
