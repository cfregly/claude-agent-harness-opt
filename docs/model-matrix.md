# Model Matrix

The model matrix is the tuning layer for new model generations. It runs the same tool-selection
cases across provider profiles, harnesses, tool-description variants, and instruction variants.

Use it when changing:

- model id
- reasoning effort or thinking budget
- provider harness
- tool names
- tool descriptions
- argument schemas
- `CLAUDE.md`
- skills
- system prompts

## Why It Exists

Models do not read tool descriptions the same way. A description that works for one model can fail
on another model, or fail when moved from prompt JSON to native tool calling. The matrix makes that
visible before a prompt or tool change is promoted.

The pass bar is still adversarially-confirmed to add value. A tuned description should beat the
baseline on realistic cases, survive heldout cases, and avoid regressions on direct easy cases.

## Included Matrix

`evals/model_matrix/coding_tool_selection.json` tests Claude Code style tools:

- `Task`: broad delegated investigation
- `Glob`: file path discovery
- `Grep`: content search
- `Read`: exact file read

The hard cases distinguish `Task` from `Grep`. Short descriptions often make models pick `Grep` for
broad investigation. Tuned descriptions state when to delegate to `Task` and when to stay with direct
file tools.

## Commands

Dry run:

```bash
python -m claude_agent_prompting model-matrix evals/model_matrix/coding_tool_selection.json --markdown
```

Smoke test one provider and a few cases:

```bash
python -m claude_agent_prompting model-matrix evals/model_matrix/coding_tool_selection.json \
  --env-file .env \
  --live \
  --require-live \
  --providers anthropic \
  --harnesses native_tools \
  --variants tuned_boundaries \
  --instruction-variants boundary_rules \
  --max-cases 2 \
  --markdown
```

Full local sweep:

```bash
python -m claude_agent_prompting model-matrix evals/model_matrix/coding_tool_selection.json \
  --env-file .env \
  --live \
  --require-live \
  --concurrency 8 \
  --markdown
```

## Reading Results

The report has one row per case and a cell summary grouped by:

- provider
- harness
- tool-description variant
- instruction variant

Use the cell summary to isolate the cause:

- If only one provider fails, tune the provider profile or model-specific instructions.
- If native tools fail but prompt JSON passes, tune provider tool schemas.
- If baseline fails and tuned passes, promote the tuned tool descriptions after heldout checks.
- If both variants fail, add harder schema guidance or split the tool.
- If instruction variants change the score, tune `CLAUDE.md`, skill instructions, or system prompt text.

## Live Result From June 24, 2026

Using local Anthropic, OpenAI, and Gemini keys, the matrix was run against:

- Anthropic `claude-sonnet-4-5`
- OpenAI `gpt-4.1`
- Gemini `gemini-2.5-pro`

Native tool harness:

- `baseline_short`: 72 of 84 passed
- `tuned_boundaries`: every provider and instruction variant scored 7 of 7

Prompt JSON harness:

- `baseline_short`: 73 of 84 passed
- `tuned_boundaries`: every provider and instruction variant scored 7 of 7

The repeated failure was the same useful one: short descriptions made models choose `Grep` for broad
repository investigation tasks that should use `Task`. Tuned boundary descriptions fixed that across
all three providers and both harnesses.

Gemini `prompt_json` initially failed because `maxOutputTokens` was too small for `gemini-2.5-pro`.
Increasing the profile output budget to 4096 removed those harness errors.
