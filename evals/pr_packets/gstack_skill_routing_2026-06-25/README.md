# gstack Skill Routing PR Packet

Share link: [gstack full PR/evidence bundle](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/gstack_skill_routing_2026-06-25)

## Human Summary

Send this packet when discussing gstack skill routing. The retained evidence shows that tighter
skill descriptions improved browser, safety, and action-routing choices across the live matrix.

## Full Bundle

[Current frontier stress receipts](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/frontier-stress-2026-07-01.md) tracks all retained current available-frontier receipts.

Bundle folder: [gstack_skill_routing_2026-06-25](https://github.com/cfregly/claude-agent-harness-opt/tree/main/evals/pr_packets/gstack_skill_routing_2026-06-25)

- PR title: [PR_TITLE.txt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/gstack_skill_routing_2026-06-25/PR_TITLE.txt)
- PR body: [PR_BODY.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/gstack_skill_routing_2026-06-25/PR_BODY.md)
- Reproduction doc: [REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/gstack_skill_routing_2026-06-25/REPRODUCTION.md)
- Evidence JSON: [evidence.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/gstack_skill_routing_2026-06-25/evidence.json)
- Matrix: [gstack_skill_selection_matrix.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/targets/gstack/gstack_skill_selection_matrix.json)
- Frontier stress receipt: [gstack_skill_matrix_frontier_available_live_2026-07-01.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/gstack_skill_matrix_frontier_available_live_2026-07-01.md)
- Frontier JSON receipt: [gstack_skill_matrix_frontier_available_live_2026-07-01.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/gstack_skill_matrix_frontier_available_live_2026-07-01.json)
- Live result: [gstack_skill_matrix_live_2026-06-25.json](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/gstack_skill_matrix_live_2026-06-25.json)
- Audit note: [gstack Skill Routing Audit](https://github.com/cfregly/claude-agent-harness-opt/blob/main/docs/gstack-skill-routing-audit.md)

## Result

Current frontier stress receipt: 496 current available-frontier cells, 484 passed, 8 failed, 4 errors on OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools`. Treat this as hill-descending coverage for the next tuning pass.

Confirmed improvement. This clears the adversarially-confirmed to add value bar.

The tuned gstack skill descriptions improved the 720-cell live matrix from 0.975 to 0.992, with
the remaining packet evidence preserved for reruns and upstream review.

## Reproduce

[REPRODUCTION.md](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/pr_packets/gstack_skill_routing_2026-06-25/REPRODUCTION.md)
contains the exact command and pinned matrix surface.
