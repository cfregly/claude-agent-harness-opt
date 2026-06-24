import unittest

from claude_agent_prompting.value_bar import evaluate_value_bar


class ValueBarTests(unittest.TestCase):
    def test_value_bar_passes_with_adversarial_confirmation(self):
        result = evaluate_value_bar(
            {
                "adversarial_review": {
                    "challenge": "Known-bad traces must fail and known-good traces must pass.",
                    "failed_to_disprove": True,
                    "open_objections": [],
                },
                "baseline": {"score": 0.4},
                "candidate": {"score": 0.9},
                "claim": "The new prompt improves trace quality.",
                "metric": "trace_review.score",
                "minimum_delta": 0.2,
            }
        )
        self.assertTrue(result.passed)
        self.assertEqual(1.0, result.score)

    def test_value_bar_fails_without_adversarial_confirmation(self):
        result = evaluate_value_bar(
            {
                "adversarial_review": {
                    "challenge": "Known-bad traces must fail.",
                    "failed_to_disprove": False,
                    "open_objections": ["candidate only passed easy traces"],
                },
                "baseline": {"score": 0.8},
                "candidate": {"score": 0.85},
                "claim": "The new prompt improves trace quality.",
                "metric": "trace_review.score",
                "minimum_delta": 0.2,
            }
        )
        self.assertFalse(result.passed)
        self.assertLess(result.score, 1.0)


if __name__ == "__main__":
    unittest.main()
