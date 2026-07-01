# Supabase MCP Database Tool Tuning PR Packet

Share link: [Supabase MCP Database Tool Tuning full PR/evidence bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/supabase_mcp_database_tool_tuning_2026-06-25)

## Human Summary

Send this packet to Supabase MCP maintainers when discussing database tool boundaries. It packages the matrix, live DDL/RLS result, reproduction command, and proposed wording for routing schema-changing SQL to apply_migration instead of execute_sql.

## Full Bundle

[Current frontier stress receipts](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/frontier-stress-2026-07-01.md) tracks all retained current available-frontier receipts.

Bundle folder: [supabase_mcp_database_tool_tuning_2026-06-25](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/supabase_mcp_database_tool_tuning_2026-06-25)

- Finding folder: [Supabase MCP Database Tool Tuning finding](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/supabase)
- PR title: [PR_TITLE.txt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/supabase_mcp_database_tool_tuning_2026-06-25/PR_TITLE.txt)
- PR body: [PR_BODY.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/supabase_mcp_database_tool_tuning_2026-06-25/PR_BODY.md)
- Reproduction doc: [REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/supabase_mcp_database_tool_tuning_2026-06-25/REPRODUCTION.md)
- Evidence JSON: [evidence.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/supabase_mcp_database_tool_tuning_2026-06-25/evidence.json)
- Matrix: [supabase_mcp_database_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/supabase_mcp_database_tool_selection.json)
- Frontier stress receipt: [supabase_mcp_database_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_database_tool_selection_frontier_available_live_2026-07-01.md)
- Frontier JSON receipt: [supabase_mcp_database_tool_selection_frontier_available_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_database_tool_selection_frontier_available_live_2026-07-01.json)
- Anthropic Opus receipt: [supabase_mcp_database_tool_selection_frontier_anthropic_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_database_tool_selection_frontier_anthropic_live_2026-07-01.md)
- Anthropic Opus JSON: [supabase_mcp_database_tool_selection_frontier_anthropic_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_database_tool_selection_frontier_anthropic_live_2026-07-01.json)
- Live result: [supabase_mcp_ddl_boundary_live_2026-06-25.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_ddl_boundary_live_2026-06-25.md)
- Detailed note: [supabase-mcp-tool-tuning.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/supabase-mcp-tool-tuning.md)

## Result

Current frontier stress receipt: 48 current available-frontier cells, 43 passed, 5 failed, 0 errors on OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools`. Treat this as hill-descending coverage for the next tuning pass.

Anthropic Opus frontier receipt: 24 Anthropic Opus cells, 0 passed, 0 failed, 24 errors. The new key passed smoke testing, then later Anthropic calls hit credit exhaustion where shown in the receipt.

Confirmed improvement. This clears the adversarially-confirmed to add value bar.

The adversarial DDL/RLS cells moved from 4/18 baseline passes to 18/18 tuned passes across Anthropic, OpenAI, Gemini, native tools, and prompt JSON.

## Evidence

- Source: [Supabase MCP repo](https://github.com/supabase/mcp)
- Matrix: [supabase_mcp_database_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/supabase_mcp_database_tool_selection.json)
- Live result: [supabase_mcp_ddl_boundary_live_2026-06-25.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/supabase_mcp_ddl_boundary_live_2026-06-25.md)
- Detailed note: [supabase-mcp-tool-tuning.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/supabase-mcp-tool-tuning.md)
- Ledger: [Confirmed Improvements](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/confirmed-improvements.md)

## Reproduce

[REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/supabase_mcp_database_tool_tuning_2026-06-25/REPRODUCTION.md) contains the exact command and pinned matrix surface.
