# gstack Skill Routing Audit

Checked on 2026-06-25.

## Target

This audit treats the generated `gstack` Codex-compatible skills as a skills-as-tools catalog.

| Field | Value |
|---|---|
| Package | `gstack` |
| Version | `0.13.3.0` |
| Commit | `cd66fc2f890982351e3178925be563681d0ab2c5` |
| Evaluated surface | `.agents/skills/*/SKILL.md` generated skill files |
| Surface hash | `68d60eeefdde254818b03ee310bf1c4c9aaf0efee8d6db35141fe9cb7da8ae12` |
| Target surface dirty | `false` |
| Worktree dirty | `true`, from unrelated local files outside the evaluated generated skill surface |

## Commands

```bash
python scripts/build_gstack_skill_target.py \
  --gstack-root /Users/admin/dev/gstack \
  --out-dir evals/targets/gstack

python -m claude_agent_harness_opt optimize-tools \
  evals/targets/gstack/gstack_agent_audit_bundle.json --markdown

python -m claude_agent_harness_opt audit-agent \
  evals/targets/gstack/gstack_agent_audit_bundle.json --markdown

python -m claude_agent_harness_opt model-matrix \
  evals/targets/gstack/gstack_skill_selection_matrix.json \
  --env-file .env --live --require-live --concurrency 8 \
  --out /tmp/gstack-skill-matrix-live-full.json

python -m claude_agent_harness_opt model-matrix \
  evals/targets/gstack/gstack_skill_selection_matrix.json \
  --env-file .env --live --require-live --providers gemini --concurrency 6 \
  --out /tmp/gstack-skill-matrix-live-gemini-rerun.json

python -m claude_agent_harness_opt model-matrix \
  evals/targets/gstack/gstack_skill_selection_matrix.json \
  --env-file .env --live --require-live \
  --providers anthropic-fable-frontier,anthropic-opus-high,openai-gpt55-frontier,openai-gpt54-high,gemini-31-pro-customtools-frontier,gemini-25-pro-high \
  --concurrency 8 \
  --out /tmp/gstack-skill-matrix-live-frontier-high.json
```

Gemini was rerun after increasing its matrix `max_tokens` to `4096`. The first full run showed
Gemini truncating prompt-JSON responses because internal thinking consumed the default output budget.
The frontier and high command is the recommended next run before making claims about current
top-tier models.

High-profile smoke run:

```bash
python -m claude_agent_harness_opt model-matrix \
  evals/targets/gstack/gstack_skill_selection_matrix.json \
  --env-file .env --live --require-live \
  --providers anthropic-opus-high,openai-gpt54-high,gemini-25-pro-high \
  --harnesses prompt_json \
  --variants gstack_boundary_tuned_skill_descriptions \
  --instruction-variants boundary_routing_rules \
  --cases browser-headless,careful-mode \
  --concurrency 3 \
  --out evals/results/gstack_high_profile_smoke_2026-06-25.json
```

The first high-profile smoke exposed a real harness compatibility issue: Claude Opus rejected the
default `temperature` parameter. The harness now omits temperature unless a profile explicitly sets
it.

Native high-profile smoke run:

```bash
python -m claude_agent_harness_opt model-matrix \
  evals/targets/gstack/gstack_skill_selection_matrix.json \
  --env-file .env --live --require-live \
  --providers anthropic-opus-high,openai-gpt54-high,gemini-25-pro-high \
  --harnesses native_tools \
  --variants gstack_boundary_tuned_skill_descriptions \
  --instruction-variants boundary_routing_rules \
  --cases browser-headless \
  --concurrency 3 \
  --out evals/results/gstack_high_profile_native_smoke_2026-06-25.json
```

## Results

This live result is a historical three-profile sweep. It covered one Anthropic profile, one OpenAI
profile, and one Gemini profile. It should not be presented as a complete frontier-model sweep.
The current generated matrix now includes separate frontier, high, and balanced profiles so a new
run can test stronger models explicitly.

Deterministic checks:

