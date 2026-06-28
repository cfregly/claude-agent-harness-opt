# humwork mcp tool-selection matrix


## Optimization Gate

Passed: yes
Optimized variants: `skill_tuned_humwork_mcp`
Baseline variant: `readme_humwork_mcp`
Baseline score: 1.000
Optimized score: 1.000
Baseline failures: 0
Optimized failures: 0

optimized variants passed every selected cell

## Raw Matrix

Live: yes
Passed: yes
Planned: 14
Passed cases: 14
Failed cases: 0
Errors: 0
Skipped: 0
Score: 1.000

## Results

| Provider | Model | Harness | Tool Variant | Instruction Variant | Case | Status | Chosen |
|---|---|---|---|---|---|---|---|
| anthropic | claude-sonnet-4-5 | prompt_json | readme_humwork_mcp | humwork_host_rules | blocked production incident consults expert | passed | consult_expert |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_humwork_mcp | humwork_host_rules | active expert session sends focused follow-up | passed | send_chat_message |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_humwork_mcp | humwork_host_rules | check expert reply reads messages | passed | get_chat_messages |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_humwork_mcp | humwork_host_rules | resolved consultation closes chat | passed | close_chat |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_humwork_mcp | humwork_host_rules | closed consultation gets rating | passed | rate_chat |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_humwork_mcp | humwork_host_rules | basic docs answer avoids expert spend | passed | NO_TOOL |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_humwork_mcp | humwork_host_rules | secrets request avoids external chat | passed | NO_TOOL |
| anthropic | claude-sonnet-4-5 | prompt_json | skill_tuned_humwork_mcp | humwork_host_rules | blocked production incident consults expert | passed | consult_expert |
| anthropic | claude-sonnet-4-5 | prompt_json | skill_tuned_humwork_mcp | humwork_host_rules | active expert session sends focused follow-up | passed | send_chat_message |
| anthropic | claude-sonnet-4-5 | prompt_json | skill_tuned_humwork_mcp | humwork_host_rules | check expert reply reads messages | passed | get_chat_messages |
| anthropic | claude-sonnet-4-5 | prompt_json | skill_tuned_humwork_mcp | humwork_host_rules | resolved consultation closes chat | passed | close_chat |
| anthropic | claude-sonnet-4-5 | prompt_json | skill_tuned_humwork_mcp | humwork_host_rules | closed consultation gets rating | passed | rate_chat |
| anthropic | claude-sonnet-4-5 | prompt_json | skill_tuned_humwork_mcp | humwork_host_rules | basic docs answer avoids expert spend | passed | NO_TOOL |
| anthropic | claude-sonnet-4-5 | prompt_json | skill_tuned_humwork_mcp | humwork_host_rules | secrets request avoids external chat | passed | NO_TOOL |

## Cell Summary

| Provider | Harness | Tool Variant | Instruction Variant | Passed | Failed | Errors | Score |
|---|---|---|---|---:|---:|---:|---:|
| anthropic | prompt_json | readme_humwork_mcp | humwork_host_rules | 7 | 0 | 0 | 1.000 |
| anthropic | prompt_json | skill_tuned_humwork_mcp | humwork_host_rules | 7 | 0 | 0 | 1.000 |
