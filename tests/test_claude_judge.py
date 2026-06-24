import json
from pathlib import Path
import unittest

from claude_agent_prompting.claude_judge import (
    build_claude_trace_judge_prompt,
    call_claude_messages,
    judge_trace_with_claude,
    parse_judge_json,
)
from claude_agent_prompting.trace_review import load_trace, review_trace


ROOT = Path(__file__).resolve().parents[1]


def fake_request(
    payload: dict,
    headers: dict[str, str],
    url: str,
    timeout: int,
) -> dict:
    assert payload["model"] == "claude-test"
    assert headers["x-api-key"] == "test-key"
    assert url == "https://api.anthropic.com/v1/messages"
    assert timeout == 60
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(
                    {
                        "findings": ["trace uses fetched evidence before calculating"],
                        "passed": True,
                        "recommended_changes": [],
                        "score": 0.91,
                        "scores": {
                            "final_answer_grounding": 0.9,
                            "reasoning_quality": 0.9,
                            "tool_effectiveness": 0.95,
                            "tool_output_use": 0.9,
                            "value_over_baseline": 0.9,
                        },
                    }
                ),
            }
        ]
    }


class ClaudeJudgeTests(unittest.TestCase):
    def test_build_prompt_includes_visible_trace_and_no_hidden_cot_instruction(self):
        trace = load_trace(ROOT / "evals" / "examples" / "agent_trace_good.json")
        review = review_trace(trace)
        prompt = build_claude_trace_judge_prompt(trace, review)
        self.assertIn("reasoning summaries", prompt)
        self.assertIn("Do not infer hidden chain-of-thought", prompt)
        self.assertIn("Rivian R1S cargo volume", prompt)

    def test_parse_judge_json_accepts_fenced_json(self):
        parsed = parse_judge_json('```json\n{"passed": true, "score": 0.8}\n```')
        self.assertTrue(parsed["passed"])
        self.assertEqual(0.8, parsed["score"])

    def test_call_claude_messages_uses_messages_api_shape(self):
        response = call_claude_messages(
            "judge this",
            api_key="test-key",
            model="claude-test",
            request_fn=fake_request,
        )
        self.assertEqual("text", response["content"][0]["type"])

    def test_judge_trace_with_claude_returns_semantic_score(self):
        trace = load_trace(ROOT / "evals" / "examples" / "agent_trace_good.json")
        review = review_trace(trace)
        result = judge_trace_with_claude(
            trace,
            review,
            api_key="test-key",
            model="claude-test",
            request_fn=fake_request,
        )
        self.assertTrue(result.passed)
        self.assertEqual(0.91, result.score)
        self.assertEqual("claude-test", result.model)


if __name__ == "__main__":
    unittest.main()
