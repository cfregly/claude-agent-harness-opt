# Autoresearch Hill Climbing

The useful idea from the autoresearch pattern is not the training domain. It is the loop:

1. Pick one editable surface.
2. Run a fixed-budget experiment.
3. Measure one clear score.
4. Keep the candidate only if it beats the baseline.
5. Log every attempt so the next run does not repeat blind guesses.

In this repo, the editable surface is the agent harness:

- tool names and descriptions
- argument and output schemas
- provider native tool wrappers
- prompt JSON wrappers
- `CLAUDE.md` style rules
- skill instructions
- Agent SDK loop controls
- IDE-agent trace adapters

The experiment is a model matrix plus trace review. The score is not a vibe check. It is tool choice,
argument quality, reasoning-note quality, tool-output use, final grounding, runtime, token use,
tool-call count, and tool-error rate.

## Why It Matters

The hard problem is not only whether one model can call one tool. The hard problem is whether a
model, provider API, harness, tool catalog, project instruction file, and skill all cooperate under
real tasks. A tool description that works in one native tool interface may fail in a JSON wrapper.
A `CLAUDE.md` rule that helps one model generation can hurt another. A trace adapter can hide the
exact argument mistake that caused the failure.

The matrix turns that into a measurable surface. The hill-climb loop turns repeated failures into
candidates. Held-out confirmation keeps the candidate from overfitting the exact failed case.

## How The Loop Works

Run the baseline on target cases:

```bash
python -m claude_agent_harness_opt grind-harness evals/model_matrix/coding_tool_selection.json \
  --env-file .env \
  --live \
  --require-live \
  --providers anthropic,openai,gemini \
  --harnesses native_tools,prompt_json \
  --instruction-variants boundary_rules \
  --cases "investigate trace review flow,map model matrix implementation" \
  --heldout-cases "find python files,read known file" \
  --min-improvement 0.05 \
  --max-live-calls 80 \
  --concurrency 8 \
  --markdown
```

The command:

- runs the baseline target cells
- generates a candidate from observed failures
- reruns the target cells
- runs held-out confirmation when a candidate beats the baseline
- promotes only when the live improvement clears the threshold and held-out cells do not regress
- emits an experiment log with each keep or reject decision

Dry runs still help with scope and cost planning, but they do not satisfy the value bar.

## Narrative

The repo is an agent harness optimization lab. It tests the full stack that determines whether an
agent uses tools well:

- model
- provider API
- harness
- tool catalog
- project rules
- skills
- trace capture
- evals

That is the differentiator. Most prompt kits stop at good wording. This repo treats wording as one
candidate in an experiment loop. The promotion rule is always adversarially-confirmed to add value.

## When It Adds Value

Use this loop when:

- tool-choice failures repeat
- a new model generation changes behavior
- a provider native tool API behaves differently from a prompt wrapper
- an Agent SDK or IDE harness hides useful trace data
- a skill or project instruction file changes tool selection
- a tool catalog grows and similar tools blur together

Do not use it when the eval surface is weak. The loop needs realistic cases, verifiable outcomes,
visible reasoning summaries or decision notes, captured tool outputs, and held-out checks. Without
those, hill climbing just optimizes noise.

## Failure Modes

The main risks are:

- overfitting to target cases
- rewarding a cheap proxy that no longer tracks real user value
- missing hidden harness transformations
- comparing models with unequal thinking or output budgets
- treating hidden chain-of-thought as available when only visible summaries can be audited
- spending live API budget on cases that deterministic checks could have rejected first

The controls are the same ones used across the repo: small realistic evals, held-out cases, fixed
call budgets, trace contracts, Claude judge review, and manual inspection of real transcripts.
