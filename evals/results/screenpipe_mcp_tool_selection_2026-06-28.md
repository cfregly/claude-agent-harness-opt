# screenpipe mcp tool-selection matrix

## Optimization Gate

Passed: yes
Optimized variants: `source_tuned_screenpipe_mcp`
Baseline variant: `readme_screenpipe_mcp`
Baseline score: 0.857
Optimized score: 1.000
Baseline failures: 1
Optimized failures: 0

optimized variants passed every selected cell

## Raw Matrix

Live: yes
Passed: no
Planned: 14
Passed cases: 13
Failed cases: 1
Errors: 0
Skipped: 0
Score: 0.929

## Results

| Provider | Model | Harness | Tool Variant | Instruction Variant | Case | Status | Chosen |
|---|---|---|---|---|---|---|---|
| anthropic | claude-sonnet-4-5 | prompt_json | readme_screenpipe_mcp | screenpipe_host_rules | broad morning recap starts summary | passed | activity-summary |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_screenpipe_mcp | screenpipe_host_rules | exact keyword uses keyword search | failed | search-content |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_screenpipe_mcp | screenpipe_host_rules | speaker transcript uses content search | passed | search-content |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_screenpipe_mcp | screenpipe_host_rules | ui button lookup uses elements | passed | search-elements |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_screenpipe_mcp | screenpipe_host_rules | known frame detail uses frame context | passed | frame-context |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_screenpipe_mcp | screenpipe_host_rules | create recurring automation uses pipe | passed | create-pipe |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_screenpipe_mcp | screenpipe_host_rules | verify pipe output uses logs | passed | pipe-logs |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_screenpipe_mcp | screenpipe_host_rules | broad morning recap starts summary | passed | activity-summary |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_screenpipe_mcp | screenpipe_host_rules | exact keyword uses keyword search | passed | keyword-search |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_screenpipe_mcp | screenpipe_host_rules | speaker transcript uses content search | passed | search-content |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_screenpipe_mcp | screenpipe_host_rules | ui button lookup uses elements | passed | search-elements |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_screenpipe_mcp | screenpipe_host_rules | known frame detail uses frame context | passed | frame-context |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_screenpipe_mcp | screenpipe_host_rules | create recurring automation uses pipe | passed | create-pipe |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_screenpipe_mcp | screenpipe_host_rules | verify pipe output uses logs | passed | pipe-logs |

## Cell Summary

| Provider | Harness | Tool Variant | Instruction Variant | Passed | Failed | Errors | Score |
|---|---|---|---|---:|---:|---:|---:|
| anthropic | prompt_json | readme_screenpipe_mcp | screenpipe_host_rules | 6 | 1 | 0 | 0.857 |
| anthropic | prompt_json | source_tuned_screenpipe_mcp | screenpipe_host_rules | 7 | 0 | 0 | 1.000 |
