# Frontier Stress Receipts - 2026-07-01

This page points maintainers to current frontier receipts for every retained MCP tool-selection eval plus the gstack skill-routing packet.

> [!NOTE]
> Use these receipts as hill-descending evidence first. A clean pass means the eval slice held on that frontier profile. A failed or errored receipt marks the next boundary or provider-state blocker to resolve.

## Start Here

| Scope | Link |
|---|---|
| Founder-facing findings | [Findings index](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings) |
| Confirmed changes | [Confirmed Improvements](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/confirmed-improvements.md) |
| Supabase example bundle | [Supabase full PR/evidence bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/supabase_mcp_database_tool_tuning_2026-06-25) |
| gstack packet | [gstack full PR/evidence bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/gstack_skill_routing_2026-06-25) |

## Human Summary

- OpenAI and Gemini available-frontier receipts: 15 retained receipts, 1356 cells, 1259 passed, 79 failed, and 18 errors.
- Anthropic Opus receipts: 15 retained receipts, 678 cells, 156 passed, 13 failed, and 509 errors.
- The newly provided Anthropic key passed a `claude-opus-4-8` smoke test, then exhausted available Anthropic credit partway through the full batch.
- `claude-fable-5` remains unavailable to the provided Anthropic key, so the retained Anthropic profile is the accessible `claude-opus-4-8` profile.

<details>
<summary>LLM / Machine-readable details</summary>

## OpenAI And Gemini Receipt Table

| Target | Scope | Status | Total | Passed | Failed | Errors | Markdown | JSON |
|---|---|---|---:|---:|---:|---:|---|---|
| Clickhouse mcp | MCP | passed | 40 | 40 | 0 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/clickhouse_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/clickhouse_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Context7 mcp | MCP | passed | 36 | 36 | 0 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/context7_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/context7_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Filesystem mcp | MCP | stress findings | 44 | 42 | 2 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/filesystem_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/filesystem_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Firecrawl mcp | MCP | stress findings | 60 | 51 | 9 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Github mcp | MCP | stress findings | 64 | 60 | 4 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/github_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/github_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| gstack Skill Routing | Skill | stress findings | 496 | 484 | 8 | 4 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/gstack_skill_matrix_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/gstack_skill_matrix_frontier_available_live_2026-07-01.json) |
| Humwork mcp | MCP | stress findings | 28 | 25 | 3 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Insforge mcp | MCP | stress findings | 76 | 64 | 11 | 1 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Openwork ui mcp | MCP | stress findings | 28 | 27 | 0 | 1 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Playwright mcp | MCP | stress findings | 52 | 43 | 9 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/playwright_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/playwright_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Postgres mcp Pro | MCP | passed | 36 | 36 | 0 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/postgres_mcp_pro_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/postgres_mcp_pro_tool_selection_frontier_available_live_2026-07-01.json) |
| Screenpipe mcp | MCP | stress findings | 44 | 43 | 1 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Slack mcp | MCP | passed | 32 | 32 | 0 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/slack_mcp_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/slack_mcp_tool_selection_frontier_available_live_2026-07-01.json) |
| Supabase mcp database | MCP | stress findings | 48 | 43 | 5 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_database_tool_selection_frontier_available_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_database_tool_selection_frontier_available_live_2026-07-01.json) |
| Zymtrace MCP | MCP | stress findings | 272 | 233 | 27 | 12 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_frontier_available_matrix_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_frontier_available_matrix_live_2026-07-01.json) |

## Anthropic Opus Receipt Table

| Target | Scope | Status | Total | Passed | Failed | Errors | Markdown | JSON |
|---|---|---|---:|---:|---:|---:|---|---|
| Clickhouse mcp | MCP | passed | 20 | 20 | 0 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/clickhouse_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/clickhouse_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Context7 mcp | MCP | stress findings | 18 | 16 | 2 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/context7_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/context7_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Filesystem mcp | MCP | passed | 22 | 22 | 0 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/filesystem_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/filesystem_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Firecrawl mcp | MCP | stress findings | 30 | 26 | 4 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/firecrawl_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Github mcp | MCP | stress findings | 32 | 30 | 2 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/github_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/github_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Humwork mcp | MCP | passed | 14 | 14 | 0 | 0 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/humwork_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Insforge mcp | MCP | stress findings | 38 | 28 | 5 | 5 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Openwork ui mcp | MCP | stress findings | 14 | 0 | 0 | 14 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/openwork_ui_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Playwright mcp | MCP | stress findings | 26 | 0 | 0 | 26 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/playwright_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/playwright_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Postgres mcp Pro | MCP | stress findings | 18 | 0 | 0 | 18 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/postgres_mcp_pro_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/postgres_mcp_pro_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Screenpipe mcp | MCP | stress findings | 22 | 0 | 0 | 22 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/screenpipe_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Slack mcp | MCP | stress findings | 16 | 0 | 0 | 16 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/slack_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/slack_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Supabase mcp database | MCP | stress findings | 24 | 0 | 0 | 24 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_database_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_database_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| Zymtrace mcp | MCP | stress findings | 136 | 0 | 0 | 136 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_tool_selection_frontier_anthropic_live_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/zymtrace_mcp_tool_selection_frontier_anthropic_live_2026-07-01.json) |
| gstack Skill Routing | Skill | stress findings | 248 | 0 | 0 | 248 | [summary](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/gstack_skill_matrix_frontier_anthropic_attempt_2026-07-01.md) | [json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/gstack_skill_matrix_frontier_anthropic_attempt_2026-07-01.json) |

## Run Shape

```bash
python -m claude_agent_harness_opt model-matrix <matrix> --env-file .env --live --require-live --providers openai-gpt55-frontier,gemini-31-pro-customtools-frontier --out <receipt> --concurrency 8
python -m claude_agent_harness_opt model-matrix <matrix> --env-file .env --live --require-live --providers anthropic-opus48-frontier --harnesses prompt_json --out <anthropic-receipt> --concurrency 8
```

</details>
