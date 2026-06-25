# Skills Versus Tools

This repo can evaluate both tools and skills, but they enter the harness at different layers.

## Difference

A tool is a callable interface. It has a name, description, input schema, arguments, tool output,
and usually error behavior. The model either chooses it correctly or it does not. Use
`optimize-tools`, `model-matrix`, and trace review to tune tool names, descriptions, schemas, and
result handling.

A skill is an instruction policy. It changes how the agent plans, routes work, uses tools, and
reports results. It is not called with arguments unless the runtime implements it that way. In this
repo, evaluate a skill as an `instruction_variant`, then compare it against a no-skill baseline on
the same cases and tool catalog.

## What We Tested

The project-local `.claude/skills/agent-audit/SKILL.md` skill was tested as the skill-under-test.
The workflow tools were synthetic command choices that mirror the repo's audit commands:

- `normalize_runtime`
- `review_trace`
- `trace_suite`
- `audit_agent`
- `optimize_tools`
- `model_matrix`
- `grind_harness`

The eval lives at:

```text
evals/model_matrix/agent_audit_skill_selection.json
```

It includes two relevant axes:

- `instruction_variants`: `no_skill` versus `agent_audit_skill`
- `tool_variants`: `workflow_tools` with clear descriptions versus `thin_workflow_tools` with vague descriptions

## Live Result

Command:

```bash
python -m claude_agent_harness_optimization model-matrix \
  evals/model_matrix/agent_audit_skill_selection.json \
  --env-file .env \
  --live \
  --require-live \
  --providers anthropic \
  --harnesses prompt_json \
  --variants thin_workflow_tools \
  --instruction-variants no_skill,agent_audit_skill \
  --markdown
```

Result:

- `no_skill` with thin tool descriptions: 6/7, score 0.857
- `agent_audit_skill` with thin tool descriptions: 7/7, score 1.000

The baseline missed the tool-description failure case and chose `audit_agent`. The skill routed the
same request to `optimize_tools`.

That is a real value signal because the skill improved the no-skill baseline on a live model run.
It is not enough to claim that the skill is globally good. The next bar is held-out cases and
provider or harness diversity.

## Interpretation

Skills are most valuable when they encode policy the tool descriptions do not fully carry:

- when to normalize raw events before review
- when a single trace review is enough
- when a full agent audit bundle is needed
- when a tool-selection problem should use `optimize-tools`
- when a new model, provider, skill, or `CLAUDE.md` change needs `model-matrix`
- when repeated failures justify `grind-harness`

Clear tool descriptions still matter. In an easier live run with concrete artifact paths and clear
workflow descriptions, both the no-skill and skill variants passed 7/7. That means the skill added
no measurable value under the easy condition. The useful conclusion is not "always add a skill."
The useful conclusion is "measure whether the skill adds value beyond clear tool descriptions."

## How To Improve A Skill

Use the same value-bar loop as tool tuning:

1. Write realistic routing cases with verifiable expected behavior.
2. Run a no-skill baseline.
3. Run the skill as an `instruction_variant`.
4. Run at least one weak or ambiguous tool-catalog stress case.
5. Add held-out cases for any boundary the skill improves.
6. Promote a skill change only when it is adversarially-confirmed to add value.

For this skill, the next improvement target is held-out routing coverage around similar audit
requests:

- full agent audit bundle versus tool-description-only audit
- model matrix versus harness grind
- raw runtime events versus normalized trace JSON
- trace suite versus one trace
- missing value-bar proof versus passing value-bar proof

## CI Scope

CI should dry-run the matrix so schema drift is caught without spending provider calls. Live runs
should stay explicit because they spend money and can vary by model version. Repository CI already
has separate live Claude gates for semantic judge and matrix behavior.
