# gstack Skill Routing Anthropic Frontier Live Result - 2026-07-01

Passed: no
Live: yes

This retained receipt uses the newly provided Anthropic key against the accessible `claude-opus-4-8` profile.

> [!NOTE]
> The new key passed a smoke test. Later cells in this batch hit Anthropic credit exhaustion, so credit-exhausted rows are retained as provider-state evidence rather than hidden or deleted.

## Matrix Summary

- total: 248
- passed_cases: 0
- failed_cases: 0
- errors: 248
- skipped: 0
- score: 0.0

## Profiles

- `anthropic-opus-high`: `claude-opus-4-8`

## Status By Profile

| Profile | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| `anthropic-opus-high` | 0 | 0 | 248 | 0 |

## Remaining Failure Clusters

- 8x `browser-compat-alias`: status `error`, chose `error: credit balance is too low`
- 8x `browser-headless`: status `error`, chose `error: credit balance is too low`
- 8x `qa-fix`: status `error`, chose `error: credit balance is too low`
- 8x `qa-report-only`: status `error`, chose `error: credit balance is too low`
- 8x `implemented-design-polish`: status `error`, chose `error: credit balance is too low`
- 8x `design-plan-review`: status `error`, chose `error: credit balance is too low`
- 8x `design-system`: status `error`, chose `error: credit balance is too low`
- 8x `design-variants`: status `error`, chose `error: credit balance is too low`
- 8x `product-brainstorm`: status `error`, chose `error: credit balance is too low`
- 8x `spec-plus-browser-validation`: status `error`, chose `error: credit balance is too low`

## Machine-readable Receipt

[JSON receipt](https://github.com/cfregly/claude-agent-harness-opt/blob/main/evals/results/gstack_skill_matrix_frontier_anthropic_attempt_2026-07-01.json)
