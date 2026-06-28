# Zymtrace MCP Finding

Share link: [Zymtrace packet](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/zymtrace)

## Result

Confirmed improvement. This clears the adversarially-confirmed to add value bar.

The held-out prompt JSON run moved from 2/5 to 5/5 on Anthropic, 2/5 to 5/5 on OpenAI, and 2/5 to
5/5 on Gemini.

## What Failed

The stock descriptions picked the right broad tools on some cases but missed required arguments and
workflow boundaries:

- default project id for project-scoped calls
- metrics-first routing for GPU and inference work
- first-pass `hot_traces` with bounded metadata
- full-trace drilldown with selected `prefix_hash`, `meta_only=false`, and `limit=1`

## Suggested Change

Encode the profiling workflow in the tool surface:

```text
Use the default project id unless the user names another project.

Use metrics discovery before querying GPU or inference metrics.

Use rank-first tools for CPU investigations, then drill into selected traces.

Use bounded hot-trace metadata first. Fetch a full trace only after a prefix hash is selected.
```

## Evidence

- Source: [Zymtrace MCP docs](https://docs.zymtrace.com/category/model-context-protocol-mcp/)
- Matrix: [zymtrace_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/zymtrace_mcp_tool_selection.json)
- Ledger: [Confirmed Improvements](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/confirmed-improvements.md)
- Sweep: [Public MCP Sweep](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/public-mcp-sweep.md)

## Reproduce

```bash
make optimize mcp=zymtrace
```
