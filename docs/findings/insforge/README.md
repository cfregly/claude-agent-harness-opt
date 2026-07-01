# InsForge MCP Finding

Share link: [InsForge packet](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/insforge)

## Human Summary

Send this to InsForge maintainers when discussing deployment safety. The confirmed fix is to reject
relative deployment paths before `create-deployment`, because that tool requires an absolute
`sourceDirectory`.

## Full Bundle

Bundle folder: [InsForge full PR/evidence bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28)

- Finding folder: [InsForge finding](https://github.com/cfregly/claude-agent-harness-opt/tree/main/docs/findings/insforge)
- PR body: [PR_BODY.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28/PR_BODY.md)
- Reproduction doc: [REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28/REPRODUCTION.md)
- Evidence JSON: [evidence.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28/evidence.json)
- Matrix: [insforge_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/insforge_mcp_tool_selection.json)
- Frontier stress receipt: [insforge_mcp_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_available_live_2026-07-01.md)
- Frontier JSON receipt: [insforge_mcp_tool_selection_frontier_available_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_available_live_2026-07-01.json)
- Receipt: [insforge_mcp_tool_selection_2026-06-28.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_2026-06-28.md)
- Detailed note: [InsForge MCP Tool Tuning](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/insforge-mcp-tool-tuning.md)
- Reproduce: [InsForge reproduction doc](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28/REPRODUCTION.md)

## Result

Confirmed improvement. This clears the adversarially-confirmed to add value bar.

Current frontier stress receipt: 76 current available-frontier cells, 64 passed, 11 failed, 1 error on OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools`. Treat this as hill-descending coverage for the next tuning pass, not as a replacement for the promoted baseline-to-tuned result.

The live Anthropic prompt JSON run moved from 15/16 to 16/16.

## What Failed

The baseline chose `create-deployment` for this task:

```text
Deploy my current directory . to InsForge now.
```

That is unsafe because InsForge deployment requires an absolute `sourceDirectory`.

The tuned version chose `NO_TOOL`.

## Suggested Change

Tighten `create-deployment`:

```text
Deploy or prepare upload for an existing source directory. Requires an absolute sourceDirectory
path.

Use when the user asks to deploy a local source tree and provides an absolute source directory.

Avoid for relative paths, starter-template creation, deployment status lookup, or triggering a
prepared deployment id in remote mode.
```

## Evidence

- Source: [InsForge MCP repo](https://github.com/InsForge/insforge-mcp)
- Matrix: [insforge_mcp_tool_selection.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/model_matrix/insforge_mcp_tool_selection.json)
- Frontier stress receipt: [insforge_mcp_tool_selection_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_frontier_available_live_2026-07-01.md)
- Receipt: [insforge_mcp_tool_selection_2026-06-28.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/insforge_mcp_tool_selection_2026-06-28.md)
- PR packet: [insforge_mcp_tool_tuning_2026-06-28](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/insforge_mcp_tool_tuning_2026-06-28)
- Detailed note: [InsForge MCP Tool Tuning](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/insforge-mcp-tool-tuning.md)

## Reproduce

```bash
make optimize mcp=insforge
```
