from pathlib import Path
import unittest

from claude_agent_harness_opt.evals import evaluate_case, load_eval_case


ROOT = Path(__file__).resolve().parents[1]


class EvalTests(unittest.TestCase):
    def test_answer_accuracy_example_passes(self):
        result = evaluate_case(load_eval_case(ROOT / "evals" / "examples" / "search_answer.json"))
        self.assertTrue(result.passed)
        self.assertEqual(1.0, result.score)

    def test_tool_use_example_passes(self):
        result = evaluate_case(load_eval_case(ROOT / "evals" / "examples" / "tool_use.json"))
        self.assertTrue(result.passed)

    def test_final_state_example_passes(self):
        result = evaluate_case(load_eval_case(ROOT / "evals" / "examples" / "final_state.json"))
        self.assertTrue(result.passed)

    def test_answer_accuracy_allows_alternative_phrasing(self):
        result = evaluate_case(
            {
                "checks": {
                    "expected_any": [
                        {
                            "label": "uncertainty",
                            "options": ["uncertain", "roughly", "approximate"],
                        }
                    ],
                    "expected_regex": [{"label": "count", "pattern": "\\b\\d+\\s+bananas\\b"}],
                },
                "output": "The answer is roughly 120 bananas.",
                "type": "answer_accuracy",
            }
        )

        self.assertTrue(result.passed)

    def test_tool_use_accepts_multiple_valid_paths(self):
        result = evaluate_case(
            {
                "requirements": {
                    "valid_tool_paths": [
                        ["web_search", "web_fetch", "calculator"],
                        ["web_search", "calculator"],
                    ]
                },
                "transcript": {
                    "tool_calls": [
                        {"name": "web_search", "args": {}},
                        {"name": "calculator", "args": {}},
                    ]
                },
                "type": "tool_use_accuracy",
            }
        )

        self.assertTrue(result.passed)


if __name__ == "__main__":
    unittest.main()
