import unittest

from claude_agent_harness_opt.suitability import score_use_case


class SuitabilityTests(unittest.TestCase):
    def test_agent_verdict_for_good_fit(self):
        result = score_use_case(
            {
                "complexity": 5,
                "value": 5,
                "viability": 5,
                "cost_of_error": 2,
                "recoverability": 5,
            }
        )
        self.assertEqual("agent", result["verdict"])

    def test_human_in_loop_for_high_cost_low_recovery(self):
        result = score_use_case(
            {
                "complexity": 5,
                "value": 5,
                "viability": 5,
                "cost_of_error": 5,
                "recoverability": 1,
            }
        )
        self.assertEqual("human_in_loop", result["verdict"])


if __name__ == "__main__":
    unittest.main()
