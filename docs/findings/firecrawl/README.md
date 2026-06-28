# Firecrawl MCP Finding

Share link: [Firecrawl packet](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/firecrawl)

## Result

Confirmed improvement. This clears the adversarially-confirmed to add value bar.

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
- Detailed note: [Firecrawl MCP Tool Tuning](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/firecrawl-mcp-tool-tuning.md)
- Ledger: [Confirmed Improvements](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/confirmed-improvements.md)

## Reproduce

```bash
make optimize mcp=firecrawl
```
