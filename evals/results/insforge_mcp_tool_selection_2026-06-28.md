# insforge mcp tool-selection matrix


## Optimization Gate

Passed: yes
Optimized variants: `source_tuned_insforge_mcp`
Baseline variant: `readme_insforge_mcp`
Baseline score: 0.938
Optimized score: 1.000
Baseline failures: 1
Optimized failures: 0

optimized variants passed every selected cell

## Raw Matrix

Live: yes
Passed: no
Planned: 32
Passed cases: 31
Failed cases: 1
Errors: 0
Skipped: 0
Score: 0.969

## Results

| Provider | Model | Harness | Tool Variant | Instruction Variant | Case | Status | Chosen |
|---|---|---|---|---|---|---|---|
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | new project setup reads instructions | passed | fetch-docs |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | new app bootstrap uses template | passed | download-template |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | backend inventory uses metadata | passed | get-backend-metadata |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | known table details use schema | passed | get-table-schema |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | explicit sql uses raw sql | passed | run-raw-sql |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | csv import uses bulk upsert | passed | bulk-upsert |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | storage inventory lists buckets | passed | list-buckets |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | create storage bucket uses create bucket | passed | create-bucket |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | read function uses get function | passed | get-function |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | update function uses update function | passed | update-function |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | function logs use container logs | passed | get-container-logs |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | sdk docs use sdk docs | passed | fetch-sdk-docs |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | client token uses anon key | passed | get-anon-key |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | absolute source deploy uses create deployment | passed | create-deployment |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | prepared remote upload starts deployment | passed | start-deployment |
| anthropic | claude-sonnet-4-5 | prompt_json | readme_insforge_mcp | insforge_host_rules | relative deploy path avoids tool | failed | create-deployment |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | new project setup reads instructions | passed | fetch-docs |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | new app bootstrap uses template | passed | download-template |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | backend inventory uses metadata | passed | get-backend-metadata |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | known table details use schema | passed | get-table-schema |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | explicit sql uses raw sql | passed | run-raw-sql |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | csv import uses bulk upsert | passed | bulk-upsert |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | storage inventory lists buckets | passed | list-buckets |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | create storage bucket uses create bucket | passed | create-bucket |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | read function uses get function | passed | get-function |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | update function uses update function | passed | update-function |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | function logs use container logs | passed | get-container-logs |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | sdk docs use sdk docs | passed | fetch-sdk-docs |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | client token uses anon key | passed | get-anon-key |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | absolute source deploy uses create deployment | passed | create-deployment |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | prepared remote upload starts deployment | passed | start-deployment |
| anthropic | claude-sonnet-4-5 | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | relative deploy path avoids tool | passed | NO_TOOL |

## Cell Summary

| Provider | Harness | Tool Variant | Instruction Variant | Passed | Failed | Errors | Score |
|---|---|---|---|---:|---:|---:|---:|
| anthropic | prompt_json | readme_insforge_mcp | insforge_host_rules | 15 | 1 | 0 | 0.938 |
| anthropic | prompt_json | source_tuned_insforge_mcp | insforge_host_rules | 16 | 0 | 0 | 1.000 |
