# Tool Selection Optimization

Tool descriptions are part of the agent runtime. If two tools sound similar, the agent has to guess.
The optimizer turns that guesswork into a testable loop.

Tune one tool means choose one callable and make the contract testable: name, `use_when`,
`avoid_when`, `input_schema`, output contract, context controls, error guidance, examples, negative
guidance, calibration cases, and held-out cases.

## Inputs

`optimize-tools` reads an agent audit bundle with:

- `tools`: names, purposes, use rules, avoid rules, input schemas, and quality checks.
- `tool_selection_cases`: calibration tasks with verifiable outcomes and optional expected tools.
- `heldout_tool_selection_cases`: cases used to check that a candidate generalizes.
- `traces`: representative runs with ordered reasoning, tool calls, tool results, and final answers.
- `tool_metrics`: runtime, tool-call count, token count, and tool error summaries.
- `value_bar`: baseline, candidate, metric, threshold, and adversarial review.

## What It Checks

The deterministic optimizer checks:

- distinct tool names and descriptions
- `input_schema` or equivalent parameter shape for every tool
- result `quality_checks` for every tool
- output contracts and helpful error guidance
- context controls for large-output tools
- namespacing for large tool catalogs
- calibration cases for each confusing tool boundary
- expected and forbidden tools in each case
- verifiable outcomes for every case
- held-out cases for promotion checks
- exact strategy overfitting through required tool order
- trace tool calls against the declared catalog
- transcript metrics for runtime, call count, token use, and tool errors
- trace failures that point back to descriptions, schemas, examples, or budgets

The Claude judge then reviews whether the descriptions and cases are semantically strong enough for
an agent to choose the right tool, use valid arguments, inspect outputs, and add value over the
baseline.

## Improve Loop

1. Run a real trace through `review-trace` or `audit-agent`.
2. Run `optimize-tools` on the same bundle.
3. Change the smallest thing that explains the failure:
   - rename or merge confusing tools
   - sharpen `use_when`
   - sharpen `avoid_when`
   - add input schema details
   - add output contracts or response formats
   - add pagination, filtering, range, truncation, or response format controls
   - add actionable error guidance
   - add result quality checks
   - add one calibration case and one held-out case for a confusing boundary
   - add a regression trace when the failure came from a real run
4. Re-run deterministic checks.
5. Re-run `--claude-judge`.
6. Keep the change only if it clears the adversarially-confirmed to add value bar.

## Commands

```bash
python -m claude_agent_harness_optimization optimize-tools evals/examples/tool_tuning_before_bundle.json --markdown || true
python -m claude_agent_harness_optimization optimize-tools evals/examples/agent_audit_bundle.json --markdown
python -m claude_agent_harness_optimization optimize-tools evals/examples/agent_audit_bundle.json --claude-judge
python -m claude_agent_harness_optimization audit-agent evals/examples/agent_audit_bundle.json --claude-judge --markdown
```

The before bundle is a deliberate negative control. It proves the gate catches a vague search tool
with no schema, no calibration cases, no held-out cases, no result checks, no runtime metrics, and no
value-bar receipt. The after bundle proves the same harness can pass a sharper tool catalog with
separate discovery, fetch, and calculation contracts.

`audit-agent --claude-judge` includes the tool-selection optimizer, so a real audit cannot pass on
trace shape alone.
