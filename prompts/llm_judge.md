# LLM Judge Prompt

```text
You are grading an agent output against a rubric.

<rubric>
[Clear pass and fail criteria]
</rubric>

<agent_output>
[Agent answer or transcript summary]
</agent_output>

Return JSON with keys passed, score, and rationale. Do not include extra text.
```
