from copy import deepcopy
from pathlib import Path
import unittest

from claude_agent_prompting.harness_optimizer import (
    HarnessGrindOptions,
    _generate_candidate_variant,
    run_harness_grind,
)
from claude_agent_prompting.model_matrix import MatrixFilters, load_matrix


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "evals" / "model_matrix" / "coding_tool_selection.json"


class HarnessOptimizerTests(unittest.TestCase):
    def test_candidate_variant_sharpens_failed_task_boundary(self):
        matrix = load_matrix(MATRIX)
        variant = next(item for item in matrix["tool_variants"] if item["name"] == "baseline_short")
        results = [
            {
                "case": "investigate trace review flow",
                "status": "failed",
            }
        ]

        candidate = _generate_candidate_variant(
            deepcopy(variant),
            matrix["cases"],
            results,
            iteration=0,
        )
        task = next(tool for tool in candidate["tools"] if tool["name"] == "Task")

        self.assertEqual("baseline_short_hill_1", candidate["name"])
        self.assertIn("broad multi-step repository investigation", task["purpose"])
        self.assertIn("trace review scoring", task["use_when"])
        self.assertIn("single known file read", task["avoid_when"])

    def test_grind_live_call_cap_counts_all_iterations(self):
        result = run_harness_grind(
            MATRIX,
            HarnessGrindOptions(
                baseline_variant="baseline_short",
                filters=MatrixFilters(
                    providers={"anthropic"},
                    harnesses={"native_tools"},
                    instruction_variants={"boundary_rules"},
                    cases={"find python files", "read known file"},
                ),
                live=True,
                max_iterations=3,
                max_live_calls=7,
            ),
        )

        self.assertFalse(result["passed"])
        self.assertEqual(8, result["projected_live_calls"])
        self.assertIn("live call cap blocked run", result["error"])

    def test_grind_dry_run_returns_candidate_report(self):
        result = run_harness_grind(
            MATRIX,
            HarnessGrindOptions(
                baseline_variant="baseline_short",
                filters=MatrixFilters(
                    providers={"anthropic"},
                    harnesses={"native_tools"},
                    instruction_variants={"boundary_rules"},
                    cases={"investigate trace review flow"},
                ),
            ),
        )

        self.assertTrue(result["passed"])
        self.assertEqual("baseline_short", result["baseline_variant"])
        self.assertEqual(2, result["projected_live_calls"])
        self.assertEqual(1, len(result["candidates"]))


if __name__ == "__main__":
    unittest.main()
