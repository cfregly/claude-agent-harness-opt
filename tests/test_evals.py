from pathlib import Path
import unittest

from claude_agent_prompting.evals import evaluate_case, load_eval_case


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


if __name__ == "__main__":
    unittest.main()
