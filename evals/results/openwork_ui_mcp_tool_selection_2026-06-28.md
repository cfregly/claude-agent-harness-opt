# openwork ui mcp tool-selection matrix


## Optimization Gate

Passed: yes
Optimized variants: `source_tuned_openwork_ui_mcp`
Baseline variant: `docs_openwork_ui_mcp`
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
| anthropic | claude-sonnet-4-5 | prompt_json | docs_openwork_ui_mcp | openwork_ui_host_rules | bridge check uses status | passed | ui_status |
| anthropic | claude-sonnet-4-5 | prompt_json | docs_openwork_ui_mcp | openwork_ui_host_rules | unknown current screen uses snapshot | passed | ui_snapshot |
| anthropic | claude-sonnet-4-5 | prompt_json | docs_openwork_ui_mcp | openwork_ui_host_rules | action discovery uses list actions | passed | ui_list_actions |
| anthropic | claude-sonnet-4-5 | prompt_json | docs_openwork_ui_mcp | openwork_ui_host_rules | known action id executes action | passed | ui_execute_action |
| anthropic | claude-sonnet-4-5 | prompt_json | docs_openwork_ui_mcp | openwork_ui_host_rules | unknown action id lists actions first | passed | ui_list_actions |
| anthropic | claude-sonnet-4-5 | prompt_json | docs_openwork_ui_mcp | openwork_ui_host_rules | coordinate click avoids semantic bridge | passed | NO_TOOL |
| anthropic | claude-sonnet-4-5 | prompt_json | docs_openwork_ui_mcp | openwork_ui_host_rules | app maybe closed checks status before action | passed | ui_status |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_openwork_ui_mcp | openwork_ui_host_rules | bridge check uses status | passed | ui_status |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_openwork_ui_mcp | openwork_ui_host_rules | unknown current screen uses snapshot | passed | ui_snapshot |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_openwork_ui_mcp | openwork_ui_host_rules | action discovery uses list actions | passed | ui_list_actions |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_openwork_ui_mcp | openwork_ui_host_rules | known action id executes action | passed | ui_execute_action |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_openwork_ui_mcp | openwork_ui_host_rules | unknown action id lists actions first | passed | ui_list_actions |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_openwork_ui_mcp | openwork_ui_host_rules | coordinate click avoids semantic bridge | passed | NO_TOOL |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_openwork_ui_mcp | openwork_ui_host_rules | app maybe closed checks status before action | passed | ui_status |

## Cell Summary

| Provider | Harness | Tool Variant | Instruction Variant | Passed | Failed | Errors | Score |
|---|---|---|---|---:|---:|---:|---:|
| anthropic | prompt_json | docs_openwork_ui_mcp | openwork_ui_host_rules | 7 | 0 | 0 | 1.000 |
| anthropic | prompt_json | source_tuned_openwork_ui_mcp | openwork_ui_host_rules | 7 | 0 | 0 | 1.000 |