| Check | Result |
|---|---|
| `optimize-tools` | pass, score `1.000` |
| `audit-agent` | pass, score `1.000` |
| Surface snapshot | pass, hash `ec3752895c47b5f0...` |

Live matrix:

| Metric | Value |
|---|---:|
| Total live cells | 720 |
| Passed | 708 |
| Failed | 12 |
| Errors | 0 |
| Score | 0.983 |

High-profile smoke matrix:

| Metric | Value |
|---|---:|
| Total live cells | 6 |
| Passed | 6 |
| Failed | 0 |
| Errors | 0 |
| Score | 1.000 |

Native high-profile smoke matrix:

| Metric | Value |
|---|---:|
| Total live cells | 3 |
| Passed | 3 |
| Failed | 0 |
| Errors | 0 |
| Score | 1.000 |

Variant comparison from the generated PR packet:

| Variant | Score |
|---|---:|
| `gstack_stock_skill_descriptions` | 0.97525 |
| `gstack_boundary_tuned_skill_descriptions` | 0.99175 |
| Delta | +0.01650 |
| Promote threshold | 0.01000 |
| Promotion | yes |

## Signals

What we learned:

- The generated gstack skill catalog is mostly well routed across the tested harnesses.
- Boundary tuning still adds measurable value on the pinned surface.
- The useful failures are adjacent-skill confusion, not broad quality failure.
- The next stronger claim requires rerunning the expanded frontier and high-profile matrix.

Browser alias boundary:

- Failing case: `browser-headless`
- Expected: `gstack_browse`
- Observed wrong choice: `gstack_gstack`
- Affected cells: OpenAI native stock, OpenAI prompt-JSON stock and tuned, Gemini stock native and prompt-JSON.
- Interpretation: the broad generated `gstack` browser alias competes with the narrower `gstack-browse` skill. Boundary-tuned descriptions fix Anthropic and Gemini, but OpenAI prompt-JSON still chooses the alias.

Suggested upstream change:

- Do not expose the broad `gstack` alias as a normal selectable workflow skill when `gstack-browse` is also present, or mark it as a compatibility alias only.
- Add an explicit line to the alias description: "Do not select this for browser testing. Select `/browse` instead."

Safety-mode boundary:

- Failing cases: `careful-mode`, `freeze-edits`
- Expected: `gstack_careful` for destructive-command warnings, `gstack_freeze` for edit-scope locking.
- Observed wrong choice: `gstack_guard`.
- Interpretation: `/guard` is attractive because it includes both safety behaviors. The skill descriptions should say `/guard` is only for requests that explicitly ask for both destructive-command warnings and directory-scoped edit locking.

Suggested upstream change:

- Add examples to `/careful`, `/freeze`, and `/guard`.
- `/careful`: "Be careful while touching prod" means warnings only.
- `/freeze`: "Only edit this directory" means edit lock only.
- `/guard`: "Warn before destructive commands and lock edits to this directory" means both.

Gemini harness budget:

- First full run: Gemini prompt-JSON returned truncated JSON and empty native outputs in many cells.
- Probe result: `finishReason=MAX_TOKENS`, with most budget consumed by internal thinking.
- Fix: set Gemini matrix `max_tokens` to `4096`.
- Rerun result: 237/240 Gemini cells passed, 0 errors.

## Artifacts

- Matrix: `evals/targets/gstack/gstack_skill_selection_matrix.json`
- Bundle: `evals/targets/gstack/gstack_agent_audit_bundle.json`
- Combined live result: `evals/results/gstack_skill_matrix_live_2026-06-25.json`
- Gemini rerun result: `evals/results/gstack_skill_matrix_live_gemini_rerun_2026-06-25.json`
- Surface snapshot: `evals/results/gstack_surface_snapshot_2026-06-25.json`
- Upstream PR packet: `evals/pr_packets/gstack_skill_routing_2026-06-25/`
- High-profile smoke result: `evals/results/gstack_high_profile_smoke_2026-06-25.json`
- Native high-profile smoke result: `evals/results/gstack_high_profile_native_smoke_2026-06-25.json`
