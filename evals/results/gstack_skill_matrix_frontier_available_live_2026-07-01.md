# gstack Skill Routing Frontier Matrix Live Result - 2026-07-01

Passed: no
Live: yes

This retained frontier receipt runs the current available frontier profiles in this workspace: OpenAI `gpt-5.5` and Gemini `gemini-3.1-pro-preview-customtools`.

> [!NOTE]
> Anthropic frontier is not included in the completed available-frontier sweep because the present Anthropic key returns a low-credit API error for `claude-opus-4-8`, and `/home/cfregly/dev/anthropic` is not present in this session.

## Matrix Summary

- total: 496
- passed_cases: 484
- failed_cases: 8
- errors: 4
- skipped: 0
- score: 0.976

## Profiles

- `anthropic-fable-frontier`: `claude-fable-5`
- `anthropic-opus-high`: `claude-opus-4-8`
- `openai-gpt55-frontier`: `gpt-5.5`
- `gemini-31-pro-customtools-frontier`: `gemini-3.1-pro-preview-customtools`

## Status By Profile

| Profile | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| `gemini-31-pro-customtools-frontier` | 241 | 3 | 4 | 0 |
| `openai-gpt55-frontier` | 243 | 5 | 0 | 0 |

## Remaining Failure Clusters

- 6x `browser-compat-alias`: status `failed`, chose `gstack_gstack`
- 4x `no-tool-general-answer`: status `error`, chose `error: HTTP 400: {`
- 1x `browser-headless`: status `failed`, chose `gstack_gstack`
- 1x `browser-compat-alias`: status `failed`, chose `gstack_browse`

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/gstack_skill_matrix_frontier_available_live_2026-07-01.json)
