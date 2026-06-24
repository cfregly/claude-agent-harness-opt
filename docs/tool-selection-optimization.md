# Tool Selection Optimization

Tool descriptions are part of the agent runtime. If two tools sound similar, the agent has to guess.
The optimizer turns that guesswork into a testable loop.

## Inputs

`optimize-tools` reads an agent audit bundle with:

- `tools`: names, purposes, use rules, avoid rules, input schemas, and quality checks.
- `tool_selection_cases`: small calibration tasks with expected and forbidden tools.
- `traces`: representative runs with ordered reasoning, tool calls, tool results, and final answers.
- `value_bar`: baseline, candidate, metric, threshold, and adversarial review.

## What It Checks

The deterministic optimizer checks:

- distinct tool names and descriptions
- `input_schema` or equivalent parameter shape for every tool
- result `quality_checks` for every tool
- calibration cases for each confusing tool boundary
- expected and forbidden tools in each case
- trace tool calls against the declared catalog
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
   - add result quality checks
   - add one calibration case for a confusing boundary
   - add a regression trace when the failure came from a real run
4. Re-run deterministic checks.
5. Re-run `--claude-judge`.
6. Keep the change only if it clears the adversarially-confirmed to add value bar.

## Commands

```bash
python -m claude_agent_prompting optimize-tools evals/examples/agent_audit_bundle.json --markdown
python -m claude_agent_prompting optimize-tools evals/examples/agent_audit_bundle.json --claude-judge
python -m claude_agent_prompting audit-agent evals/examples/agent_audit_bundle.json --claude-judge --markdown
```

`audit-agent --claude-judge` includes the tool-selection optimizer, so a real audit cannot pass on
trace shape alone.
