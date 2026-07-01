# Frontier Stress Receipts - 2026-07-01

This page points maintainers to the current available-frontier receipts for every retained MCP tool-selection eval plus the gstack skill-routing packet.

> [!NOTE]
> Use these receipts as hill-descending evidence first. A clean pass means the eval slice held on available frontier models. A failed receipt marks the next boundary to tune, not a hidden failure.

## Start Here

| Scope | Link |
|---|---|
| Founder-facing findings | [Findings index](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings) |
| Confirmed changes | [Confirmed Improvements](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/confirmed-improvements.md) |
| Supabase example bundle | [Supabase full PR/evidence bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/supabase_mcp_database_tool_tuning_2026-06-25) |
| gstack packet | [gstack full PR/evidence bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/gstack_skill_routing_2026-06-25) |

## Human Summary

- 15 current available-frontier receipts are retained: 14 MCP receipts and 1 skill-routing receipt.
- The completed live frontier providers are OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools`.
- 4 receipts passed outright. 11 receipts are retained as descent targets for the next tuning pass.
- Anthropic frontier is blocked by account credit state in this workspace. The configured key is present, but a smoke call returns a low-credit API error, and `/home/cfregly/dev/anthropic` is not present here.

<details>
<summary>LLM / Machine-readable details</summary>

## Frontier Receipt Table

| Target | Scope | Status | Total | Passed | Failed | Errors | Markdown | JSON |
|---|---|---|---:|---:|---:|---:|---|---|
| ClickHouse MCP | MCP | passed | 40 | 40 | 0 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/clickhouse_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/clickhouse_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Context7 MCP | MCP | passed | 36 | 36 | 0 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/context7_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/context7_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Filesystem MCP | MCP | stress findings | 44 | 42 | 2 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/filesystem_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/filesystem_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Firecrawl MCP | MCP | stress findings | 60 | 51 | 9 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| GitHub MCP | MCP | stress findings | 64 | 60 | 4 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/github_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/github_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Humwork MCP | MCP | stress findings | 28 | 25 | 3 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| InsForge MCP | MCP | stress findings | 76 | 64 | 11 | 1 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| OpenWork UI MCP | MCP | stress findings | 28 | 27 | 0 | 1 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Playwright MCP | MCP | stress findings | 52 | 43 | 9 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/playwright_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/playwright_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Postgres MCP Pro | MCP | passed | 36 | 36 | 0 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/postgres_mcp_pro_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/postgres_mcp_pro_tool_selection_frontier_available_live_2026-07-01.json) |
| Screenpipe MCP | MCP | stress findings | 44 | 43 | 1 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Slack MCP | MCP | passed | 32 | 32 | 0 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/slack_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/slack_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Supabase MCP Database | MCP | stress findings | 48 | 43 | 5 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_database_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_database_tool_selection_frontier_available_live_2026-07-01.json) |
| Zymtrace MCP | MCP | stress findings | 272 | 233 | 27 | 12 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_frontier_available_matrix_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_frontier_available_matrix_live_2026-07-01.json) |
| gstack Skill Routing | Skill | stress findings | 496 | 484 | 8 | 4 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/gstack_skill_matrix_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/gstack_skill_matrix_frontier_available_live_2026-07-01.json) |

## Run Shape

```bash
python -m claude_agent_harness_opt model-matrix <matrix> --env-file .env --live --require-live --providers openai-gpt55-frontier,gemini-31-pro-customtools-frontier --out <receipt> --concurrency 8
```

</details>
