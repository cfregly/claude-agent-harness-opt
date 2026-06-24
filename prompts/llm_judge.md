# LLM Judge Prompt

```text
You are grading an agent output against a rubric.

<rubric>
[Clear pass and fail criteria]
[Value claim, baseline, minimum improvement, and adversarial challenge]
</rubric>

<agent_output>
[Agent answer or transcript summary]
</agent_output>

Return JSON with keys passed, score, value_bar_passed, and rationale. Do not include extra text.
```
